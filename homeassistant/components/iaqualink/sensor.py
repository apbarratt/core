"""Support for Aqualink temperature sensors."""
from __future__ import annotations

from iaqualink.device import AqualinkSensor

from homeassistant.components.sensor import DOMAIN, SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AqualinkEntity
from .const import DOMAIN as AQUALINK_DOMAIN

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up discovered sensors."""
    devs = []
    for dev in hass.data[AQUALINK_DOMAIN][DOMAIN]:
        devs.append(HassAqualinkSensor(dev))
    async_add_entities(devs, True)


class HassAqualinkSensor(AqualinkEntity, SensorEntity):
    """Representation of a sensor."""

    def __init__(self, dev: AqualinkSensor) -> None:
        """Initialize AquaLink sensor."""
        super().__init__(dev)
        self._attr_name = dev.label
        if dev.name.endswith("_temp"):
            self._attr_native_unit_of_measurement = (
                UnitOfTemperature.FAHRENHEIT
                if dev.system.temp_unit == "F"
                else UnitOfTemperature.CELSIUS
            )
            self._attr_device_class = SensorDeviceClass.TEMPERATURE

    @property
    def native_value(self) -> int | float | None:
        """Return the state of the sensor."""
        if self.dev.state == "":
            return None

        try:
            return int(self.dev.state)
        except ValueError:
            return float(self.dev.state)
