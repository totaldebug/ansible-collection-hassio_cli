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

## Configuration

### Install

Include this collection as a requirement with your playbook.

### Usage

### Addon Examples

```yaml
# Install Samba share addon
- hassio_addon:
    state: present
    name: core_samba

# Uninstall DHCP server and Grafana addons
- hassio_addon:
    state: absent
    name: {{ item }}
  with_items:
    - grafana
    - core_dhcp_server

# Start Samba share addon
- hassio_addon:
    state: started
    addon: core_samba

# Stop Samba share addon
- hassio_addon:
    state: stopped
    name: core_samba

# Update Samba share addon
- hassio_addon:
    state: updated
    name: core_samba
```

### Host Examples

```yaml
# Reboot HassIO OS
- hassio_host:
    state: rebooted

# Update HassIO OS
- hassio_host:
    state: updated
```

### Snapshot Examples

```yaml
# Create snapshot with name snap-10-01-2021
- hassio_snapshot:
    state: new
    name: "snap-10-01-2021"

# Remove snapshot with name snap-10-01-2021
- hassio_snapshot:
    state: remove
    name: "snap-10-01-2021"

# Restore snapshot with name snap-10-01-2021
- hassio_snapshot:
    state: restore
    name: "snap-10-01-2021"

# Reload the files on disk to check for new or removed snapshots
- hassio_snapshot:
    state: reload
```

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
