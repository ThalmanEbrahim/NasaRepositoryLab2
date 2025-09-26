#!/usr/bin/env python3
"""
Stargazing Information App - GUI Version
A modern graphical interface for astronomy enthusiasts
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import datetime
import math
import ephem
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import threading

@dataclass
class StarInfo:
    name: str
    magnitude: float
    constellation: str
    ra: float
    dec: float

@dataclass
class PlanetInfo:
    name: str
    magnitude: float
    phase: float
    distance: float
    elongation: float

class StargazingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌟 Stargazing Information App")
        self.root.geometry("1000x700")
        self.root.configure(bg='#0a0a0a')
        
        # Initialize app with default location (NYC)
        self.app = None
        self.latitude = 40.7128
        self.longitude = -74.0060
        
        # Create the GUI
        self.create_widgets()
        self.update_data()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🌟 Stargazing Information App", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Location input section
        self.create_location_section(main_frame, 1)
        
        # Main content area with notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        main_frame.rowconfigure(2, weight=1)
        
        # Create tabs
        self.create_overview_tab()
        self.create_moon_tab()
        self.create_planets_tab()
        self.create_stars_tab()
        self.create_conditions_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def create_location_section(self, parent, row):
        """Create location input section"""
        loc_frame = ttk.LabelFrame(parent, text="📍 Location", padding="10")
        loc_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Latitude
        ttk.Label(loc_frame, text="Latitude:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.lat_var = tk.StringVar(value="40.7128")
        lat_entry = ttk.Entry(loc_frame, textvariable=self.lat_var, width=15)
        lat_entry.grid(row=0, column=1, padx=(0, 20))
        
        # Longitude
        ttk.Label(loc_frame, text="Longitude:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.lon_var = tk.StringVar(value="-74.0060")
        lon_entry = ttk.Entry(loc_frame, textvariable=self.lon_var, width=15)
        lon_entry.grid(row=0, column=3, padx=(0, 20))
        
        # Update button
        update_btn = ttk.Button(loc_frame, text="Update Location", command=self.update_location)
        update_btn.grid(row=0, column=4, padx=(0, 10))
        
        # Refresh button
        refresh_btn = ttk.Button(loc_frame, text="🔄 Refresh Data", command=self.update_data)
        refresh_btn.grid(row=0, column=5)
        
    def create_overview_tab(self):
        """Create overview tab"""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="📊 Overview")
        
        # Create scrollable text widget
        self.overview_text = scrolledtext.ScrolledText(overview_frame, wrap=tk.WORD, 
                                                      font=('Consolas', 10), bg='#1a1a1a', 
                                                      fg='#ffffff', insertbackground='white')
        self.overview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_moon_tab(self):
        """Create moon information tab"""
        moon_frame = ttk.Frame(self.notebook)
        self.notebook.add(moon_frame, text="🌙 Moon")
        
        # Moon phase display
        phase_frame = ttk.LabelFrame(moon_frame, text="Moon Phase", padding="10")
        phase_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.moon_phase_var = tk.StringVar()
        self.moon_illumination_var = tk.StringVar()
        self.moon_altitude_var = tk.StringVar()
        self.moon_azimuth_var = tk.StringVar()
        
        ttk.Label(phase_frame, text="Phase:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(phase_frame, textvariable=self.moon_phase_var, font=('Arial', 12, 'bold')).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(phase_frame, text="Illumination:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(phase_frame, textvariable=self.moon_illumination_var).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(phase_frame, text="Altitude:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(phase_frame, textvariable=self.moon_altitude_var).grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(phase_frame, text="Azimuth:").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(phase_frame, textvariable=self.moon_azimuth_var).grid(row=3, column=1, sticky=tk.W, padx=(10, 0))
        
        # Moon rise/set times
        times_frame = ttk.LabelFrame(moon_frame, text="Rise/Set Times", padding="10")
        times_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.moon_rise_var = tk.StringVar()
        self.moon_set_var = tk.StringVar()
        
        ttk.Label(times_frame, text="Next Rise:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(times_frame, textvariable=self.moon_rise_var).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(times_frame, text="Next Set:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(times_frame, textvariable=self.moon_set_var).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
    def create_planets_tab(self):
        """Create planets tab"""
        planets_frame = ttk.Frame(self.notebook)
        self.notebook.add(planets_frame, text="🪐 Planets")
        
        # Planets list
        planets_list_frame = ttk.LabelFrame(planets_frame, text="Visible Planets", padding="10")
        planets_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for planets
        columns = ('Name', 'Magnitude', 'Distance', 'Phase')
        self.planets_tree = ttk.Treeview(planets_list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.planets_tree.heading(col, text=col)
            self.planets_tree.column(col, width=120)
        
        # Scrollbar for planets
        planets_scrollbar = ttk.Scrollbar(planets_list_frame, orient=tk.VERTICAL, command=self.planets_tree.yview)
        self.planets_tree.configure(yscrollcommand=planets_scrollbar.set)
        
        self.planets_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        planets_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_stars_tab(self):
        """Create stars tab"""
        stars_frame = ttk.Frame(self.notebook)
        self.notebook.add(stars_frame, text="⭐ Stars")
        
        # Stars list
        stars_list_frame = ttk.LabelFrame(stars_frame, text="Bright Visible Stars", padding="10")
        stars_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create treeview for stars
        columns = ('Name', 'Constellation', 'Magnitude')
        self.stars_tree = ttk.Treeview(stars_list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.stars_tree.heading(col, text=col)
            self.stars_tree.column(col, width=150)
        
        # Scrollbar for stars
        stars_scrollbar = ttk.Scrollbar(stars_list_frame, orient=tk.VERTICAL, command=self.stars_tree.yview)
        self.stars_tree.configure(yscrollcommand=stars_scrollbar.set)
        
        self.stars_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        stars_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_conditions_tab(self):
        """Create observing conditions tab"""
        conditions_frame = ttk.Frame(self.notebook)
        self.notebook.add(conditions_frame, text="🌌 Conditions")
        
        # Overall conditions
        overall_frame = ttk.LabelFrame(conditions_frame, text="Overall Conditions", padding="10")
        overall_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.conditions_score_var = tk.StringVar()
        self.conditions_status_var = tk.StringVar()
        self.conditions_recommendation_var = tk.StringVar()
        
        ttk.Label(overall_frame, text="Score:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(overall_frame, textvariable=self.conditions_score_var, font=('Arial', 14, 'bold')).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(overall_frame, text="Status:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(overall_frame, textvariable=self.conditions_status_var, font=('Arial', 12)).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(overall_frame, text="Recommendation:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(overall_frame, textvariable=self.conditions_recommendation_var, wraplength=400).grid(row=2, column=1, sticky=tk.W, padx=(10, 0))
        
        # Environmental factors
        env_frame = ttk.LabelFrame(conditions_frame, text="Environmental Factors", padding="10")
        env_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.light_pollution_var = tk.StringVar()
        self.sun_altitude_var = tk.StringVar()
        
        ttk.Label(env_frame, text="Light Pollution:").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(env_frame, textvariable=self.light_pollution_var).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(env_frame, text="Sun Altitude:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(env_frame, textvariable=self.sun_altitude_var).grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
    def update_location(self):
        """Update location and refresh data"""
        try:
            self.latitude = float(self.lat_var.get())
            self.longitude = float(self.lon_var.get())
            self.status_var.set("Location updated successfully")
            self.update_data()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid latitude and longitude values.")
            
    def update_data(self):
        """Update all data in a separate thread"""
        def update_thread():
            try:
                self.status_var.set("Updating data...")
                self.root.update()
                
                # Import the stargazing app
                from stargazing_app import StargazingApp
                self.app = StargazingApp(self.latitude, self.longitude)
                
                # Update all displays
                self.update_overview()
                self.update_moon_info()
                self.update_planets()
                self.update_stars()
                self.update_conditions()
                
                self.status_var.set("Data updated successfully")
                
            except Exception as e:
                self.status_var.set(f"Error: {str(e)}")
                messagebox.showerror("Error", f"Failed to update data: {str(e)}")
        
        # Run in separate thread to prevent GUI freezing
        threading.Thread(target=update_thread, daemon=True).start()
        
    def update_overview(self):
        """Update overview tab"""
        if not self.app:
            return
            
        current_time = self.app.get_current_time()
        moon_info = self.app.get_moon_phase()
        conditions = self.app.get_observing_conditions()
        
        overview_text = f"""
