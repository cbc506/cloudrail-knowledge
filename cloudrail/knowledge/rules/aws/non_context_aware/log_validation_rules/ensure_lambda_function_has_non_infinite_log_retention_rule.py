from typing import List, Dict

from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class EnsureLambdaFunctionHasNonInfiniteLogRetentionRule(BaseRule):

    def get_id(self) -> str:
        return 'non_car_lambda_logging_not_infnite'

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []

        for lambda_func in env_context.lambda_function_list:
            if lambda_func.log_group.retention_in_days == 0 or not lambda_func.log_group.retention_in_days:
                if lambda_func.log_group.is_pseudo:
                    issues.append(
                        Issue(
                            f'Upon creation, {lambda_func.get_type()} `{lambda_func.get_friendly_name()}` '
                            f'will have a log group generated automatically with its retention set to Never Expire'
                            , lambda_func, lambda_func))
                else:
                    issues.append(
                        Issue(
                            f'The {lambda_func.log_group.get_type()} `{lambda_func.log_group.get_friendly_name()}` has '
                            f'retention set to Never Expire', lambda_func, lambda_func.log_group))
        return issues

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.lambda_function_list)
