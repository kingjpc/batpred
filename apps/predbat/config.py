# -----------------------------------------------------------------------------
# Predbat Home Battery System
# Copyright Trefor Southwell 2024 - All Rights Reserved
# This application maybe used for personal use only and not for commercial use
# -----------------------------------------------------------------------------
# fmt off
# pylint: disable=consider-using-f-string
# pylint: disable=line-too-long
# pylint: disable=attribute-defined-outside-init

from datetime import datetime, timedelta
from predbat import THIS_VERSION


TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
TIME_FORMAT_SECONDS = "%Y-%m-%dT%H:%M:%S.%f%z"
TIME_FORMAT_SOLCAST = "%Y-%m-%dT%H:%M:%S.%f0%z"  # 2024-05-31T18:00:00.0000000Z
TIME_FORMAT_OCTOPUS = "%Y-%m-%d %H:%M:%S%z"
TIME_FORMAT_SOLIS = "%Y-%m-%d %H:%M:%S"
PREDICT_STEP = 5
RUN_EVERY = 5
CONFIG_ROOTS = ["/config", "/conf", "/homeassistant", "./"]
TIME_FORMAT_HA = "%Y-%m-%dT%H:%M:%S%z"
TIMEOUT = 60 * 5
CONFIG_REFRESH_PERIOD = 60 * 8

# 240v x 100 amps x 3 phases / 1000 to kW / 60 minutes in an hour is the maximum kWh in a 1 minute period
MAX_INCREMENT = 240 * 100 * 3 / 1000 / 60
MINUTE_WATT = 60 * 1000

INVERTER_TEST = False  # Run inverter control self test

# Create an array of times in the day in 5-minute intervals
BASE_TIME = datetime.strptime("00:00:00", "%H:%M:%S")
OPTIONS_TIME = [((BASE_TIME + timedelta(seconds=minute * 60)).strftime("%H:%M:%S")) for minute in range(0, 24 * 60, 5)]

# Inverter modes
PREDBAT_MODE_OPTIONS = ["Monitor", "Control SOC only", "Control charge", "Control charge & discharge"]
PREDBAT_MODE_MONITOR = 0
PREDBAT_MODE_CONTROL_SOC = 1
PREDBAT_MODE_CONTROL_CHARGE = 2
PREDBAT_MODE_CONTROL_CHARGEDISCHARGE = 3

# Predbat update options
PREDBAT_UPDATE_OPTIONS = [f"{THIS_VERSION} Loading..."]
PREDBAT_SAVE_RESTORE = ["save current", "restore default"]

