# AGENTS.md — Codex Execution Rules (DCS Lua → Windows Overlay EXE)

You are operating inside a DCS World mission scripting repository.

Primary Lua file:
`TPG_Battle_Cost_Calculator_V2.0 BETA.lua`

Your mission is to generate and maintain a Windows desktop EXE overlay that mirrors exactly what the Lua script displays on screen when expanded.

You are NOT allowed to invent new analytics or redesign the data model.

---

# CORE OBJECTIVE

Create:

1) A Windows desktop application (WPF, .NET 8 preferred)
2) A single-file EXE build target
3) Live or near-live data updates from DCS
4) A movable, draggable, resizable window
5) Display ONLY what `WeaponTracker.buildReport()` outputs when expanded

No extra metrics.
No additional UI panels.
No new calculations.

Mirror the script exactly.

---

# WHAT MUST BE DISPLAYED

The EXE must replicate this structure:

## 1. Header
```
--- TPG BATTLE COST COUNTER ---
```

## 2. Economic Balance Section
```
=== ECONOMIC BALANCE OF FIRE ===
RED  |██████░░░░| XX.X% $#,###,###
BLUE |██████░░░░| XX.X% $#,###,###
```

Render these as:

- Two horizontal bars (RED and BLUE)
- Percent text
- Formatted currency
- Correct proportion relative to WAR TOTAL

---

## 3. Expanded Coalition Sections (BLUE FIRST)

### BLUE COALITION
- FIRED lines
- DMG lines
- LOSS lines

### RED COALITION
- FIRED lines
- DMG lines
- LOSS lines

Each line contains:

Label: FIRED / DMG / LOSS  
Item name (weapon or typeName)  
Count  
Currency symbol + formatted total  
Percentage of coalition total  

Ordering rules:
- FIRED: stable sort by total cost descending
- DMG: cost descending
- LOSS: cost descending

---

## 4. Footer
```
WAR TOTAL: $#,###,###
```

---

## 5. Optional Health List

Only display if:
`WeaponTracker.ui.showHealthList == true`

Display as collapsible section.
Default state: collapsed.

---

# DATA TRANSPORT RULES

Preferred transport: UDP

Fallback: File write

---

## UDP (Primary)

- Protocol: UDP
- Host: 127.0.0.1
- Port: 7777
- Update rate: 0.5–1.0 seconds
- Windows app listens immediately on startup

If no packets received within 3 seconds:
→ Automatically switch to file-watch fallback mode.

---

## File Fallback (If UDP Blocked)

Lua writes:

```
Saved Games\DCS\Logs\tpg_battle_cost_latest.json
```

Windows app:
- Poll every 500–1000ms
- Reload when modified timestamp changes

---

# PAYLOAD FORMAT

Preferred format: Structured JSON

```
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

Alternate format allowed:
```
{ "reportText": "<exact WeaponTracker.buildReport() output>" }
```

If raw text is provided:
Parse into the same UI sections.

---

# LUA SIDE REQUIREMENTS

You are allowed to:

- Add `WeaponTracker.exportSnapshot()`
- Add UDP sender using LuaSocket
- Add file writer fallback
- Schedule export every 1 second using `timer.scheduleFunction`

You are NOT allowed to:

- Change cost logic
- Change percentage calculations
- Modify existing balance math
- Add new economics features

Exporter must reflect exactly what `buildReport()` would show.

---

# WINDOWS APP REQUIREMENTS

Preferred stack:
C# + WPF (.NET 8)

Project location:
```
/src/TPGOverlay/
```

Must include:

- TPGOverlay.sln
- WPF project
- UDP listener service
- File watcher service
- Data model classes
- ViewModel layer
- Persistent window state (size + position)
- Single-file publish profile

---

# WINDOW BEHAVIOR

- Draggable by clicking anywhere on background
- Resizable
- Remembers position on close
- Does NOT steal DCS focus
- Works cleanly on second monitor
- High contrast
- Clean, readable layout
- No forced fullscreen

---

# BUILD INSTRUCTIONS (Must Work)

```
dotnet restore
dotnet build -c Release
dotnet publish -c Release -r win-x64 /p:PublishSingleFile=true /p:SelfContained=true
```

Output:
Single EXE file, no external runtime dependency.

---

# NON-GOALS (STRICT)

Do NOT add:

- Fuel burn tracking
- Sustainability gauges
- Trend graphs
- Time-series data
- Cost per minute
- External analytics

Only mirror what the Lua script currently displays.

---

# FAILURE CONDITIONS

You have failed if:

- The EXE displays additional metrics not in the Lua overlay
- Data does not update live
- UDP fallback not implemented
- Window is not draggable
- Project does not build with dotnet publish
- Coalition ordering is incorrect (BLUE must appear first in expanded section)

---

# SUMMARY

Mirror the expanded on-screen DCS report.
Export via UDP.
Fallback to file.
Build a clean, draggable Windows overlay EXE.
No extra features.