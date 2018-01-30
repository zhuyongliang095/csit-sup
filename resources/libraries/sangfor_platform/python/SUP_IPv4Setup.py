from robot.api.deco import keyword

from resources.libraries.python.topology import NodeType, Topology

class SUP_IPv4Setup(object):
    """SUP IPv4 setup in topology."""
    
    @staticmethod
    @keyword('SUP Get IPv4 network of node "${node}" interface "${port}" '
             'from "${nodes_addr}"')
    def get_ip_network(node, iface_key, nodes_addr):
        """Return IPv4 address of the node port.

        :param node: Node in the topology.
        :param iface_key: Interface key of the node.
        :param nodes_addr: Nodes IPv4 addresses.
        :type node: dict
        :type iface_key: str
        :type nodes_addr: dict
        :returns: IPv4 address.
        :rtype: str
        """
        link = Topology.get_link_by_interface(node, iface_key)
        
        network=nodes_addr[link].get("net_addr")
        prefix=nodes_addr[link].get("prefix")
        
        return network,prefix
       