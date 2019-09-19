#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Mikhail Yohman (@FragmentedPacket) <mikhail.yohman@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: netbox_vlan
short_description: Create, update or delete vlans within Netbox
description:
  - Creates, updates or removes vlans from Netbox
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
requirements:
  - pynetbox
version_added: '0.1.0'
options:
  netbox_url:
    description:
      - URL of the Netbox instance resolvable by Ansible control host
    required: true
  netbox_token:
    description:
      - The token created within Netbox to authorize API access
    required: true
  data:
    description:
      - Defines the vlan configuration
    suboptions:
      site:
        description:
          - The site the VLAN will be associated to
      vlan_group:
        description:
          - The VLAN group the VLAN will be associated to
      vid:
        description:
          - The VLAN ID
        required: true
      name:
        description:
          - The name of the vlan
        required: true
      tenant:
        description:
          - The tenant that the vlan will be assigned to
      status:
        description:
          - The status of the vlan
        choices:
          - Active
          - Reserved
          - Deprecated
      vlan_role:
        description:
          - Required if I(state=present) and the vlan does not exist yet
      description:
        description:
          - The description of the vlan
      tags:
        description:
          - Any tags that the vlan may need to be associated with
      custom_fields:
        description:
          - must exist in Netbox
    required: true
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
    default: 'yes'
    type: bool
"""

EXAMPLES = r"""
- name: "Test Netbox modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create vlan within Netbox with only required information
      netbox_vlan:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test VLAN
          vid: 400
        state: present

    - name: Delete vlan within netbox
      netbox_vlan:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test VLAN
          vid: 400
        state: absent

    - name: Create vlan with all information
      netbox_vlan:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test VLAN
          vid: 400
          site: Test Site
          group: Test VLAN Group
          tenant: Test Tenant
          status: Deprecated
          vlan_role: Test VLAN Role
          description: Just a test
          tags:
            - Schnozzberry
        state: present
"""

RETURN = r"""
vlan:
  description: Serialized object as created or already existent within Netbox
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.fragmentedpacket.netbox_modules.plugins.module_utils.netbox_ipam import (
    NetboxIpamModule,
    NB_VLANS,
)


def main():
    """
    Main entry point for module execution
    """
    argument_spec = dict(
        netbox_url=dict(type="str", required=True),
        netbox_token=dict(type="str", required=True, no_log=True),
        data=dict(type="dict", required=True),
        state=dict(required=False, default="present", choices=["present", "absent"]),
        validate_certs=dict(type="bool", default=True),
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    # Fail if vlan name is not given
    if not module.params["data"].get("name"):
        module.fail_json(msg="missing name")

    netbox_vlan = NetboxIpamModule(module, NB_VLANS)
    netbox_vlan.run()


if __name__ == "__main__":
    main()
