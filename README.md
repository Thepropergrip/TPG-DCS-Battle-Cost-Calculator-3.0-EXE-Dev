# TPG Battle Cost Counter — Windows Overlay

This project adds a live Windows desktop overlay (EXE) for:

`TPG_Battle_Cost_Calculator_V2.0 BETA.lua`

The overlay mirrors **exactly what the script displays on-screen when expanded**, and nothing more.

It runs as a movable, draggable Windows window, suitable for a second monitor.

---

# Architecture Overview

```
DCS Mission Script (Lua)
        ↓
UDP (preferred) OR JSON file fallback
        ↓
TPGOverlay.exe (WPF, .NET 8)
        ↓
Second Monitor Live Display
```

The EXE does NOT change DCS behavior.  
It only displays the existing cost data externally.

---

# What Gets Displayed (No Extras)

The Windows overlay replicates:

• Header:
  - `TPG BATTLE COST COUNTER`

• `ECONOMIC BALANCE OF FIRE`
  - RED bar (percent + total cost)
  - BLUE bar (percent + total cost)

• BLUE COALITION panel:
  - FIRED lines
  - DMG lines
  - LOSS lines

• RED COALITION panel:
  - FIRED lines
  - DMG lines
  - LOSS lines

• `WAR TOTAL`

• Optional Health List (if enabled in Lua)

No added analytics.  
No trend graphs.  
No new metrics.

---

# Setup Instructions

---

## 1️⃣ Build the Windows EXE

### Requirements

- Windows 10 or 11
- .NET 8 SDK  
  https://dotnet.microsoft.com/download

---

### Build

From repo root:

```bash
dotnet restore
dotnet build -c Release
```

---

### Publish Single-File EXE

```bash
dotnet publish -c Release -r win-x64 /p:PublishSingleFile=true /p:SelfContained=true
```

The EXE will be located in:

```
/src/TPGOverlay/bin/Release/net8.0-windows/win-x64/publish/
```

Move `TPGOverlay.exe` anywhere you like.

---

## 2️⃣ Enable Data Export in DCS

You have two communication options:

---

# OPTION A — UDP (Preferred)

### Why UDP?

- Near real-time (0.5–1s updates)
- No file polling
- Lightweight
- Clean architecture

---

### Step 1 — Allow LuaSocket (If Needed)

Open:

```
Saved Games\DCS\Scripts\MissionScripting.lua
```

Ensure these lines are commented out:

```lua
-- sanitizeModule('socket')
-- sanitizeModule('lfs')
```

If they are active, comment them so socket is allowed.

---

### Step 2 — UDP Settings

The exporter sends JSON to:

```
127.0.0.1:7777
```

The Windows EXE listens automatically on launch.

---

### Step 3 — Launch Order

1. Start `TPGOverlay.exe`
2. Start DCS mission
3. Data should appear within 1 second

---

# OPTION B — File Fallback (If UDP Blocked)

If UDP does not work:

The Lua script writes:

```
Saved Games\DCS\Logs\tpg_battle_cost_latest.json
```

The EXE automatically switches to file-watch mode if:

- No UDP packets are received within 3 seconds

Polling interval:
- 500–1000ms

---

# Window Behavior

The overlay window:

- Draggable by clicking anywhere
- Resizable
- Remembers last position/size
- Safe to move to second monitor
- Does not steal DCS focus
- Can be minimized independently

---

# Data Schema (Used by Overlay)

Preferred payload format:

```json
{
  "version": "2.0",
  "timestamp": 1712334823,
  "currency": {
    "code": "USD",
    "symbol": "$"
  },
  "balance": {
    "redCost": 81070000,
    "blueCost": 57320000,
    "warTotal": 138390000,
    "redPctTotal": 0.586,
    "bluePctTotal": 0.414
  },
  "coalitions": {
    "blue": {
      "fired": [],
      "dmg": [],
      "loss": []
    },
    "red": {
      "fired": [],
      "dmg": [],
      "loss": []
    }
  },
  "healthList": {
    "enabled": true,
    "lines": []
  }
}
```

If structured JSON is not used, raw `reportText` is accepted and parsed.

---

# Troubleshooting

## No Data Showing

- Confirm mission script is enabled:
  - `WeaponTracker.ui.scriptEnabled = true`
  - `WeaponTracker.ui.displayEnabled = true`
- Confirm firewall is not blocking localhost UDP
- Confirm port 7777 is not in use
- Confirm MissionScripting.lua allows socket

---

## Overlay Not Updating

- Check `Saved Games\DCS\Logs\dcs.log`
- Verify export interval is not disabled
- Confirm healthList toggle does not suppress output

---

# Performance Impact

- UDP export every 1 second
- Minimal CPU load
- No measurable FPS impact in DCS

---

# Project Structure

```
/src/TPGOverlay/
    TPGOverlay.sln
    TPGOverlay.csproj
    MainWindow.xaml
    UdpListener.cs
    FileWatcher.cs
    Models/
    Services/

/lua/
    tpg_export.lua
```

---

# Non-Goals

The following are intentionally excluded:

- Fuel burn tracking
- Economic sustainability gauges
- Cost per minute
- Trend graphs
- Historical tracking

This overlay mirrors the current DCS script only.

---

# License

Internal / Mission Use Only  
TPG Project
