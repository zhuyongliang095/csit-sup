# Copyright (c) 2018 sangfor.
# Licensed under the Apache License, Version 2.0 (the "License");
# author @zhuyl
# time 20180119

"""sangfor platform api library."""

from resources.libraries.python.sangfor_platform.config_ipc import config_ipc,config_ipc_data

class l2_config(object):
    
    @staticmethod
    def sup_l2_config_access(node,interface,vlanid):
        oper='edit'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','vlan')
        tmp.set_config_member('interface_name',"{}".format(interface))
        tmp.set_config_member('access_vlanid',vlanid)
        data=tme.get_data()
        msg=config_ipc.config_api(node,data)
        
    @staticmethod
    def sup_l2_config_trunk(node,interface,trunk_list=[]):
        oper='edit'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','vlan')
        tmp.set_config_member('interface_name',"{}".format(interface))
        tmp.set_config_member('vlan_bitmap',trunk_list)
        data=tme.get_data()
        msg=config_ipc.config_api(node,data)
    
    @staticmethod
    def sup_l2_config_native(node,interface,nativeid):
        oper='edit'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','vlan')
        tmp.set_config_member('interface_name',"{}".format(interface))
        tmp.set_config_member('native_vlanid',nativeid)
        data=tme.get_data()
        msg=config_ipc.config_api(node,data)
        
    @staticmethod
    def sup_l2_config_trunk_native(node,interface,nativeid):
        oper='edit'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','vlan')
        tmp.set_config_member('interface_name',"{}".format(interface))
        tmp.set_config_member('vlan_bitmap',trunk_list)
        tmp.set_config_member('native_vlanid',nativeid)
        data=tme.get_data()
        msg=config_ipc.config_api(node,data)
        
    @staticmethod
    def sup_l2_config_show(node,):
        oper='query'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','vlan_show')
        data=tme.get_data()
        return config_ipc.config_api(node,data)
        
    @staticmethod
    def sup_l2_config_access_show(node,):
        oper='query'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','vlan_show')
        data=tme.get_data()
        msg=l2_config.sup_l2_config_show(node,)
        
        
    @staticmethod
    def sup_l2_config_trunk_show(node,):
        oper='query'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','vlan_show')
        data=tme.get_data()
        msg=config_ipc.config_api(node,data)
        
    @staticmethod
    def sup_l2_config_native_show(node,):
        oper='query'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','vlan_show')
        data=tme.get_data()
        msg=config_ipc.config_api(node,data)