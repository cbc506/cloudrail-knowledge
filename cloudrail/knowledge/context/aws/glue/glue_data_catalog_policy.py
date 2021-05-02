from typing import List, Optional
from cloudrail.knowledge.context.aws.iam.policy import Policy, PolicyStatement
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class GlueDataCatalogPolicy(Policy):

    def __init__(self,
                 policy_statements: Optional[List[PolicyStatement]],
                 raw_document: str,
                 account: str,
                 region: str):
        super().__init__(account, policy_statements, raw_document, AwsServiceName.AWS_GLUE_RESOURCE_POLICY)
        self.account: str = account
        self.region: str = region

    def get_keys(self) -> List[str]:
        return [self.region]

    def get_name(self) -> str:
        return 'Glue Data Catalog policy of region ' + self.region

    def get_type(self, is_plural: bool = False) -> str:
        return 'Glue Data Catalog resource policy'
