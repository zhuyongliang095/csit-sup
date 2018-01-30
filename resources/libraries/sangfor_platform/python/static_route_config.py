# Copyright (c) 2018 sangfor.
# Licensed under the Apache License, Version 2.0 (the "License");
# author @zhuyl

"""sangfor platform api library."""

import json

from robot.api import logger

from resources.libraries.sangfor_platform.python.config_ipc import config_ipc,config_ipc_data

class static_route_config(object):
    
    
    def sup_set_static_route(self,node,network,prefix,nexthop,metric=1):
        oper='edit'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','route')
        tmp.set_config_member('destip',"{}".format(network))
        tmp.set_config_member('masklen',int(prefix))
        tmp.set_config_member('gateway',nexthop)
        tmp.set_config_member('flag',0)
        tmp.set_config_member('distance',int(metric))
        tmp.set_config_member('weight',1)
        tmp.set_config_member("ifname", "")
        data=tmp.get_data()
        logger.debug(data)
        msg=config_ipc.config_api(node,data)
        
    def sup_unset_static_route(self,node,network,prefix,nexthop,metric=1):
        oper='delete'
        tmp=config_ipc_data()
        tmp.set_oper(oper)
        tmp.set_config_member('configStructName','route')
        tmp.set_config_member('destip',"{}".format(network))
        tmp.set_config_member('masklen',int(prefix))
        tmp.set_config_member('gateway',nexthop)
        tmp.set_config_member('flag',0)
        tmp.set_config_member('distance',int(metric))
        tmp.set_config_member('weight',1)
        tmp.set_config_member("ifname", "")
        data=tmp.get_data()
        logger.debug(data)
        msg=config_ipc.config_api(node,data)