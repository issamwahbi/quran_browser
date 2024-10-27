"""Config flow for Quran Browser integration."""

from __future__ import annotations

from typing import Any

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol

from .const import DOMAIN


class QuranBrowserConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Quran Browser."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            # Create the configuration entry using the provided reciter ID
            return self.async_create_entry(title="Quran Browser", data=user_input)

        # Prompt the user to input the reciter ID
        data_schema = vol.Schema(
            {
                vol.Required("reciter_id"): int,
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema)

    async def async_step_onboarding(
        self, data: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by onboarding."""
        # Skip form, as it’s only initialized by onboarding, and create entry with default data
        return self.async_create_entry(title="Quran Browser", data={})

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> QuranBrowserOptionsFlow:
        """Return the options flow for this configuration entry."""
        return QuranBrowserOptionsFlow(config_entry)


class QuranBrowserOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Quran Browser."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize the options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Optional("reciter_id", default=self.config_entry.options.get("reciter_id", 1)): int,
            }
        )
        return self.async_show_form(step_id="init", data_schema=data_schema)
