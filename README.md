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

Example (based on python-bitcoinrpc's documentation)
=======
.. code:: python

    from ether_rpc_wrapper import EtherRpcWrapper

    # rpc_user and rpc_password are set in the bitcoin.conf file
    rpc_connection = EtherRpcWrapper(rpochost, rpcport)
    best_block_hash = rpc_connection.eth_blockNumber()

    // Result
    {
    "id":83,
    "jsonrpc": "2.0",
    "result": "0x4b7" // 1207
    }

    print(rpc_connection.eth_getBlockByNumber(best_block_hash))
