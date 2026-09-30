from pydantic import BaseModel

from app.bootstrap import create_app_container
from app.evals.scenarios import Scenario


class ScenarioResult(BaseModel):
    scenario_name: str

    agent_ok: bool

    final_answer: str | None

    trace: list[dict]

    final_order_status: str | None


class ScenarioRunner:
    def run(self, scenario: Scenario) -> ScenarioResult:
        app = create_app_container()

        agent_result = app.runner.run(
            user_message=scenario.user_message,
            context=scenario.context,
        )

        final_order_status = None

        if scenario.expected.final_order_status is not None:
            order_id = self._find_order_id(
                agent_result["trace"]
            )

            if order_id is not None:
                order = app.repository.get_order(order_id)

                if order is not None:
                    final_order_status = order.status.value

        return ScenarioResult(
            scenario_name=scenario.name,
            agent_ok=agent_result["ok"],
            final_answer=agent_result.get("final_answer"),
            trace=agent_result["trace"],
            final_order_status=final_order_status,
        )

    def _find_order_id(
        self,
        trace: list[dict],
    ) -> int | None:
        for item in trace:
            arguments = item.get("arguments") or {}

            order_id = arguments.get("order_id")

            if order_id is not None:
                return order_id

        return None