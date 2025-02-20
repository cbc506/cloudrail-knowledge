import logging
import time
from abc import abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, TypeVar, Generic, Optional
from cloudrail.knowledge.rules.rule_parameters.base_paramerter import ParameterType
from cloudrail.knowledge.context.mergeable import Mergeable
from cloudrail.knowledge.context.aws.resources.account.account import Account


@dataclass
class Issue:
    evidence: str
    exposed: Mergeable
    violating: Mergeable


class RuleResultType(str, Enum):
    SUCCESS = 'success'
    FAILED = 'failed'
    SKIPPED = 'skipped'


@dataclass
class RuleResponse:
    rule_id: str
    status: RuleResultType
    issues: List[Issue] = field(default_factory=list)
    reason: Optional[str] = None


EnvCtx = TypeVar('EnvCtx')


class BaseRule(Generic[EnvCtx]):
    def validate_parameters(self, parameter_types: List[ParameterType]) -> bool:
        for parameter_type in self.get_needed_parameters():
            if parameter_type not in parameter_types:
                logging.warning('Rule : {} failed to run!\nMissing parameter type: {}'.format(self.get_id(),
                                                                                              parameter_type))
                return False
        return True

    def run(self,
            environment_context: EnvCtx,
            parameters: Dict[ParameterType, dict]) -> RuleResponse:
        if not self.should_run_rule(environment_context):
            logging.info('skipped rule {}, reason {}'.format(self.get_id(), 'no relevant resources'))
            return RuleResponse(self.get_id(), RuleResultType.SKIPPED)

        logging.info('start run rule {}'.format(self.get_id()))
        start_time: float = time.time()
        if self.validate_parameters(list(parameters.keys())):
            total_issues = self.execute(environment_context, parameters)
            filtered_missing_data_issues = self._filter_missing_data_issues(total_issues)
            filtered_non_iac_managed_issues = self._filter_non_iac_managed_issues(filtered_missing_data_issues, self.filter_non_iac_managed_issues())
            filtered_duplicate_issues = self._filter_duplicate_issues(filtered_non_iac_managed_issues)
            logging.info(f'run rule {self.get_id()} completed in {(time.time() - start_time)}s.\n'
                         f'number of total issues: {len(total_issues)}\n'
                         f'number of non missing data issues: {len(filtered_missing_data_issues)}\n'
                         f'number of iac managed issues: {len(filtered_non_iac_managed_issues)}\n'
                         f'number of no duplicate issues: {len(filtered_duplicate_issues)}\n')
            final_issues_list = filtered_duplicate_issues

            if not final_issues_list:
                rule_result = RuleResponse(self.get_id(), RuleResultType.SUCCESS)
            else:
                rule_result = RuleResponse(self.get_id(), RuleResultType.FAILED, final_issues_list)
        else:
            rule_result = RuleResponse(self.get_id(), RuleResultType.SKIPPED)
        logging.info('finish run rule {}'.format(self.get_id()))
        return rule_result

    @staticmethod
    def _filter_missing_data_issues(issues: List[Issue]) -> List[Issue]:
        return [issue for issue in issues if issue.exposed and issue.violating]

    @classmethod
    def _filter_non_iac_managed_issues(cls, issues: List[Issue], filter_non_iac_managed_issues: bool) -> List[Issue]:
        if filter_non_iac_managed_issues:
            return [issue for issue in issues if
                    (issue.exposed and issue.exposed.iac_state) or
                    (issue.violating and issue.violating.iac_state) or
                    (isinstance(issue.violating, Account) and isinstance(issue.exposed, Account))]
        else:
            return issues

    @staticmethod
    def _filter_duplicate_issues(issues: List[Issue]) -> List[Issue]:
        filtered_issues = []
        exposed_entites = set()
        for issue in issues:
            if issue.exposed not in exposed_entites:
                exposed_entites.add(issue.exposed)
                filtered_issues.append(issue)
        return filtered_issues

    @abstractmethod
    def execute(self, env_context: EnvCtx, parameters: Dict[ParameterType, any]) -> List[Issue]:
        pass

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def get_needed_parameters(self) -> List[ParameterType]:
        pass

    @staticmethod
    def filter_non_iac_managed_issues() -> bool:
        return True

    @abstractmethod
    def should_run_rule(self, environment_context: EnvCtx) -> bool:
        return True
