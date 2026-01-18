# BME69X and BSEC3.2.1.0 for Python

Bosch Sensortec released BSEC v3.2.1.0 in April 2025, and bme69x-python-library provides a Python 3.x wrapper for the binary library available from BoschSensortec.  This release supports multiple sensors, isolated configuration and state data. Support for TVOC data has been added but is only supported in LP mode.  

This Python wrapper for BSEC3 supports the BME690 sensor. The main use case for the Raspberry PI is with (1 or 2) single sensor BME690 modules, in one of two modes IAQ (Air Quality) or SEL (Selectivity - sniffing using an AI Studio model).

If you have a BME680 or BME688 please use the final release of BSEC2 Python wrapper for v2.6.1.0 which is stable and has 64bit and 32 bit support [here] (https://github.com/mcalisterkm/bme68x-python-library-bsec2.6.1.0).  

### Pre-requisites

The BME690 uses I2C which will need to be enabled on the target PI and can be enabled using raspi-config and its "Interface Options" menu.  i2c-tools (apt install i2c-tools) is a useful utility to validate the I2C port your sensor is working on (i2cdetect -y 1). This release supports changing the I2C bus used on the PI, and running multiple sensors (0x76 & 0x77 tested).

The Raspbian Bookworm Lite OS requires the python3 development package to be installed. (sudo apt install python3-dev)

### How to install the extension with BSEC
High level steps: 
- setup a Python virtual environment
- clone [this repo](https://github.com/mcalisterkm/bme69x-python-library-bsec3.2.1.0) to a desired location (virtual env) on your hard drive
- download the licensed BSEC3 library [from BOSCH](https://www.bosch-sensortec.com/software-tools/software/bme688-and-bme690-software/)<br>
- unzip it into the *bme69x-python-library-bsec3.2.1.0* folder, next to this *README.md* file
- open a new terminal window inside the *bme69x-python-library-bsec3.2.1.0* folder, and run the setup.py script.

Note: Only bsec_v3-2-1-0.zip is supported by this release.

Recent versions of Raspbian require local Python packages to be installed in a Python virtual environment (venv)
1) Let's review how to create a virtual env called `BME690'
````
# The first step is to create the virtual environment BSEC3 in your home directory (/home/<user>)
$ python -m venv --system-site-packages ./BSEC3
$ cd BSEC3
````
To invoke the virtual env
````
$ source ./bin/activate
(BSEC3)<user>:~/BSEC3 $ 
````

To exit a virtual env
````
(BSEC3)<user>:~/BSEC3 $ deactivate
$
````
To remove a virtual environment, first deactivate, then delete it (cd ~ ; rm -rf ./BSEC3)

2) Download Software

In the BSEC3 virtual env directory clone this repo or download the zip using the Github Green "<> Code" button . The  download is named bme69x-python-library-bsec3.2.1.0.zip, unzip it and your folder should look like this:

```
$cd ~
$cd BSEC3
$ source ./bin/activate
(BSEC3) <user>:~/BSEC3 $ 

## Unpack the zip file then cd into directory 

(BSEC3) <user>:~/BSEC3 $ cd bme69x-python-library-bsec3.2.1.0
(BSEC3) <user>:~/BSEC3 $ ls -l
-rw-r--r-- 1 kpi kpi  9563 Nov 30 19:18 API.md
drwxr-xr-x 4 kpi kpi  4096 Apr 13  2025 BME690_SensorAPI
-rw-r--r-- 1 kpi kpi  2933 Apr 13  2025 bme69xConstants.py
-rw-r--r-- 1 kpi kpi 85683 Nov 30 23:55 bme69xmodule.c
-rw-r--r-- 1 kpi kpi   571 Apr 13  2025 bsecConstants.py
-rw-r--r-- 1 kpi kpi  7835 Nov 30 08:32 Documentation.md
drwxr-xr-x 4 kpi kpi  4096 Nov 30 23:57 examples
-rw-r--r-- 1 kpi kpi 17625 Nov 30 23:55 internal_functions.c
-rw-r--r-- 1 kpi kpi  2490 Nov 30 23:54 internal_functions.h
-rw-r--r-- 1 kpi kpi  1065 Apr 13  2025 LICENSE
-rw-r--r-- 1 kpi kpi 10249 Aug 12 15:41 README.md
-rw-r--r-- 1 kpi kpi  3422 Nov 30 22:41 setup.py
drwxr-xr-x 3 kpi kpi  4096 Apr 13  2025 tools

```

3) BSEC3 Library

