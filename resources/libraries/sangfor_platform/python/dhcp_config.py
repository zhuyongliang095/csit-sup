# Copyright (c) 2018 sangfor.
# Licensed under the Apache License, Version 2.0 (the "License");
# author @zhuyl
# time 20180119

"""sangfor platform api library."""

import json

from robot.api import logger

from resources.libraries.sangfor_platform.python.config_ipc import config_ipc,config_ipc_data

class dhcp_config(object):

    def sup_set_dhcp_server(self, node, dhcp_pool_name, start_ip, end_ip, gateway, netmask, lease , dns=[], wins=[]):
        '''config dhcp server for sangfor sup
        
        :param node: sangfor sup node.
        :param dhcp_pool_name: dhcp pool name.
        :param start_ip: dhcp pool start ip.
        :param end_ip: dhcp pool end ip.
        :param gateway: dhcp pool gataway.
        :param netmask: dhcp pool netmask.
        :param lease: dhcp pool lease.
        :param dns: dhcp pool dns.
        :param wins: dhcp pool dns.
        :type node: node
        :type string: str
        :type string: ipv4 eg 1.1.1.10
        :type string: ipv4 eg 1.1.1.20
        :type string: ipv4 eg 1.1.1.1
        :type string: ipv4 eg 255.255.255.0
        :type list: list eg ['202.106.0.20'] or ['192.168.0.1','202.106.0.20']
        :type list: list eg ['202.106.0.20'] or ['192.168.0.1','202.106.0.20']
        :type list: int eg 3600
        '''
        oper='edit'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','dhcp_pool')
        tmp.set_config_member('dhcp_pool_name',"{}".format(dhcp_pool_name))
        tmp.set_config_member('gateway',"{}".format(gateway))
        tmp.set_config_member('netmask',"{}".format(netmask))
        tmp.set_config_member('start_ip',"{}".format(start_ip))
        tmp.set_config_member('end_ip',"{}".format(end_ip))
        tmp.set_config_member('lease',"{}".format(lease))
        
        if isinstance(dns, list): 
            tmp.set_config_member('dns',dns)
        else 
            raise "type(dns) is not list : {}".format(dns)
        if isinstance(wins, list): 
            tmp.set_config_member('wins',wins)
        else 
            raise "type(wins) is not list : {}".format(wins)
            
        data=tmp.get_data()
        msg=config_ipc.config_api(node,data)
        
    def sup_del_dhcp_server(self, node, dhcp_pool_name):
        '''config dhcp server for sangfor sup
        
        :param node: sangfor sup node.
        :param dhcp_pool_name: dhcp pool name.
        :type node: node
        :type string: str
        '''
        oper='delete'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','dhcp_pool')
        tmp.set_config_member('dhcp_pool_name',"{}".format(dhcp_pool_name))
        
        data=tmp.get_data()
        msg=config_ipc.config_api(node,data)
        
        
    def sup_show_dhcp_server_all(self,node):
        oper='query'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','dhcp_pool_show')
        data=tmp.get_data()
        msg=config_ipc.config_api(node,data)
        
    def sup_show_dhcp_server(self,node,dhcp_pool_name):
        oper='query'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','dhcp_pool_show')
        tmp.set_config_member('dhcp_pool_name',dhcp_pool_name)
        data=tmp.get_data()
        msg=config_ipc.config_api(node,data)
    