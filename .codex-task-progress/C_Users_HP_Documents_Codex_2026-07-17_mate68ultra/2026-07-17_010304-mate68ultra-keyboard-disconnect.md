# Mate68 Ultra+ keyboard disconnect diagnosis

- Objective: Diagnose the sudden keyboard connection failure and garbled-input risk using read-only Windows evidence while the keyboard remains unplugged.
- Safety boundary: Do not reconnect, enable, restart, uninstall, or modify the keyboard/device without explicit user approval.
- Evidence: Incident reproduced after reconnect; keyboard opened applications and emitted an unsolicited `W` plus shortcut-like input. Windows identified the device as `HID\\VID_0416&PID_0110` with keyboard collections Col01 and Col05. No HID problem-state device or relevant driver failure was found.
- Timeline decision: Kernel-Power unexpected shutdown at 00:56 was explained by the user's forced restart, not an independent crash.
- Safety actions: User unplugged the keyboard. A disconnected-device disable attempt was rejected by Windows because the device was not connected; no device state changed. Newly opened PotPlayer was closed.
- Recovery evidence: Installed MelGeek Hive desktop version is 1.6.0 at `D:\\Program Files\\MelGeek Hive`. Official MADE68 Ultra manual warns to keep magnetic objects such as speakers/headphones at least 30 cm away. Official forum ties calibration state to severe automatic key triggering and recommends factory reset plus normal-force recalibration.
- Current status: Keyboard remains unplugged and safe. Awaiting confirmation that magnetic objects have been cleared from the desk.
- Next action: With magnetic sources removed, reconnect under supervision, restore factory defaults in HIVE, recalibrate using normal typing force, then verify in a safe text surface. If random input persists, isolate cable/USB port and hardware/PCB fault.
