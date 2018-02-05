# Copyright (c) 2018 sangfor.
# Licensed under the Apache License, Version 2.0 (the "License");
# author @zhuyl
# time 20180119

"""sangfor platform api library."""

import json

from robot.api import logger

from resources.libraries.sangfor_platform.python.config_ipc import config_ipc,config_ipc_data

def _profix_to_ip4(profix):
    profix=int(profix)
    bitmap=[0]*4
    for x in range(profix/8):
        bitmap[x]=255
    for x in range(profix%8):
        mask=0x1<<(8-x)
        bitmap[profix/8+1]|=mask
    for x in range(len(bitmap)):
        bitmap[x]=str(bitmap[x])
    return '.'.join(bitmap)

class inter_config():
    
    def sup_set_interface_ip4(self,node,interface,ip4,profix):
        if node['type'] == 'DUT' :
            oper='edit'
            tmp=config_ipc_data()
            tmp.set_oper(oper)
            tmp.set_config_member('configStructName','interface')
            tmp.set_config_member('ifname',"{}".format(interface))
            tmp.set_config_member('ipv4',"{}".format(ip4))
            tmp.set_config_member('ipmaskv4',"{}".format(_profix_to_ip4(profix)))
            data=tmp.get_data()
            msg=config_ipc.config_api(node,data)
        else :
            logger.debug("type : {} ,don't set ip".format(node['type']))
            
    def sup_set_interface_secondary_ip4(self,node,interface,ip4,profix):
        if node['type'] == 'DUT' :
            oper='edit'
            tmp=config_ipc_data()
            tmp.set_oper(oper)
            tmp.set_config_member('configStructName','interface_secondary_ipv4')
            tmp.set_config_member('ipv4',ip4)
            tmp.set_config_member('ipmaskv4',profix)
            tmp.set_config_level_structName('interface')
            tmp.set_config_level_member('ifname',"{}".format(interface))
            data=tmp.get_data()
            msg=config_ipc.config_api(node,data)
        else :
            logger.debug("type : {} ,don't set ip".format(node['type']))
    
    def sup_unset_interface_ip4(self,node,interface,ip4,profix):
        if node['type'] == 'DUT' :
            oper='unset'
            tmp=config_ipc_data()
            tmp.set_oper(oper)
            tmp.set_config_member('configStructName','interface')
            tmp.set_config_member('ifname',"{}".format(interface))
            tmp.set_config_member('ipv4',"{}".format(ip4))
            tmp.set_config_member('ipmaskv4',"{}".format(_profix_to_ip4(profix)))
            tmp.set_config_member("mode_flags", 1)
            data=tmp.get_data()
            msg=config_ipc.config_api(node,data)
        else :
            logger.debug("type : {} ,don't unset ip".format(node['type']))
    
    def sup_del_interface_secondary_ip4(self,node,interface,ip4,profix):
        if node['type'] == 'DUT' :
            oper='delete'
            tmp=config_ipc_data()
            tmp.set_oper(oper)
            tmp.set_config_member('configStructName','interface_secondary_ipv4')
            tmp.set_config_member('ipv4',ip4)
            tmp.set_config_member('ipmaskv4',profix)
            tmp.set_config_level_structName('interface')
            tmp.set_config_level_member('ifname',"{}".format(interface))
            data=tmp.get_data()
            msg=config_ipc.config_api(node,data)
        else :
            logger.debug("type : {} ,don't set ip".format(node['type']))
    
    def sup_set_interface_dhcpServer(self,node,interface,dhcp_pool_name):
        if node['type'] == 'DUT' :
            oper='edit'
            tmp=config_ipc_data()
            tmp.set_oper(oper)
            tmp.set_config_member('configStructName','interface')
            tmp.set_config_member('ifname',"{}".format(interface))
            tmp.set_config_member('dhcp_pool_name',"{}".format(dhcp_pool_name))
            data=tmp.get_data()
            msg=config_ipc.config_api(node,data)
        else :
            logger.debug("type : {} ,don't unset ip".format(node['type']))
    
    def sup_unset_interface_dhcpServer(self,node,interface):
        if node['type'] == 'DUT' :
            oper='unset'
            tmp=config_ipc_data()
            tmp.set_oper(oper)
            tmp.set_config_member('configStructName','interface')
            tmp.set_config_member('ifname',"{}".format(interface))
            tmp.set_config_member('dhcp_pool_name',"")
            data=tmp.get_data()
            msg=config_ipc.config_api(node,data)
        else :
            logger.debug("type : {} ,don't unset ip".format(node['type']))