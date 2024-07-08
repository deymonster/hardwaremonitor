from models.license import LicenseBase


class ILicenseRead(LicenseBase):
    id: int


class ILisenseCreate(LicenseBase):
    pass


class ILicenseUpdate(LicenseBase):
    id: int
