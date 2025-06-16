from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD
from .api_wrapper import GetairAPIWrapper

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up integration via configuration.yaml (not used)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Getair Sensors from a config entry."""

    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]

    wrapper = GetairAPIWrapper(username, password)

    # Connect und Update blockieren – also auslagern
    if not await hass.async_add_executor_job(wrapper.connect):
        return False

    await hass.async_add_executor_job(wrapper.update_all_devices)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = wrapper

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
