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
import json

from ansible_collections.totaldebug.hassio_cli.plugins.module_utils.hassio_utils import *
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

hassio = "ha"
host = "core"

def join(*args):
    return " ".join(list(args))


def execute_core(ansible, action, token=None):
    token_argument = join("--api-token", token) if token is not None else ""
    cmd = join(hassio, host, action, token_argument)
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
    module_args = dict(
            state=dict(type='str', required=True, choices=["restarted", "updated", "stopped", "started"]),
            token=dict(type='bool', required=False),
        )

    ansible_module = AnsibleModule(
        argument_spec = module_args,
        supports_check_mode = True,
        )

    switch = {"updated": update}
    state = ansible_module.params["state"]
    token = ansible_module.params["token"]
    
    facts = json.loads(get_info(ansible_module, "os", token)[1])["data"]
    
    result = dict(
        changed=True,
        message='',
    )

    if state in state_and_changed:
        result["changed"] = state_and_changed[state](facts)

    if ansible_module.check_mode:
        ansible_module.exit_json(**result)

    switch = {"restarted": restart, "stop": stop, "updated": update, "started": start}
    state = ansible_module.params["state"]
    token = ansible_module.params["token"]

    try:
        action = switch.get(state, lambda: __raise(Exception("Action is undefined")))
        message = action(ansible_module, token)

        result = dict()

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
