"""Shared catalog metadata (datasheet content) and supplier model."""

from pydantic import BaseModel, Field


COUNTRY_FLAGS: dict[str, str] = {
    "France": "🇫🇷",
    "Allemagne": "🇩🇪",
    "Italie": "🇮🇹",
    "Espagne": "🇪🇸",
    "Suisse": "🇨🇭",
    "Royaume-Uni": "🇬🇧",
    "Belgique": "🇧🇪",
    "Pays-Bas": "🇳🇱",
    "Suède": "🇸🇪",
    "Finlande": "🇫🇮",
    "Norvège": "🇳🇴",
    "Danemark": "🇩🇰",
    "Autriche": "🇦🇹",
    "Canada": "🇨🇦",
    "États-Unis": "🇺🇸",
    "Japon": "🇯🇵",
}

ESA_MEMBER_STATES: set[str] = {
    "France",
    "Allemagne",
    "Italie",
    "Espagne",
    "Suisse",
    "Royaume-Uni",
    "Belgique",
    "Pays-Bas",
    "Suède",
    "Finlande",
    "Norvège",
    "Danemark",
    "Autriche",
}


def is_esa_member(country: str) -> bool:
    """Return True if the country is an ESA member or participating European state."""
    return country in ESA_MEMBER_STATES


def country_with_flag(country: str) -> str:
    """Format country name with its corresponding flag emoji."""
    if not country:
        return "—"
    flag = COUNTRY_FLAGS.get(country, "🌍")
    return f"{flag} {country}"


class CatalogMeta(BaseModel):
    """Datasheet-oriented fields shared by every catalog item."""

    image: str = Field("", description="Illustration file name in data/images (e.g. 'payload_sar.jpg')")
    long_description: str = Field("", description="Descriptive paragraph shown on the datasheet")
    key_features: list[str] = Field(default_factory=list, description="Bullet points of main features")
    interfaces: list[str] = Field(default_factory=list, description="Electrical / data / mechanical interfaces")


class Supplier(BaseModel):
    """Fictive supplier (inspired by a real company)."""

    id: str
    name: str
    country: str = ""
    country_code: str = ""
    kind: str = Field("newspace", description="'historique' or 'newspace'")
    categories: list[str] = Field(
        default_factory=list,
        description="Any of: platform, payload, equipment, launcher",
    )
    description: str = ""
    founded: int | None = None
    website: str = ""
    image: str = ""
