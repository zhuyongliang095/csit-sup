# Copyright (c) 2016 Cisco and/or its affiliates.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

*** Settings ***
| Library | resources.libraries.python.InterfaceUtil
| Library | resources.libraries.python.NodePath

*** Keywords ***
| SUP Configure path in 2-node circular topology
| | [Documentation] | Compute path for testing on two given nodes in circular
| | ...             | topology and set corresponding test case variables.
| | ...
| | ... | *Arguments:*
| | ... | - ${tg_node} - TG node. Type: dictionary
| | ... | - ${dut_node} - DUT node. Type: dictionary
| | ... | - ${tg2_node} - Node where the path ends. Must be the same as TG node
| | ... |   parameter in circular topology. Type: dictionary
| | ...
| | ... | *Return:*
| | ... | - No value returned
| | ...
| | ... | _NOTE:_ This KW sets following test case variables:
| | ... | - ${tg_node} - TG node.
| | ... | - ${tg_to_dut_if1} - 1st TG interface towards DUT.
| | ... | - ${tg_to_dut_if2} - 2nd TG interface towards DUT.
| | ... | - ${dut_node} - DUT node.
| | ... | - ${dut_to_tg_if1} - 1st DUT interface towards TG.
| | ... | - ${dut_to_tg_if2} - 2nd DUT interface towards TG.
| | ... | - ${tg_to_dut_if1_mac}
| | ... | - ${tg_to_dut_if2_mac}
| | ... | - ${dut_to_tg_if1_mac}
| | ... | - ${dut_to_tg_if2_mac}
| | ...
| | ... | *Example:*
| | ...
| | ... | \| Given Configure path in 2-node circular topology \| ${nodes['TG']} \
| | ... | \| ${nodes['DUT1']} \| ${nodes['TG']} \|
| | ...
| | [Arguments] | ${tg_node} | ${dut_node} | ${tg2_node}
| | Should Be Equal | ${tg_node} | ${tg2_node}
| | Append Nodes | ${tg_node} | ${dut_node} | ${tg_node}
| | Compute Path | always_same_link=${FALSE}
| | ${tg_to_dut_if1} | ${tmp}= | First Interface
| | ${tg_to_dut_if2} | ${tmp}= | Last Interface
| | ${dut_to_tg_if1} | ${tmp}= | First Ingress Interface
| | ${dut_to_tg_if2} | ${tmp}= | Last Egress Interface
| | ${tg_to_dut_if1_mac}= | Get interface mac | ${tg_node} | ${tg_to_dut_if1}
| | ${tg_to_dut_if2_mac}= | Get interface mac | ${tg_node} | ${tg_to_dut_if2}
| | ${dut_to_tg_if1_mac}= | Get interface mac | ${dut_node} | ${dut_to_tg_if1}
| | ${dut_to_tg_if2_mac}= | Get interface mac | ${dut_node} | ${dut_to_tg_if2}
| | ${dut_to_tg_if1_name}= | Get interface name | ${dut_node} | ${dut_to_tg_if1}
| | ${dut_to_tg_if2_name}= | Get interface name | ${dut_node} | ${dut_to_tg_if2}
| | Set Test Variable | ${tg_to_dut_if1}
| | Set Test Variable | ${tg_to_dut_if2}
| | Set Test Variable | ${dut_to_tg_if1}
| | Set Test Variable | ${dut_to_tg_if2}
| | Set Test Variable | ${tg_to_dut_if1_mac}
| | Set Test Variable | ${tg_to_dut_if2_mac}
| | Set Test Variable | ${dut_to_tg_if1_mac}
| | Set Test Variable | ${dut_to_tg_if2_mac}
| | Set Test Variable | ${dut_to_tg_if1_name}
| | Set Test Variable | ${dut_to_tg_if2_name}
| | Set Test Variable | ${tg_node}
| | Set Test Variable | ${dut_node}