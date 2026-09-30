from dataclasses import dataclass

from app.repositories.memory import CommerceRepository
from app.domain.services import CommerceService
from app.policies.permissions import PermissionPolicy
from app.agent.tools import CommerceTools
from app.agent.dispatcher import ToolDispatcher
from app.agent.llm import CommerceLLM
from app.agent.runner import AgentRunner


@dataclass
class AppContainer:
    repository: CommerceRepository
    service: CommerceService
    policy: PermissionPolicy
    tools: CommerceTools
    dispatcher: ToolDispatcher
    llm: CommerceLLM
    runner: AgentRunner


def create_app_container() -> AppContainer:
    repository = CommerceRepository()

    service = CommerceService(repository)

    policy = PermissionPolicy()

    tools = CommerceTools(
        service=service,
        permission_policy=policy,
    )

    dispatcher = ToolDispatcher(tools)

    llm = CommerceLLM()

    runner = AgentRunner(
        llm=llm,
        dispatcher=dispatcher,
    )

    return AppContainer(
        repository=repository,
        service=service,
        policy=policy,
        tools=tools,
        dispatcher=dispatcher,
        llm=llm,
        runner=runner,
    )