#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hassio_core
author: "mjkl-gh"
short_description: Manage Home Assistant (HassIO) core
version_added: "3.2.0"
description:
  - Manage Home Assistant (HassIO, hass.io) core - restart, update, stop
options:
  state:
    description:
      - State of home assistant core
    required: true
    choices: ['restarted', 'updated', 'stop',  "started"]
"""

EXAMPLES = """
# restart HassIO Core
- hassio_core:
    state: updated
    token: <SUPERVISOR_TOKEN>
"""

# ===========================================
# Module execution.
#
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

hassio = "ha"
host = "core"


def join(*args):
    return " ".join(list(args))


def execute_core(ansible, action, token):
    cmd = join(hassio, host, action, "--api-token", token)
    return ansible.run_command(cmd)


def start(ansible, token):
    return execute_core(ansible, "start", token)


def restart(ansible, token):
    return execute_core(ansible, "restart", token)


def stop(ansible, token):
    return execute_core(ansible, "stop", token)


def update(ansible, token):
    return execute_core(ansible, "update", token)


def __raise(ex):
    raise ex


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(
                required=True, choices=["restarted", "updated", "stopped", "started"]
            ),
            token=dict(required=True),
        ),
        # TODO
        supports_check_mode=False,
    )

    switch = {"restarted": restart, "stop": stop, "updated": update, "started": start}
    state = module.params["state"]
    token = module.params["token"]

    try:
        action = switch.get(state, lambda: __raise(Exception("Action is undefined")))
        message = action(module, token)

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
