"""The Quran Browser integration."""

from __future__ import annotations
from aiodns.error import DNSError

from homeassistant.const import __version__
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .quran_client import QuranClient, QuranClientError
from .const import DOMAIN

type QuranBrowserConfigEntry = ConfigEntry[QuranClient]

async def async_setup_entry(hass: HomeAssistant, entry: QuranBrowserConfigEntry) -> bool:
    """Set up Quran Browser from a config entry."""
    session = async_get_clientsession(hass)
    quran_client = QuranClient(session=session, user_agent=f"HomeAssistant/{__version__}")

    try:
        # Optional: Test the connection by fetching chapters or audio files
        await quran_client.fetch_chapters()
    except  (DNSError, QuranClientError) as err:
        raise ConfigEntryNotReady("Could not connect to Quran API") from err

    entry.runtime_data = quran_client

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
