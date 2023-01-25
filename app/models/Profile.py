from pydantic import BaseModel

class Profile(BaseModel):
    businessPhones: list | None = None
    displayName: str | None = None
    givenName: str | None = None
    jobTitle: str | None = None
    mail: str | None = None
    mobilePhone: str | None = None
    officeLocation: str | None = None
    preferredLanguage: str | None = None
    surname: str | None = None
    userPrincipalName: str | None = None
    id: str | None = None