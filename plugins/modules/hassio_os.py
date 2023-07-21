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

from ansible_collections.totaldebug.hassio_cli.plugins.module_utils.hassio_utils import *

hassio = "ha"
host = "os"

def main():
    module_args = dict(
            state=dict(type='str', required=True, choices=["updated"]),
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
        changed=facts["update_available"] is "true",
        message='',
    )

    if ansible_module.check_mode:
        ansible_module.exit_json(**result)

    try:
        if facts["update_available"] is "true":
            action = switch.get(state, lambda: __raise(Exception("Action is undefined")))
            result['message'] = action(module, token)
        ansible_module.exit_json(**result)
    except Exception as e:
        ansible_module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
