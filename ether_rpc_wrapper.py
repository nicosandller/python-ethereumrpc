import requests
import json
import decimal
from requests.exceptions import ConnectionError
import logging

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
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

    def __call__(self, *args):
        """
        Make a request to the rpc demon with the method name.
        When the instance of the class is summoned like a function,
        this method gets called.
        """
        EtherRpcWrapper.__id_count += 1
        log.debug("-%s-> %s %s" % (EtherRpcWrapper.__id_count,
                                   self.__rpc_call,
                                   json.dumps(args,
                                              default=self.EncodeDecimal)
                                   ))
        postdata = json.dumps({'version': '1.1',
                               'method': self.__rpc_call,
                               'params': args,
                               'id': EtherRpcWrapper.__id_count
                               },
                              default=self.EncodeDecimal
                              )
        url = ''.join(['http://', self.__rpchost, ':', self.__rpcport])
        try:
            r = requests.post(url, data=postdata, headers=self.__headers)
        except ConnectionError:
            print 'There was a problem connecting to the RPC daemon.'
            print 'Check the connection and connection parameters:'
            error = 'Host: %s, Port: %s, Username: %s, Password: %s' \
                % (self.__rpchost, self.__rpcport,)
            log.error("Error connecting to rpc demon: %s" % error)
            return ConnectionError
        if r.status_code == 200:
            log.debug("Response: %s" % r.json())
            if 'error' in r.json():
                return r.json()
            else:
                return r.json()['result']

        else:
            log.error("Error! Status code: %s" % r.status_code)
            log.error("Text: %s" % r.text)
            log.error("Json: %s" % r.json())
            return r.json()

        def EncodeDecimal(o):
            if isinstance(o, decimal.Decimal):
                return float(round(o, 8))
            raise TypeError(repr(o) + " is not JSON serializable")

        def batch_(self, rpc_calls):
            """
            Batch RPC call.
            Pass array of arrays: [ [ "method", params... ], ... ]
            Returns array of results.
            """
            batch_data = []
            for rpc_call in rpc_calls:
                EtherRpcWrapper.__id_count += 1
                m = rpc_call.pop(0)
                batch_data.append({"jsonrpc": "2.0",
                                   "method": m,
                                   "params": rpc_call,
                                   "id": EtherRpcWrapper.__id_count
                                   })

            postdata = json.dumps(batch_data, default=self.EncodeDecimal)
            log.debug("--> " + postdata)
            url = ''.join(['http://', self.__rpchost, ':', self.__rpcport])
            try:
                r = requests.post(url, data=postdata, headers=self.__headers)
            except ConnectionError:
                print 'There was a problem connecting to the RPC daemon.'
                print 'Check the connection and connection parameters:'
                print 'Host: %s, Port: %s, Username: %s, Password: %s' \
                    % (self.__rpchost, self.__rpcport, self.__rpcuser,
                       self.__rpcpasswd)
                return ConnectionError
            if r.status_code == 200:
                log.info("Response: %s" % r.json())
                if 'error' in r.json():
                    return r.json()
                else:
                    return r.json()['result']
            else:
                log.error("Error! Status code: %s" % r.status_code)
                log.error("Text: %s" % r.text)
                log.error("Json: %s" % r.json())
                return r.json()
