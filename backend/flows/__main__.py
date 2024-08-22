from prefect import serve

import sync_agent_data

sync_agent_data_deployment = sync_agent_data.sync_agent_data.to_deployment(
    name="sync_agent_data"
)

serve(sync_agent_data_deployment)