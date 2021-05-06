import unittest

from cloudrail.knowledge.context.aws.codebuild.codebuild_project import CodeBuildProject
from cloudrail.knowledge.context.aws.ec2.network_interface import NetworkInterface
from cloudrail.knowledge.context.aws.ec2.security_group import SecurityGroup
from cloudrail.knowledge.context.aws.ec2.security_group_rule import ConnectionType, SecurityGroupRule, SecurityGroupRulePropertyType
from cloudrail.knowledge.context.aws.networking_config.network_resource import NetworkResource
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.rules.aws.non_context_aware.ensure_security_group_include_description_rule import EnsureSecurityGroupIncludeDescriptionRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from cloudrail.dev_tools.rule_test_utils import create_empty_entity


class TestEnsureSecurityGroupIncludeDescriptionRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureSecurityGroupIncludeDescriptionRule()

    def test_non_car_aws_ec2_security_group_rule_no_desc__all_items__fail(self):
        # Arrange
        codebuild_project: CodeBuildProject = create_empty_entity(CodeBuildProject)
        network_resource: NetworkResource = create_empty_entity(NetworkResource)
        network_interface = create_empty_entity(NetworkInterface)
        security_group: SecurityGroup = create_empty_entity(SecurityGroup)
        inbound_permissions = [SecurityGroupRule(0, 65535, '-1', SecurityGroupRulePropertyType.IP_RANGES,
                                                 '0.0.0.0/0', False, ConnectionType.Inbound,
                                                 'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
        outbound_permissions = [SecurityGroupRule(0, 65535, '-1',
                                                  SecurityGroupRulePropertyType.IP_RANGES, '10.10.10.0/24', False,
                                                  ConnectionType.Outbound, 'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
        security_group.has_description = False
        security_group.inbound_permissions = inbound_permissions
        security_group.outbound_permissions = outbound_permissions
        network_interface.security_groups.append(security_group)
        network_resource.network_interfaces.append(network_interface)
        codebuild_project.network_resource = network_resource
        context = EnvironmentContext(codebuild_projects=[codebuild_project])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(3, len(result.issues))

    def test_non_car_aws_ec2_security_group_rule_no_desc__inbound_rule_affected__fail(self):
        # Arrange
        codebuild_project: CodeBuildProject = create_empty_entity(CodeBuildProject)
        network_resource: NetworkResource = create_empty_entity(NetworkResource)
        network_interface = create_empty_entity(NetworkInterface)
        security_group: SecurityGroup = create_empty_entity(SecurityGroup)
        inbound_permissions = [SecurityGroupRule(0, 65535, '-1', SecurityGroupRulePropertyType.IP_RANGES,
                                                 '0.0.0.0/0', False, ConnectionType.Inbound,
                                                 'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
        outbound_permissions = [SecurityGroupRule(0, 65535, '-1',
                                                  SecurityGroupRulePropertyType.IP_RANGES, '10.10.10.0/24', True,
                                                  ConnectionType.Outbound, 'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
        security_group.has_description = True
        security_group.inbound_permissions = inbound_permissions
        security_group.outbound_permissions = outbound_permissions
        network_interface.security_groups.append(security_group)
        network_resource.network_interfaces.append(network_interface)
        codebuild_project.network_resource = network_resource
        context = EnvironmentContext(codebuild_projects=[codebuild_project])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertEqual(result.issues[0].violating.connection_type, ConnectionType.Inbound)

    def test_non_car_aws_ec2_security_group_rule_no_desc__outbound_rule_affected__fail(self):
        # Arrange
        codebuild_project: CodeBuildProject = create_empty_entity(CodeBuildProject)
        network_resource: NetworkResource = create_empty_entity(NetworkResource)
        network_interface = create_empty_entity(NetworkInterface)
        security_group: SecurityGroup = create_empty_entity(SecurityGroup)
        inbound_permissions = [SecurityGroupRule(0, 65535, '-1', SecurityGroupRulePropertyType.IP_RANGES,
                                                 '0.0.0.0/0', True, ConnectionType.Inbound,
                                                 'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
        outbound_permissions = [SecurityGroupRule(0, 65535, '-1',
                                                  SecurityGroupRulePropertyType.IP_RANGES, '10.10.10.0/24', False,
                                                  ConnectionType.Outbound, 'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
        security_group.has_description = True
        security_group.inbound_permissions = inbound_permissions
        security_group.outbound_permissions = outbound_permissions
        network_interface.security_groups.append(security_group)
        network_resource.network_interfaces.append(network_interface)
        codebuild_project.network_resource = network_resource
        context = EnvironmentContext(codebuild_projects=[codebuild_project])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertEqual(result.issues[0].violating.connection_type, ConnectionType.Outbound)

    def test_non_car_aws_ec2_security_group_rule_no_desc__only_sg_affected__fail(self):
        # Arrange
        codebuild_project: CodeBuildProject = create_empty_entity(CodeBuildProject)
        network_resource: NetworkResource = create_empty_entity(NetworkResource)
        network_interface = create_empty_entity(NetworkInterface)
        security_group: SecurityGroup = create_empty_entity(SecurityGroup)
        inbound_permissions = [SecurityGroupRule(0, 65535, '-1', SecurityGroupRulePropertyType.IP_RANGES,
                                                 '0.0.0.0/0', True, ConnectionType.Inbound,
                                                 'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
        outbound_permissions = [SecurityGroupRule(0, 65535, '-1',
                                                  SecurityGroupRulePropertyType.IP_RANGES, '10.10.10.0/24', True,
                                                  ConnectionType.Outbound, 'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
        security_group.has_description = False
        security_group.inbound_permissions = inbound_permissions
        security_group.outbound_permissions = outbound_permissions
        network_interface.security_groups.append(security_group)
        network_resource.network_interfaces.append(network_interface)
        codebuild_project.network_resource = network_resource
        context = EnvironmentContext(codebuild_projects=[codebuild_project])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))
        self.assertEqual(result.issues[0].violating, security_group)
        self.assertEqual(result.issues[0].exposed, security_group)

    def test_non_car_aws_ec2_security_group_rule_no_desc_pass(self):
        # Arrange
        codebuild_project: CodeBuildProject = create_empty_entity(CodeBuildProject)
        network_resource: NetworkResource = create_empty_entity(NetworkResource)
        network_interface = create_empty_entity(NetworkInterface)
        security_group: SecurityGroup = create_empty_entity(SecurityGroup)
        inbound_permissions = [SecurityGroupRule(0, 65535, '-1', SecurityGroupRulePropertyType.IP_RANGES,
                                                 '0.0.0.0/0', True, ConnectionType.Inbound,
                                                 'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
        outbound_permissions = [SecurityGroupRule(0, 65535, '-1',
                                                  SecurityGroupRulePropertyType.IP_RANGES, '10.10.10.0/24', True,
                                                  ConnectionType.Outbound, 'AllInclusiveSecurityGroup', 'us-east-1', '1111111')]
        security_group.has_description = True
        security_group.inbound_permissions = inbound_permissions
        security_group.outbound_permissions = outbound_permissions
        network_interface.security_groups.append(security_group)
        network_resource.network_interfaces.append(network_interface)
        codebuild_project.network_resource = network_resource
        context = EnvironmentContext(codebuild_projects=[codebuild_project])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
