from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureKinesisStreamEncryptedAtRestRule(BaseRule):

    def get_id(self) -> str:
        return 'non_car_kinesis_stream_encrypt_at_rest'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for kinesis_stream in env_context.kinesis_streams:
            if not kinesis_stream.encrypted_at_rest:
                issues.append(
                    Issue(
                        f'The {kinesis_stream.get_type()} `{kinesis_stream.get_friendly_name()}` '
                        f'is not set to use encryption at rest', kinesis_stream, kinesis_stream))

        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.kinesis_streams)
