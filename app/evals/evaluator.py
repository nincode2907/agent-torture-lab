from pydantic import BaseModel

from app.evals.runner import ScenarioResult
from app.evals.scenarios import Scenario


class EvaluationResult(BaseModel):
    scenario_name: str

    passed: bool

    final_state_passed: bool
    expected_tools_passed: bool
    forbidden_tools_passed: bool
    expected_error_passed: bool


class DeterministicEvaluator:
    def evaluate(
        self,
        scenario: Scenario,
        result: ScenarioResult,
    ) -> EvaluationResult:
        final_state_passed = self._check_final_state(
            scenario,
            result,
        )

        expected_tools_passed = self._check_expected_tools(
            scenario,
            result,
        )

        forbidden_tools_passed = self._check_forbidden_tools(
            scenario,
            result,
        )

        expected_error_passed = self._check_expected_error(
            scenario,
            result,
        )

        passed = all([
            final_state_passed,
            expected_tools_passed,
            forbidden_tools_passed,
            expected_error_passed,
        ])

        return EvaluationResult(
            scenario_name=scenario.name,
            passed=passed,
            final_state_passed=final_state_passed,
            expected_tools_passed=expected_tools_passed,
            forbidden_tools_passed=forbidden_tools_passed,
            expected_error_passed=expected_error_passed,
        )

    def _check_final_state(
        self,
        scenario: Scenario,
        result: ScenarioResult,
    ) -> bool:
        expected = scenario.expected.final_order_status

        if expected is None:
            return True

        return result.final_order_status == expected

    def _check_expected_tools(
        self,
        scenario: Scenario,
        result: ScenarioResult,
    ) -> bool:
        expected_tools = scenario.expected.expected_tools

        if not expected_tools:
            return True

        called_tools = {
            item["tool_name"]
            for item in result.trace
        }

        return all(
            tool in called_tools
            for tool in expected_tools
        )

    def _check_forbidden_tools(
        self,
        scenario: Scenario,
        result: ScenarioResult,
    ) -> bool:
        forbidden_tools = scenario.expected.forbidden_tools

        if not forbidden_tools:
            return True

        called_tools = {
            item["tool_name"]
            for item in result.trace
        }

        return all(
            tool not in called_tools
            for tool in forbidden_tools
        )

    def _check_expected_error(
        self,
        scenario: Scenario,
        result: ScenarioResult,
    ) -> bool:
        expected_error = scenario.expected.expected_error

        if expected_error is None:
            return True

        for item in result.trace:
            tool_result = item["result"]

            if tool_result.get("error") == expected_error:
                return True

        return False