# Configuration options inside HA
CONFIG_ITEMS = [
    {
        "name": "version",
        "friendly_name": "Predbat Core Update",
        "type": "update",
        "title": "Predbat",
        "installed_version": THIS_VERSION,
        "release_url": f"https://github.com/springfall2008/batpred/releases/tag/{THIS_VERSION}",
        "entity_picture": "https://user-images.githubusercontent.com/48591903/249456079-e98a0720-d2cf-4b71-94ab-97fe09b3cee1.png",
        "restore": False,
        "default": False,
    },
    {
        "name": "expert_mode",
        "friendly_name": "Expert Mode",
        "type": "switch",
        "default": False,
    },
    {
        "name": "active",
        "friendly_name": "Predbat Active",
        "type": "switch",
        "default": False,
        "restore": False,
    },
    {
        "name": "pv_metric10_weight",
        "friendly_name": "Metric 10 Weight",
        "type": "input_number",
        "min": 0,
        "max": 1.0,
        "step": 0.01,
        "unit": "*",
        "icon": "mdi:multiplication",
        "default": 0.15,
    },
    {
        "name": "pv_scaling",
        "friendly_name": "PV Scaling",
        "type": "input_number",
        "min": 0,
        "max": 2.0,
        "step": 0.01,
        "unit": "*",
        "icon": "mdi:multiplication",
        "default": 1.0,
    },
    {
        "name": "load_scaling",
        "friendly_name": "Load Scaling",
        "type": "input_number",
        "min": 0,
        "max": 2.0,
        "step": 0.01,
        "unit": "*",
        "icon": "mdi:multiplication",
        "default": 1.0,
    },
    {
        "name": "load_scaling10",
        "friendly_name": "Load Scaling PV10%",
        "type": "input_number",
        "min": 0,
        "max": 2.0,
        "step": 0.01,
        "unit": "*",
        "icon": "mdi:multiplication",
        "default": 1.1,
    },
    {
        "name": "load_scaling_saving",
        "friendly_name": "Load Scaling for saving sessions",
        "type": "input_number",
        "min": 0,
        "max": 2.0,
        "step": 0.01,
        "unit": "*",
        "icon": "mdi:multiplication",
        "default": 1.0,
    },
    {
        "name": "battery_rate_max_scaling",
        "friendly_name": "Battery rate max scaling charge",
        "type": "input_number",
        "min": 0,
        "max": 1.0,
        "step": 0.01,
        "unit": "*",
        "icon": "mdi:multiplication",
        "default": 1.0,
    },
    {
        "name": "battery_rate_max_scaling_discharge",
        "friendly_name": "Battery rate max scaling discharge",
        "type": "input_number",
        "min": 0,
        "max": 1.0,
        "step": 0.01,
        "unit": "*",
        "icon": "mdi:multiplication",
        "default": 1.0,
    },
    {
        "name": "battery_loss",
        "friendly_name": "Battery loss charge ",
        "type": "input_number",
        "min": 0,
        "max": 1.0,
        "step": 0.01,
        "unit": "*",
        "icon": "mdi:call-split",
        "default": 0.03,
    },
    {
        "name": "battery_loss_discharge",
        "friendly_name": "Battery loss discharge",
        "type": "input_number",
        "min": 0,
        "max": 1.0,
        "step": 0.01,
        "unit": "*",
        "icon": "mdi:call-split",
        "default": 0.03,
    },
    {
        "name": "inverter_loss",
        "friendly_name": "Inverter Loss",
        "type": "input_number",
        "min": 0,
        "max": 1.0,
        "step": 0.01,
        "unit": "*",
        "icon": "mdi:call-split",
        "default": 0.04,
    },
    {
        "name": "inverter_hybrid",
        "friendly_name": "Inverter Hybrid",
        "type": "switch",
        "default": True,
    },
    {
        "name": "inverter_soc_reset",
        "friendly_name": "Inverter SOC Reset",
        "type": "switch",
        "enable": "expert_mode",
        "default": True,
    },
    {
        "name": "inverter_set_charge_before",
        "friendly_name": "Inverter Set charge window before start",
        "type": "switch",
        "enable": "expert_mode",
        "default": True,
    },
    {
        "name": "battery_capacity_nominal",
        "friendly_name": "Use the Battery Capacity Nominal size",
        "type": "switch",
        "enable": "expert_mode",
        "default": False,
    },
    {
        "name": "car_charging_energy_scale",
        "friendly_name": "Car charging energy scale",
        "type": "input_number",
        "min": 0,
        "max": 1.0,
        "step": 0.01,
        "unit": "*",
        "icon": "mdi:multiplication",
        "default": 1.0,
    },
    {
        "name": "car_charging_threshold",
        "friendly_name": "Car charging threshold",
        "type": "input_number",
        "min": 4,
        "max": 8.5,
        "step": 0.10,
        "unit": "kW",
        "icon": "mdi:ev-station",
        "default": 6.0,
    },
    {
        "name": "car_charging_rate",
        "friendly_name": "Car charging rate",
        "type": "input_number",
        "min": 1,
        "max": 8.5,
        "step": 0.10,
        "unit": "kW",
        "icon": "mdi:ev-station",
        "default": 7.4,
    },
    {
        "name": "car_charging_loss",
        "friendly_name": "Car charging loss",
        "type": "input_number",
        "min": 0,
        "max": 1.0,
        "step": 0.01,
        "unit": "*",
        "icon": "mdi:call-split",
        "default": 0.08,
    },
    {
        "name": "best_soc_min",
        "friendly_name": "Best SOC Min",
        "type": "input_number",
        "min": 0,
        "max": 30.0,
        "step": 0.10,
        "unit": "kWh",
        "icon": "mdi:battery-50",
        "enable": "expert_mode",
        "default": 0.0,
    },
    {
        "name": "best_soc_max",
        "friendly_name": "Best SOC Max",
        "type": "input_number",
        "min": 0,
        "max": 30.0,
        "step": 0.10,
        "unit": "kWh",
        "icon": "mdi:battery-50",
        "enable": "expert_mode",
        "default": 0.0,
    },
    {
        "name": "best_soc_keep",
        "friendly_name": "Best SOC Keep",
        "type": "input_number",
        "min": 0,
        "max": 30.0,
        "step": 0.10,
        "unit": "kWh",
        "icon": "mdi:battery-50",
        "default": 0.5,
    },
    {
        "name": "metric_min_improvement",
        "friendly_name": "Metric Min Improvement",
        "type": "input_number",
        "min": -50,
        "max": 50.0,
        "step": 0.1,
        "unit": "p",
        "icon": "mdi:currency-usd",
        "enable": "expert_mode",
        "default": 0.0,
    },
    {
        "name": "metric_min_improvement_discharge",
        "friendly_name": "Metric Min Improvement Discharge",
        "type": "input_number",
        "min": -50,
        "max": 50.0,
        "step": 0.1,
        "unit": "p",
        "icon": "mdi:currency-usd",
        "enable": "expert_mode",
        "default": 0.1,
    },
    {
        "name": "metric_battery_cycle",
        "friendly_name": "Metric Battery Cycle Cost",
        "type": "input_number",
        "min": -50,
        "max": 50.0,
        "step": 0.1,
        "unit": "p/kWh",
        "icon": "mdi:currency-usd",
        "enable": "expert_mode",
        "default": 0,
    },
    {
        "name": "metric_battery_value_scaling",
        "friendly_name": "Metric Battery Value Scaling",
        "type": "input_number",
        "min": 0,
        "max": 2.0,
        "step": 0.1,
        "unit": "*",
        "icon": "mdi:multiplication",
        "enable": "expert_mode",
        "default": 1.0,
    },
    {
        "name": "metric_future_rate_offset_import",
        "friendly_name": "Metric Future Rate Offset Import",
        "type": "input_number",
        "min": -50,
        "max": 50.0,
        "step": 0.1,
        "unit": "p/kWh",
        "icon": "mdi:currency-usd",
        "enable": "expert_mode",
        "default": 0.0,
    },
    {
        "name": "metric_future_rate_offset_export",
        "friendly_name": "Metric Future Rate Offset Export",
        "type": "input_number",
        "min": -50,
        "max": 50.0,
        "step": 0.1,
        "unit": "p/kWh",
        "icon": "mdi:currency-usd",
        "enable": "expert_mode",
        "default": 0.0,
    },
    {
        "name": "metric_inday_adjust_damping",
        "friendly_name": "In-day adjustment damping factor",
        "type": "input_number",
        "min": 0.5,
        "max": 2.0,
        "step": 0.05,
        "unit": "*",
        "icon": "mdi:call-split",
        "enable": "expert_mode",
        "default": 0.95,
    },
    {
        "name": "metric_cloud_enable",
        "friendly_name": "Enable Cloud Model",
        "type": "switch",
        "default": True,
        "enable": "expert_mode",
    },
    {
        "name": "metric_load_divergence_enable",
        "friendly_name": "Enable Load Divergence Model",
        "type": "switch",
        "default": True,
        "enable": "expert_mode",
    },
    {
        "name": "metric_self_sufficiency",
        "friendly_name": "Metric Self Sufficiency",
        "type": "input_number",
        "min": 0,
        "max": 100,
        "step": 0.5,
        "unit": "p/kWh",
        "icon": "mdi:currency-usd",
        "enable": "expert_mode",
        "default": 0.0,
    },
    {
        "name": "set_reserve_min",
        "friendly_name": "Set Reserve Min",
        "type": "input_number",
        "min": 4,
        "max": 100,
        "step": 1,
        "unit": "%",
        "icon": "mdi:percent",
        "default": 4.0,
        "reset_inverter": True,
    },
    {
        "name": "rate_low_threshold",
        "friendly_name": "Rate Low Threshold",
        "type": "input_number",
        "min": 0.00,
        "max": 2.00,
        "step": 0.05,
        "unit": "*",
        "icon": "mdi:multiplication",
        "enable": "expert_mode",
        "default": 0.0,
    },
    {
        "name": "rate_high_threshold",
        "friendly_name": "Rate High Threshold",
        "type": "input_number",
        "min": 0.00,
        "max": 2.00,
        "step": 0.05,
        "unit": "*",
        "icon": "mdi:multiplication",
        "enable": "expert_mode",
        "default": 0.0,
    },
    {
        "name": "combine_rate_threshold",
        "friendly_name": "Combine Rate Threshold",
        "type": "input_number",
        "min": 0,
        "max": 5.0,
        "step": 0.1,
        "unit": "p",
        "icon": "mdi:table-merge-cells",
        "enable": "expert_mode",
        "default": 0.0,
    },
    {
        "name": "car_charging_hold",
        "friendly_name": "Car charging hold",
        "type": "switch",
        "default": True,
        "reset_inverter": True,
    },
    {
        "name": "car_charging_manual_soc",
        "friendly_name": "Car charging manual SOC",
        "type": "switch",
        "default": False,
    },
    {
        "name": "car_charging_manual_soc_kwh",
        "friendly_name": "Car manual SOC kWh",
        "type": "input_number",
        "min": 0,
        "max": 100,
        "step": 0.01,
        "unit": "kWh",
        "icon": "mdi:ev-station",
        "enable": "car_charging_manual_soc",
        "default": 0.0,
        "restore": False,
    },
    {
        "name": "octopus_intelligent_charging",
        "friendly_name": "Octopus Intelligent Charging",
        "type": "switch",
        "default": True,
    },
    {
        "name": "octopus_intelligent_ignore_unplugged",
        "friendly_name": "Ignore Intelligent slots when car is unplugged",
        "type": "switch",
        "default": False,
        "enable": "expert_mode",
    },
    {
        "name": "car_charging_plan_smart",
        "friendly_name": "Car Charging Plan Smart",
        "type": "switch",
        "default": False,
    },
    {
        "name": "car_charging_plan_max_price",
        "friendly_name": "Car Charging Plan max price",
        "type": "input_number",
        "min": -99,
        "max": 99,
        "step": 1,
        "unit": "p",
        "icon": "mdi:ev-station",
        "default": 0,
    },
    {
        "name": "car_charging_from_battery",
        "friendly_name": "Allow car to charge from battery",
        "type": "switch",
        "default": False,
        "reset_inverter": True,
    },
    {
        "name": "calculate_discharge_oncharge",
        "friendly_name": "Calculate Discharge on charge slots",
        "type": "switch",
        "enable": "expert_mode",
        "default": True,
    },
    {
        "name": "calculate_second_pass",
        "friendly_name": "Calculate full second pass (slower)",
        "type": "switch",
        "enable": "expert_mode",
        "default": False,
    },
    {
        "name": "calculate_tweak_plan",
        "friendly_name": "Calculate tweak second pass",
        "type": "switch",
        "enable": "expert_mode",
        "default": False,
    },
    {
        "name": "calculate_secondary_order",
        "friendly_name": "Calculate secondary order slots",
        "type": "switch",
        "enable": "expert_mode",
        "default": True,
    },
    {
        "name": "calculate_inday_adjustment",
        "friendly_name": "Calculate in-day adjustment",
        "type": "switch",
        "enable": "expert_mode",
        "default": True,
    },
    {
        "name": "calculate_plan_every",
        "friendly_name": "Calculate plan every N minutes",
        "type": "input_number",
        "min": 5,
        "max": 60,
        "step": 5,
        "unit": "minutes",
        "icon": "mdi:clock-end",
        "enable": "expert_mode",
        "default": 10,
    },
    {
        "name": "combine_charge_slots",
        "friendly_name": "Combine Charge Slots",
        "type": "switch",
        "default": False,
    },
    {
        "name": "combine_discharge_slots",
        "friendly_name": "Combine Discharge Slots",
        "type": "switch",
        "enable": "expert_mode",
        "default": False,
    },
    {
        "name": "set_status_notify",
        "friendly_name": "Set Status Notify",
        "type": "switch",
        "default": True,
    },
    {
        "name": "set_inverter_notify",
        "friendly_name": "Set Inverter Notify",
        "type": "switch",
        "default": False,
    },
    {
        "name": "set_charge_freeze",
        "friendly_name": "Set Charge Freeze",
        "type": "switch",
        "enable": "expert_mode",
        "default": True,
        "reset_inverter": True,
    },
    {
        "name": "set_charge_low_power",
        "friendly_name": "Set Charge Low Power Mode",
        "type": "switch",
        "default": False,
        "reset_inverter": True,
    },
    {
        "name": "set_reserve_enable",
        "friendly_name": "Set Reserve Enable",
        "type": "switch",
        "enable": "expert_mode",
        "default": True,
        "reset_inverter": True,
    },
    {
        "name": "set_discharge_freeze_only",
        "friendly_name": "Set Discharge Freeze Only",
        "type": "switch",
        "enable": "expert_mode",
        "default": False,
        "reset_inverter": True,
    },
    {
        "name": "set_discharge_during_charge",
        "friendly_name": "Set Discharge During Charge",
        "type": "switch",
        "default": True,
    },
    {
        "name": "set_read_only",
        "friendly_name": "Read Only mode",
        "type": "switch",
        "default": False,
        "reset_inverter_force": True,
    },
    {
        "name": "balance_inverters_enable",
        "friendly_name": "Balance Inverters Enable (Beta)",
        "type": "switch",
        "default": False,
    },
    {
        "name": "balance_inverters_charge",
        "friendly_name": "Balance Inverters for charging",
        "type": "switch",
        "enable": "balance_inverters_enable",
        "default": True,
    },
    {
        "name": "balance_inverters_discharge",
        "friendly_name": "Balance Inverters for discharge",
        "type": "switch",
        "enable": "balance_inverters_enable",
        "default": True,
    },
    {
        "name": "balance_inverters_crosscharge",
        "friendly_name": "Balance Inverters for cross-charging",
        "type": "switch",
        "enable": "balance_inverters_enable",
        "default": True,
    },
    {
        "name": "balance_inverters_threshold_charge",
        "friendly_name": "Balance Inverters threshold charge",
        "type": "input_number",
        "min": 1,
        "max": 20,
        "step": 1,
        "unit": "%",
        "icon": "mdi:percent",
        "enable": "balance_inverters_enable",
        "default": 1.0,
    },
    {
        "name": "balance_inverters_threshold_discharge",
        "friendly_name": "Balance Inverters threshold discharge",
        "type": "input_number",
        "min": 1,
        "max": 20,
        "step": 1,
        "unit": "%",
        "icon": "mdi:percent",
        "enable": "balance_inverters_enable",
        "default": 1.0,
    },
    {
        "name": "debug_enable",
        "friendly_name": "Debug Enable",
        "type": "switch",
        "icon": "mdi:bug-outline",
        "default": False,
    },
    {
        "name": "car_charging_plan_time",
        "friendly_name": "Car charging planned ready time",
        "type": "select",
        "options": OPTIONS_TIME,
        "icon": "mdi:clock-end",
        "default": "07:00:00",
    },
    {
        "name": "mode",
        "friendly_name": "Predbat mode",
        "type": "select",
        "options": PREDBAT_MODE_OPTIONS,
        "icon": "mdi:state-machine",
        "default": PREDBAT_MODE_OPTIONS[PREDBAT_MODE_CONTROL_CHARGEDISCHARGE],
        "reset_inverter_force": True,
    },
    {
        "name": "update",
        "friendly_name": "Predbat update",
        "type": "select",
        "options": PREDBAT_UPDATE_OPTIONS,
        "icon": "mdi:state-machine",
        "default": None,
        "restore": False,
        "save": False,
    },
    {
        "name": "manual_charge",
        "friendly_name": "Manual force charge",
        "type": "select",
        "options": ["off"],
        "icon": "mdi:state-machine",
        "default": "off",
        "restore": False,
        "manual": True,
    },
    {
        "name": "manual_discharge",
        "friendly_name": "Manual force discharge",
        "type": "select",
        "options": ["off"],
        "icon": "mdi:state-machine",
        "default": "off",
        "restore": False,
        "manual": True,
    },
    {
        "name": "manual_idle",
        "friendly_name": "Manual force idle",
        "type": "select",
        "options": ["off"],
        "icon": "mdi:state-machine",
        "default": "off",
        "restore": False,
        "manual": True,
    },
    {
        "name": "manual_freeze_charge",
        "friendly_name": "Manual force charge freeze",
        "type": "select",
        "options": ["off"],
        "icon": "mdi:state-machine",
        "default": "off",
        "restore": False,
        "manual": True,
    },
    {
        "name": "manual_freeze_discharge",
        "friendly_name": "Manual force discharge freeze",
        "type": "select",
        "options": ["off"],
        "icon": "mdi:state-machine",
        "default": "off",
        "restore": False,
        "manual": True,
    },
    {
        "name": "saverestore",
        "friendly_name": "Save/restore settings",
        "type": "select",
        "options": PREDBAT_SAVE_RESTORE,
        "icon": "mdi:state-machine",
        "default": "",
        "restore": False,
        "save": False,
    },
    {
        "name": "auto_update",
        "friendly_name": "Predbat automatic update enable",
        "type": "switch",
        "default": False,
    },
    {
        "name": "load_filter_modal",
        "friendly_name": "Apply modal filter historical load",
        "type": "switch",
        "enable": "expert_mode",
        "default": True,
    },
    {
        "name": "iboost_enable",
        "friendly_name": "iBoost enable",
        "type": "switch",
        "default": False,
    },
    {
        "name": "carbon_enable",
        "friendly_name": "Carbon enable",
        "type": "switch",
        "default": False,
    },
    {
        "name": "carbon_metric",
        "friendly_name": "Carbon Metric",
        "type": "input_number",
        "min": 0,
        "max": 500,
        "step": 1,
        "unit": "p/Kg",
        "icon": "mdi:molecule-co2",
        "default": 0,
        "enable": "carbon_enable",
    },
    {
        "name": "iboost_solar",
        "friendly_name": "iBoost on solar power",
        "type": "switch",
        "default": True,
        "enable": "iboost_enable",
    },
    {
        "name": "iboost_gas",
        "friendly_name": "iBoost when import electricity cheaper than gas",
        "type": "switch",
        "default": False,
        "enable": "iboost_enable",
    },
    {
        "name": "iboost_gas_export",
        "friendly_name": "iBoost when export electricity cheaper than gas",
        "type": "switch",
        "default": False,
        "enable": "iboost_enable",
    },
    {
        "name": "iboost_charging",
        "friendly_name": "iBoost when battery charging",
        "type": "switch",
        "default": False,
        "enable": "iboost_enable",
    },
    {
        "name": "iboost_rate",
        "friendly_name": "iBoost on energy rates",
        "type": "switch",
        "enable": "iboost_enable",
        "default": False,
    },
    {
        "name": "iboost_rate_threshold",
        "friendly_name": "iBoost max import boost price",
        "type": "input_number",
        "min": -10,
        "max": 100,
        "step": 1,
        "unit": "p/kWh",
        "icon": "mdi:currency-usd",
        "enable": "iboost_enable",
        "default": 100,
    },
    {
        "name": "iboost_rate_threshold_export",
        "friendly_name": "iBoost max export boost price",
        "type": "input_number",
        "min": -10,
        "max": 100,
        "step": 1,
        "unit": "p/kWh",
        "icon": "mdi:currency-usd",
        "enable": "iboost_enable",
        "default": 100,
    },
    {
        "name": "iboost_smart",
        "friendly_name": "iBoost when rates are lowest to hit target energy",
        "type": "switch",
        "enable": "iboost_enable",
        "default": False,
    },
    {
        "name": "iboost_discharge",
        "friendly_name": "iBoost is allowed when battery is force discharging",
        "type": "switch",
        "enable": "iboost_enable",
        "default": False,
    },
    {
        "name": "iboost_gas_scale",
        "friendly_name": "iBoost gas price scaling",
        "type": "input_number",
        "min": 0,
        "max": 2.0,
        "step": 0.1,
        "unit": "*",
        "icon": "mdi:multiplication",
        "enable": "iboost_enable",
        "default": 1.0,
    },
    {
        "name": "iboost_max_energy",
        "friendly_name": "iBoost max energy",
        "type": "input_number",
        "min": 0,
        "max": 20,
        "step": 0.1,
        "unit": "kWh",
        "enable": "iboost_enable",
        "default": 3.0,
    },
    {
        "name": "iboost_today",
        "friendly_name": "iBoost today",
        "type": "input_number",
        "min": 0,
        "max": 5,
        "step": 0.1,
        "unit": "kWh",
        "enable": "iboost_enable",
        "default": 0.0,
    },
    {
        "name": "iboost_max_power",
        "friendly_name": "iBoost max power",
        "type": "input_number",
        "min": 0,
        "max": 3500,
        "step": 100,
        "unit": "W",
        "enable": "iboost_enable",
        "default": 2400,
    },
    {
        "name": "iboost_min_power",
        "friendly_name": "iBoost min power",
        "type": "input_number",
        "min": 0,
        "max": 3500,
        "step": 100,
        "unit": "W",
        "enable": "iboost_enable",
        "default": 500,
    },
    {
        "name": "iboost_min_soc",
        "friendly_name": "iBoost min soc",
        "type": "input_number",
        "min": 0,
        "max": 100,
        "step": 5,
        "unit": "%",
        "icon": "mdi:percent",
        "enable": "iboost_enable",
        "default": 0.0,
    },
    {
        "name": "iboost_value_scaling",
        "friendly_name": "iBoost value scaling",
        "type": "input_number",
        "min": 0,
        "max": 2.0,
        "step": 0.1,
        "unit": "*",
        "enable": "iboost_enable",
        "icon": "mdi:multiplication",
        "default": 0.75,
    },
    {
        "name": "holiday_days_left",
        "friendly_name": "Holiday days left",
        "type": "input_number",
        "min": 0,
        "max": 28,
        "step": 1,
        "unit": "days",
        "icon": "mdi:clock-end",
        "default": 0,
        "restore": False,
    },
    {
        "name": "forecast_plan_hours",
        "friendly_name": "Plan forecast hours",
        "type": "input_number",
        "min": 8,
        "max": 96,
        "step": 1,
        "unit": "hours",
        "icon": "mdi:clock-end",
        "enable": "expert_mode",
        "default": 24,
    },
    {
        "name": "plan_debug",
        "friendly_name": "HTML Plan Debug",
        "type": "switch",
        "default": False,
        "enable": "expert_mode",
    },
]

