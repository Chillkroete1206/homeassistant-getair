from __future__ import annotations

from homeassistant import config_entries
from homeassistant.core import callback

import voluptuous as vol

from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD


class GetairConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Getair Sensors."""

    VERSION = 1

    def __init__(self):
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Getair", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=self._errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return GetairOptionsFlowHandler(config_entry)


class GetairOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Getair Sensors."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return self.async_create_entry(title="", data={})
