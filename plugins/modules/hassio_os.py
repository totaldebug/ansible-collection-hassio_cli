#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hassio_host
author: "marksie1988 / TotalDebug (@marksie1988)"
short_description: Manage Home Assistant (HassIO) host
version_added: "2.0.1"
description:
  - Manage Home Assistant (HassIO, hass.io) host - update
options:
  state:
    description:
      - State of host
    required: true
    choices: ['updated']
"""

EXAMPLES = """
# Update HassIO OS
- hassio_host:
    state: update
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

def update(ansible):
    cmd = join(hassio, host, "update")
    return ansible.run_command(cmd)

def __raise(ex):
    raise ex


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(required=True, choices=["updated"])
        ),
        # TODO
        supports_check_mode=False,
    )

    switch = {"updated": update}
    state = module.params["state"]

    try:
        action = switch.get(state, lambda: __raise(Exception("Action is undefined")))
        result = action(module)
        module.exit_json(msg=result)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
