# Copyright (c) 2018 sangfor.
# Licensed under the Apache License, Version 2.0 (the "License");
# author @zhuyl
# time 20180119

"""sangfor platform api library."""

import json

from robot.api import logger

from resources.libraries.sangfor_platform.python.config_ipc import config_ipc,config_ipc_data

class l2_config(object):
    
    @staticmethod
    def sup_l2_config_access(node,interface,vlanid):
        oper='edit'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','vlan')
        tmp.set_config_member('interface_name',"{}".format(interface))
        tmp.set_config_member('access_vlanid',int(vlanid))
        tmp.set_config_member('native_vlanid',0)
        tmp.set_config_member('vlan_bitmap',[0]*512)
        tmp.set_config_level_structName('interface')
        tmp.set_config_level_member('ifname',"{}".format(interface))
        data=tmp.get_data()
        msg=config_ipc.config_api(node,data)
        
    @staticmethod
    def sup_l2_config_trunk(node,interface,trunk_list=[]):
        oper='edit'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','vlan')
        tmp.set_config_member('interface_name',"{}".format(interface))
        tmp.set_config_member('access_vlanid',0)
        tmp.set_config_level_structName('interface')
        tmp.set_config_level_member('ifname',"{}".format(interface))
        trunk_list=json.loads(trunk_list)
        MIN_VLAN_ID = 1
        MAX_VLAN_ID = 4094
        bitmap=[0]*512
        if trunk_list and len(trunk_list) > 0:
            for i in range(0, len(trunk_list)):
                element = trunk_list[i]
                list = element.split("-")
                if list and len(list) == 1:
                    min_vlanid = int(str(list[0]))
                    max_vlanid = min_vlanid
                elif list and len(list) == 2:
                    min_vlanid = int(str(list[0]))
                    max_vlanid = int(str(list[1]))
                else:
                    logger.warning(
                        "vlan_type is {}, vlanid_range input error ".format(vlan_type)
                        )
                    raise Exception(
                        "vlan_type is {}, vlanid_range input error ".format(vlan_type)
                        )

                if min_vlanid < MIN_VLAN_ID \
                        or max_vlanid > MAX_VLAN_ID \
                        or min_vlanid > max_vlanid:
                    logger.warning(
                        "vlanid_range input error ,please input {}-{}".format(MIN_VLAN_ID, MAX_VLAN_ID)
                        )
                    raise Exception(
                        "vlanid_range input error ,please input {}-{}".format(MIN_VLAN_ID, MAX_VLAN_ID)
                        )

                for ele in range(min_vlanid, max_vlanid + 1):
                    mask = 0x1 << (ele % 8)
                    bitmap[(ele / 8)] |= mask
        tmp.set_config_member('vlan_bitmap',bitmap)
        data=tmp.get_data()
        msg=config_ipc.config_api(node,data)
    
    @staticmethod
    def sup_l2_config_native(node,interface,nativeid):
        oper='edit'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','vlan')
        tmp.set_config_member('interface_name',"{}".format(interface))
        tmp.set_config_member('access_vlanid',0)
        tmp.set_config_member('native_vlanid',int(nativeid))
        tmp.set_config_level_structName('interface')
        tmp.set_config_level_member('ifname',"{}".format(interface))
        data=tmp.get_data()
        msg=config_ipc.config_api(node,data)
        
    @staticmethod
    def sup_l2_config_show(node,):
        oper='query'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','vlan_show')
        data=tmp.get_data()
        return config_ipc.config_api(node,data)
        