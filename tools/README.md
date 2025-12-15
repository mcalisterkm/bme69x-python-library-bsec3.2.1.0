Tools
=====

- Sniff.py
This is an example of using an exported AI Model on a single sensor module.
The output is the model predictions for each of two classes in the model.
- 690-tools.bmeproject
This is the data and model saved from BME AI Studio using Coffe Beans, Air, and Chocolate data recorded on a 8x BME690 Sensor. There are algorithms for Air-Coffe, Air-Coffee-Chocolate, and Air-Coffee-Chocolate with more Chocolate data added as it was a little light first time round. 

Sniff.py is using the Air-Coffee model (2 classes), and you may like to extend it to all three classes  (Air Coffee Chocolate), by changing the paths and subscribing to the three classes. Note the heater profile used to collect data is HP324 which has a heater cycle of ~27 sec, so some sleeps are required to avoid timing errors. Using the standard heater profile  HP354 at 10.7 sec cycle time would not need to sleep so much. A lot of sleep time means very little power is used, as it is the heater element that uses it, but it's a balance that requires a little experimentation.

The 690-tools.bmeproject is a complete project with all data, it can be opened in BME AI Studio and you can make changes and re-train. What AI Studio will not do is export a model for a BME 688 using this data collected using the 690 8x devkit.