The BSEC3 Library is unzipped into the BSEC3/bme69x-python-library-bsec3.2.1.0 directory which is where you are from the previous step and it should look like this:
`````
$ ls -l
total 232
-rw-r--r-- 1 kpi kpi  9563 Nov 30 19:18 API.md
drwxr-xr-x 4 kpi kpi  4096 Apr 13  2025 BME690_SensorAPI
-rw-r--r-- 1 kpi kpi  2933 Apr 13  2025 bme69xConstants.py
-rw-r--r-- 1 kpi kpi 85683 Nov 30 23:55 bme69xmodule.c
-rw-r--r-- 1 kpi kpi   571 Apr 13  2025 bsecConstants.py
drwxr-xr-x 5 kpi kpi  4096 Nov 30 19:11 bsec_v3-2-1-0
-rw-r--r-- 1 kpi kpi  7835 Nov 30 08:32 Documentation.md
drwxr-xr-x 4 kpi kpi  4096 Nov 30 23:57 examples
..........
`````

4) Build
Your present working directory ($ pwd) should be /home/<user>/BSEC3/bme69x-python-library-bsec3.2.1.0 
Make sure your Python virtual env is still enabled, and now we build & install the module in this venv.
````agsl

$ cd /home/<user>/BME690
$ source /home/<user>/BME690/bin/activate
$(BME690) 
````

a. For 32 bit PI3 or above (Inc PI Zero 2)
```bash
$(BME690) BSEC3=32; export BSEC3; python3 setup.py install
```
b. For PI5 running Raspbian 64 bit
```bash
$(BME690) BSEC3=64;export BSEC3; python3 setup.py install
```
c. For PI Zero and early Arm V6 PI's, no environment variable is set
```bash
$(BME690) python3 setup.py install
```
Note: For scripts (cron, bash etc) to run a virtual environment python3 all you have to do is use the full path: /home/<user_name>/BME690/bin/python3 

### How to use the extension
- to import in Python
```python
import bme69x
```
or as a Class
```python
from bme69x import BME69X
```
- see Documentation.md for a quick overview and API.md as a reference
- to test the installation make sure you connected your BME690 sensor via I2C
- run the following code in a Python3 interpreter
```python
from bme69x import BME69X

# Replace I2C_ADDR with the I2C address of your sensor
# Typically  I2C is  0x76  or 0x77  (Pimoroni BME690 module requires a link to be cut for 0x77)
bme69x = BME69X(I2C_ADDR,1, 0)
bme69x.set_heatr_conf(1, 320, 100, 1)
data = bme69x.get_data()
```

The examples folder has useful programs, include burning in a sensor, using ultra low power mode, using multiple sensor modules, and  saving and loading config and state data for a sensor. 
The tools folder provide a sample AI Model, data and code to use with a BME690 sensor to classify smells. Collecting data is best done with the BME690  8 sensor BOSCH Sensortec DevKit


### A walk through a 32bit PI4 installation follows.
```
$ sudu apt install i2c-tools
$ i2cdetect -y 1
0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- 77 
```
The BME690 module is showing up on port 0x77.
If it fails to show up check connections and the module documentation. 

Install "Python3-dev" package (If you miss this step you may see a Python.h missing error)
```
$ sudo apt install python3-dev
```

As I am using Raspbian bookworm a virtual environment is required.
```
$ python -m venv --system-site-packages BSEC3
$ cd BSEC3
$ source bin/activate
<user>:~/BSEC3 $
```
Next clone this repo into the virtual environment 
```
(690)<user>:~/BSEC3 $ ls -l
total 20
drwxr-xr-x  2 kpi kpi 4096 Jun 23 23:22 bin
drwxr-xr-x 11 kpi kpi 4096 Jun 23 23:32 bme69x-python-library-bsec3.2.1.0
drwxr-xr-x  3 kpi kpi 4096 Jun 23 23:22 include
drwxr-xr-x  3 kpi kpi 4096 Jun 23 23:22 lib
-rw-r--r--  1 kpi kpi  173 Jun 23 23:22 pyvenv.cfg
```

