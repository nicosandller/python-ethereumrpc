import requests
import json
import decimal
from requests.exceptions import ConnectionError
import logging

log = logging.getLogger("EtherRpc")


class EtherRpcWrapper(object):
    __id_count = 0

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

    def __getattr__(self, name):
        """
        Return an instance of EtherRpcWrapper with an rpc_call defined.
        When the attribute (method) is not defined (i.e: instance.getinfo()),
        then __getattr__ is called with the name (getinfo) as parameter.
        It then calls EtherRpcWrapper as a function,
        defining self.rpc_call to the attribute's name.
        """
        if name.startswith('__') and name.endswith('__'):
            raise AttributeError
        if self.__rpc_call is not None:
            name = "%s.%s" % (self.__rpc_call, name)
        # Return an instance of the client. Will call the __call__ method.
        log.debug('Making http request with method:%s' % name)
        return EtherRpcWrapper(self.__rpchost, self.__rpcport, name)
