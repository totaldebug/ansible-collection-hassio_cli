#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hassio_os
author: "mjkl-gh"
short_description: Manage Home Assistant (HassIO) host
version_added: "3.2.0"
description:
  - Manage Home Assistant (HassIO, hass.io) OS - update
options:
  state:
    description:
      - State of OS
    required: true
    choices: ['updated']
"""

EXAMPLES = """
# Update HassIO OS
- hassio_os:
    state: updated
    token: <SUPERVISOR_TOKEN>
"""

# ===========================================
# Module execution.
#
import json
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

from ansible_collections.totaldebug.hassio_cli.plugins.module_utils.hassio_utils import (
    get_info,
    update,
    state_and_changed,
    __raise,
)
host = "os"

def main():
    module_args = dict(
        state=dict(type="str", required=True, choices=["updated"]),
        token=dict(type="bool", required=False),
    )

    ansible_module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    switch = {"updated": update}
    state = ansible_module.params["state"]
    token = ansible_module.params["token"]

    try:
        facts_json = get_info(ansible_module, "os", token)[1]
        facts = json.loads(facts_json)["data"]

        result = dict(changed=False, message="", ansible_facts=facts)

        if state in state_and_changed:
            result["changed"] = state_and_changed[state](facts)
        else:
            __raise(Exception("Check function is undefined"))

        if ansible_module.check_mode:
            ansible_module.exit_json(**result)

        if facts["update_available"] is True:

            action = switch.get(
                state, lambda module, token: __raise(Exception("Action is undefined"))
            )

            if message[0] != 0:
                result["failed"] = True
                result["msg"] = message
                ansible_module.fail_json(**result)

            if message[0] == 0:
                result["changed"] = True
                result["message"] = action(ansible_module, token)

        ansible_module.exit_json(**result)
    except Exception as e:
        ansible_module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == "__main__":
    main()


def main():
    switch = {
        "restarted": partial(restart, module),
        "stopped": partial(stop, module),
        "updated": partial(update, module),
        "started": partial(start, module),
    }

    module_args = dict(
        state=dict(type="str", required=True, choices=switch.keys()),
        token=dict(type="bool", required=False),
    )

    ansible_module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    state = ansible_module.params["state"]
    token = ansible_module.params["token"]

    try:
        facts_json = get_info(ansible_module, module, token)[1]
        facts = json.loads(facts_json)["data"]

        result = dict(changed=False, message="", ansible_facts=facts)

        if state in state_and_changed:
            result["changed"] = state_and_changed[state](facts)
        else:
            __raise(Exception("Check function is undefined"))

        if ansible_module.check_mode:
            ansible_module.exit_json(**result)

        if facts["update_available"] is True:
            action = switch.get(
                state,
                lambda ansible_module, token: __raise(Exception("Action is undefined")),
            )
            message = action(ansible_module, token)

        if message[0] == 1:
            result["failed"] = True
            result["msg"] = message
            ansible_module.fail_json(**result)

        if message[0] == 0:
            result["changed"] = True
            result["msg"] = message
            ansible_module.exit_json(**result)

    except Exception as e:
        ansible_module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
