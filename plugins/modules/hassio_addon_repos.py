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
import os
import hashlib

data_point = "addons_custom_list"


def write_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def get_hash_from_repository(name):
    """Generate a hash from repository."""
    key = name.lower().encode()
    return hashlib.sha1(key).hexdigest()[:8]

def add_repo(repo, dir):
    filename = f"{dir}/config.json"
    path = os.path.join(dir, "/addons/git", get_hash_from_repository(repo))
    DockerPath = os.path.join("/data/addons/git", get_hash_from_repository(repo))
    os.system(
        f'docker exec hassio_supervisor bash -c "mkdir {DockerPath}; cd {DockerPath}; git clone {repo}.git ."'
    )
    with open(filename, "r+") as json_file:
        data = json.load(json_file)
        temp = data[data_point]
        if repo not in temp:
            temp.append(repo)
            write_json(data, filename)
            return True, f"{path} - {repo} Added."
        return False, f"{path} - {repo} Already exists."


def remove_repo(repo, dir):
    filename = f"{dir}/config.json"
    path = os.path.join(dir, get_hash_from_repository(repo))
    with open(filename, "r+") as json_file:
        data = json.load(json_file)
        temp = data[data_point]
        if repo in temp:
            temp.remove(repo)
            write_json(data, filename)
            return True, f"{repo} Removed."
        return False, f"{repo} doesn't exist."


def __raise(ex):
    raise ex


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(
                required=True,
                aliases=["repo"],
            ),
            state=dict(
                required=True,
                choices=["present", "absent"],
            ),
            src=dict(
                default="/usr/share/hassio/",
            ),
        ),
        supports_check_mode=False,
    )
    choice_map = {
        "present": add_repo,
        "absent": remove_repo,
    }

    name = module.params["name"]
    src = module.params["src"]
    state = module.params["state"]

    try:
        action = choice_map.get(
            state, lambda: __raise(Exception("Action is undefined"))
        )
        result = action(name, src)
        module.exit_json(changed=result[0], msg=result[1])
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())


if __name__ == "__main__":
    main()
