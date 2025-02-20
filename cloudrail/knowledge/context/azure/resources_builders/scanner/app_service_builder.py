from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service import AzureAppService
from cloudrail.knowledge.context.azure.resources.webapp.azure_app_service_type import AzureAppServiceType

from cloudrail.knowledge.context.azure.resources_builders.scanner.base_azure_scanner_builder import BaseAzureScannerBuilder


class AppServiceBuilder(BaseAzureScannerBuilder):

    def get_file_name(self) -> str:
        return 'app-service.json'

    def do_build(self, attributes: dict) -> AzureAppService:
        if attributes['kind'] == AzureAppServiceType.APP.value:
            return AzureAppService(name=attributes['name'],
                                   https_only=attributes['properties']['httpsOnly'],
                                   client_cert_required=attributes['properties'].get('clientCertEnabled', False))
        return None
