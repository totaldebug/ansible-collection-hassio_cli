from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hassio_addon_repos
author: "marksie1988 / TotalDebug (@marksie1988)"
short_description: Manage Home Assistant (HassIO) addon repositories
version_added: "2.1.0"
description:
  - Manage Home Assistant (HassIO, hass.io) addon repositories - add and remove custom addon repositories
options:
  state:
    description:
      - State of addon
    required: true
    choices: ['present', 'absent']
  repo:
    description:
      - URL of repo to add or remove.
    required: true
  src:
    description:
      - Source file default: /usr/share/hassio/config.json
"""

EXAMPLES = """
# Adds repo if not present
- hassio_addon_repos:
    src: /usr/share/hassio/config.json
    repo: https://github.com/helto4real/hassio-add-ons
    state: present
"""

# ===========================================
# Module execution.
#
import traceback

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native
import json

data_point = "addons_custom_list"


def write_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def present(filename, repo):
    with open() as json_file:
        data = json.load(json_file)
        temp = data[data_point]
        if repo not in temp:
            temp.append(repo)
            write_json(data, filename)


def absent(filename, repo):
    with open() as json_file:
        data = json.load(json_file)
        temp = data[data_point]
        if repo in temp:
            temp.remove(repo)
            write_json(data, filename)


def __raise(ex):
    raise ex


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(required=True, choices=["present", "absent"],),
            repo=dict(required=True),
            src=dict(required=True, default="/usr/share/hassio/config.json"),
        ),
        supports_check_mode=False,
    )
    state = module.params["state"]
    repo = module.params["repo"]
    src = module.params["src"]

    try:
        message = state(src, repo)
        module.exit_json(msg=message)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
