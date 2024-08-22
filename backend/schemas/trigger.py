from models.agent_trigger import AgentTriggerBase

class ITriggerRead(AgentTriggerBase):
    id: int


class ITriggerCreate(AgentTriggerBase):
    pass


class ITriggerUpdate(AgentTriggerBase):
    id: int