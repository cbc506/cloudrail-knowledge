from typing import List

from cloudrail.knowledge.context.aws.kms.kms_key import KmsKey
from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class SageMakerNotebookInstance(AwsResource):

    def __init__(self,
                 name: str,
                 arn: str,
                 kms_key_id: str,
                 region: str,
                 account: str,
                 direct_internet_access: bool):
        super().__init__(account, region, AwsServiceName.AWS_SAGEMAKER_NOTEBOOK_INSTANCE)
        self.name: str = name
        self.arn: str = arn
        self.kms_key_id: str = kms_key_id
        self.kms_data: KmsKey = None
        self.direct_internet_access: bool = direct_internet_access

    def get_keys(self) -> List[str]:
        return [self.arn]

    def get_name(self) -> str:
        return self.name

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'SageMaker Notebook Instance'
        else:
            return 'SageMaker Notebook Instances'

    def get_cloud_resource_url(self) -> str:
        return '{0}sagemaker/home?region={1}#/notebook-instances/{2}' \
            .format(self.AWS_CONSOLE_URL, self.region, self.name)

    def get_arn(self) -> str:
        return self.arn

    @property
    def is_tagable(self) -> bool:
        return True
