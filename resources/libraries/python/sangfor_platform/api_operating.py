# Copyright (c) 2018 sangfor.
# Licensed under the Apache License, Version 2.0 (the "License");
# author @zhuyl
# time 20180119

"""sangfor platform api library."""

import requests

class api_operating(object):
    """sangfor platform api configure."""
    
    @staticmethod
    def platform_cfg_api_get(node,url):
        """sangfor platform configure of api get

        param node: Node in topology
        param url: url for configure
        type node: dict
        type url: str
        return : replay status_code 
        rtype : int
        return : replay text
        rtype : str
        """
        host=node['host']
        url='http://'+host+':80/'+url
        re=requests.get(url)
        status_code = re.status_code
        replay_text = re.text
        re.close()
        return status_code,replay_text
        
    @staticmethod
    def platform_cfg_api_post(node,url,cfg):
        """sangfor platform configure of api post

        param node: Node in topology
        param url: url for configure
        param cfg: configuration
        type node: dict
        type url: str
        type cfg: dict
        return : replay status_code 
        rtype : int
        return : replay text
        rtype : str
        """
        host=node['host']
        url='http://'+host+':80/'+url
        re=requests.post(url,cfg)
        status_code = re.status_code
        replay_text = re.text
        re.close()
        return status_code,replay_text
        
    @staticmethod
    def platform_cfg_api_del(node,url):
        """sangfor platform configure of api del

        param node: Node in topology
        param url: url for configure
        type node: dict
        type url: str
        return : 
        rtype : 
        """
        host=node['host']
        url='http://'+host+':80/'+url
        re=requests.delete(url,)
        status_code = re.status_code
        replay_text = re.text
        re.close()
        return status_code,replay_text