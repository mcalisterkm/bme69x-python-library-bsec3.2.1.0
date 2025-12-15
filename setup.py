from setuptools import setup, Extension, find_packages
from pathlib import Path
import os

# This expects an environment variable to be set to select the BSEC2 library
# If it is not set a 32bit ArmV6 build is carried out. 
# For 64 bit PI4 or PI5  
# BSEC3=64;export BSEC3; python setup.py install
# For 32 bit PI3 or above (Inc PI Zero 2)
# BSEC3=32; export BSEC3; python setup.py install
# For PI Zero and early Arm V6 PI's
# python setup.py install
# Configs for bme680, bme688 and bme690 are included in BSEC: the 690 33v_3s_4d config is selected by default.

BSEC3=os.environ.get("BSEC3", None)
# Three PI Architectures are supported by BSEC2.6: PiThree_ArmV6 32 bit,  PiThree_ArmV8 32 bit,  PiFour_ArmV8 64 bit (also works for PI5) 

if BSEC3 == '64':
    algo = 'bsec_v3-2-1-0/algo/bsec_IAQ_Sel/bin/RaspberryPi/PiFour_Armv8'
    # 64 bit Raspbian OS - PI 4 and PI5, ARM V8A, ARM V8.2-A  Must be 64 bit OS
elif BSEC3 == '32':
    algo = 'bsec_v3-2-1-0/algo/bsec_IAQ_Sel/bin/RaspberryPi/PiThree_ArmV8'
    # 32bit Raspbian OS - PI 5 / 4 / 3 /  Zero 2, ARM V8A  Must be 32bit  OS
else:
    algo = 'bsec_v3-2-1-0/bsec_IAQ_Sel/bin/RaspberryPi/PiThree_ArmV6'
    # 32bit Raspbian OS - Pi Zero, Arm V6 Must be 32 bit OS

BSEC = True

if BSEC:
    ext_comp_args = ['-D BSEC ' '-fPIC ' '-g']
    libs = ['pthread', 'm', 'rt', 'algobsec']
    lib_dirs = ['/usr/local/lib',
                algo ]
else:
    ext_comp_args = []
    libs = ['pthread', 'm', 'rt']
    lib_dirs = ['/usr/local/lib']

LIBDIR = Path(__file__).parent

README = (LIBDIR / "README.md").read_text()

include_dirs=['/usr/local/include', 'bsec_v3-2-1-0/algo/bsec_IAQ_Sel/inc']
bme69x = Extension('bme69x',
                   extra_compile_args=ext_comp_args,
                   include_dirs=include_dirs,
                   libraries=libs,
                   library_dirs=lib_dirs,
                   depends=['BME690_SensorAPI/bme69x.h', 'BME690_SensorAPI/bme69x.c',
                            'BME690_SensorAPI/bme69x_defs.h', 'internal_functions.h', 'internal_functions.c'],
                   sources=['bme69xmodule.c', 'BME690_SensorAPI/bme69x.c', 'internal_functions.c'])

setup(name='bme69x',
      version='3.2.1',
      description='pi3g Python interface for BME69X sensor and BSEC',
      long_description=README,
      long_description_content_type='text/markdown',
      url='https://github.com/mcalisterkm/bme68x-python-library-bsec3.2.1.0',
      author='Multiple',
      author_email='',
      license='MIT',
      classifiers=[
           'Development Status :: 4 - Alpha§',
           'Intended Audience :: Developers',
           'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: Implementation :: CPython',
          'Topic :: Scientific/Engineering :: Atmospheric Science',
      ],
      keywords='bme69x bme690 bme680 bme688 BME69X BME68X BME690 BME680 BME688 bsec BSEC Bosch Sensortec environment sensor',
      packages=find_packages(),
      py_modules=['bme69xConstants', 'bsecConstants'],
      package_data={
          'bme69x': [
               'bsec_v3-2-1-0/algo/bsec_IAQ_Sel/config/bme690/bme690_sel_33v_3s_4d/bsec_selectivity.config',
          ]
      },
      headers=['BME690_SensorAPI/bme69x.h',
               'BME690_SensorAPI/bme69x_defs.h', 'internal_functions.h'],
      ext_modules=[bme69x])
