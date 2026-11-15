# Test Plan

## Functional tests
- ESP32-CAM connects to Wi-Fi
- camera snapshot available
- I2C soil sensor returns stable values
- moisture reading changes between dry and wet soil
- BME280 returns valid temperature and humidity
- float switch changes state correctly
- pump runs on manual command
- pump is blocked on low reservoir

## Integration tests
- dashboard shows all planter values
- Raspberry Pi receives planter telemetry
- remote access works over Tailscale
- watering events are logged
- image updates appear on dashboard

## Control tests
- dry threshold triggers watering
- wet threshold / hysteresis prevents chattering
- cooldown prevents repeated cycles
- max runtime safety limit works

## Reliability tests
- 24-hour node uptime test
- repeated Wi-Fi reconnect test
- repeated manual watering test
- soak test under normal operating cycle
