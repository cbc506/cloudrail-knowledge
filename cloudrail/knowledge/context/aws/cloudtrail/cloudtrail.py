from typing import List
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class CloudTrail(AwsResource):

    def __init__(self,
                 name: str,
                 kms_encryption: bool,
                 arn: str,
                 log_file_validation: bool,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_CLOUDTRAIL)
        self.name: str = name
        self.kms_encryption: bool = kms_encryption
        self.arn: str = arn
        self.log_file_validation: bool = log_file_validation

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.name

    def get_arn(self) -> str:
        return self.arn

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'CloudTrail'
        else:
            return 'CloudTrails'

    def get_cloud_resource_url(self) -> str:
        return '{0}cloudtrail/home?region={1}#/trails/{2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.arn)

    @property
    def is_tagable(self) -> bool:
        return True
