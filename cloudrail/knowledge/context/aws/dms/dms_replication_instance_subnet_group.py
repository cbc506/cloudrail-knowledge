from typing import List, Optional
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class DmsReplicationInstanceSubnetGroup(AwsResource):

    def __init__(self,
                 account: str,
                 region: str,
                 rep_subnet_group_id: str,
                 subnet_ids: List,
                 vpc_id: Optional[str]):
        super().__init__(account, region, AwsServiceName.AWS_DMS_REPLICATION_SUBNET_GROUP)
        self.rep_subnet_group_id: str = rep_subnet_group_id
        self.subnet_ids: List = subnet_ids
        self.vpc_id: Optional[str] = vpc_id

    def get_keys(self) -> List[str]:
        return [self.account, self.region, self.rep_subnet_group_id]

    def get_id(self) -> str:
        return self.rep_subnet_group_id

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Dms Subnet Group'
        else:
            return 'Dms Subnet Groups'

    def get_arn(self) -> str:
        return f"arn:aws:dms:{self.region}:{self.account}:subgrp:{self.rep_subnet_group_id}"

    def get_cloud_resource_url(self) -> str:
        return '{0}dms/v2/home?region={1}#subnetGroupDetail/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.rep_subnet_group_id)

    @property
    def is_tagable(self) -> bool:
        return True
