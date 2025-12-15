# BME69X Python Library — API Reference

This file is a concise, developer-focused API reference for the `bme69x` Python wrapper. It documents the primary constructor, public methods, expected arguments and return values, important notes (state/config files, heater durations, sample rates), and small usage examples.

If you want a guided Quick Start, see `Documentation.md`.

---

## Table of contents

- Constructor
- Basic usage example
- Core methods
  - I/O and lifecycle
  - Heater / measurement configuration
  - BSEC state and config management
  - Data retrieval
  - Subscription and advanced functions
- Constants and recommended values
- Examples
- Notes & troubleshooting

---

## Constructor

```python
from bme69x import BME69X

sensor = BME69X(
    i2c_addr,            # Required: 0x76 or 0x77
    i2c_bus=1,           # Optional: I2C bus number (default: 1 -> /dev/i2c-1)
    debug_mode=0,        # Optional: 0 (off) or 1 (on)
    sensor_name=None     # Optional: string used for config/state filenames
)
```

- Returns: a `BME69X` instance
- Behavior:
  - Allocates a per-sensor BSEC instance on the heap (avoids corrupting wrapper memory).
  - Opens the specified I2C bus and creates an I2C file descriptor for the instance.
  - If `sensor_name` omitted a default id such as `sensor_0x77` is generated.

---

## Basic usage example

```python
from time import sleep
from bme69x import BME69X
import bme69xConstants as cnst
import bsecConstants as bsec

sensor = BME69X(i2c_addr=0x76, sensor_name='sensor_0x76')
sensor.load_bsec_conf()
sensor.load_bsec_state()
# For FORCED_MODE pass scalar temperature and duration (uint16_t each):
sensor.set_heatr_conf(cnst.BME69X_ENABLE, 320, 5, cnst.BME69X_FORCED_MODE)
sensor.set_sample_rate(bsec.BSEC_SAMPLE_RATE_LP)

sleep(1)
data = sensor.get_bsec_data()
print(data)
```

---

## Core methods

The list below shows the primary public methods exposed on the `BME69X` instance.

### I/O and lifecycle

- `get_chip_id()` -> int
  - Returns the numeric chip ID (e.g. `0x61`) or raises an exception on error.

- `get_variant()` -> str
  - Returns a short string identifying the sensor variant (e.g., `BME690`).

- `close_i2c()` -> int
  - Closes the instance I2C fd. Returns `0` on success, `< 0` on error.

- `open_i2c(i2c_addr: int)` -> int
  - Re-open I2C connection to `i2c_addr`. Returns `0` on success or raises on error.

### Debug helpers

- `enable_debug_mode()` / `disable_debug_mode()`
  - Toggle the C-extension's debug prints (useful for troubleshooting). These set `debug_mode` internally.

- `print_dur_prof()`
  - Print the current duration profile array to the console (TTY).

### Heater and measurement configuration

- `set_heatr_conf(enable: int, temperature_profile: int|list[int], duration_profile: int|list[int], operation_mode: int)` -> int
  - Configure the heater. Behavior depends on `operation_mode`:
    - FORCED_MODE: pass scalar `temperature_profile` and `duration_profile` (each `uint16_t`). Example: `320, 5`.
    - PARALLEL_MODE or SEQUENTIAL_MODE: pass `temperature_profile` and `duration_profile` as Python lists of equal length (1..10). Example: `[320, 100]` and `[5, 2]`.
  - `duration_profile` units are 140 ms per unit. Example: `[5,2,10,30,5,5,5,5,5,5]` → sum=77 units → 77*140ms ≈ 10.78 s total heat time.
  - `operation_mode` is one of `cnst.BME69X_FORCED_MODE`, `cnst.BME69X_PARALLEL_MODE`, or `cnst.BME69X_SEQUENTIAL_MODE`.
  - The function will set the instance's internal `op_mode` to the provided `operation_mode` (it is the 4th argument).
  - Returns `0` on success, non-zero on failure.

- `set_sample_rate(rate: float)`
  - Sets the sampling rate for virtual sensors via BSEC. Use constants in `bsecConstants`.
  - Examples: `bsec.BSEC_SAMPLE_RATE_ULP`, `bsec.BSEC_SAMPLE_RATE_LP`, `bsec.BSEC_SAMPLE_RATE_CONT`.

### Data retrieval

- `get_data()` -> (BME690_API measurement)
  - Read physical sensor outputs (temperature, pressure, humidity, gas resistance). Useful for raw data reads.
  - Returns: sample number, timestamp (ms), temperature (°C), pressure (Pa), humidity (%rH), gas resistance (kΩ), status.

- `get_bsec_data()` -> dict | None
  - Read processed results from BSEC including IAQ and virtual sensor values.
  - Returns a dict with keys such as `sample_nr`, `timestamp`, `iaq`, `iaq_accuracy`, `temperature`, `raw_temperature`, `humidity`, `raw_humidity`, `raw_gas`, `static_iaq`, `co2_equivalent`, `breath_voc_equivalent`, `comp_gas_value`, etc.
  - May return `None` (or empty) if no new BSEC-processed output is available (sensor not ready / polled too frequently).

Example `get_bsec_data()` return snippet (keys you can expect):

```
{
  'sample_nr': 123,
  'timestamp': 1590000000000000000,  # ns
  'iaq': 50.0,
  'iaq_accuracy': 3,
  'temperature': 24.12,
  'raw_temperature': 24.2,
  'humidity': 45.3,
  'raw_humidity': 45.6,
  'raw_gas': 1200.0,
  'static_iaq': 48.5,
  'co2_equivalent': 420.0,
  'breath_voc_equivalent': 0.5,
  'comp_gas_value': -0.123
}
```

