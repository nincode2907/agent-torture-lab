from pydantic import BaseModel


class AgentContext(BaseModel):
    user_id: int
    role: str
    approved: bool = False