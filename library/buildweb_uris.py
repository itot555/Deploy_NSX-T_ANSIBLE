#!/usr/bin python
# coding=utf-8
#
# Copyright © 2015-2016 VMware, Inc. All Rights Reserved.
#
# Licensed under the X11 (MIT) (the “License”) set forth below;
#
# you may not use this file except in compliance with the License. Unless required by applicable law or agreed to in
# writing, software distributed under the License is distributed on an “AS IS” BASIS, without warranties or conditions
# of any kind, EITHER EXPRESS OR IMPLIED. See the License for the specific language governing permissions and
# limitations under the License. Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# "THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.”

__author__ = 'yfauser'


def get_buildweb_data(build, module):
    build_list = []
    response = open_url('http://buildapi.eng.vmware.com/ob/build/{}/'.format(build))
    resp_json = json.loads(response.read())

    components_url = resp_json.get('_component_builds_url')
    build_tree_url = resp_json.get('_buildtree_url')

    response = open_url('http://buildapi.eng.vmware.com{}'.format(components_url))
    resp_json = json.loads(response.read())

    for build in resp_json['_list']:
        component_url = build.get('_component_build_url')
        response = open_url('http://buildapi.eng.vmware.com{}'.format(component_url))
        resp_json = json.loads(response.read())

        product = resp_json.get('product')
        if product == 'nsx-edgenode':
            product_name = 'nsx-edge'
        else:
            product_name = product

        id = resp_json.get('id')
        version = resp_json.get('version')
        ova_filename = '{}-{}.{}.ova'.format(product_name, version, id)
        ova_path = '{}publish/{}/exports/ova/{}'.format(build_tree_url, product, ova_filename)

        build_list.append({'product': product_name, 'id': id, 'version': version,
                           'build_tree_url': build_tree_url, 'ova_path': ova_path, 'ova_filename': ova_filename})

    return build_list

def get_uri(build_list, product):
    for build in build_list:
        if build.get('product') == product:
            return build.get('ova_path')

def get_filename(build_list, product):
    for build in build_list:
        if build.get('product') == product:
            return build.get('ova_filename')

def main():
    global module
    module = AnsibleModule(
        argument_spec = dict(
            build_id=dict(required=True),
        ),
        supports_check_mode = True,
    )

    build_infos = get_buildweb_data(module.params['build_id'], module)

    nsx_manager_uri = get_uri(build_infos, 'nsx-manager')
    nsx_controller_uri = get_uri(build_infos, 'nsx-controller')
    nsx_gw_uri = get_uri(build_infos, 'nsx-edge')
    nsx_manager_filename = get_filename(build_infos, 'nsx-manager')
    nsx_controller_filename = get_filename(build_infos, 'nsx-controller')
    nsx_gw_filename = get_filename(build_infos, 'nsx-edge')

    facts = {'nsx_manager_uri': nsx_manager_uri, 'nsx_controller_uri' : nsx_controller_uri, 'nsx_gw_uri': nsx_gw_uri,
             'nsx_manager_filename': nsx_manager_filename, 'nsx_controller_filename' : nsx_controller_filename,
             'nsx_gw_filename': nsx_gw_filename}

    module.exit_json(changed=False, ansible_facts=facts)


from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
main()
