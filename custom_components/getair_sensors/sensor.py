from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import EntityCategory

from functools import partial

from .const import DOMAIN
from .api_wrapper import GetairAPIWrapper, Device


ALL_ATTRIBUTES = {
    "temperature": {"unit": "°C", "class": "temperature", "default": True},
    "humidity": {"unit": "%", "class": "humidity", "default": True},
    "speed": {"unit": None, "class": None, "default": True},
    "runtime": {"unit": "h", "class": None, "default": False},
    "last-filter-change": {"unit": "h", "class": None, "default": False},
    "mode": {"unit": None, "class": None, "default": False},
    "mode-deadline": {"unit": None, "class": None, "default": False},
    "target-temp": {"unit": "°C", "class": "temperature", "default": False},
    "target-hmdty-level": {"unit": None, "class": None, "default": False},
    "auto-mode-voc": {"unit": None, "class": None, "default": False},
    "auto-mode-silent": {"unit": None, "class": None, "default": False},
    "hmdty-outdoors": {"unit": "%", "class": "humidity", "default": False},
    "temp-outdoors": {"unit": "°C", "class": "temperature", "default": False},
    "time-profile": {"unit": None, "class": None, "default": False},
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    wrapper: GetairAPIWrapper = hass.data[DOMAIN][entry.entry_id]
    entities: list[SensorEntity] = []

    for device in wrapper.devices:
        base_id = device.device_id

        for zone_index in range(1, 4):
            zone_id = f"{zone_index}.{base_id}"

            zone_data = await hass.async_add_executor_job(
                partial(device._api._request_get, f"devices/{zone_id}/services/Zone")
            )

            if not zone_data or "name" not in zone_data:
                continue

            zone_name = zone_data["name"].replace(" ", "_")

            for attr, meta in ALL_ATTRIBUTES.items():
                value = zone_data.get(attr)
                entities.append(
                    GetairZoneSensor(
                        device_id=base_id,
                        zone_name=zone_name,
                        attribute=attr,
                        value=value,
                        unit=meta["unit"],
                        device_class=meta["class"],
                        enabled_by_default=meta["default"],
                    )
                )

    async_add_entities(entities)


class GetairZoneSensor(SensorEntity):
    def __init__(
        self,
        device_id: str,
        zone_name: str,
        attribute: str,
        value: float | str | bool | None,
        unit: str | None,
        device_class: str | None,
        enabled_by_default: bool,
    ):
        self._device_id = device_id
        self._zone_name = zone_name
        self._attr_name = f"{zone_name}_{attribute}"
        self._attr_unique_id = f"{device_id}_{zone_name}_{attribute}"
        self._value = value
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_entity_category = (
            EntityCategory.DIAGNOSTIC if not enabled_by_default else None
        )
        self._attr_entity_registry_enabled_default = enabled_by_default
        self._attr = attribute

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device_id)},  # Nur device_id, ohne zone_name
            "name": "Getair Lüftungsanlage",  # Einheitlicher Gerätename
            "manufacturer": "Getair",
            "model": "Lüftungsanlage",
            # kein entry_type nötig
        }

    @property
    def native_value(self):
        if self._attr == "speed" and self._value is not None:
            return round(self._value, 1)
        return self._value
