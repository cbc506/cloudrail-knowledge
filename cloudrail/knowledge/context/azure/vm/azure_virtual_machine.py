from enum import Enum
from typing import List, Optional

from cloudrail.knowledge.context.azure.azure_resource import AzureResource
from cloudrail.knowledge.context.azure.constants.azure_resource_type import AzureResourceType
from cloudrail.knowledge.context.azure.network_resource import NetworkResource


class OperatingSystemType(Enum):
    WINDOWS = 'Windows'
    LINUX = 'Linux'


class AzureVirtualMachine(AzureResource):
    """
        Attributes:
            name: The name of this Public IP.
            network_interface_ids: A list of Network Interface ID's which are associated with the Virtual Machine.
            network_interfaces: A list of Network Interface which are associated with the Virtual Machine.
    """
    def __init__(self, name: str, network_interface_ids: List[str], os_type: OperatingSystemType):
        super().__init__(AzureResourceType.AZURERM_VIRTUAL_MACHINE)
        self.name: str = name
        self.network_interface_ids: List[str] = network_interface_ids
        self.os_type: OperatingSystemType = os_type
        self.network_resource: NetworkResource = NetworkResource()

    def get_keys(self) -> List[str]:
        return [self.get_id()]

    def get_cloud_resource_url(self) -> Optional[str]:
        pass

    @property
    def is_tagable(self) -> bool:
        return True
