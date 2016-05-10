=================
python-ethereumrpc
=================

This module was based on jgarzik's python-bitcoinrpc with some small mods based
on ethereum's rpc and one major change to use requests library instead of
httplib for the calls.

Installation
============

Install the library using pip::

    pip install python-ethereumrpc

Example
=======
.. code:: python

    from ether_rpc_wrapper import EtherRpcWrapper

    rpc_connection = EtherRpcWrapper(rpochost, rpcport)
    best_block_hash = rpc_connection.eth_blockNumber()
    print(rpc_connection.eth_getBlockByNumber(best_block_hash))
