# 🌟 Stargazing Information App

A comprehensive Python application designed to assist NASA astronomers and space enthusiasts with real-time stargazing information and optimal viewing conditions for astronomical observations.

## Project Idea & NASA/Space Benefits

This application helps NASA and space organizations by providing:
- **Mission Planning Support**: Real-time astronomical data for satellite launches and space missions
- **Ground Station Operations**: Optimal viewing conditions for tracking spacecraft and satellites
- **Research Assistance**: Accurate celestial object positions for astronomical research
- **Public Outreach**: Educational tool for NASA's public engagement and citizen science programs
- **Observatory Operations**: Supporting ground-based telescope operations with precise celestial calculations

## Technologies & Tools Used

- **Python 3.7+** - Core programming language
- **PyEphem** - Astronomical calculations and ephemeris data
- **PyTZ** - Timezone handling and conversions
- **TimezoneFinder** - Geographic timezone detection
- **Tkinter** - GUI interface (built into Python)
- **JSON** - Data storage and configuration
- **Datetime** - Time and date calculations

## How to Run the Project

### Prerequisites
- Python 3.7 or higher installed on your system

### Installation Steps

1. **Clone or download the project files**

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python launcher.py
   ```

4. **Choose your interface:**
   - Option 1: GUI Version (Recommended) - User-friendly graphical interface
   - Option 2: Terminal Version - Command-line interface

### Usage Instructions

1. **Launch the app** using the launcher
2. **Enter your location** when prompted (latitude/longitude) or use default NYC coordinates
3. **Select from menu options:**
   - View current astronomical report
   - Get moon phase information
   - Check planet positions and visibility
   - Browse visible stars catalog
   - Assess observing conditions
   - Exit application

### Alternative Direct Launch
- **GUI Version**: `python stargazing_gui.py`
- **Terminal Version**: `python stargazing_app.py`

---

*Happy stargazing! 🌟*
