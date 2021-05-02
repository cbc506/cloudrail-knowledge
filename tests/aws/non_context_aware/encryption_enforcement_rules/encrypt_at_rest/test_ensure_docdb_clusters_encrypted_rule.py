import unittest

from cloudrail.knowledge.context.aws.docdb.docdb_cluster import DocumentDbCluster
from cloudrail.knowledge.context.environment_context import EnvironmentContext
from cloudrail.knowledge.context.terraform_state import TerraformState
from cloudrail.knowledge.rules.aws.non_context_aware.encryption_enforcement_rules.encrypt_at_rest.ensure_docdb_clusters_encrypted_rule import \
    EnsureDocdbClustersEncryptedRule
from cloudrail.knowledge.rules.base_rule import RuleResultType
from tests.rule_test_utils import create_empty_entity


class TestEnsureDocdbClustersEncryptedRule(unittest.TestCase):
    def setUp(self):
        self.rule = EnsureDocdbClustersEncryptedRule()

    def test_not_car_docdb_cluster_encrypted_at_rest_fail(self):
        # Arrange
        document_db_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        terraform_state = create_empty_entity(TerraformState)
        document_db_cluster.terraform_state = terraform_state
        document_db_cluster.terraform_state.is_new = True
        document_db_cluster.storage_encrypted = False

        context = EnvironmentContext(docdb_cluster=[document_db_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.FAILED, result.status)
        self.assertEqual(1, len(result.issues))

    def test_not_car_docdb_cluster_encrypted_at_rest_pass(self):
        # Arrange
        document_db_cluster: DocumentDbCluster = create_empty_entity(DocumentDbCluster)
        terraform_state = create_empty_entity(TerraformState)
        document_db_cluster.terraform_state = terraform_state
        document_db_cluster.terraform_state.is_new = True
        document_db_cluster.storage_encrypted = True

        context = EnvironmentContext(docdb_cluster=[document_db_cluster])
        # Act
        result = self.rule.run(context, {})
        # Assert
        self.assertEqual(RuleResultType.SUCCESS, result.status)
        self.assertEqual(0, len(result.issues))
