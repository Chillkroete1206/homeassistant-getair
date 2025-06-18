from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api_wrapper import GetairAPIWrapper
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)


class GetairDataUpdateCoordinator(DataUpdateCoordinator[dict[str, dict]]):
    """Koordinator für das Abrufen von Zonen-Daten der Getair Lüftungsgeräte."""

    def __init__(self, hass: HomeAssistant, wrapper: GetairAPIWrapper) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} Coordinator",
            update_interval=SCAN_INTERVAL,
        )
        self.api_wrapper = wrapper

    async def _async_update_data(self) -> dict[str, dict]:
        """Hole aktuelle Zonen-Daten aller Geräte."""
        try:
            return await self.hass.async_add_executor_job(
                self.api_wrapper.update_all_zones
            )
        except Exception as err:
            raise UpdateFailed(f"Fehler beim Abrufen der Zonen-Daten: {err}") from err
