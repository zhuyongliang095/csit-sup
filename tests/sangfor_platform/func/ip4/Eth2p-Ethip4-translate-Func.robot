| *** Settings *** |
| Library        | resources.libraries.python.NodePath |
| Library        | resources.libraries.python.Trace |
| Library        | resources.libraries.sangfor_platform.python.inter_config |
| Library        | resources.libraries.python.IPv4Setup.IPv4Setup |
| Library        | resources.libraries.sangfor_platform.python.SUP_IPv4Setup |
| Library        | resources.libraries.sangfor_platform.python.static_route_config |
| Resource       | resources/libraries/robot/shared/default.robot |
| Resource       | resources/libraries/robot/shared/interfaces.robot |
| Resource       | resources/libraries/robot/ip/ip4.robot |

| *** Variables *** |
| ${ip4_profix_24} | 24 |

| *** Test Cases *** |
| TC01:DUT1 with ICMP4 translate between TG and DUT2 links |
|    | [Setup] | Run Keywords | Save Vpp PIDs |
|    | ... | AND | Reset VAT History On All DUTs | ${nodes} |
|    | ... | AND | Clear interface counters on all vpp nodes in topology | ${nodes} |
|    | Append Nodes | ${nodes['TG']} | ${nodes['DUT1']} | ${nodes['DUT2']} |
|    | Compute Path | always_same_link=False |
|    | ${TG_to_DUT1_port} | ${tmp}= | Next Interface |
|    | ${DUT1_to_TG_port} | ${tmp}= | Next Interface |
|    | ${DUT1_to_DUT2_port} | ${tmp}= | Next Interface |
|    | ${DUT2_to_DUT1_port} | ${tmp}= | Last Interface |
|    | ${DUT1_to_TG_name}= | Get interface name | ${nodes['DUT1']} | ${DUT1_to_TG_port} |
|    | ${DUT1_to_DUT2_name}= | Get interface name | ${nodes['DUT1']} | ${DUT1_to_DUT2_port} |
|    | ${DUT2_to_DUT1_name}= | Get interface name | ${nodes['DUT2']} | ${DUT2_to_DUT1_port} |
|    | ${hops}= | Set Variable | ${1} |
|    | ${TG_to_DUT1_IP}= | Get IPv4 Address Of Node "${nodes['TG']}" Interface "${TG_to_DUT1_port}" From "${nodes_ipv4_addr}" |
|    | ${DUT1_to_TG_IP}= | Get IPv4 Address Of Node "${nodes['DUT1']}" Interface "${DUT1_to_TG_port}" From "${nodes_ipv4_addr}" |
|    | ${DUT1_to_DUT2_IP}= | Get IPv4 Address Of Node "${nodes['DUT1']}" Interface "${DUT1_to_DUT2_port}" From "${nodes_ipv4_addr}" |
|    | ${DUT2_to_DUT1_IP}= | Get IPv4 Address Of Node "${nodes['DUT2']}" Interface "${DUT2_to_DUT1_port}" From "${nodes_ipv4_addr}" |
|    | Sup Set Interface Ip4 | ${nodes['DUT1']} | ${DUT1_to_TG_name} | ${DUT1_to_TG_IP} | ${ip4_profix_24} |
|    | Sup Set Interface Ip4 | ${nodes['DUT1']} | ${DUT1_to_DUT2_name} | ${DUT1_to_DUT2_IP} | ${ip4_profix_24} |
|    | Sup Set Interface Ip4 | ${nodes['DUT2']} | ${DUT2_to_DUT1_name} | ${DUT2_to_DUT1_IP} | ${ip4_profix_24} |
|    | ${TG_and_DUT1_link_network} | ${TG_and_DUT1_link_prefix}= | Sup Get IPv4 network of node "${nodes['DUT1']}" interface "${DUT1_to_TG_port}" from "${nodes_ipv4_addr}" |
|    | Sup Set Static route | ${nodes['DUT2']} | ${TG_and_DUT1_link_network} | ${TG_and_DUT1_link_prefix} | ${DUT1_to_DUT2_IP} |
|    | Route Traffic from interface '${TG_to_DUT1_port}' on node '${nodes['TG']}' to interface '${DUT2_to_DUT1_port}' on node '${nodes['DUT2']}' '${hops}' hops away using IPv4 |
|    | [Teardown] | Run Keywords | Sup Unset Interface Ip4 | ${nodes['DUT1']} | ${DUT1_to_TG_name} | ${DUT1_to_TG_IP} | ${ip4_profix_24} |
|    | ... | AND | Sup unset Interface Ip4 | ${nodes['DUT1']} | ${DUT1_to_DUT2_name} | ${DUT1_to_DUT2_IP} | ${ip4_profix_24} |
|    | ... | AND | Sup Unset Interface Ip4 | ${nodes['DUT2']} | ${DUT2_to_DUT1_name} | ${DUT2_to_DUT1_IP} | ${ip4_profix_24} |
|    | ... | AND | Show Packet trace on all DUTs | ${nodes} |
|    | ... | AND | Show VAT History On All DUTs | ${nodes} |
|    | ... | AND | Verify VPP PID in Teardown |

