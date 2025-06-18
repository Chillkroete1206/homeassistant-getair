from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD
from .api_wrapper import GetairAPIWrapper
from .coordinator import GetairDataUpdateCoordinator

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up integration via configuration.yaml (nicht verwendet)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Getair Sensors aus einer ConfigEntry."""

    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]

    wrapper = GetairAPIWrapper(username, password)

    # Verbindung zur API aufbauen (synchron im Executor)
    connected = await hass.async_add_executor_job(wrapper.connect)
    if not connected:
        return False

    coordinator = GetairDataUpdateCoordinator(hass, wrapper)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Entfernt eine ConfigEntry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