Now copy the BoschSensortech bsec_v3-2-1-0 into the bmx69x repo clone. 
It should look like this.

```
$ ls -l
-rw-r--r-- 1 kpi kpi  9563 Nov 30 19:18 API.md
drwxr-xr-x 4 kpi kpi  4096 Apr 13  2025 BME690_SensorAPI
-rw-r--r-- 1 kpi kpi  2933 Apr 13  2025 bme69xConstants.py
-rw-r--r-- 1 kpi kpi 85683 Nov 30 23:55 bme69xmodule.c
-rw-r--r-- 1 kpi kpi   571 Apr 13  2025 bsecConstants.py
drwxr-xr-x 5 kpi kpi  4096 Nov 30 19:11 bsec_v3-2-1-0
drwxr-xr-x 5 kpi kpi  4096 Jul  6 18:17 build
-rw-r--r-- 1 kpi kpi  7835 Nov 30 08:32 Documentation.md
drwxr-xr-x 4 kpi kpi  4096 Nov 30 23:57 examples
-rw-r--r-- 1 kpi kpi 17625 Nov 30 23:55 internal_functions.c
-rw-r--r-- 1 kpi kpi  2490 Nov 30 23:54 internal_functions.h
-rw-r--r-- 1 kpi kpi  1065 Apr 13  2025 LICENSE
-rw-r--r-- 1 kpi kpi 10249 Aug 12 15:41 README.md
-rw-r--r-- 1 kpi kpi  3422 Nov 30 22:41 setup.py

```
From here run the installer with the 32bit env set for my Pi 4 board and 32 bit raspbian.

```
(BSEC3) <user>:~/ $ BSEC3=32; export BSEC3; python3 setup.py install
```

There are a bunch of warnings about unused variables, and it should complete with the last few lines looking like this:
```
Installed /home/<user>/BSEC3/lib/python3.11/site-packages/bme69x-3.2.1-py3.11-linux-aarch64.egg
Processing dependencies for bme69x==3.2.1
Finished processing dependencies for bme69x==3.2.1
```

Change to the examples directory and run the forced mode example:
```
(BME690x) <user>:~/BME690x/bme69x-python-library-bsec3.2.1.0/examples $ ls
airquality.py  build       conf            force_ulp.py          parallel_mode.py      read_conf.py
bme_ptrs.log   burn_in.py  forced_mode.py  multi_sensor_test.py  parallel_mode_ulp.py  README.md
(BME690x) kpi@dev2:~/BME690x/bme69x-python-library-bsec3.2.1.0/examples $ python3 forced_mode.py
TESTING FORCED MODE WITHOUT BSEC
{'sample_nr': 1, 'timestamp': 3956208, 'raw_temperature': 54.29930877685547, 'raw_pressure': 931.8998413085938, 'raw_humidity': 108.98556518554688, 'raw_gas': 109.448486328125, 'status': 160}

TESTING FORCED MODE WITH BSEC
{'sample_nr': 1, 'timestamp': 626732524746608, 'iaq': 50.0, 'iaq_accuracy': 0, 'static_iaq': 50.0, 'static_iaq_accuracy': 0, 'co2_equivalent': 500.0, 'co2_accuracy': 0, 'breath_voc_equivalent': 0.49999991059303284, 'breath_voc_accuracy': 0, 'raw_temperature': 20.232421875, 'raw_pressure': 100879.46875, 'raw_humidity': 44.31648254394531, 'raw_gas': 25241.5703125, 'stabilization_status': 128, 'run_in_status': 144, 'temperature': 15.232421875, 'humidity': 60.71345901489258, 'gas_percentage': 0.0, 'gas_percentage_accuracy': 0}
```
As the status and accuracy are all zero it is time to burn in this sensor for 24 hours. 


The original PI3G repository is available [here] (https://github.com/pi3g/bme68x-python-library) which works with BSEC 2.0.6.1/BME68x (32bit) from 2022.
