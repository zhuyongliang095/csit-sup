| *** Settings *** |
| Documentation  | *L2BD with VLAN tag rewrite test cases - translate-1-1* |
| ...            |
| ...            | *[Top] Network Topologies:* TG-DUT1-DUT2-TG 3-node circular topology |
| ...            | with single links between nodes. |
| ...            | *[Enc] Packet encapsulations:* Eth-dot1q-IPv4-ICMPv4 or |
| ...            | Eth-dot1q-IPv6-ICMPv6 on TG-DUT1 and DUT1-DUT2, Eth-IPv4-ICMPv4 or |
| ...            | Eth-IPv6-ICMPv6 on TG-DUT2 for L2 switching of IPv4/IPv6. |
| ...            | *[Cfg] DUT configuration:* DUT1 is configured with bridge domain (L2BD) |
| ...            | switching combined with MAC learning enabled and added VLAN |
| ...            | sub-interface with VLAN tag rewrite translate-1-1 method of interface |
| ...            | towards TG and interface towards DUT2. DUT2 is configured with L2 |
| ...            | bridge domain (L2BD) switching between VLAN sub-interface with VLAN tag |
| ...            | rewrite pop-1 method of interface towards DUT1 and interface towards TG. |
| ...            | *[Ver] TG verification:* Test ICMPv4 Echo Request packets are |
| ...            | sent from TG on link to DUT1 and received in TG on link form DUT2; |
| ...            | on receive TG verifies packets for correctness and their IPv4 src-addr, |
| ...            | dst-addr and MAC addresses. |
| ...            | *[Ref] Applicable standard specifications:* IEEE 802.1q, IEEE 802.1ad. |
| Test Setup     | Set up functional test |
| Test Teardown  | Tear down functional test |
| Force Tags     | 3_NODE_SINGLE_LINK_TOPO | HW_ENV | VM_ENV | SKIP_VPP_PATCH | SUP | BVT |
| Resource       | resources/libraries/robot/shared/default.robot |
| Resource       | resources/libraries/robot/l2/l2_bridge_domain.robot |
| Resource       | resources/libraries/robot/shared/testing_path.robot |
| Resource       | resources/libraries/robot/l2/tagging.robot |
| Resource       | resources/libraries/robot/l2/l2_traffic.robot |
| Library        | resources.libraries.python.Trace |
| Library        | resources.libraries.sangfor_platform.python.l2_config |
| Resource       | resources/libraries/sangfor_platform/robot/shared/testing_path.robot |

| *** Variables *** |
| ${vlan_access} | 10 |
| ${vlan_trunk}  | ["1-10"] |
| ${vlan_trunk_5} | 5 |
| ${vlan_trunk_10} | 10 |
| ${vlan_native} | 20 |

| *** Test Cases *** |
| TC01:DUT1 with Vlan Access translate-10-10 switch ICMPv4 between two TG links |
|    | [Tags] | SUP | BVT | 3_NODE_SINGLE_LINK_TOPO | HW_ENV |
|    | Given Sup Configure path in 2-node circular topology | ${nodes['TG']} | ${nodes['DUT1']} | ${nodes['TG']} |
|    | When Sup L2 Config Access | ${nodes['DUT1']} | ${dut_to_tg_if1_name} | ${vlan_access} |
|    | And Sup L2 config Access | ${nodes['DUT1']} | ${dut_to_tg_if2_name} | ${vlan_access} |
|    | Then Send ICMPv4 bidirectionally and verify received packets | ${tg_node} | ${tg_to_dut_if1} | ${tg_to_dut_if2} |

| TC02:DUT1 with Vlan Trunk translate-10-10 switch ICMPv4 between two TG links |
|    | [Tags] | SUP | BVT | 3_NODE_SINGLE_LINK_TOPO | HW_ENV |
|    | Given Sup Configure path in 2-node circular topology | ${nodes['TG']} | ${nodes['DUT1']} | ${nodes['TG']} |
|    | When Sup L2 Config trunk | ${nodes['DUT1']} | ${dut_to_tg_if1_name} | ${vlan_trunk} |
|    | And Sup L2 config trunk | ${nodes['DUT1']} | ${dut_to_tg_if2_name} | ${vlan_trunk} |
|    | Then Send ICMP packet and verify received packet | ${tg_node} | ${tg_to_dut_if1} | ${tg_to_dut_if2} | encaps=Dot1q | vlan1=${vlan_trunk_5} | encaps_rx=Dot1q |
|    | Then Send ICMP packet and verify received packet | ${tg_node} | ${tg_to_dut_if1} | ${tg_to_dut_if2} | encaps=Dot1q | vlan1=${vlan_trunk_10} | encaps_rx=Dot1q |

| TC03:DUT1 with Vlan native translate-10-10 switch ICMPv4 between two TG links |
|    | [Tags] | SUP | BVT | 3_NODE_SINGLE_LINK_TOPO | HW_ENV | test |
|    | Given Sup Configure path in 2-node circular topology | ${nodes['TG']} | ${nodes['DUT1']} | ${nodes['TG']} |
|    | When Sup L2 Config native | ${nodes['DUT1']} | ${dut_to_tg_if1_name} | ${vlan_native} |
|    | And Sup L2 config native | ${nodes['DUT1']} | ${dut_to_tg_if2_name} | ${vlan_native} |
|    | Then Send ICMPv4 bidirectionally and verify received packets | ${tg_node} | ${tg_to_dut_if1} | ${tg_to_dut_if2} |
