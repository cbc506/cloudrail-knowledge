from typing import List, Dict

from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.context.aws.ec2.ec2_instance import Ec2Instance
from cloudrail.knowledge.context.environment_context import EnvironmentContext


class Ec2RoleShareRule(BaseRule):

    def get_id(self) -> str:
        return 'ec2_role_share_rule'

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        ec2s: List[Ec2Instance] = env_context.ec2s

        for private_ec2 in (x for x in ec2s if not x.network_resource.is_inbound_public and x.iam_profile_id):
            public_ec2s = [x.get_friendly_name() for x in ec2s if x.network_resource.is_inbound_public
                           and x.iam_profile_id == private_ec2.iam_profile_id]
            profile = private_ec2.iam_role.get_friendly_name() \
                if private_ec2.iam_role  \
                else private_ec2.iam_profile_id
            if public_ec2s:
                issues.append(
                    Issue(
                        f"~Instance `{public_ec2s}`~. Instance is publicly exposed. "
                        f"Instance uses IAM role `{profile}`. "
                        f"Private EC2 instance shares IAM role `{profile}` as well. "
                        f"~Instance `{private_ec2.get_friendly_name()}`~",
                        private_ec2,
                        private_ec2.iam_role))
        return issues

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.ec2s)
