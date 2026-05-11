# ==========================================
# 🛰️ ZENITH_SPATIAL_OS // VISUAL.PY
# STATUS: v60.0_COMPLETE_12_TONE_LATCH
# ROLE: THE DESIGN LAW // 432Hz NEON REGISTRY
# LOCATION: /Volumes/X9 Pro/Zenith Rebuild Main/visual.py
# ==========================================

import tkinter as tk

# 👑 THE NEON PALETTE
ZENITH_GOLD   = "#FFFF00" # Solar Neon
OBSIDIAN      = "#000000"
NEURAL_GREEN  = "#39FF14" # Heart Laser
LASER_BLUE    = "#00E5FF" # Electric Cyan
CYBER_TEAL    = "#00BFFF"
RED_SIGNAL    = "#FF0000" # Pure Red
COBALT_NEON   = "#007FFF" # Azure Glow
SELECT_GLOW   = "#FFFFFF"
THERMAL_AMBER = "#FFBF00" # Orange Pulse

# 🧬 THE ANCESTRAL DNA (Complete 12-Tone 432Hz Scale)
# Format: [ROLE, NEON_HEX, FREQUENCY_HZ]
RESONANCE_MAP = {
    "C":  ["ROOT_CORE",    "#FF0000", 256.0],  # Root Red
    "C#": ["VITALITY",     "#FF4D00", 271.2],  # Neon Orange
    "D":  ["THERMAL",      "#FF8C00", 288.0],  # Vivid Amber
    "D#": ["PULSE_LOAD",   "#FFBF00", 305.1],  # Electric Gold
    "E":  ["SOLAR_POWER",  "#FFFF00", 324.0],  # Solar Yellow (Neon)
    "F":  ["HEART_LINK",   "#39FF14", 341.3],  # Heart Laser Green
    "F#": ["FLUX_WAVE",    "#00FF9F", 362.0],  # Flux Teal
    "G":  ["DEEP_VOICE",   "#00E5FF", 384.0],  # Electric Cyan
    "G#": ["SHIELD_BOND",  "#007FFF", 406.4],  # Azure Glow
    "A":  ["NEURAL_MEM",   "#BF00FF", 432.0],  # Neural Purple (THE ANCHOR)
    "A#": ["LOGIC_GATE",   "#FF00FF", 457.2],  # Indigo Strike
    "B":  ["ZENITH_PEAK",  "#FF007F", 483.3]   # Hot Magenta
}

STATUS_COLORS = {
    "SUCCESS": NEURAL_GREEN,
    "ERROR":   "#FF0000",
    "INFO":    CYBER_TEAL,
    "VOID":    "#4B0082",
    "WARNING": THERMAL_AMBER,
    "DANGER":  "#8B0000",
    "ZENITH":  NEURAL_GREEN,
    "CHAT":    CYBER_TEAL
}

FORGE_VOID = {
    "bg": "#050505",
    "fg": "#FFFFFF",
    "insertbackground": NEURAL_GREEN,
    "font": ("Courier New", 12),
    "padx": 10,
    "pady": 10,
    "undo": True,
    "bd": 0
}