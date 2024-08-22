from pydantic import BaseModel
from uuid import UUID

class OSInfo(BaseModel):
    ComputerName: str | None
    ShutdownTime: str | None
    ProductName: str  | None
    EditionID: str | None
    DisplayVersion: str | None
    CurrentBuild: str | None
    UBR: int | None
    InstallDate: str | None
    RegisteredOwner: str | None
    TimeZone: str | None
    ActivateKey: str | None

class BIOSInfo(BaseModel):
    SystemBiosVersion: str | None
    BIOSVendor: str | None
    BIOSVersion: str | None
    BIOSReleaseDate: str | None

class MotherboardInfo(BaseModel):
    SystemManufacturer: str | None
    SystemProductName: str | None
    Product: str | None
    SerialNumber: str | None
    Version: str | None


class CPUInfo(BaseModel):
    ProcessorNameString: str | None
    Identifier: str | None
    VendorIdentifier: str | None
    MHz: int | None

class HDDSSDInfo(BaseModel):
    Vendor: str | None
    Model: str | None
    SerialNumber: str | None

class NICInfo(BaseModel):
    Description: str | None
    NetCfgInstanceId: str | None
    DefaultGateway: str | None
    IPAddress: str | None
    Name: str | None

class AgentData(BaseModel):
    UUID: UUID
    OS: OSInfo
    BIOS: BIOSInfo
    Motherboard: MotherboardInfo
    CPU: CPUInfo
    HDD: list[HDDSSDInfo]
    NIC: list[NICInfo]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "UUID": "0b906723-98c9-4519-92ff-aee0d856e205",
                    "OS": {
                        "ComputerName": "SOME NAME HERE",
                        "ShutdownTime": "00:00:00",
                        "ProductName": "Windows 10",
                        "EditionID": "Windows 10 Home",
                        "DisplayVersion": "10.0.19041",
                        "CurrentBuild": "19041",
                        "UBR": 0,
                        "InstallDate": "2020-01-01 00:00:00",
                        "RegisteredOwner": "SOME NAME HERE",
                        "TimeZone": "Ekaterinburg Standard Time",
                        "ActivateKey": "HERE CAN BE ACTIVATE KEY"
                    },
                    "BIOS": {
                        "SystemBiosVersion": "10.0.19041",
                        "BIOSVendor": "Microsoft Corporation",
                        "BIOSVersion": "10.0.19041",
                        "BIOSReleaseDate": "01/01/2020",
                    },
                    "Motherboard": {
                        "SystemManufacturer": "Microsoft Corporation",
                        "SystemProductName": "Surface Pro 6",
                        "Product": "Surface Pro 6",
                        "SerialNumber": "SOME SERIAL NUMBER",
                        "Version": "10.0.19041",
                    },
                    "CPU": {
                        "ProcessorNameString": "Intel(R) Core(TM) i5-10210U CPU @ 1.60GHz",
                        "Identifier": "Intel(R) Core(TM) i5-10210U CPU @ 1.60GHz",
                        "VendorIdentifier": "GenuineIntel",
                        "MHz": 1660,
                    },
                    "HDD": [
                        {
                            "Vendor": "Samsung",
                            "Model": "Samsung SSD 970 EVO",
                            "SerialNumber": "SOME SERIAL NUMBER",
                        },
                        {
                            "Vendor": "Kingston",
                            "Model": "Kingston SSD",
                            "SerialNumber": "SOME SERIAL NUMBER",
                        }
                    ],
                    "NIC": [{
                        "Description": "Realtek PCIe GbE Family Controller",
                        "NetCfgInstanceId": "{5CC17E3B-2094-4A73-96AD-004D2F263DE2}",
                        "DefaultGateway": "192.168.1.1",
                        "IPAddress": "192.168.1.20",
                        "Name": "Ethernet"
                    }],

                }
            ]
        }
    }



