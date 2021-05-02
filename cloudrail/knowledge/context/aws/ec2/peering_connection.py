from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


@dataclass
class PeeringVpcInfo:
    vpc_id: str
    cidr_blocks: List[str]


class PeeringConnection(AwsResource):
    def __init__(self,
                 peering_id: str,
                 accepter_vpc_info: PeeringVpcInfo,
                 requester_vpc_info: PeeringVpcInfo,
                 status: str,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_VPC_PEERING_CONNECTION)
        self.peering_id: str = peering_id
        self.accepter_vpc_info: PeeringVpcInfo = accepter_vpc_info
        self.requester_vpc_info: PeeringVpcInfo = requester_vpc_info
        self.status: str = status

    @abstractmethod
    def get_keys(self) -> List[str]:
        return [self.peering_id]

    def get_extra_data(self) -> str:
        vpcs = f'vpcs: {[self.accepter_vpc_info.vpc_id, self.requester_vpc_info.vpc_id]}'
        status = 'status: {}'.format(self.status) if self.status else ''
        return ', '.join([vpcs, status])

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'VPC peering connection'
        else:
            return 'VPC peering connections'

    def get_id(self) -> str:
        return self.peering_id

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#PeeringConnections:vpcPeeringConnectionId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.peering_id)

    @property
    def is_tagable(self) -> bool:
        return True
