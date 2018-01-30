| *** Settings *** |
| Library        | resources.libraries.python.NodePath |
| Library        | resources.libraries.python.Trace |
| Resource       | resources/libraries/robot/shared/default.robot |
| Resource       | resources/libraries/robot/shared/interfaces.robot |
| Resource       | resources/libraries/robot/ip/ip4.robot |
| Library        | resources.libraries.sangfor_platform.python.inter_config |
| Library        | resources.libraries.python.IPv4Setup.IPv4Setup |

| *** Variables *** |
| ${ip4_profix_24} | 24 |

| *** Test Cases *** |
| TC01:DUT replies to ICMPv4 Echo Req to its ingress interface |
|    | Append Nodes | ${nodes['TG']} | ${nodes['DUT1']} |
|    | Compute Path |
|    | ${src_port} | ${src_node}= | First Interface |
|    | ${dst_port} | ${dst_node}= | Last Interface |
|    | ${src_port_name}= | Get interface name | ${src_node} | ${src_port} |
|    | ${dst_port_name}= | Get interface name | ${dst_node} | ${dst_port} |
|    | ${hops}= | Set Variable | ${0} |
|    | ${src_ip}= | Get IPv4 Address Of Node "${src_node}" Interface "${src_port}" From "${nodes_ipv4_addr}" |
|    | ${dst_ip}= | Get IPv4 Address Of Node "${dst_node}" Interface "${dst_port}" From "${nodes_ipv4_addr}" |
|    | Sup Set Interface Ip4 | ${src_node} | ${src_port_name} | ${src_ip} | ${ip4_profix_24} |
|    | Sup Set Interface Ip4 | ${dst_node} | ${dst_port_name} | ${dst_ip} | ${ip4_profix_24} |
|    | Route Traffic from interface '${src_port}' on node '${src_node}' to interface '${dst_port}' on node '${dst_node}' '${hops}' hops away using IPv4 |
|    | [Teardown] | Run Keywords | Sup Unset Interface Ip4 | ${src_node} | ${src_port_name} | ${src_ip} | ${ip4_profix_24} |
|    | ... | AND | Sup Unset Interface Ip4 | ${dst_node} | ${dst_port_name} | ${dst_ip} | ${ip4_profix_24} |
