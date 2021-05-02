from typing import List

from cloudrail.knowledge.context.aws.iam.policy import Policy
from cloudrail.knowledge.context.aws.iam.policy_statement import PolicyStatement
from cloudrail.knowledge.context.aws.service_name import AwsServiceName


class EcrRepositoryPolicy(Policy):

    def __init__(self,
                 repo_name: str,
                 policy_statements: List[PolicyStatement],
                 raw_document: str,
                 account: str):
        super().__init__(account, policy_statements, raw_document, AwsServiceName.AWS_ECR_REPOSITORY_POLICY)
        self.repo_name: str = repo_name

    def get_keys(self) -> List[str]:
        return [self.repo_name, self.region, self.account]

    def get_name(self) -> str:
        return self.repo_name + " policy"

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'ECR repository resource policy'
        else:
            return 'ECR repository resource policies'
