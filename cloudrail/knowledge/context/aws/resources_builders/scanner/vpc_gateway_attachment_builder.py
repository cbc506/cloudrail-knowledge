from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_vpc_internet_gateway_attachment


class VpcGatewayAttachmentBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ec2-describe-internet-gateways.json'

    def get_section_name(self) -> str:
        return 'InternetGateways'

    def do_build(self, attributes: dict):
        return build_vpc_internet_gateway_attachment(attributes)
