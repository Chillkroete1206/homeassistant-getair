# Getair Sensors

Custom integration for Home Assistant to monitor and control **Getair** ventilation systems via HTTP API.

---

## 📦 Features

- Support for multiple **zones** (e.g., "Erdgeschoss", "Obergeschoss", "Dachgeschoss")
- Sensor entities per zone:
  - Speed (fan level)
  - Temperature
  - Humidity
- Automatic login & token refresh
- UI-based configuration (no YAML required)
- Configurable update interval

---

## 🛠️ Installation (via HACS)

1. Go to **HACS → Integrations → ⋮ → Custom repositories**
2. Add this repository URL: https://github.com/Chillkroete1206/getair_sensors
3. Select repository type: **Integration**
4. After adding, search for `Getair Sensors` in HACS and install it
5. Restart Home Assistant
6. Go to **Settings → Devices & Services → Integrations → Add Integration**
7. Search for `Getair Sensors` and follow the setup instructions

---

## ⚙️ Configuration

After installation, configure the integration via the Home Assistant UI:

- Required fields:
- `username`: Your GetAir login (email)
- `password`: Your GetAir password

---

## 🧪 Example Entities Created

For each active zone (e.g. "1 - Erdgeschoss"):

- `sensor.getair_speed_1_erdgeschoss`
- `sensor.getair_temperature_1_erdgeschoss`
- `sensor.getair_humidity_1_erdgeschoss`

---

## 🔒 Security Notice

- No credentials are stored in YAML.
- Tokens and login data are handled securely using Home Assistant's built-in secrets management.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author & Codeowners

- GitHub: [@Chillkroete1206](https://github.com/Chillkroete1206)

---

## 📚 Documentation

More information available in the `custom_components/getair_sensors/` source directory.

---

## 🧩 HACS Compatibility

This repository is [HACS](https://hacs.xyz/) compatible. Make sure the following file exists in the root:
- `hacs.json`