| TC02:DUT1 and DUT2 with ICMP translate between two TG links |
|    | [Setup] | Run Keywords | Save Vpp PIDs |
|    | ... | AND | Reset VAT History On All DUTs | ${nodes} |
|    | ... | AND | Clear interface counters on all vpp nodes in topology | ${nodes} |
|    | Append Nodes | ${nodes['TG']} | ${nodes['DUT1']} | ${nodes['DUT2']} | ${nodes['TG']} |
|    | Compute Path |
|    | ${TG_to_DUT1_port} | ${tmp}= | Next Interface |
|    | ${DUT1_to_TG_port} | ${tmp}= | Next Interface |
|    | ${DUT1_to_DUT2_port} | ${tmp}= | Next Interface |
|    | ${DUT2_to_DUT1_port} | ${tmp}= | Next Interface |
|    | ${DUT2_to_TG_port} | ${tmp}= | Next Interface |
|    | ${TG_to_DUT2_port} | ${tmp}= | Last Interface |
|    | ${DUT1_to_TG_name}= | Get interface name | ${nodes['DUT1']} | ${DUT1_to_TG_port} |
|    | ${DUT1_to_DUT2_name}= | Get interface name | ${nodes['DUT1']} | ${DUT1_to_DUT2_port} |
|    | ${DUT2_to_DUT1_name}= | Get interface name | ${nodes['DUT2']} | ${DUT2_to_DUT1_port} |
|    | ${DUT2_to_TG_name}= | Get interface name | ${nodes['DUT2']} | ${DUT2_to_TG_port} |
|    | ${hops}= | Set Variable | ${2} |
|    | ${TG_to_DUT1_IP}= | Get IPv4 Address Of Node "${nodes['TG']}" Interface "${TG_to_DUT1_port}" From "${nodes_ipv4_addr}" |
|    | ${DUT1_to_TG_IP}= | Get IPv4 Address Of Node "${nodes['DUT1']}" Interface "${DUT1_to_TG_port}" From "${nodes_ipv4_addr}" |
|    | ${DUT1_to_DUT2_IP}= | Get IPv4 Address Of Node "${nodes['DUT1']}" Interface "${DUT1_to_DUT2_port}" From "${nodes_ipv4_addr}" |
|    | ${DUT2_to_DUT1_IP}= | Get IPv4 Address Of Node "${nodes['DUT2']}" Interface "${DUT2_to_DUT1_port}" From "${nodes_ipv4_addr}" |
|    | ${DUT2_to_TG_IP}= | Get IPv4 Address Of Node "${nodes['DUT2']}" Interface "${DUT2_to_TG_port}" From "${nodes_ipv4_addr}" |
|    | ${TG_and_DUT1_link_network} | ${TG_and_DUT1_link_prefix}= | Sup Get IPv4 network of node "${nodes['DUT1']}" interface "${DUT1_to_TG_port}" from "${nodes_ipv4_addr}" |
|    | ${DUT1_and_DUT2_link_network} | ${DUT1_and_DUT2_link_prefix}= | Sup Get IPv4 network of node "${nodes['DUT1']}" interface "${DUT1_to_DUT2_port}" from "${nodes_ipv4_addr}" |
|    | ${TG_and_DUT2_link_network} | ${TG_and_DUT2_link_prefix}= | Sup Get IPv4 network of node "${nodes['DUT2']}" interface "${DUT2_to_TG_port}" from "${nodes_ipv4_addr}" |
|    | Sup Set Interface Ip4 | ${nodes['DUT1']} | ${DUT1_to_TG_name} | ${DUT1_to_TG_IP} | ${TG_and_DUT1_link_prefix} |
|    | Sup Set Interface Ip4 | ${nodes['DUT1']} | ${DUT1_to_DUT2_name} | ${DUT1_to_DUT2_IP} | ${DUT1_and_DUT2_link_prefix} |
|    | Sup Set Interface Ip4 | ${nodes['DUT2']} | ${DUT2_to_DUT1_name} | ${DUT2_to_DUT1_IP} | ${DUT1_and_DUT2_link_prefix} |
|    | Sup Set Interface Ip4 | ${nodes['DUT2']} | ${DUT2_to_TG_name} | ${DUT2_to_TG_IP} | ${TG_and_DUT2_link_prefix} |
|    | Sup Set Static route | ${nodes['DUT1']} | ${TG_and_DUT2_link_network} | ${TG_and_DUT2_link_prefix} | ${DUT2_to_DUT1_IP} |
|    | Sup Set Static route | ${nodes['DUT2']} | ${TG_and_DUT1_link_network} | ${TG_and_DUT1_link_prefix} | ${DUT1_to_DUT2_IP} |
|    | Route Traffic from interface '${TG_to_DUT1_port}' on node '${nodes['TG']}' to interface '${TG_to_DUT2_port}' on node '${nodes['TG']}' '${hops}' hops away using IPv4 |
|    | [Teardown] | Run Keywords | Sup Unset Interface Ip4 | ${nodes['DUT1']} | ${DUT1_to_TG_name} | ${DUT1_to_TG_IP} | ${TG_and_DUT1_link_prefix} |
|    | ... | AND | Sup unset Interface Ip4 | ${nodes['DUT1']} | ${DUT1_to_DUT2_name} | ${DUT1_to_DUT2_IP} | ${DUT1_and_DUT2_link_prefix} |
|    | ... | AND | Sup Unset Interface Ip4 | ${nodes['DUT2']} | ${DUT2_to_DUT1_name} | ${DUT2_to_DUT1_IP} | ${DUT1_and_DUT2_link_prefix} |
|    | ... | AND | Sup Unset Interface Ip4 | ${nodes['DUT2']} | ${DUT2_to_TG_name} | ${DUT2_to_TG_IP} | ${TG_and_DUT2_link_prefix} |
|    | ... | AND | Show Packet trace on all DUTs | ${nodes} |
|    | ... | AND | Show VAT History On All DUTs | ${nodes} |
|    | ... | AND | Verify VPP PID in Teardown |