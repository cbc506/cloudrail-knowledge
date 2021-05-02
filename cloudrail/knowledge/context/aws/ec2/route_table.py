from dataclasses import dataclass
from typing import List, Optional
from netaddr import IPNetwork

from cloudrail.knowledge.context.aws.service_name import AwsServiceName
from cloudrail.knowledge.utils.utils import is_subset
from cloudrail.knowledge.context.aws.aws_resource import AwsResource
from cloudrail.knowledge.context.aws.ec2.route import Route, RouteTargetType


@dataclass
class RouteTableRawData:
    is_default: bool = False


class RouteTable(AwsResource):

    def __init__(self,
                 route_table_id: str,
                 vpc_id: str,
                 name: str,
                 region: str,
                 account: str):
        super().__init__(account, region, AwsServiceName.AWS_ROUTE_TABLE)
        self.route_table_id: str = route_table_id
        self.vpc_id: str = vpc_id
        self.name: str = name
        self.aliases.add(route_table_id)
        self.routes: List[Route] = []
        self.raw_data: RouteTableRawData = RouteTableRawData()

    def get_keys(self) -> List[str]:
        return [self.route_table_id]

    def get_id(self) -> str:
        return self.route_table_id

    def get_name(self) -> str:
        return self.name

    def get_extra_data(self) -> str:
        vpc_id = 'vpc_id: {}'.format(self.vpc_id) if self.vpc_id else ''

        return ', '.join([vpc_id])

    def with_raw_data(self, is_default: bool):
        self.raw_data.is_default = is_default
        return self

    def get_most_specific_route(self, cidr_block: str) -> Optional[Route]:
        most_specific_route: Optional[Route] = None
        for route in self.routes:
            if is_subset(cidr_block, route.destination) and \
                    (most_specific_route is None or
                     IPNetwork(route.destination).prefixlen > IPNetwork(most_specific_route.destination).prefixlen):
                most_specific_route = route
        return most_specific_route

    def get_prefix_list_route_by_id(self, prefix_list_id: str) -> Optional[Route]:
        for route in self.routes:
            if prefix_list_id == route.destination:
                return route
        return None

    def get_internet_gateway_routes(self) -> List[Route]:
        return [route for route in self.routes
                if route.is_internet_gateway_target()]

    def get_nat_gateway_route(self) -> List[Route]:
        return [route for route in self.routes
                if route.target_type == RouteTargetType.NAT_GATEWAY_ID]

    def get_type(self, is_plural: bool = False) -> str:
        if not is_plural:
            return 'Route table'
        else:
            return 'Route tables'

    def get_cloud_resource_url(self) -> str:
        return '{0}vpc/home?region={1}#RouteTables:routeTableId={2}'\
            .format(self.AWS_CONSOLE_URL, self.region, self.route_table_id)

    def get_arn(self) -> str:
        pass

    @property
    def is_tagable(self) -> bool:
        return True
