#!/usr/bin/env python3
"""
Stargazing Information App - GUI Version
A modern graphical interface for astronomy enthusiasts
"""

# import gui and other needed modules
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import datetime
import math
import ephem
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import threading

# class to store star information
@dataclass
class StarInfo:
    name: str
    magnitude: float
    constellation: str
    ra: float
    dec: float

# class to store planet information
@dataclass
class PlanetInfo:
    name: str
    magnitude: float
    phase: float
    distance: float
    elongation: float

# main gui class
class StargazingGUI:
    def __init__(self, root):
        # setup main window
        self.root = root
        self.root.title("🌟 Stargazing Information App")
        self.root.geometry("1200x800")
        
        # define colors for space theme
        self.colors = {
            'bg_primary': '#0B1426',      # Deep space blue
            'bg_secondary': '#1A2332',    # Lighter space blue
            'bg_accent': '#2A3441',       # Card background
            'text_primary': '#E8F4FD',    # Light blue-white
            'text_secondary': '#B8D4EA',  # Muted blue
            'accent_blue': '#4A9EFF',     # Bright blue
            'accent_purple': '#8B5FBF',   # Purple
            'accent_gold': '#FFD700',     # Gold for stars
            'accent_green': '#00FF7F',    # Green for good conditions
            'accent_red': '#FF6B6B',      # Red for warnings
            'border': '#3A4A5C'           # Border color
        }
        
        # setup window background
        self.root.configure(bg=self.colors['bg_primary'])
        
        # set default location coordinates
        self.app = None
        self.latitude = 26.0
        self.longitude = 50.0
        
        # setup gui styling
        self.setup_styles()
        
        # create all gui elements
        self.create_widgets()
        self.update_data()
    
    # setup gui styling and colors
    def setup_styles(self):
        """Setup custom styles for ttk widgets"""
        style = ttk.Style()
        
        # try to use dark theme
        try:
            style.theme_use('clam')
        except:
            pass
        
        # set default widget colors
        style.configure('.',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_secondary'],
                       selectbackground=self.colors['accent_blue'],
                       selectforeground='white')
        
        # set frame colors
        style.configure('Main.TFrame',
                       background=self.colors['bg_primary'])
        
        style.configure('TFrame',
                       background=self.colors['bg_primary'])
        
        # set label colors
        style.configure('TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'])
        
        # Configure label frame styles
        style.configure('Card.TLabelframe',
                       background=self.colors['bg_accent'],
                       foreground=self.colors['text_primary'],
                       borderwidth=2,
                       relief='solid',
                       bordercolor=self.colors['border'])
        
        style.configure('Card.TLabelframe.Label',
                       background=self.colors['bg_accent'],
                       foreground=self.colors['accent_blue'],
                       font=('Segoe UI', 11, 'bold'))
        
        # Configure button styles
        style.configure('Action.TButton',
                       background=self.colors['accent_blue'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('Action.TButton',
                 background=[('active', self.colors['accent_purple']),
                           ('pressed', '#3A7BD5')])
        
        # Configure entry styles
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=2,
                       bordercolor=self.colors['border'],
                       insertcolor=self.colors['accent_blue'],
                       selectbackground=self.colors['accent_blue'],
                       selectforeground='white')
        
        style.map('Modern.TEntry',
                 fieldbackground=[('focus', self.colors['bg_secondary']),
                                ('!focus', self.colors['bg_secondary'])],
                 bordercolor=[('focus', self.colors['accent_blue']),
                            ('!focus', self.colors['border'])])
        
        # Configure label styles
        style.configure('Title.TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['accent_gold'],
                       font=('Segoe UI', 18, 'bold'))
        
        style.configure('Header.TLabel',
                       background=self.colors['bg_accent'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('Info.TLabel',
                       background=self.colors['bg_accent'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 10))
        
        style.configure('Value.TLabel',
                       background=self.colors['bg_accent'],
                       foreground=self.colors['accent_blue'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Configure notebook styles
        style.configure('Modern.TNotebook',
                       background=self.colors['bg_primary'],
                       borderwidth=0,
                       tabmargins=[0, 0, 0, 0])
        
        style.configure('Modern.TNotebook.Pane',
                       background=self.colors['bg_primary'])
        
        style.configure('Modern.TNotebook.Tab',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'),
                       focuscolor='none')
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['bg_accent']),
                           ('active', self.colors['bg_secondary']),
                           ('!active', self.colors['bg_secondary'])],
                 foreground=[('selected', self.colors['accent_blue']),
                           ('active', self.colors['text_primary']),
                           ('!active', self.colors['text_secondary'])])
        
        # Configure frame styles to ensure dark backgrounds
        style.configure('Dark.TFrame',
                       background=self.colors['bg_primary'])
        
        style.configure('DarkCard.TFrame', 
                       background=self.colors['bg_accent'])
        
        # Configure treeview styles
        style.configure('Modern.Treeview',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_secondary'],
                       borderwidth=2,
                       relief='solid',
                       bordercolor=self.colors['border'],
                       lightcolor=self.colors['bg_secondary'],
                       darkcolor=self.colors['bg_secondary'])
        
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['bg_accent'],
                       foreground=self.colors['accent_blue'],
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=1,
                       relief='solid')
        
        style.map('Modern.Treeview',
                 background=[('selected', self.colors['accent_blue']),
                           ('focus', self.colors['bg_secondary'])],
                 foreground=[('selected', 'white'),
                           ('focus', self.colors['text_primary'])])
        
        style.map('Modern.Treeview.Heading',
                 background=[('active', self.colors['accent_purple']),
                           ('pressed', self.colors['accent_blue'])])
        
        # Configure scrollbar styles
        style.configure('Modern.Vertical.TScrollbar',
                       background=self.colors['bg_secondary'],
                       troughcolor=self.colors['bg_primary'],
                       borderwidth=0,
                       arrowcolor=self.colors['text_secondary'],
                       darkcolor=self.colors['bg_accent'],
                       lightcolor=self.colors['bg_accent'])
        
        # Configure default scrollbar
        style.configure('Vertical.TScrollbar',
                       background=self.colors['bg_secondary'],
                       troughcolor=self.colors['bg_primary'],
                       borderwidth=0,
                       arrowcolor=self.colors['text_secondary'],
                       darkcolor=self.colors['bg_accent'],
                       lightcolor=self.colors['bg_accent'])
        
        # Configure default entry
        style.configure('TEntry',
                       fieldbackground=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=2,
                       bordercolor=self.colors['border'],
                       insertcolor=self.colors['accent_blue'])
        
        # Configure default button
        style.configure('TButton',
                       background=self.colors['accent_blue'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10))
        
        style.map('TButton',
                 background=[('active', self.colors['accent_purple']),
                           ('pressed', '#3A7BD5')])
        
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="15", style='Main.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title with gradient effect
        title_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        title_frame.grid(row=0, column=0, columnspan=3, pady=(0, 25), sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(title_frame, text="🌟 Stargazing Information App", 
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(title_frame, text="Explore the Night Sky with Precision", 
                                  background=self.colors['bg_primary'],
                                  foreground=self.colors['text_secondary'],
                                  font=('Segoe UI', 11, 'italic'))
        subtitle_label.pack(pady=(5, 0))
        
        # Location input section
        self.create_location_section(main_frame, 1)
        
        # Main content area with notebook
        self.notebook = ttk.Notebook(main_frame, style='Modern.TNotebook')
        self.notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=15)
        main_frame.rowconfigure(2, weight=1)
        
        # Create tabs
        self.create_overview_tab()
        self.create_moon_tab()
        self.create_planets_tab()
        self.create_stars_tab()
        self.create_conditions_tab()
        
        # Time display section
        self.create_time_section(main_frame, 3)
        
        # Status bar with modern styling
        status_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'], height=30)
        status_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(15, 0))
        status_frame.grid_propagate(False)
        
        self.status_var = tk.StringVar()
        self.status_var.set("🚀 Ready - Welcome to Stargazing App!")
        status_bar = tk.Label(status_frame, textvariable=self.status_var, 
                             bg=self.colors['bg_secondary'], 
                             fg=self.colors['text_secondary'],
                             font=('Segoe UI', 9),
                             anchor='w')
        status_bar.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def create_location_section(self, parent, row):
        """Create location input section"""
        loc_frame = ttk.LabelFrame(parent, text="📍 Observer Location", padding="15", style='Card.TLabelframe')
        loc_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Latitude
        ttk.Label(loc_frame, text="Latitude:", style='Info.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 8))
        self.lat_var = tk.StringVar(value="26.0")
        lat_entry = ttk.Entry(loc_frame, textvariable=self.lat_var, width=15, style='Modern.TEntry')
        lat_entry.grid(row=0, column=1, padx=(0, 25))
        
        # Longitude
        ttk.Label(loc_frame, text="Longitude:", style='Info.TLabel').grid(row=0, column=2, sticky=tk.W, padx=(0, 8))
        self.lon_var = tk.StringVar(value="50.0")
        lon_entry = ttk.Entry(loc_frame, textvariable=self.lon_var, width=15, style='Modern.TEntry')
        lon_entry.grid(row=0, column=3, padx=(0, 25))
        
        # Update button
        update_btn = ttk.Button(loc_frame, text="📍 Update Location", command=self.update_location, style='Action.TButton')
        update_btn.grid(row=0, column=4, padx=(0, 15))
        
        # Refresh button
        refresh_btn = ttk.Button(loc_frame, text="🔄 Refresh Data", command=self.update_data, style='Action.TButton')
        refresh_btn.grid(row=0, column=5)
        
    def create_time_section(self, parent, row):
        """Create time display section"""
        time_frame = ttk.LabelFrame(parent, text="🕐 Time Information", padding="15", style='Card.TLabelframe')
        time_frame.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Time variables
        self.timezone_var = tk.StringVar()
        self.local_time_var = tk.StringVar()
        self.utc_time_var = tk.StringVar()
        
        # Timezone
        ttk.Label(time_frame, text="Timezone:", style='Info.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 8))
        ttk.Label(time_frame, textvariable=self.timezone_var, style='Value.TLabel').grid(row=0, column=1, sticky=tk.W, padx=(0, 25))
        
        # Local time
        ttk.Label(time_frame, text="Local Time:", style='Info.TLabel').grid(row=0, column=2, sticky=tk.W, padx=(0, 8))
        ttk.Label(time_frame, textvariable=self.local_time_var, style='Value.TLabel').grid(row=0, column=3, sticky=tk.W, padx=(0, 25))
        
        # UTC time
        ttk.Label(time_frame, text="UTC Time:", style='Info.TLabel').grid(row=0, column=4, sticky=tk.W, padx=(0, 8))
        ttk.Label(time_frame, textvariable=self.utc_time_var, style='Value.TLabel').grid(row=0, column=5, sticky=tk.W)
        
    def create_overview_tab(self):
        """Create overview tab with modern card-based layout"""
        overview_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(overview_frame, text="📊 Overview")
        
        # Main container with dark background
        main_container = tk.Frame(overview_frame, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Create scrollable frame
        canvas = tk.Canvas(main_container, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview, style='Modern.Vertical.TScrollbar')
        self.overview_scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_primary'])
        
        self.overview_scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.overview_scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Create overview sections
        self.create_overview_sections()
    
    def create_overview_sections(self):
        """Create the overview sections with modern card layout"""
        # Location and Time Info Card
        self.location_info_frame = ttk.LabelFrame(self.overview_scrollable_frame, text="📍 Location & Time", 
                                                 padding="20", style='Card.TLabelframe')
        self.location_info_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Location info variables
        self.overview_location_var = tk.StringVar()
        self.overview_timezone_var = tk.StringVar()
        self.overview_local_time_var = tk.StringVar()
        self.overview_utc_time_var = tk.StringVar()
        
        # Location info layout
        tk.Label(self.location_info_frame, text="Location:", bg=self.colors['bg_accent'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 10)).grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        tk.Label(self.location_info_frame, textvariable=self.overview_location_var, bg=self.colors['bg_accent'], 
                fg=self.colors['text_primary'], font=('Segoe UI', 10, 'bold')).grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        
        tk.Label(self.location_info_frame, text="Timezone:", bg=self.colors['bg_accent'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 10)).grid(row=0, column=2, sticky=tk.W, padx=(0, 15))
        tk.Label(self.location_info_frame, textvariable=self.overview_timezone_var, bg=self.colors['bg_accent'], 
                fg=self.colors['accent_blue'], font=('Segoe UI', 10, 'bold')).grid(row=0, column=3, sticky=tk.W)
        
        tk.Label(self.location_info_frame, text="Local Time:", bg=self.colors['bg_accent'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 10)).grid(row=1, column=0, sticky=tk.W, padx=(0, 15), pady=(15, 0))
        tk.Label(self.location_info_frame, textvariable=self.overview_local_time_var, bg=self.colors['bg_accent'], 
                fg=self.colors['text_primary'], font=('Segoe UI', 10, 'bold')).grid(row=1, column=1, sticky=tk.W, padx=(0, 30), pady=(15, 0))
        
        tk.Label(self.location_info_frame, text="UTC Time:", bg=self.colors['bg_accent'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 10)).grid(row=1, column=2, sticky=tk.W, padx=(0, 15), pady=(15, 0))
        tk.Label(self.location_info_frame, textvariable=self.overview_utc_time_var, bg=self.colors['bg_accent'], 
                fg=self.colors['text_primary'], font=('Segoe UI', 10, 'bold')).grid(row=1, column=3, sticky=tk.W, pady=(15, 0))
        
        # Observing Conditions Card
        self.conditions_overview_frame = ttk.LabelFrame(self.overview_scrollable_frame, text="🌌 Observing Conditions", 
                                                       padding="20", style='Card.TLabelframe')
        self.conditions_overview_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Conditions variables
        self.overview_score_var = tk.StringVar()
        self.overview_conditions_var = tk.StringVar()
        self.overview_moon_phase_var = tk.StringVar()
        self.overview_light_pollution_var = tk.StringVar()
        
        # Score display with prominent styling
        score_container = tk.Frame(self.conditions_overview_frame, bg=self.colors['bg_accent'])
        score_container.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 15))
        
        tk.Label(score_container, text="Overall Score:", bg=self.colors['bg_accent'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 12)).pack(side=tk.LEFT)
        self.overview_score_label = tk.Label(score_container, textvariable=self.overview_score_var, bg=self.colors['bg_accent'], 
                                           fg=self.colors['accent_gold'], font=('Segoe UI', 16, 'bold'))
        self.overview_score_label.pack(side=tk.LEFT, padx=(15, 0))
        
        # Conditions details
        tk.Label(self.conditions_overview_frame, text="Status:", bg=self.colors['bg_accent'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 10)).grid(row=1, column=0, sticky=tk.W, padx=(0, 15))
        tk.Label(self.conditions_overview_frame, textvariable=self.overview_conditions_var, bg=self.colors['bg_accent'], 
                fg=self.colors['text_primary'], font=('Segoe UI', 10, 'bold')).grid(row=1, column=1, sticky=tk.W, padx=(0, 30))
        
        tk.Label(self.conditions_overview_frame, text="Light Pollution:", bg=self.colors['bg_accent'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 10)).grid(row=1, column=2, sticky=tk.W, padx=(0, 15))
        tk.Label(self.conditions_overview_frame, textvariable=self.overview_light_pollution_var, bg=self.colors['bg_accent'], 
                fg=self.colors['accent_blue'], font=('Segoe UI', 10, 'bold')).grid(row=1, column=3, sticky=tk.W)
        
        # Moon Information Card
        self.moon_overview_frame = ttk.LabelFrame(self.overview_scrollable_frame, text="🌙 Moon Information", 
                                                 padding="20", style='Card.TLabelframe')
        self.moon_overview_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Moon variables
        self.overview_moon_phase_name_var = tk.StringVar()
        self.overview_moon_illumination_var = tk.StringVar()
        self.overview_moon_altitude_var = tk.StringVar()
        
        tk.Label(self.moon_overview_frame, text="Phase:", bg=self.colors['bg_accent'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 10)).grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        tk.Label(self.moon_overview_frame, textvariable=self.overview_moon_phase_name_var, bg=self.colors['bg_accent'], 
                fg=self.colors['accent_gold'], font=('Segoe UI', 12, 'bold')).grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        
        tk.Label(self.moon_overview_frame, text="Illumination:", bg=self.colors['bg_accent'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 10)).grid(row=0, column=2, sticky=tk.W, padx=(0, 15))
        tk.Label(self.moon_overview_frame, textvariable=self.overview_moon_illumination_var, bg=self.colors['bg_accent'], 
                fg=self.colors['text_primary'], font=('Segoe UI', 10, 'bold')).grid(row=0, column=3, sticky=tk.W)
        
        tk.Label(self.moon_overview_frame, text="Altitude:", bg=self.colors['bg_accent'], 
                fg=self.colors['text_secondary'], font=('Segoe UI', 10)).grid(row=1, column=0, sticky=tk.W, padx=(0, 15), pady=(15, 0))
        tk.Label(self.moon_overview_frame, textvariable=self.overview_moon_altitude_var, bg=self.colors['bg_accent'], 
                fg=self.colors['text_primary'], font=('Segoe UI', 10, 'bold')).grid(row=1, column=1, sticky=tk.W, padx=(0, 30), pady=(15, 0))
        
        # Planets Card
        self.planets_overview_frame = ttk.LabelFrame(self.overview_scrollable_frame, text="🪐 Visible Planets", 
                                                    padding="20", style='Card.TLabelframe')
        self.planets_overview_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Create planets display area
        self.planets_display_frame = tk.Frame(self.planets_overview_frame, bg=self.colors['bg_accent'])
        self.planets_display_frame.pack(fill=tk.X)
        
        # Stars Card
        self.stars_overview_frame = ttk.LabelFrame(self.overview_scrollable_frame, text="⭐ Brightest Stars", 
                                                  padding="20", style='Card.TLabelframe')
        self.stars_overview_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Create stars display area
        self.stars_display_frame = tk.Frame(self.stars_overview_frame, bg=self.colors['bg_accent'])
        self.stars_display_frame.pack(fill=tk.X)
        
    def create_moon_tab(self):
        """Create moon information tab"""
        moon_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(moon_frame, text="🌙 Moon")
        
        # Container frame
        container = tk.Frame(moon_frame, bg=self.colors['bg_primary'])
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Moon phase display
        phase_frame = ttk.LabelFrame(container, text="🌙 Moon Phase", padding="20", style='Card.TLabelframe')
        phase_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.moon_phase_var = tk.StringVar()
        self.moon_illumination_var = tk.StringVar()
        self.moon_altitude_var = tk.StringVar()
        self.moon_azimuth_var = tk.StringVar()
        
        # Create a grid layout for moon info
        ttk.Label(phase_frame, text="Phase:", style='Info.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        ttk.Label(phase_frame, textvariable=self.moon_phase_var, style='Header.TLabel').grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        
        ttk.Label(phase_frame, text="Illumination:", style='Info.TLabel').grid(row=0, column=2, sticky=tk.W, padx=(0, 15))
        ttk.Label(phase_frame, textvariable=self.moon_illumination_var, style='Value.TLabel').grid(row=0, column=3, sticky=tk.W)
        
        ttk.Label(phase_frame, text="Altitude:", style='Info.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 15), pady=(15, 0))
        ttk.Label(phase_frame, textvariable=self.moon_altitude_var, style='Value.TLabel').grid(row=1, column=1, sticky=tk.W, padx=(0, 30), pady=(15, 0))
        
        ttk.Label(phase_frame, text="Azimuth:", style='Info.TLabel').grid(row=1, column=2, sticky=tk.W, padx=(0, 15), pady=(15, 0))
        ttk.Label(phase_frame, textvariable=self.moon_azimuth_var, style='Value.TLabel').grid(row=1, column=3, sticky=tk.W, pady=(15, 0))
        
        # Moon rise/set times
        times_frame = ttk.LabelFrame(container, text="⏰ Rise/Set Times", padding="20", style='Card.TLabelframe')
        times_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.moon_rise_var = tk.StringVar()
        self.moon_set_var = tk.StringVar()
        
        ttk.Label(times_frame, text="Next Rise:", style='Info.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        ttk.Label(times_frame, textvariable=self.moon_rise_var, style='Value.TLabel').grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        
        ttk.Label(times_frame, text="Next Set:", style='Info.TLabel').grid(row=0, column=2, sticky=tk.W, padx=(0, 15))
        ttk.Label(times_frame, textvariable=self.moon_set_var, style='Value.TLabel').grid(row=0, column=3, sticky=tk.W)
        
    def create_planets_tab(self):
        """Create planets tab"""
        planets_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(planets_frame, text="🪐 Planets")
        
        # Container frame
        container = tk.Frame(planets_frame, bg=self.colors['bg_primary'])
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Planets list
        planets_list_frame = ttk.LabelFrame(container, text="🪐 Visible Planets Tonight", padding="15", style='Card.TLabelframe')
        planets_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for planets with modern styling
        columns = ('Name', 'Magnitude', 'Distance', 'Phase')
        self.planets_tree = ttk.Treeview(planets_list_frame, columns=columns, show='headings', height=12, style='Modern.Treeview')
        
        # Configure column headers and widths
        column_configs = {
            'Name': {'text': '🪐 Planet', 'width': 150},
            'Magnitude': {'text': '✨ Magnitude', 'width': 120},
            'Distance': {'text': '📏 Distance', 'width': 140},
            'Phase': {'text': '🌓 Phase', 'width': 100}
        }
        
        for col, config in column_configs.items():
            self.planets_tree.heading(col, text=config['text'])
            self.planets_tree.column(col, width=config['width'], anchor='center')
        
        # Scrollbar for planets
        planets_scrollbar = ttk.Scrollbar(planets_list_frame, orient=tk.VERTICAL, command=self.planets_tree.yview, style='Modern.Vertical.TScrollbar')
        self.planets_tree.configure(yscrollcommand=planets_scrollbar.set)
        
        self.planets_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        planets_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_stars_tab(self):
        """Create stars tab"""
        stars_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(stars_frame, text="⭐ Stars")
        
        # Container frame
        container = tk.Frame(stars_frame, bg=self.colors['bg_primary'])
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Stars list
        stars_list_frame = ttk.LabelFrame(container, text="⭐ Bright Visible Stars Tonight", padding="15", style='Card.TLabelframe')
        stars_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview for stars with modern styling
        columns = ('Name', 'Constellation', 'Magnitude')
        self.stars_tree = ttk.Treeview(stars_list_frame, columns=columns, show='headings', height=15, style='Modern.Treeview')
        
        # Configure column headers and widths
        star_column_configs = {
            'Name': {'text': '⭐ Star Name', 'width': 180},
            'Constellation': {'text': '🌌 Constellation', 'width': 180},
            'Magnitude': {'text': '✨ Magnitude', 'width': 120}
        }
        
        for col, config in star_column_configs.items():
            self.stars_tree.heading(col, text=config['text'])
            self.stars_tree.column(col, width=config['width'], anchor='center')
        
        # Scrollbar for stars
        stars_scrollbar = ttk.Scrollbar(stars_list_frame, orient=tk.VERTICAL, command=self.stars_tree.yview, style='Modern.Vertical.TScrollbar')
        self.stars_tree.configure(yscrollcommand=stars_scrollbar.set)
        
        self.stars_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        stars_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_conditions_tab(self):
        """Create observing conditions tab"""
        conditions_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(conditions_frame, text="🌌 Conditions")
        
        # Container frame
        container = tk.Frame(conditions_frame, bg=self.colors['bg_primary'])
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Overall conditions
        overall_frame = ttk.LabelFrame(container, text="🌌 Overall Observing Conditions", padding="20", style='Card.TLabelframe')
        overall_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.conditions_score_var = tk.StringVar()
        self.conditions_status_var = tk.StringVar()
        self.conditions_recommendation_var = tk.StringVar()
        
        # Score display with large, prominent styling
        score_frame = tk.Frame(overall_frame, bg=self.colors['bg_accent'])
        score_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        ttk.Label(score_frame, text="Observing Score:", style='Info.TLabel', background=self.colors['bg_accent']).pack(side=tk.LEFT)
        score_label = ttk.Label(score_frame, textvariable=self.conditions_score_var, 
                               background=self.colors['bg_accent'], 
                               foreground=self.colors['accent_gold'],
                               font=('Segoe UI', 16, 'bold'))
        score_label.pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Label(overall_frame, text="Status:", style='Info.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 15), pady=(0, 10))
        ttk.Label(overall_frame, textvariable=self.conditions_status_var, style='Header.TLabel').grid(row=1, column=1, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(overall_frame, text="Recommendation:", style='Info.TLabel').grid(row=2, column=0, sticky=tk.NW, padx=(0, 15))
        rec_label = ttk.Label(overall_frame, textvariable=self.conditions_recommendation_var, 
                             style='Value.TLabel', wraplength=500)
        rec_label.grid(row=2, column=1, sticky=tk.W)
        
        # Environmental factors
        env_frame = ttk.LabelFrame(container, text="🌍 Environmental Factors", padding="20", style='Card.TLabelframe')
        env_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.light_pollution_var = tk.StringVar()
        self.sun_altitude_var = tk.StringVar()
        
        ttk.Label(env_frame, text="Light Pollution:", style='Info.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
        ttk.Label(env_frame, textvariable=self.light_pollution_var, style='Value.TLabel').grid(row=0, column=1, sticky=tk.W, padx=(0, 30))
        
        ttk.Label(env_frame, text="Sun Altitude:", style='Info.TLabel').grid(row=0, column=2, sticky=tk.W, padx=(0, 15))
        ttk.Label(env_frame, textvariable=self.sun_altitude_var, style='Value.TLabel').grid(row=0, column=3, sticky=tk.W)
        
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
                self.update_time_info()
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
        
    def update_time_info(self):
        """Update time information display"""
        if not self.app:
            return
            
        timezone_info = self.app.get_timezone_info()
        
        self.timezone_var.set(f"{timezone_info['timezone_name']} ({timezone_info['utc_offset']})")
        self.local_time_var.set(timezone_info['local_time'])
        self.utc_time_var.set(timezone_info['utc_time'])
        
    def update_overview(self):
        """Update overview tab with card-based layout"""
        if not self.app:
            return
            
        current_time = self.app.get_current_time()
        timezone_info = self.app.get_timezone_info()
        moon_info = self.app.get_moon_phase()
        conditions = self.app.get_observing_conditions()
        
        # Update location and time info
        self.overview_location_var.set(f"{self.latitude:.2f}°N, {self.longitude:.2f}°W")
        self.overview_timezone_var.set(f"{timezone_info['timezone_name']} ({timezone_info['utc_offset']})")
        self.overview_local_time_var.set(timezone_info['local_time'])
        self.overview_utc_time_var.set(timezone_info['utc_time'])
        
        # Update observing conditions with color coding
        score = conditions['score']
        if score >= 80:
            score_color = self.colors['accent_green']
        elif score >= 65:
            score_color = self.colors['accent_blue']
        elif score >= 50:
            score_color = self.colors['accent_gold']
        elif score >= 35:
            score_color = '#FFA500'  # Orange
        else:
            score_color = self.colors['accent_red']
        
        self.overview_score_var.set(f"{conditions['score']}/100")
        self.overview_score_label.configure(fg=score_color)
        self.overview_conditions_var.set(conditions['conditions'])
        self.overview_light_pollution_var.set(conditions['light_pollution'])
        
        # Update moon information
        self.overview_moon_phase_name_var.set(moon_info['phase_name'])
        self.overview_moon_illumination_var.set(f"{moon_info['illumination']}%")
        self.overview_moon_altitude_var.set(f"{moon_info['altitude']:.1f}°")
        
        # Update planets display
        self.update_planets_overview()
        
        # Update stars display
        self.update_stars_overview()
    
    def update_planets_overview(self):
        """Update planets overview section"""
        # Clear existing planets display
        for widget in self.planets_display_frame.winfo_children():
            widget.destroy()
        
        planets = self.app.get_planet_info()
        if planets:
            for i, planet in enumerate(planets[:6]):  # Show up to 6 planets
                planet_frame = tk.Frame(self.planets_display_frame, bg=self.colors['bg_accent'])
                planet_frame.grid(row=i//3, column=i%3, sticky=(tk.W, tk.E), padx=10, pady=5)
                
                # Planet name
                tk.Label(planet_frame, text=f"🪐 {planet.name}", bg=self.colors['bg_accent'], 
                        fg=self.colors['accent_blue'], font=('Segoe UI', 10, 'bold')).pack(anchor='w')
                
                # Planet details
                tk.Label(planet_frame, text=f"Magnitude: {planet.magnitude:.1f}", bg=self.colors['bg_accent'], 
                        fg=self.colors['text_secondary'], font=('Segoe UI', 9)).pack(anchor='w')
                tk.Label(planet_frame, text=f"Distance: {planet.distance:.2f} AU", bg=self.colors['bg_accent'], 
                        fg=self.colors['text_secondary'], font=('Segoe UI', 9)).pack(anchor='w')
        else:
            tk.Label(self.planets_display_frame, text="No planets currently visible above horizon", 
                    bg=self.colors['bg_accent'], fg=self.colors['text_secondary'], 
                    font=('Segoe UI', 10, 'italic')).pack(pady=10)
    
    def update_stars_overview(self):
        """Update stars overview section"""
        # Clear existing stars display
        for widget in self.stars_display_frame.winfo_children():
            widget.destroy()
        
        stars = self.app.get_visible_stars()
        for i, star in enumerate(stars[:6]):  # Show top 6 stars
            star_frame = tk.Frame(self.stars_display_frame, bg=self.colors['bg_accent'])
            star_frame.grid(row=i//3, column=i%3, sticky=(tk.W, tk.E), padx=10, pady=5)
            
            # Star name
            tk.Label(star_frame, text=f"⭐ {star.name}", bg=self.colors['bg_accent'], 
                    fg=self.colors['accent_gold'], font=('Segoe UI', 10, 'bold')).pack(anchor='w')
            
            # Star details
            tk.Label(star_frame, text=f"Constellation: {star.constellation}", bg=self.colors['bg_accent'], 
                    fg=self.colors['text_secondary'], font=('Segoe UI', 9)).pack(anchor='w')
            tk.Label(star_frame, text=f"Magnitude: {star.magnitude:.2f}", bg=self.colors['bg_accent'], 
                    fg=self.colors['text_secondary'], font=('Segoe UI', 9)).pack(anchor='w')
        
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
        
        # Color-code the score based on quality
        score = conditions['score']
        if score >= 80:
            score_color = self.colors['accent_green']
        elif score >= 65:
            score_color = self.colors['accent_blue']
        elif score >= 50:
            score_color = self.colors['accent_gold']
        elif score >= 35:
            score_color = '#FFA500'  # Orange
        else:
            score_color = self.colors['accent_red']
        
        self.conditions_score_var.set(f"{conditions['score']}/100")
        self.conditions_status_var.set(conditions['conditions'])
        self.conditions_recommendation_var.set(conditions['recommendation'])
        self.light_pollution_var.set(conditions['light_pollution'])
        self.sun_altitude_var.set(f"{conditions['sun_altitude']:.1f}°")

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    
    # Set window properties before creating the app
    root.minsize(1000, 600)
    root.state('zoomed') if root.tk.call('tk', 'windowingsystem') == 'win32' else root.attributes('-zoomed', True)
    
    app = StargazingGUI(root)
    
    # center window on screen
    root.update_idletasks()
    if root.state() != 'zoomed':
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
    
    # handle window closing
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # start gui main loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        on_closing()

# run gui when script is executed
if __name__ == "__main__":
    main()