# Bill of Materials

## Current single-planter prototype
| Item | Qty | Estimated Cost (USD) | Notes |
|---|---:|---:|---|
| Raspberry Pi 4 or 5 | 1 | 60-90 | Supervisor node |
| microSD / storage | 1 | 10-20 | Pi storage |
| ESP32-CAM | 1 | 8-15 | Planter edge node |
| I2C capacitive soil moisture sensor | 1 | 8-20 | Moisture sensing |
| BME280 module | 1 | 5-12 | Temp/humidity |
| Side-mount float switch | 1 | 5-12 | Low-water cutoff |
| 12V mini submersible pump | 1 | 8-18 | Cheap small pump |
| MOSFET / driver components | 1 | 3-10 | Pump switching |
| Flyback diode | 1-2 | 1-3 | Pump protection |
| 12V power supply | 1 | 10-20 | Pump rail |
| Buck converter (12V to 5V) | 1 | 5-10 | Logic supply if used |
| Tubing | 1 set | 5-15 | Water path |
| Reservoir | 1 | 5-20 | Water storage |
| Breadboard / perfboard | 1 | 5-15 | Prototyping |
| Jumper wires / connectors | 1 set | 5-15 | Interconnect |
| Enclosure / printed mounts | 1 set | 5-20 | Mechanical packaging |

## Future per-planter expansion
For each additional planter module:
- 1 ESP32-CAM
- 1 I2C soil sensor
- 1 BME280 or shared environment plan
- 1 float-switch strategy
- 1 mini submersible pump
- 1 driver stage
- 1 tube branch
