from prefect import flow
from flows.sync_hardware_data import process_agent_data
from schemas.agent_data import AgentData


@flow
async def sync_agent_data(data: AgentData):
    await process_agent_data(data)