from typing import List

from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class S3BucketEncryption(AwsResource):

    def __init__(self,
                 bucket_name: str,
                 encrypted: bool,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_S3_BUCKET)
        self.bucket_name: str = bucket_name
        self.encrypted: bool = encrypted

    def get_keys(self) -> List[str]:
        return [self.bucket_name]

    def get_name(self) -> str:
        return self.bucket_name

    def get_cloud_resource_url(self) -> str:
        return 'https://s3.console.aws.amazon.com/s3/buckets/{0}?region={1}&tab=properties'\
            .format(self.bucket_name, self.region)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False
