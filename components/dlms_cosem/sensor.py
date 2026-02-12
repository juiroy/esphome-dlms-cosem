import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from . import (
    DlmsCosem,
    dlms_cosem_ns,
    obis_code,
    CONF_DLMS_COSEM_ID,
    CONF_OBIS_CODE,
    CONF_DONT_PUBLISH,
    CONF_OBIS_CLASS,
    CONF_MIN_UPDATE_INTERVAL,
)

DlmsCosemSensor = dlms_cosem_ns.class_("DlmsCosemSensor", sensor.Sensor)

CONF_MULTIPLIER = "multiplier"

CONFIG_SCHEMA = cv.All(
    sensor.sensor_schema(
        DlmsCosemSensor,
    ).extend(
        {
            cv.GenerateID(CONF_DLMS_COSEM_ID): cv.use_id(DlmsCosem),
            cv.Required(CONF_OBIS_CODE): obis_code,
            cv.Optional(CONF_DONT_PUBLISH, default=False): cv.boolean,
            cv.Optional(CONF_MULTIPLIER, default=1.0): cv.float_,
            cv.Optional(CONF_OBIS_CLASS, default=3): cv.int_,
            cv.Optional(CONF_MIN_UPDATE_INTERVAL): cv.positive_time_period_milliseconds,
        }
    ),
    cv.has_exactly_one_key(CONF_OBIS_CODE),
)


async def to_code(config):
    component = await cg.get_variable(config[CONF_DLMS_COSEM_ID])
    var = await sensor.new_sensor(config)
    cg.add(var.set_obis_code(config[CONF_OBIS_CODE]))
    cg.add(var.set_dont_publish(config.get(CONF_DONT_PUBLISH)))
    cg.add(var.set_multiplier(config[CONF_MULTIPLIER]))
    cg.add(var.set_obis_class(config[CONF_OBIS_CLASS]))
    if CONF_MIN_UPDATE_INTERVAL in config:
        cg.add(var.set_update_interval(config[CONF_MIN_UPDATE_INTERVAL]))
    cg.add(component.register_sensor(var))
