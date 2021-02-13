#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.0",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: hassio_addons
author: "marksie1988 / TotalDebug (@marksie1988)"
short_description: Manage Home Assistant (HassIO) addons
version_added: "1.0"
description:
  - Manage Home Assistant (HassIO, hass.io) addons - install, uninstall, start, stop, update addons
options:
  state:
    description:
      - State of addon
    required: true
    choices: ['present', 'absent', 'started', 'stopped', 'updated']
  name:
    description:
      - Name of addon to install.
    aliases: ['addon']
    required: true
"""

EXAMPLES = """
# Install Samba share addon
- hassio_addon:
    state: present
    name: core_samba

# Uninstall DHCP server and Grafana addons
- hassio_addon:
    state: absent
    name: "{{ item }}"
  with_items:
    - grafana
    - core_dhcp_server

# Start Samba share addon
- hassio_addon:
    state: started
    addon: core_samba

# Stop Samba share addon
- hassio_addon:
    state: stopped
    name: core_samba

# Update Samba share addon
- hassio_addon:
    state: updated
    name: core_samba
"""

# ===========================================
# Module execution.
#
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

hassio = "ha"
addons = "ad"


def join(*args):
    return " ".join(list(args))


def execute_addon(ansible, action, name):
    cmd = join(hassio, addons, action, name)
    return ansible.run_command(cmd)


def install(ansible, name):
    return execute_addon(ansible, "install", name)


def uninstall(ansible, name):
    return execute_addon(ansible, "uninstall", name)


def start(ansible, name):
    return execute_addon(ansible, "start", name)


def stop(ansible, name):
    return execute_addon(ansible, "stop", name)


def update(ansible, name):
    return execute_addon(ansible, "update", name)


def __raise(ex):
    raise ex


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(
                required=True,
                choices=["present", "absent", "started", "stopped", "updated"],
            ),
            name=dict(required=True, aliases=["addon"]),
        ),
        # TODO
        supports_check_mode=False,
    )

    switch = {
        "present": install,
        "absent": uninstall,
        "started": start,
        "stopped": stop,
        "updated": update,
    }
    state = module.params["state"]
    name = module.params["name"]

    try:
        action = switch.get(state, lambda: __raise(Exception("Action is undefined")))
        message = action(module, name)

        result = dict()

        if message[0] == 1:
            result["failed"] = True
            result["msg"] = message
            module.fail_json(**result)

        if message[0] == 0:
            result["changed"] = True
            result["msg"] = message
            module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
