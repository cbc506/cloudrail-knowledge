# from typing import Dict, List
# from cloudrail.knowledge.context.azure.azure_environment_context import AzureEnvironmentContext
# from cloudrail.knowledge.context.azure.azure_resources.web_app.azure_app_service import FtpState
# from cloudrail.knowledge.rules.azure.azure_base_rule import AzureBaseRule
# from cloudrail.knowledge.rules.base_rule import Issue
# from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
#
#
# class FunctionAppEnforcesFtpsOnlyRule(AzureBaseRule):
#
#     def get_id(self) -> str:
#         return 'non_car_function_app_enforces_ftps_only'
#
#     def execute(self, env_context: AzureEnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
#         issues: List[Issue] = []
#         for app in env_context.app_services.values():
#             if app.site_config is None or app.site_config.ftp_state != FtpState.FTPS_ONLY:
#                 issues.append(
#                     Issue(
#                         f'The Function App `{app.name}` is not enforcing FTPS only.',
#                         app,
#                         app))
#         return issues
#
#     def should_run_rule(self, environment_context: AzureEnvironmentContext) -> bool:
#         return bool(environment_context.app_services)
