<h4 align="center">An Ansible collection containing modules for executing HA CLI Commands.</h4>

<p align="center">
    <a href="https://github.com/totaldebug/ansible-module-hassio/commits/master">
    <img src="https://img.shields.io/github/last-commit/totaldebug/ansible-module-hassio.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub last commit">
    <a href="https://github.com/totaldebug/ansible-module-hassio/issues">
    <img src="https://img.shields.io/github/issues-raw/totaldebug/ansible-module-hassio.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub issues">
    <a href="https://github.com/totaldebug/ansible-module-hassio/pulls">
    <img src="https://img.shields.io/github/issues-pr-raw/totaldebug/ansible-module-hassio.svg?style=flat-square&logo=github&logoColor=white"
         alt="GitHub pull requests">
</p>

<p align="center">
  <a href="#about">About</a> •
  <a href="#features">Features</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#author">Author</a> •
  <a href="#support">Support</a> •
  <a href="#donate">Donate</a> •
  <a href="#license">License</a>
</p>

---

## About

<table>
<tr>
<td>

**ansible-module-hassio** is a **high-quality** _Ansible Collection Module_ that executes **HA CLI** commands on your hassio ansible clients.

Hass.io is an operating system that will take care of installing and updating Home Assistant, is managed from the Home Assistant UI, allows creating/restoring snapshots of your configuration and can easily be extended using Hass.io add-ons including Google Assistant and Let’s Encrypt.

</td>
</tr>
</table>

## Features

|                            |         🔰         |
| -------------------------- | :----------------: |
| Manage Hassio addons       |         ✔️         |
| Manage Hassio Host         |         ✔️         |
| Manage Hassio Snapshots    |         ✔️         |
| Add / Remove Addon Repos   |         ✔️         |

## Configuration

### Install

Include this collection as a requirement with your playbook.

```
ansible-galaxy collection install totaldebug.hassio_cli
```

### Usage
#### hassio_addons

| Option          | Required | Description |
| --------------- | :------: | :---------: |
| name (alias: addon) | True | The name of the addon |
| state | True | The state of the addon ["present", "absent", "started", "stopped", "updated"] |

<details>
  <summary>Examples</summary>

<!--START_SECTION:hassio_addons-->
```yaml
# Install Samba share addon
- totaldebug.hassio_cli.hassio_addon:
    state: present
    name: core_samba

# Uninstall DHCP server and Grafana addons
- totaldebug.hassio_cli.hassio_addons:
    state: absent
    name: {{ item }}
  with_items:
    - core_dhcp_server
    - core_mosquitto

# Start Samba share addon
- totaldebug.hassio_cli.hassio_addons:
    state: started
    addon: core_samba

# Stop Samba share addon
- totaldebug.hassio_cli.hassio_addons:
    state: stopped
    name: core_samba

# Update Samba share addon
- totaldebug.hassio_cli.hassio_addons:
    state: updated
    name: core_samba
```
<!--END_SECTION:hassio_addons-->

</details>

#### hassio_host

| Option          | Required | Description |
| --------------- | :------: | :---------: |
| state | True | ["rebooted", "updated", "shutdown"] |

<details>
  <summary>Examples</summary>

<!--START_SECTION:hassio_host-->
```yaml
# Reboot HassIO OS
- totaldebug.hassio_cli.hassio_host:
    state: rebooted

# Update HassIO OS
- totaldebug.hassio_cli.hassio_host:
    state: updated
```
<!--END_SECTION:hassio_host-->


#### hassio_snapshot

| Option          | Required | Description |
| --------------- | :------: | :---------: |
| name | False | The name of the snapshot |
| state | True | ["new", "remove", "restore", "reload"] |

<details>
  <summary>Examples</summary>

<!--START_SECTION:hassio_snapshot-->
```yaml
# Create snapshot with name snap-10-01-2021
- totaldebug.hassio_cli.hassio_snapshot:
    state: new
    name: "snap-10-01-2021"

# Remove snapshot with name snap-10-01-2021
- totaldebug.hassio_cli.hassio_snapshot:
    state: remove
    name: "snap-10-01-2021"

# Restore snapshot with name snap-10-01-2021
- totaldebug.hassio_cli.hassio_snapshot:
    state: restore
    name: "snap-10-01-2021"

# Reload the files on disk to check for new or removed snapshots
- totaldebug.hassio_cli.hassio_snapshot:
    state: reload
```
<!--END_SECTION:hassio_snapshot-->

#### hassio_addon_repos

| Option          | Required | Description |
| --------------- | :------: | :---------: |
| name (alias: repo) | True | The URL of the repo to be added |
| state | True | ["present", "absent"] |
| src | False | File where config is stored, Default: `/usr/share/hassio/config.json` |

<details>
  <summary>Examples</summary>

<!--START_SECTION:hassio_addon_repos-->
```yaml
# Addrepo to config
- totaldebug.hassio_cli.hassio_addon_repos:
    state: present
    repo: "https://github.com/helto4real/hassio-add-ons"

# Remove repo from config
- totaldebug.hassio_cli.hassio_snapshot:
    state: absent
    repo: "https://github.com/helto4real/hassio-add-ons"
    src: "/usr/share/hassio/config.json"

```
<!--END_SECTION:hassio_addon_repos-->

## Contributing

Got **something interesting** you'd like to **share**? Learn about [contributing](https://github.com/totaldebug/.github/blob/main/.github/CONTRIBUTING.md).

### Versioning

This project follows semantic versioning.

In the context of semantic versioning, consider the role contract to be defined by the role variables.

- Breaking Changes or changes that require user intervention will increase the major version. This includes changing the default value of a role variable.
- Changes that do not require user intervention, but add new features, will increase the minor version.
- Bug fixes will increase the patch version.

## Author

| [![TotalDebug](https://totaldebug.uk/assets/images/logo.png)](https://linkedin.com/in/marksie1988) |
|:--:|
| **marksie1988 (Steven Marks)** |

## Support

Reach out to me at one of the following places:

- via [Discord](https://discord.gg/6fmekudc8Q)
- Raise an issue in GitHub

## Donate

Please consider supporting this project by sponsoring, or just donating a little via [our sponsor page](https://github.com/sponsors/marksie1988)

## License

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-orange.svg?style=flat-square)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

- Copyright © [Total Debug](https://totaldebug.uk "Total Debug").
