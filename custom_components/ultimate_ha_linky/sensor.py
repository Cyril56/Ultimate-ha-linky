from homeassistant.components.sensor import SensorEntity
from homeassistant.const import ENERGY_KILO_WATT_HOUR

SENSORS = [
    ("conso_linky_day", "Consommation Jour", "daily"),
    ("conso_linky_week", "Consommation Semaine", "weekly"),
    ("conso_linky_month", "Consommation Mois", "monthly"),
    ("conso_linky_year", "Consommation Année", "yearly"),
]

async def async_setup_entry(hass, config_entry, async_add_entities):
    # Récupérer la classe/coordinator existant qui gère les données ENEDIS
    coordinator = hass.data["ultimate_ha_linky"][config_entry.entry_id]

    sensors = []
    for sensor_id, name, period in SENSORS:
        sensors.append(LinkyConsoSensor(coordinator, sensor_id, name, period))
    async_add_entities(sensors)

class LinkyConsoSensor(SensorEntity):
    def __init__(self, coordinator, sensor_id, name, period):
        self.coordinator = coordinator
        self._attr_unique_id = sensor_id
        self._attr_name = name
        self._period = period
        self._attr_native_unit_of_measurement = ENERGY_KILO_WATT_HOUR

    @property
    def native_value(self):
        # Récupérer la valeur depuis le coordinator en fonction de la période
        return self.coordinator.data.get(self._period)
