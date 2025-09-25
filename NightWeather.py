#!/usr/bin/env python3
"""
Stargazing Information App
A comprehensive tool for astronomy enthusiasts to get stargazing information
"""

import datetime
import math
import json
from typing import Dict, List, Tuple, Optional
import ephem
from dataclasses import dataclass
@dataclass
class StarInfo:
    name: str
    magnitude: float
    constellation: str
    ra: float  # Right ascension in hours
    dec: float  # Declination in degrees

@dataclass
class PlanetInfo:
    name: str
    magnitude: float
    phase: float
    distance: float  # Distance from Earth in AU
    elongation: float  # Angular distance from Sun

class StargazingApp:
    def init(self, latitude: float = 40.7128, longitude: float = -74.0060):
        """
        Initialize the stargazing app with observer location

        Args:
            latitude: Observer's latitude in degrees (default: New York City)
            longitude: Observer's longitude in degrees (default: New York City)
        """
        self.latitude = latitude
        self.longitude = longitude
        self.observer = ephem.Observer()
        self.observer.lat = str(latitude)
        self.observer.lon = str(longitude)

Bright stars data
        self.bright_stars = [
            StarInfo("Sirius", -1.46, "Canis Major", 6.7525, -16.7161),
            StarInfo("Canopus", -0.74, "Carina", 6.3992, -52.6956),
            StarInfo("Arcturus", -0.05, "Boötes", 14.2611, 19.1824),
            StarInfo("Vega", 0.03, "Lyra", 18.6156, 38.7836),
            StarInfo("Capella", 0.08, "Auriga", 5.2781, 45.9980),
            StarInfo("Rigel", 0.13, "Orion", 5.2422, -8.2016),
            StarInfo("Procyon", 0.34, "Canis Minor", 7.6550, 5.2249),
            StarInfo("Betelgeuse", 0.42, "Orion", 5.9194, 7.4070),
            StarInfo("Achernar", 0.46, "Eridanus", 1.6286, -57.2367),
            StarInfo("Hadar", 0.61, "Centaurus", 14.0639, -60.3731),
        ]

Planet names for ephem
        self.planets = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

    def get_current_time(self) -> datetime.datetime:
        """Get current UTC time"""
        return datetime.datetime.utcnow()
def get_next_rise_set(self, body, event_type: str) -> Optional[str]:
        """Get next rise or set time for a celestial body"""
        try:
            if event_type == 'rise':
                next_event = self.observer.next_rising(body)
            else:
                next_event = self.observer.next_setting(body)
            return str(next_event)
        except:
            return None
def get_moon_phase(self, date: Optional[datetime.datetime] = None) -> Dict:
        """
        Calculate moon phase information

        Args:
            date: Date to calculate for (default: current time)

        Returns:
            Dictionary with moon phase information
        """
        if date is None:
            date = self.get_current_time()

        self.observer.date = date
        moon = ephem.Moon()
        moon.compute(self.observer)

Calculate moon phase (0 = new moon, 0.5 = full moon, 1 = new moon)
        phase = moon.moon_phase

Determine phase name
        if phase < 0.125:
            phase_name = "New Moon"
        elif phase < 0.375:
            phase_name = "Waxing Crescent"
        elif phase < 0.625:
            phase_name = "First Quarter"
        elif phase < 0.875:
            phase_name = "Waxing Gibbous"
        else:
            phase_name = "Full Moon"

Calculate illumination percentage
        illumination = (1 - abs(2 * phase - 1)) * 100

        return {
            'phase': phase,
            'phase_name': phase_name,
            'illumination': round(illumination, 1),
            'altitude': math.degrees(moon.alt),
            'azimuth': math.degrees(moon.az),
            'distance': moon.earth_distance,
            'next_rise': self.get_next_rise_set(moon, 'rise'),
            'next_set': self.get_next_rise_set(moon, 'set')
        }
        def get_planet_info(self, date: Optional[datetime.datetime] = None) -> List[PlanetInfo]:
        """
        Get information about visible planets

        Args:
            date: Date to calculate for (default: current time)

        Returns:
            List of PlanetInfo objects
        """
        if date is None:
            date = self.get_current_time()

        self.observer.date = date
        planet_info = []

        for planet_name in self.planets:
            try:
                planet = getattr(ephem, planet_name)()
                planet.compute(self.observer)

Only include planets that are above horizon
                if planet.alt > 0:
                    planet_info.append(PlanetInfo(
                        name=planet_name,
                        magnitude=planet.mag,
                        phase=planet.phase if hasattr(planet, 'phase') else 0,
                        distance=planet.earth_distance,
                        elongation=planet.elong if hasattr(planet, 'elong') else 0
                    ))
            except Exception as e:
                print(f"Error calculating {planet_name}: {e}")

        return sorted(planet_info, key=lambda x: x.magnitude)
        def get_visible_stars(self, min_magnitude: float = 2.0) -> List[StarInfo]:
        """
        Get list of bright stars visible tonight

        Args:
            min_magnitude: Maximum magnitude (brightness) to include

        Returns:
            List of visible stars
        """
        visible_stars = []
        current_time = self.get_current_time()
        self.observer.date = current_time

        for star in self.bright_stars:
            if star.magnitude <= min_magnitude:
                # Check if star is above horizon
                star_obj = ephem.FixedBody()
                star_obj._ra = ephem.hours(str(star.ra))
                star_obj._dec = ephem.degrees(str(star.dec))
                star_obj.compute(self.observer)

                if star_obj.alt > 0:  # Above horizon
                    visible_stars.append(star)

        return sorted(visible_stars, key=lambda x: x.magnitude)