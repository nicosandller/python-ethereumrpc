import requests
import json
import decimal
from requests.exceptions import ConnectionError
import logging

log = logging.getLogger("EtherRpc")


class EtherRpcWrapper(object):

    def __init__(self,
                 rpchost,
                 rpcport,
                 rpc_call=None,
                 ):
        self.__rpchost = rpchost
        self.__rpcport = rpcport
        self.__rpc_call = rpc_call
        self.__headers = {'Host': self.__rpchost,
                          'User-Agent': 'EtherRpcWrapper v0.1',
                          'Content-type': 'application/json'
                          }
