from typing import List, Optional

from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class DocumentDbCluster(AwsResource):

    def __init__(self,
                 cluster_identifier: str,
                 storage_encrypted: bool,
                 parameter_group_name: str,
                 kms_key_id: str,
                 region: str,
                 account: str,
                 cluster_arn: str):
        super().__init__(account, region, AwsServiceName.AWS_DOCDB_CLUSTER)
        self.cluster_identifier: str = cluster_identifier
        self.storage_encrypted: bool = storage_encrypted
        self.parameter_group_name: str = parameter_group_name
        self.kms_key_id: str = kms_key_id
        self.kms_data: Optional[KmsKey] = None
        self.cluster_arn: str = cluster_arn

    def get_keys(self) -> List[str]:
        return [self.account, self.region, self.cluster_identifier]

    def get_name(self) -> str:
        return self.cluster_identifier

    def get_arn(self) -> str:
        return self.cluster_arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'DocumentDB Cluster'
        else:
            return 'DocumentDB Clusters'

    def get_cloud_resource_url(self) -> str:
        return '{0}docdb/home?region={1}#cluster-details/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.cluster_identifier)

    @property
    def is_tagable(self) -> bool:
        return True
