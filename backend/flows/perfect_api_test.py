import asyncio
from prefect.client.orchestration import get_client

from schemas.agent_data import AgentData
from services.agent_data import AgentTriggerService

agent_data = {
  "UUID": "0b906723-98c9-4519-92ff-aee0d856e209",
  "OS": {
    "ComputerName": "PC-POPOV",
    "ShutdownTime": "2024-08-12 04:12:02",
    "ProductName": "Windows 10 Pro",
    "EditionID": "Professional",
    "DisplayVersion": "22H2",
    "CurrentBuild": "19045",
    "UBR": 4651,
    "InstallDate": "2024-04-09 19:57:06",
    "RegisteredOwner": "User",
    "TimeZone": "Ekaterinburg Standard Time",
    "ActivateKey": "RJV8C-JKWBG-4TF6X-P3TJ7-JQKTP"
  },
  "BIOS": {
    "SystemBiosVersion": "ALASKA - 1072009",
    "BIOSVendor": "American Megatrends Inc.",
    "BIOSVersion": "5.12",
    "BIOSReleaseDate": "11/04/2020"
  },
  "Motherboard": {
    "SystemManufacturer": "OPTION",
    "SystemProductName": "B250RU01",
    "Product": "B250RU01",
    "SerialNumber": "",
    "Version": ""
  },
  "CPU": {
    "ProcessorNameString": "Intel(R) Pentium(R) Gold G5420 CPU @ 3.80GHz",
    "Identifier": "Intel64 Family 6 Model 158 Stepping 10",
    "VendorIdentifier": "GenuineIntel",
    "MHz": 3792
  },
  "HDD": [
    {
      "Vendor": "Option",
      "Model": "60",
      "SerialNumber": "AA000000000000000072"
    },
    {
      "Vendor": "ST31000524AS",
      "Model": "Unknown",
      "SerialNumber": "9VPGGRLK"
    }
  ],
  "NIC": [
    {
      "Description": "Realtek PCIe GbE Family Controller",
      "NetCfgInstanceId": "{5CC17E3B-2094-4A73-96AD-004D2F263DE2}",
      "DefaultGateway": "192.168.13.1",
      "IPAddress": "192.168.13.179",
      "Name": "Ethernet"
    }
  ]
}


async def send_data(payload: AgentData):
  await AgentTriggerService.run_agent_trigger(data=payload)


async def main2(agent_data):
  agent_data_obj = AgentData(**agent_data)
  await send_data(agent_data_obj)


async def get_flows():
    client = get_client()
    r = await client.read_flows(limit=5)
    return r

async def main():
    r = await get_flows()
    for flow in r:
        print(flow.name, flow.id)

if __name__ == "__main__":
    asyncio.run(main2(agent_data))