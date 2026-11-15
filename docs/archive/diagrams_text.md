# Text Diagrams

## System block diagram
Phone/Laptop -> Tailscale -> Raspberry Pi -> local Wi-Fi -> ESP32-CAM Planter Node 1

## Planter node wiring block
ESP32-CAM
- I2C -> soil moisture sensor
- I2C -> BME280
- GPIO input -> float switch
- GPIO output -> MOSFET gate -> mini submersible pump
- camera -> planter image

## Fluidic block
Reservoir -> mini submersible pump -> tube -> planter soil
