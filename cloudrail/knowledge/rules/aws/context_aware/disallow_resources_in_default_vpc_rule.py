from typing import List, Dict
from cloudrail.knowledge.context.aws.networking_config.network_entity import NetworkEntity
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.base_rule import BaseRule, Issue
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType


class DisallowResourcesInDefaultVpcRule(BaseRule):

    def execute(self, env_context: EnvironmentContext, parameters: Dict[ParameterType, any]) -> List[Issue]:
        issues: List[Issue] = []
        network_entity_list: List[NetworkEntity] = env_context.get_all_network_entities()

        for entity in network_entity_list:
            if entity.network_resource.vpc is not None and entity.network_resource.vpc.is_default:  # some resources can be out of vpc
                issues.append(Issue(self._format_evidence(entity.get_friendly_name()), entity, entity))

        return issues

    def get_id(self) -> str:
        return "disallow_default_vpc"

    def get_needed_parameters(self) -> List[ParameterType]:
        return []

    @staticmethod
    def _format_evidence(entity: str) -> str:
        return f"~Default VPC~. `{entity}` is defined within the default VPC."

    def should_run_rule(self, environment_context: EnvironmentContext) -> bool:
        return bool(environment_context.get_all_network_entities())
