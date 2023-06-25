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
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

hassio = "ha"
host = "os"


def join(*args):
    return " ".join(list(args))


def update(ansible, token):
    cmd = join(hassio, host, "update", "--api-token", token)
    return ansible.run_command(cmd)


def __raise(ex):
    raise ex


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(required=True, choices=["updated"]), token=dict(required=True)
        ),
        # TODO
        supports_check_mode=False,
    )

    switch = {"updated": update}
    state = module.params["state"]
    token = module.params["token"]

    try:
        action = switch.get(state, lambda: __raise(Exception("Action is undefined")))
        result = action(module, token)
        module.exit_json(msg=result)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