🌟 STARGAZING REPORT
{'='*50}
Location: {self.latitude:.2f}°N, {self.longitude:.2f}°W
Date/Time: {current_time.strftime('%Y-%m-%d %H:%M UTC')}

🌙 OBSERVING CONDITIONS
{'-'*30}
Overall Score: {conditions['score']}/100
Conditions: {conditions['conditions']}
Moon Phase: {conditions['moon_phase']} ({conditions['moon_illumination']}% illuminated)
Light Pollution: {conditions['light_pollution']}
Recommendation: {conditions['recommendation']}

🌕 MOON INFORMATION
{'-'*30}
Phase: {moon_info['phase_name']}
Illumination: {moon_info['illumination']}%
Altitude: {moon_info['altitude']:.1f}°
Azimuth: {moon_info['azimuth']:.1f}°

🪐 VISIBLE PLANETS
{'-'*30}
"""
        
        planets = self.app.get_planet_info()
        if planets:
            for planet in planets:
                overview_text += f"{planet.name}: Magnitude {planet.magnitude:.1f}, Distance {planet.distance:.2f} AU\n"
        else:
            overview_text += "No planets currently visible above horizon\n"
            
        overview_text += f"""
⭐ BRIGHTEST VISIBLE STARS
{'-'*30}
"""
        
        stars = self.app.get_visible_stars()
        for star in stars[:5]:
            overview_text += f"{star.name} ({star.constellation}): Magnitude {star.magnitude:.2f}\n"
            
        self.overview_text.delete(1.0, tk.END)
        self.overview_text.insert(1.0, overview_text)
        
    def update_moon_info(self):
        """Update moon information tab"""
        if not self.app:
            return
            
        moon_info = self.app.get_moon_phase()
        
        self.moon_phase_var.set(moon_info['phase_name'])
        self.moon_illumination_var.set(f"{moon_info['illumination']}%")
        self.moon_altitude_var.set(f"{moon_info['altitude']:.1f}°")
        self.moon_azimuth_var.set(f"{moon_info['azimuth']:.1f}°")
        
        self.moon_rise_var.set(moon_info['next_rise'] or "Not visible")
        self.moon_set_var.set(moon_info['next_set'] or "Not visible")
        
    def update_planets(self):
        """Update planets tab"""
        if not self.app:
            return
            
        # Clear existing items
        for item in self.planets_tree.get_children():
            self.planets_tree.delete(item)
            
        planets = self.app.get_planet_info()
        for planet in planets:
            self.planets_tree.insert('', 'end', values=(
                planet.name,
                f"{planet.magnitude:.1f}",
                f"{planet.distance:.2f} AU",
                f"{planet.phase:.1f}%" if hasattr(planet, 'phase') else "N/A"
            ))
            
    def update_stars(self):
        """Update stars tab"""
        if not self.app:
            return
            
        # Clear existing items
        for item in self.stars_tree.get_children():
            self.stars_tree.delete(item)
            
        stars = self.app.get_visible_stars()
        for star in stars:
            self.stars_tree.insert('', 'end', values=(
                star.name,
                star.constellation,
                f"{star.magnitude:.2f}"
            ))
            
    def update_conditions(self):
        """Update observing conditions tab"""
        if not self.app:
            return
            
        conditions = self.app.get_observing_conditions()
        
        self.conditions_score_var.set(f"{conditions['score']}/100")
        self.conditions_status_var.set(conditions['conditions'])
        self.conditions_recommendation_var.set(conditions['recommendation'])
        self.light_pollution_var.set(conditions['light_pollution'])
        self.sun_altitude_var.set(f"{conditions['sun_altitude']:.1f}°")

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = StargazingGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()