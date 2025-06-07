import os
from xrpl.asyncio.clients import AsyncJsonRpcClient

TESTNET_URL = os.getenv("XRPL_RPC_URL")

class XrplSingleton:
    """Singleton class for Xrpl client."""
    _instance = None


    @staticmethod
    def get_instance():
        if XrplSingleton._instance is None:
            XrplSingleton._instance = AsyncJsonRpcClient(TESTNET_URL)
        return XrplSingleton._instance

# Create a single instance to be reused
xrpl_client = XrplSingleton.get_instance()
