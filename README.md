<meta name="author" content="Marco Noce">
<meta name="description" content="Gathers facts about Solaris SMF services on a SunOS/Oracle Solaris host by svcs">
<meta name="copyright" content="Marco Noce 2024">
<meta name="keywords" content="ansible, module, fact, solaris, svcs, smf, services">

<div align="center">

![Ansible Custom Module][ansible-shield]
![Oracle Solaris][solaris-shield]
![python][python-shield]
![license][license-shield]

</div>


### svcs_facts ansible custom module
#### Gathers facts about Solaris SMF services on a SunOS/Oracle Solaris host by svcs

#### Description :

<b>svcs_facts</b> is a custom module for ansible that creates an ansible_facts containing the list and details of SMF services on a SunOS/Oracle Solaris host

#### Repo files:

```
├── /library                
│   └── svcs_facts.py  ##<-- python custom module
└── svcs_list.yml      ##<-- ansible playbook example
```

#### Requirements :

*  This module supports SunOS/Oracle Solaris only
*  The SMF services info are gathered from the [svcs] command

#### Parameters :

*  no parameters are needed

#### Attributes :

|Attribute |Support|Description                                                                         |
|----------|-------|------------------------------------------------------------------------------------|
|check_mode|full   |Can run in check_mode and return changed status prediction without modifying target.|
|facts     |full   |Action returns an ansible_facts dictionary that will update existing host facts.    |

#### Examples :

#### Tasks
```yaml
---
- name: Gather facts SMF service
  svcs_facts:

- name: set fact for debug
  set_fact:
    sendmail_state: "{{ ansible_facts.svcs_list | selectattr('FMRI','equalto', 'svc:/network/smtp:sendmail' ) | map(attribute='STATE') | first }}"
    sendmail_stime: "{{ ansible_facts.svcs_list | selectattr('FMRI','equalto', 'svc:/network/smtp:sendmail' ) | map(attribute='STIME') | first }}"

- name: print STATE of sendmail service
  debug:
    msg: "sendmail service is in {{sendmail_state}} state from {{sendmail_stime}}"

```
#### svcs_list facts:
```json
"ansible_facts": {
    "svcs_list": [
      {
        "STATE": "disabled",
        "NSTATE": "-",
        "STIME": "21:21:57",
        "CTID": "67",
        "FMRI": "svc:/platform/i86pc/acpihpd:default"
      }
  ]
},
```
#### debug output from example :
```
TASK [print STATE of sendmail service] *****************************************
ok: [sol11host] => {
    "msg": "sendmail service is in online state from 21:22:06"
}
```
#### Returned Facts :

*  Facts returned by this module are added/updated in the hostvars host facts and can be referenced by name just like any other host fact. They do not need to be registered in order to use them.

|Key       |Type                  |Description                                                                       |Returned|Sample            |
|----------|----------------------|----------------------------------------------------------------------------------|------- |------------------|
|svcs_list |list / elements=string|SMF Services list                                                                 |        |                  |
|STATE     |string                |The state of the service instance.                                                |always  |"online"          |
|NSTATE    |string                |The next state of the service.                                                    |always  |"-"               |
|STIME     |string                |If the service instance entered the current state within the last 24 hours, this value indicates the time that it did so. Otherwise, this value indicates the date on which it did so, printed with underscores (_) in place of blanks.                            |always  |"21:21:47"         |
|CTID      |string                |The primary contract ID for the service instance. Not all instances have valid primary contract IDs.                                                              |always  |"67" |
|FMRI      |string                |The FMRI of the service instance.                                 |always  |"svc:/network/smtp:sendmail"          |

## SANITY TEST

* Ansible sanity test is available in [SANITY.md] file

## Integration

1. Assuming you are in the root folder of your ansible project.

Specify a module path in your ansible configuration file.

```shell
$ vim ansible.cfg
```
```ini
[defaults]
...
library = ./library
...
```

Create the directory and copy the python modules into that directory

```shell
$ mkdir library
$ cp path/to/module library
```

2. If you use Ansible AWX and have no way to edit the control node, you can add the /library directory to the same directory as the playbook .yml file

```
├── root repository
│   ├── playbooks
│   │    ├── /library                
│   │    │   └── svcs_facts.py      ##<-- python custom module
│   │    └── your_playbook.yml      ##<-- you playbook
```   

[ansible-shield]: https://img.shields.io/badge/Ansible-custom%20module-blue?style=for-the-badge&logo=ansible&logoColor=lightgrey
[solaris-shield]: https://img.shields.io/badge/oracle-solaris-red?style=for-the-badge&logo=oracle&logoColor=red
[python-shield]: https://img.shields.io/badge/python-blue?style=for-the-badge&logo=python&logoColor=yellow
[license-shield]: https://img.shields.io/github/license/nomakcooper/svcs_facts?style=for-the-badge&label=LICENSE

[svcs]: https://docs.oracle.com/cd/E86824_01/html/E54763/svcs-1.html
[SANITY.md]: SANITY.md
