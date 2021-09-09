from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_load_balancer


class LoadBalancerBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'elbv2-describe-load-balancers.json'

    def get_section_name(self) -> str:
        return 'LoadBalancers'

    def do_build(self, attributes: dict):
        return build_load_balancer(attributes)
