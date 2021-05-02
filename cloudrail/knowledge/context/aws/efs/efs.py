from typing import List
from cloudrail.knowledge.context.aws.efs.efs_policy import EfsPolicy
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class Efs(AwsResource):

    def __init__(self,
                 creation_token: str,
                 efs_id: str,
                 arn: str,
                 encrypted: bool,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_EFS_FILE_SYSTEM)
        self.creation_token: str = creation_token
        self.efs_id: str = efs_id
        self.arn: str = arn
        self.policy: EfsPolicy = None
        self.encrypted: bool = encrypted

    def get_keys(self) -> List[str]:
        return [self.efs_id]

    def get_name(self) -> str:
        return self.creation_token

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'EFS file system'
        else:
            return 'EFS file systems'

    def get_cloud_resource_url(self) -> str:
        return '{0}efs/home?region={1}#/file-systems/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.efs_id)

    @property
    def is_tagable(self) -> bool:
        return True
