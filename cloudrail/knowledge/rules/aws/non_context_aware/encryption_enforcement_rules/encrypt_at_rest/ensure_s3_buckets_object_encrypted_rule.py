from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureS3BucketObjectsEncryptedRule(BaseRule):

    def get_id(self) -> str:
        return 'not_car_s3_bucket_object_encrypt_at_rest'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for s3_bucket_object in env_context.s3_bucket_objects:
            if not s3_bucket_object.encrypted and not s3_bucket_object.owning_bucket.is_inbound_public():
                issues.append(
                    Issue(
                        f'The {s3_bucket_object.get_type()} `{s3_bucket_object.get_friendly_name()}` '
                        f'is not set to be encrypted at rest', s3_bucket_object, s3_bucket_object))

        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.s3_bucket_objects)