"""
GE Inverters are the default but not all inverters have the same parameters so this constant
maps the parameters that are different between brands.

The approach is to attempt to mimic the GE model with dummy entities in HA so that predbat GE
code can be used with minimal modification.
"""
INVERTER_DEF = {
    "GE": {
        "name": "GivEnergy",
        "has_rest_api": True,
        "has_mqtt_api": False,
        "has_service_api": False,
        "output_charge_control": "power",
        "has_charge_enable_time": True,
        "has_discharge_enable_time": False,
        "has_target_soc": True,
        "has_reserve_soc": True,
        "has_timed_pause": True,
        "charge_time_format": "HH:MM:SS",
        "charge_time_entity_is_option": True,
        "soc_units": "kWh",
        "num_load_entities": 1,
        "has_ge_inverter_mode": True,
        "time_button_press": False,
        "clock_time_format": "%H:%M:%S",
        "write_and_poll_sleep": 10,
        "has_time_window": True,
        "support_charge_freeze": True,
        "support_discharge_freeze": True,
        "has_idle_time": False,
        "can_span_midnight": True,
    },
    "GEC": {
        "name": "GivEnergy Cloud",
        "has_rest_api": False,
        "has_mqtt_api": False,
        "has_service_api": False,
        "output_charge_control": "power",
        "has_charge_enable_time": True,
        "has_discharge_enable_time": True,
        "has_target_soc": True,
        "has_reserve_soc": True,
        "has_timed_pause": True,
        "charge_time_format": "HH:MM:SS",
        "charge_time_entity_is_option": True,
        "soc_units": "kWh",
        "num_load_entities": 1,
        "has_ge_inverter_mode": False,
        "time_button_press": False,
        "clock_time_format": "%H:%M:%S",
        "write_and_poll_sleep": 10,
        "has_time_window": True,
        "support_charge_freeze": True,
        "support_discharge_freeze": True,
        "has_idle_time": False,
        "can_span_midnight": True,
    },
    "GEE": {
        "name": "GivEnergy EMC",
        "has_rest_api": False,
        "has_mqtt_api": False,
        "has_service_api": False,
        "output_charge_control": "power",
        "has_charge_enable_time": False,
        "has_discharge_enable_time": False,
        "has_target_soc": True,
        "has_reserve_soc": True,
        "has_timed_pause": False,
        "charge_time_format": "HH:MM:SS",
        "charge_time_entity_is_option": True,
        "soc_units": "kWh",
        "num_load_entities": 1,
        "has_ge_inverter_mode": False,
        "time_button_press": False,
        "clock_time_format": "%H:%M:%S",
        "write_and_poll_sleep": 10,
        "has_time_window": True,
        "support_charge_freeze": True,
        "support_discharge_freeze": False,
        "has_idle_time": True,
        "can_span_midnight": False,
    },
    "GS": {
        "name": "Ginlong Solis",
        "has_rest_api": False,
        "has_mqtt_api": False,
        "has_service_api": False,
        "output_charge_control": "current",
        "has_charge_enable_time": False,
        "has_discharge_enable_time": False,
        "has_target_soc": False,
        "has_reserve_soc": False,
        "has_timed_pause": False,
        "charge_time_format": "H M",
        "charge_time_entity_is_option": False,
        "soc_units": "%",
        "num_load_entities": 2,
        "has_ge_inverter_mode": False,
        "time_button_press": True,
        "clock_time_format": "%Y-%m-%d %H:%M:%S",
        "write_and_poll_sleep": 2,
        "has_time_window": True,
        "support_charge_freeze": False,
        "support_discharge_freeze": False,
        "has_idle_time": False,
        "can_span_midnight": True,
    },
    "SE": {
        "name": "SolarEdge",
        "has_rest_api": False,
        "has_mqtt_api": False,
        "has_service_api": True,
        "output_charge_control": "power",
        "has_charge_enable_time": False,
        "has_discharge_enable_time": False,
        "has_target_soc": False,
        "has_reserve_soc": False,
        "has_timed_pause": False,
        "charge_time_format": "S",
        "charge_time_entity_is_option": False,
        "soc_units": "%",
        "num_load_entities": 1,
        "has_ge_inverter_mode": False,
        "time_button_press": False,
        "clock_time_format": "%Y-%m-%d %H:%M:%S",
        "write_and_poll_sleep": 2,
        "has_time_window": False,
        "support_charge_freeze": False,
        "support_discharge_freeze": False,
        "has_idle_time": False,
        "can_span_midnight": True,
    },
    "SX4": {
        "name": "Solax Gen4 (Modbus Power Control)",
        "has_rest_api": False,
        "has_mqtt_api": False,
        "has_service_api": False,
        "output_charge_control": "power",
        "has_charge_enable_time": False,
        "has_discharge_enable_time": False,
        "has_target_soc": False,
        "has_reserve_soc": False,
        "has_timed_pause": False,
        "charge_time_format": "S",
        "charge_time_entity_is_option": False,
        "soc_units": "%",
        "num_load_entities": 1,
        "has_ge_inverter_mode": False,
        "time_button_press": True,
        "clock_time_format": "%Y-%m-%d %H:%M:%S",
        "write_and_poll_sleep": 2,
        "has_time_window": False,
        "support_charge_freeze": False,
        "support_discharge_freeze": False,
        "has_idle_time": False,
        "can_span_midnight": True,
    },
    "SF": {
        "name": "Sofar HYD",
        "has_rest_api": False,
        "has_mqtt_api": True,
        "has_service_api": False,
        "output_charge_control": "none",
        "has_charge_enable_time": False,
        "has_discharge_enable_time": False,
        "has_target_soc": False,
        "has_reserve_soc": False,
        "has_timed_pause": False,
        "charge_time_format": "S",
        "charge_time_entity_is_option": False,
        "soc_units": "%",
        "num_load_entities": 1,
        "has_ge_inverter_mode": False,
        "time_button_press": False,
        "clock_time_format": "%Y-%m-%d %H:%M:%S",
        "write_and_poll_sleep": 2,
        "has_time_window": False,
        "support_charge_freeze": False,
        "support_discharge_freeze": False,
        "has_idle_time": False,
        "can_span_midnight": True,
    },
    "HU": {
        "name": "Huawei Solar",
        "has_rest_api": False,
        "has_mqtt_api": False,
        "has_service_api": True,
        "output_charge_control": "power",
        "has_charge_enable_time": False,
        "has_discharge_enable_time": False,
        "has_target_soc": False,
        "has_reserve_soc": False,
        "has_timed_pause": False,
        "charge_time_format": "S",
        "charge_time_entity_is_option": False,
        "soc_units": "%",
        "num_load_entities": 1,
        "has_ge_inverter_mode": False,
        "time_button_press": False,
        "clock_time_format": "%Y-%m-%d %H:%M:%S",
        "write_and_poll_sleep": 2,
        "has_time_window": False,
        "support_charge_freeze": False,
        "support_discharge_freeze": False,
        "has_idle_time": False,
        "can_span_midnight": True,
    },
    "SK": {
        "name": "Sunsynk",
        "has_rest_api": False,
        "has_mqtt_api": False,
        "has_service_api": True,
        "output_charge_control": "current",
        "current_dp": 0,
        "has_charge_enable_time": False,
        "has_discharge_enable_time": False,
        "has_target_soc": True,
        "has_reserve_soc": False,
        "has_timed_pause": False,
        "charge_time_format": "S",
        "charge_time_entity_is_option": False,
        "soc_units": "%",
        "num_load_entities": 1,
        "has_ge_inverter_mode": False,
        "time_button_press": False,
        "clock_time_format": "%Y-%m-%d %H:%M:%S",
        "write_and_poll_sleep": 5,
        "has_time_window": False,
        "support_charge_freeze": False,
        "support_discharge_freeze": False,
        "has_idle_time": False,
        "can_span_midnight": True,
    },
}

