#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: hassio_core_facts

short_description: Ansible facts module for the hassio cli

version_added: "3.2.0"

description: This module collects facts about the home assistant core instance running on the host

author:
    - mjkl-gh (@mjkl-gh)
'''

EXAMPLES = r'''
# Pass in a message
- name: gather facts about home assistant core
  hassio_core_facts:
    token: <SUPERVISOR_TOKEN>
'''

RETURN = r'''
core:
    arch: 
        description: The architecture of the machine
        type: str
        returned: always
        sample: amd64
    audio_input:
        description: Profile name for audio input
        type: str
        returned: always
        sample:  None
    audio_output:
        description: Profile name for audio output
        type: str
        returned: always
        sample:  None
    boot:
        description: Start core on boot
        type: bool
        returned: always
        sample: true
    image:
        description: The docker image used
        type: str
        returned: optional
        sample:  ghcr.io/home-assistant/qemux86-64-homeassistant
    ip_address:
        description: ipv4 address of the core installation
        type: str
        returned: always
        sample:  172.30.32.1
    machine:
        description: The machine type
        type: str
        returned: always
        sample:  qemux86-64
    port: 
        description: The TCP port the core installtions runs on
        type: str
        returned: always
        sample: 8123
    ssl: 
        description: Whether ssl is activated
        type: bool
        returned: always
        sample: true
    update_available: 
        description: Whether the core installation can be updated
        type: str
        returned: always
        sample: true
    version: 
        description: The current version of home assistant core
        type: str
        returned: always
        sample: 2023.2.5
    version_latest: 
        description: The latest version of home assistant core
        type: str
        returned: always
        sample: 2023.3.5
    watchdog: 
        description: Whether a watchdog is active on the core installation
        type: bool
        returned: optional
        sample: true
os: {
    board: 
        description: Board type the OS is running on
        type: str
        returned: always
        sample: ova
    boot: 
        description: The active boot partition
        type: str
        returned: always
        sample: B
    data_disk: 
        description: The current data disk in use
        type: str
        returned: always
        sample: /dev/vda8
    update_available: 
        description: Whether the core installation can be updated
        type: bool
        returned: always
        sample: false
    version: 
        description: The current version of home assistant OS
        type: str
        returned: always
        sample: 9.5
    version_latest: 
        description: The latest version of home assistant OS
        type: str
        returned: always
        sample: 9.5
'''

from ansible.module_utils.basic import AnsibleModule
import json

def join(*args):
    return " ".join(list(args))

def get_info(ansible, module, token=None):
    token_argument = join("--api-token ", token) if token is not None else ""
    cmd = join("ha ", module, " info --raw-json ", token_argument)
    return ansible.run_command(cmd)


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
            token=dict(required=False),
        )

    result = dict(
        changed=False,
    )

    ansible_module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    facts = dict()

    for module in ("os", "core"):
        message = get_info(ansible_module, module, ansible_module.params["token"])
        if message[0] != 0:
            result["failed"] = True
            result["msg"] = message
            ansible_module.fail_json(**result)

        if message[0] == 0:
            facts[module] = json.loads(message[1])["data"]


    result["ansible_facts"] = facts
    ansible_module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
