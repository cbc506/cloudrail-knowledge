from cloudrail.knowledge.context.aws.resources_builders.scanner.base_aws_scanner_builder import BaseAwsScannerBuilder
from cloudrail.knowledge.context.aws.resources_builders.scanner.cloud_mapper_component_builder import build_directory_service


class CloudDirectoryBuilder(BaseAwsScannerBuilder):

    def get_file_name(self) -> str:
        return 'ds-describe-directories.json'

    def get_section_name(self) -> str:
        return 'DirectoryDescriptions'

    def do_build(self, attributes: dict):
        return build_directory_service(attributes)
