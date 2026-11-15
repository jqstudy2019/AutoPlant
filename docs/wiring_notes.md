# Wiring Notes

## Planter Module 1

### ESP32-CAM responsibilities
- Wi-Fi communication
- camera snapshots
- reading I2C soil sensor
- reading BME280 over I2C
- reading float switch digital state
- controlling pump MOSFET output

### Connected devices
- I2C capacitive soil moisture sensor
- BME280
- float switch
- MOSFET pump driver
- 12V mini submersible pump

## Power architecture
- 12V rail for mini pump
- regulated 5V supply for ESP32-CAM board input as required
- shared ground between pump supply, ESP32-CAM, and sensors

## Safety notes
- never drive pump directly from ESP32-CAM GPIO
- use a MOSFET or driver stage
- include flyback diode across pump
- place float switch so low-water state triggers before dry-run

## I2C notes
- soil sensor and BME280 share the same I2C bus
- verify sensor addresses before final wiring
- keep the bus at the correct logic voltage for the ESP32-CAM
