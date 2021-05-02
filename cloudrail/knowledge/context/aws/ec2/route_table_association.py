from typing import List

from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.context.aws.aws_resource import AwsResource


class RouteTableAssociation(AwsResource):

    def __init__(self,
                 subnet_id: str,
                 route_table_id: str,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_ROUTE_TABLE_ASSOCIATION)
        self.route_table_id: str = route_table_id
        self.subnet_id: str = subnet_id

    def get_keys(self) -> List[str]:
        return [self.route_table_id, self.subnet_id]

    def get_extra_data(self) -> str:
        route_table_id = 'route_table_id: {}'.format(self.route_table_id) if self.route_table_id else ''
        subnet_id = 'vpc_id: {}'.format(self.subnet_id) if self.subnet_id else ''

        return ', '.join([route_table_id, subnet_id])

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Route table association'
        else:
            return 'Route table associations'

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#RouteTables:routeTableId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.route_table_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return False
