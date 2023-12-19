"""Support for MelCloud device sensors."""
from __future__ import annotations

from typing import Any
import logging


from pymelcloud import DEVICE_TYPE_ERV

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MelCloudDevice
from .const import DOMAIN

from homeassistant.components.select import SelectEntity
from homeassistant.const import STATE_UNKNOWN
from homeassistant.helpers.typing import StateType, Dict

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up MelCloud device control based on config_entry."""
    print('Entities size')
    mel_devices = hass.data[DOMAIN][entry.entry_id]
    entities: list[SelectEntity] = [
        ErvFanSpeedSelect(mel_device) for mel_device in mel_devices[DEVICE_TYPE_ERV]
    ] + [
        ErvVentilationModeSelect(mel_device) for mel_device in mel_devices[DEVICE_TYPE_ERV]
    ]
    size = len(entities)
    print('Entities size')
    _LOGGER.error('Setting up MELCloud device sensors')
    _LOGGER.error(size)
    print(size)
    async_add_entities(entities, True)

class ErvFanSpeedSelect(SelectEntity):
    def __init__(self, mel_device):
        print('INIT SELECT')
        self._mel_device = mel_device
        self._fan_speeds = self._mel_device.device.fan_speeds() or []

    @property
    def name(self) -> str:
        return f"Fan Speed"

    @property
    def unique_id(self) -> str:
        return f"{self._mel_device.device.serial}-{self._mel_device.device.mac}_fan_speed"

    @property
    def state(self) -> StateType:
        return self._mel_device.device.fan_speed() or STATE_UNKNOWN

    @property
    def options(self) -> list:
        return self._fan_speeds

    async def async_select_option(self, option: str) -> None:
        set_dict = {"fan_speed": option}
        await self._mel_device.device.set(set_dict)

class ErvVentilationModeSelect(SelectEntity):
    def __init__(self, mel_device):
        self._mel_device = mel_device
        self._ventilation_modes = self._mel_device.device.ventilation_modes() or []

    @property
    def name(self) -> str:
        return f"Ventilation Mode"

    @property
    def unique_id(self) -> str:
        return f"{self._mel_device.device.serial}-{self._mel_device.device.mac}_ventilation_mode"

    @property
    def state(self) -> StateType:
        return self._mel_device.device.ventilation_mode() or STATE_UNKNOWN

    @property
    def options(self) -> list:
        return self._ventilation_modes

    async def async_select_option(self, option: str) -> None:
        set_dict = {"ventilation_mode": option}
        await self._mel_device.device.set(set_dict)
