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
module: hassio_host
author: "marksie1988 / TotalDebug (@marksie1988)"
short_description: Manage Home Assistant (HassIO) host
version_added: "1.0"
description:
  - Manage Home Assistant (HassIO, hass.io) host - reboot, update, shutdown
options:
  state:
    description:
      - State of host
    required: true
    choices: ['rebooted', 'updated', 'shutdown']
"""

EXAMPLES = """
# Reboot HassIO OS
- hassio_host:
    state: rebooted
"""

# ===========================================
# Module execution.
#
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

hassio = "ha"
host = "ho"


def join(*args):
    return " ".join(list(args))


def reboot(ansible):
    cmd = join(hassio, host, "reboot")
    return ansible.run_command(cmd)


def update(ansible):
    cmd = join(hassio, host, "update")
    return ansible.run_command(cmd)


def shutdown(ansible):
    cmd = join(hassio, host, "shutdown")
    return ansible.run_command(cmd)


def __raise(ex):
    raise ex


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(required=True, choices=["rebooted", "updated", "shutdown"])
        ),
        # TODO
        supports_check_mode=False,
    )

    switch = {"rebooted": reboot, "shutdown": shutdown, "updated": update}
    state = module.params["state"]

    try:
        action = switch.get(state, lambda: __raise(Exception("Action is undefined")))
        result = action(module)
        module.exit_json(msg=result)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
