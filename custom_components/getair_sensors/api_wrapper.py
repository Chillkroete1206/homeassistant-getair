import logging

from .const import AUTH_URL, API_URL
from .api import API, Device

_LOGGER = logging.getLogger(__name__)


class GetairAPIWrapper:
    """Wrapper zur Verwendung der originalen Getair API in Home Assistant."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.api: API | None = None
        self.devices: list[Device] = []

    def connect(self) -> bool:
        """Stellt eine Verbindung zur Getair Cloud her."""
        self.api = API()
        self.api._auth_url = AUTH_URL
        self.api._api_url = API_URL

        def _mock_load_credentials():
            return {
                "username": self.username,
                "password": self.password,
                "auth_url": AUTH_URL,
                "api_url": API_URL,
            }

        self.api._load_credentials = _mock_load_credentials

        if self.api.connect():
            _LOGGER.info("Erfolgreich mit Getair API verbunden.")
            self.devices = self.api.get_devices()
            return True
        else:
            _LOGGER.error("Verbindung zur Getair API fehlgeschlagen.")
            return False

    def update_all_zones(self) -> dict[str, dict]:
        """Lädt aktuelle Zonen-Daten für alle Geräte."""
        result: dict[str, dict] = {}

        for device in self.devices:
            for zone_index in range(1, 4):
                zone_id = f"{zone_index}.{device.device_id}"
                try:
                    zone_data = device._api._request_get(
                        f"devices/{zone_id}/services/Zone"
                    )
                    if zone_data and "name" in zone_data:
                        result[zone_id] = zone_data
                    else:
                        _LOGGER.debug(
                            f"Zone {zone_id} enthält keine Daten oder keinen Namen."
                        )
                except Exception as e:
                    _LOGGER.exception(f"Fehler beim Abrufen der Zone {zone_id}: {e}")

        return result
