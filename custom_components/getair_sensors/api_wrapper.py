from .const import AUTH_URL, API_URL
from .api import API, Device

import logging

_LOGGER = logging.getLogger(__name__)


class GetairAPIWrapper:
    """Wrapper to use the original Getair API in Home Assistant context."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.api: API | None = None
        self.devices: list[Device] = []

    def connect(self) -> bool:
        """Establish connection to Getair cloud."""
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
            _LOGGER.info("Successfully connected to Getair API.")
            self.devices = self.api.get_devices()
            return True
        else:
            _LOGGER.error("Failed to connect to Getair API.")
            return False

    def update_all_devices(self) -> bool:
        """Fetch fresh data for all registered devices (blocking – wrap in executor_job!)."""
        if not self.devices:
            return False

        success = True
        for device in self.devices:
            try:
                ok = device.fetch()
            except Exception as e:
                _LOGGER.exception(f"Error fetching device {device.device_id}: {e}")
                ok = False
            if not ok:
                _LOGGER.warning(f"Failed to update device {device.device_id}")
                success = False
        return success
