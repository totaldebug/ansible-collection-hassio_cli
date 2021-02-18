#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hassio_snapshot
author: "marksie1988 / TotalDebug (@marksie1988)"
short_description: Manage Home Assistant (HassIO) snapshot
version_added: "2.0.1"
description:
  - Manage Home Assistant (HassIO, hass.io) snaposhot - reboot, update, shutdown
options:
  state:
    description:
      - State of snapshot
    required: true
    choices: ['new', 'remove', 'restore', 'reload']
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
snap = "snap"


def with_name(name):
    return "-name {}".format(name)


def join(*args):
    return " ".join(list(args))


def execute_snapshot(ansible, action, name):
    cmd = join(hassio, snap, action, with_name(name))
    return ansible.run_command(cmd)


def new(ansible, name):
    return execute_snapshot(ansible, "new", name)


def remove(ansible, name):
    return execute_snapshot(ansible, "remove", name)


def restore(ansible, name):
    return execute_snapshot(ansible, "restore", name)


def reload(ansible):
    cmd = join(hassio, snap, "reload")
    return ansible.run_command(cmd)


def __raise(ex):
    raise ex


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(required=True, choices=["new", "remove", "restore", "reload"])
        ),
        # TODO
        supports_check_mode=False,
    )

    switch = {"new": new, "remove": remove, "restore": restore, "reload": reload}
    state = module.params["state"]

    try:
        action = switch.get(state, lambda: __raise(Exception("Action is undefined")))
        result = action(module)
        module.exit_json(msg=result)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
