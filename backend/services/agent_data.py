from prefect.deployments import run_deployment

from schemas.agent_data import AgentData


class AgentTriggerService:

    @staticmethod
    async def run_agent_trigger(data: AgentData):
        parameters = data.dict()
        await run_deployment(
            name="sync-agent-data/sync_agent_data",
            parameters={"data": parameters},
            timeout=0,
        ) # type: ignore