### BSEC state and config management

To support per-sensor calibration and persistent state, the library exposes helpers that write/read sensor-specific files. Filenames include the `sensor_id` and live under the `conf/` directory by convention.

- `load_bsec_conf()`
  - Loads the BSEC configuration from `conf/bsec_config_{sensor_id}.txt` into the BSEC instance.

- `save_bsec_conf()`
  - Retrieves the current BSEC config and writes to `conf/bsec_config_{sensor_id}.txt`.

- `load_bsec_state()`
  - Loads saved BSEC state from `conf/state_data_{sensor_id}.txt` and applies it to the instance.

- `save_bsec_state()`
  - Retrieves BSEC state and writes it to `conf/state_data_{sensor_id}.txt`.

Helper accessors:

- `get_bsec_conf()` -> list[int]
- `get_bsec_state()` -> list[int]
- `set_bsec_state(state_list: list[int])` -> int
- `set_bsec_conf(conf_list: list[int])` -> int

Notes:

- `get_bsec_state()` commonly returns an array of ~197 integers for BSEC v3 state; config arrays can be much larger (e.g., ~2277 ints) depending on the AI Studio export.
- the exported .config, .c and .h, files have the same data (it's packed bytes in the .config not readily readable), and it is possible to copy the array of integers from the .c file into a python array of ints.  When writing the array to disk in Python you may end up with a textual list; use the parsing snippet in `Documentation.md` or the example below to read/restore it.

Parsing example (restore from text file):

```python
with open(state_path, 'r') as f:
    s = f.read().strip()
ints = [int(x) for x in s.strip()[1:-1].split(',') if x.strip()]
sensor.set_bsec_state(ints)
```

### Subscription and advanced functions

- `subscribe_gas_estimates(count: int)`
  - Subscribe to a number (0-4) of BSEC gas estimates (gas estimate outputs).

- `subscribe_ai_classes()`
  - Subscribe to AI classes if BSEC config includes trained classes.

- `update_bsec_subscription(requests: list[tuple])` -> result
  - Update virtual sensor subscription. Pass list of `(sensor_id, sample_rate)` tuples.

- `get_bsec_version()` -> str
  - Returns a string identifying the BSEC library version (e.g., `3.2.0.0`).

---

As the Raspberry PI uses a standard Linux system running two or more sensors with BSEC2 meant running seperate .py programs (simple solution) With BSEC3 and supporting multiple sensors it is now possible to run one AI scan to broadly classify a sample and then based on that result load a second sensor with a more specific model to identify within the general class. For example the broad classification model on the first snesor may include 'fruit', and using that result a specific fruit model could be loaded on the second sensor to look at freshness. This can all be done in one python application.

## Constants and recommended values

- Heater durations: unit = 140 ms per unit for the `duration_profile` lists. So a heater profile of 5,5,10 totals 20 units multiplied by 140ms gives 2.8sec
- Sample rate constants: see `bsecConstants.py` for available options. Typical values:
  - `BSEC_SAMPLE_RATE_ULP` — very low power (period ~300s)
  - `BSEC_SAMPLE_RATE_LP`  — low power (period ~3s)
  - `BSEC_SAMPLE_RATE_CONT` — continuous (faster)

Recommended tuning tips:

- The effective cycle time depends on the heater profile sum (units × 140 ms) plus BSEC processing latency. For typical heater profiles you may need to sleep multiple seconds between polling. Become familiar with Duty Cycle and Heater Profiles in AI Studio.
- If `get_bsec_data()` returns `None` frequently, increase sleep to align with the heater cycle time. e.g. ULP is 300 sec +- a small window. A sleep of 298sec works well.
---

## Examples


1) Minimal single-sensor forced-mode read

```python
from time import sleep
from bme69x import BME69X
import bme69xConstants as cnst
import bsecConstants as bsec

sensor = BME69X(0x76, sensor_name='sensor_76')
sensor.load_bsec_state()
# FORCED_MODE: scalar temperature 320 C and duration 5 x 140ms = 700ms cycle
sensor.set_heatr_conf(cnst.BME69X_ENABLE, 320, 5, cnst.BME69X_FORCED_MODE)
sensor.set_sample_rate(bsec.BSEC_SAMPLE_RATE_LP)
# sleep for 1 cycle
sleep(0.7)
# This is what starts the heater cycle
print(sensor.get_bsec_data())
```

2) Template: per-sensor collector (run by cron/systemd)

```python
#!/usr/bin/env python3
from time import sleep
from bme69x import BME69X
import bme69xConstants as cnst
import bsecConstants as bsec

sensor = BME69X(0x76, sensor_name='sensor_76')
sensor.load_bsec_conf()
sensor.load_bsec_state()
temp_prof=[320,100]
dur_prof=[5,2]
sensor.set_heatr_conf(cnst.BME69X_ENABLE, temp_prof, dur_prof, cnst.BME69X_PARALLEL_MODE)
sensor.set_sample_rate(bsec.BSEC_SAMPLE_RATE_LP)

sleep(2)
data = sensor.get_bsec_data()
if data:
    print(data)
else:
    print('null')
```

Schedule with cron/systemd for independent duty cycles per sensor.

---

## Notes & troubleshooting

- If you get a bus error or SIGBUS: ensure your extension was built for the correct architecture and BSEC binary is the right variant. The wrapper allocates a separate heap-based BSEC instance to avoid function pointer corruption.
- If `get_bsec_data()` often returns `None` or you see -16 (timing error) returned from functions, the typical causes are:
  - Polling faster than the device/BSEC can produce processed output
  - Heater profile with a long duty cycle and BSEC sample rate mismatches
  - Incorrect sample-rate subscription for BSEC virtual sensors