# Control modes for Solax inverters
SOLAX_SOLIS_MODES = {
    "Selfuse - No Grid Charging": 1,
    "Timed Charge/Discharge - No Grid Charging": 3,
    "Backup/Reserve - No Grid Charging": 17,
    "Selfuse": 33,
    "Timed Charge/Discharge": 35,
    "Off-Grid Mode": 37,
    "Battery Awaken": 41,
    "Battery Awaken + Timed Charge/Discharge": 43,
    "Backup/Reserve - No Timed Charge/Discharge": 49,
    "Backup/Reserve": 51,
    "Feed-in priority - No Grid Charging": 64,
    "Feed-in priority - No Timed Charge/Discharge": 96,
    "Feed-in priority": 98,
}
# New modes are from 2024.03.2 controlled with solax_modbus_new in apps.yaml
SOLAX_SOLIS_MODES_NEW = {
    "Self-Use - No Grid Charging": 1,
    "Timed Charge/Discharge - No Grid Charging": 3,
    "Backup/Reserve - No Grid Charging": 17,
    "Self-Use - No Timed Charge/Discharge": 33,
    "Self-Use": 35,
    "Off-Grid Mode": 37,
    "Battery Awaken": 41,
    "Battery Awaken + Timed Charge/Discharge": 43,
    "Backup/Reserve - No Timed Charge/Discharge": 49,
    "Backup/Reserve": 51,
    "Feed-in priority - No Grid Charging": 64,
    "Feed-in priority - No Timed Charge/Discharge": 96,
    "Feed-in priority": 98,
}
