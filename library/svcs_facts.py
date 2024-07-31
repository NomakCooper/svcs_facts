#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: svcs_facts
author:
    - Marco Noce (@NomakCooper)
description:
    - Gathers facts about Solaris SMF services by svcs.
    - This module currently supports SunOS Family, Oracle Solaris 10/11.
requirements:
  - svcs
short_description: Gathers facts about solaris SMF services.
notes:
  - |
    This module shows the list of solaris SMF services.
'''

EXAMPLES = r'''
- name: Gather facts SMF service
  svcs_facts:

- name: set fact for debug
  set_fact:
    sendmail_state: "{{ ansible_facts.svcs_list | selectattr('FMRI','equalto', 'svc:/network/smtp:sendmail' ) | map(attribute='STATE') | first }}"
    sendmail_stime: "{{ ansible_facts.svcs_list | selectattr('FMRI','equalto', 'svc:/network/smtp:sendmail' ) | map(attribute='STIME') | first }}"

- name: print STATE of sendmail service
  debug:
    msg: "sendmail service is in {{sendmail_state}} state from {{sendmail_stime}}"

'''

RETURN = r'''
ansible_facts:
  description: Dictionary containing details of SMF services
  returned: always
  type: complex
  contains:
    svcs_list:
      description: A list of SMF services.
      returned: always
      type: list
      contains:
        STATE:
          description: The state of the service instance.
          returned: always
          type: str
          sample: "online"
        NSTATE:
          description: The next state of the service.
          returned: always
          type: str
          sample: "-"
        STIME:
          description: If the service instance entered the current state within the last 24 hours, this value indicates the time that it did so. Otherwise, this value indicates the date on which it did so, printed with underscores (_) in place of blanks.
          returned: always
          type: str
          sample: "21:21:47"
        CTID:
          description: The primary contract ID for the service instance. Not all instances have valid primary contract IDs.
          returned: always
          type: str
          sample: "67"
        FMRI:
          description: The FMRI of the service instance.
          returned: always
          type: str
          sample: "svc:/network/smtp:sendmail"                                        
'''

import re
import platform
from ansible.module_utils.common.text.converters import to_native
from ansible.module_utils.basic import AnsibleModule


def svcs_parse(raw):

    results = list()

    lines = raw.splitlines()

    # skip headers ( skip header and global zone row )
    # STATE          NSTATE        STIME           CTID      FMRI

    lines = lines[1:]

    for line in lines:
        cells = line.split(None, 5)
        try:
            if len(cells) == 5:
                STATE, NSTATE, STIME, CTID, FMRI = cells
        except ValueError:
            # unexpected stdout from zoneadm
            raise EnvironmentError(
                'Expected `svcs` table layout " STATE,NSTATE,STIME,CTID,FMRI" \
                but got something else: {0}'.format(line)
            )

        result = {
            'STATE': STATE,
            'NSTATE': NSTATE,
            'STIME': STIME,
            'CTID': CTID,
            'FMRI': FMRI,
        }
        results.append(result)
    return results


def main():
    command_args = ['-a', '-v']
    commands_map = {
        'svcs': {
            'args': [],
            'parse_func': svcs_parse
        },
    }
    module = AnsibleModule(
        argument_spec=dict(
            #no arguments necessary
        ),
        supports_check_mode=True,
    )

    commands_map['svcs']['args'] = command_args

    if platform.system() != 'SunOS':
        module.fail_json(msg='This module requires SunOS.')

    result = {
        'changed': False,
        'ansible_facts': {
            'svcs_list': [],
        },
    }

    try:
        command = None
        bin_path = None
        for c in sorted(commands_map):
            bin_path = module.get_bin_path(c, required=False)
            if bin_path is not None:
                command = c
                break

        if bin_path is None:
            raise EnvironmentError(msg='Unable to find any of the supported commands in PATH: {0}'.format(", ".join(sorted(commands_map))))

        
        args = commands_map[command]['args']
        rc, stdout, stderr = module.run_command([bin_path] + args)
        if rc == 0:
            parse_func = commands_map[command]['parse_func']
            results = parse_func(stdout)

            for service in results:
                result['ansible_facts']['svcs_list'].append(service)
    except (KeyError, EnvironmentError) as e:
        module.fail_json(msg=to_native(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
