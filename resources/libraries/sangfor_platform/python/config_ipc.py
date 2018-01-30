# Copyright (c) 2018 sangfor.
# Licensed under the Apache License, Version 2.0 (the "License");
# author @zhuyl
# time 20180119

"""sangfor platform api library."""

import socket
import json
import struct

from robot.api import logger

class config_ipc(object):

    @staticmethod
    def _generate_socket(SERVER_IP,SERVER_PORT):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, e:
            raise IOError('socket init error :%s' % e)
            
        try:
            sock.connect((SERVER_IP, SERVER_PORT))
        except socket.gaierror, e:
            sock.close()
            raise IOError('connect to server %s fail :%s' % SERVER_PATH, e)
            
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 256 * 1024)
        except socket.error,e:
            sock.close()
            raise IOError('socket SO_SNDBUF opt set fail :%s' % e)
            
        return sock
    
    @staticmethod
    def _close_socket(sock):
        try:
            sock.close()
        except socket.error,e:
            logger.debug("close socket error : {}".format(e))
    
    @staticmethod
    def _send(sock, send_buf):
        try:
            sock.sendall(send_buf)
        except socket.error:
            raise IOError('send buf error %s' % str(send_buf))
    
    @staticmethod
    def _recv(sock, buf_len):
        try:
            ret = sock.recv(buf_len)
        except socket.error:
            raise IOError('recv buf error')
        return ret
    
    @staticmethod
    def _send_recv(sock, send_buf, recv_len):
        config_ipc._send(sock,send_buf)
        ret=config_ipc._recv(sock,recv_len)
        
        while True:
            other_ret = config_ipc._recv(sock,recv_len)
            if not other_ret:
                break
            ret += str(other_ret)
        
        return ret
    
    @staticmethod
    def config_api(node,data):
        '''sangfor platform configure api
        
        param node : Node in topolgy
        param data : config data
        type node : dict
        type data : dict
        return : response msg
        rtype : str
        '''
        service=node['host']
        port=5654
        data=json.dumps(data)
        logger.debug("config :{}".format(data))
        data = struct.pack('!L', len(data))+data
        sock=config_ipc._generate_socket(service,port)
        msg=config_ipc._send_recv(sock,data,256 * 1024)
        config_ipc._close_socket(sock)
        logger.debug("response:{}".format(msg))
        return msg
        
        
class config_ipc_data(object):
    
    def __init__(self):
        self._api_config_data={"language":"en",
            "version":1,
            "operator":"query",
            "config":{
            "configStructName":"vlan_show",
            }
        }
    
    def set_oper(self,oper):
        self._api_config_data['operator']=oper
        
    def set_config_member(self,member,value):
        self._api_config_data['config'][member]=value
        
    def set_config_level_structName(self,name):
        self._api_config_data['config']['level']=[{}]
        self._api_config_data['config']['level'][0]['configStructName']=name
    
    def set_config_level_member(self,member,value):
        self._api_config_data['config']['level'][0][member]=value
        
    def get_data(self):
        return self._api_config_data
    
#import requests
#class api_operating(object):
#    """sangfor platform api configure."""
#    
#    @staticmethod
#    def platform_cfg_api_get(node,url):
#        """sangfor platform configure of api get
#
#        param node: Node in topology
#        param url: url for configure
#        type node: dict
#        type url: str
#        return : replay status_code 
#        rtype : int
#        return : replay text
#        rtype : str
#        """
#        host=node['host']
#        url='http://'+host+':80/'+url
#        re=requests.get(url)
#        status_code = re.status_code
#        replay_text = re.text
#        re.close()
#        return status_code,replay_text
#        
#    @staticmethod
#    def platform_cfg_api_post(node,url,cfg):
#        """sangfor platform configure of api post
#
#        param node: Node in topology
#        param url: url for configure
#        param cfg: configuration
#        type node: dict
#        type url: str
#        type cfg: dict
#        return : replay status_code 
#        rtype : int
#        return : replay text
#        rtype : str
#        """
#        host=node['host']
#        url='http://'+host+':80/'+url
#        re=requests.post(url,cfg)
#        status_code = re.status_code
#        replay_text = re.text
#        re.close()
#        return status_code,replay_text
#        
#    @staticmethod
#    def platform_cfg_api_del(node,url):
#        """sangfor platform configure of api del
#
#        param node: Node in topology
#        param url: url for configure
#        type node: dict
#        type url: str
#        return : 
#        rtype : 
#        """
#        host=node['host']
#        url='http://'+host+':80/'+url
#        re=requests.delete(url,)
#        status_code = re.status_code
#        replay_text = re.text
#        re.close()
#        return status_code,replay_text