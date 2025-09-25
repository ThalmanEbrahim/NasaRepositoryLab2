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
        def get_observing_conditions(self) -> Dict:
        """
        Get current observing conditions

        Returns:
            Dictionary with observing conditions
        """
        current_time = self.get_current_time()
        moon_info = self.get_moon_phase(current_time)

Determine observing quality based on moon phase
        if moon_info['illumination'] < 10:
            conditions = "Excellent - Dark sky"
        elif moon_info['illumination'] < 50:
            conditions = "Good - Some moonlight"
        else:
            conditions = "Fair - Bright moonlight"

        return {
            'conditions': conditions,
            'moon_illumination': moon_info['illumination'],
            'moon_phase': moon_info['phase_name'],
            'recommendation': self.get_observing_recommendation(moon_info['illumination'])
        }

    def get_observing_recommendation(self, moon_illumination: float) -> str:
        """Get observing recommendations based on moon phase"""
        if moon_illumination < 10:
            return "Perfect for deep sky objects, galaxies, and nebulae"
        elif moon_illumination < 25:
            return "Good for planets, bright star clusters, and double stars"
        elif moon_illumination < 50:
            return "Best for planets, bright stars, and lunar observation"
        else:
            return "Ideal for lunar observation and bright planets only"
            def print_stargazing_report(self):
        """Print a comprehensive stargazing report"""
        print("=" * 60)
        print("🌟 STARGAZING REPORT 🌟")
        print("=" * 60)
        print(f"Location: {self.latitude:.2f}°N, {self.longitude:.2f}°W")
        print(f"Date/Time: {self.get_current_time().strftime('%Y-%m-%d %H:%M UTC')}")
        print()
        
        # Observing conditions
        conditions = self.get_observing_conditions()
        print("🌙 OBSERVING CONDITIONS")
        print("-" * 30)
        print(f"Conditions: {conditions['conditions']}")
        print(f"Moon Phase: {conditions['moon_phase']}")
        print(f"Moon Illumination: {conditions['moon_illumination']}%")
        print(f"Recommendation: {conditions['recommendation']}")
        print()
        
        # Moon information
        moon_info = self.get_moon_phase()
        print("🌕 MOON INFORMATION")
        print("-" * 30)
        print(f"Phase: {moon_info['phase_name']}")
        print(f"Altitude: {moon_info['altitude']:.1f}°")
        print(f"Azimuth: {moon_info['azimuth']:.1f}°")
        if moon_info['next_rise']:
            print(f"Next Rise: {moon_info['next_rise']}")
        if moon_info['next_set']:
            print(f"Next Set: {moon_info['next_set']}")
        print()
        
        # Visible planets
        planets = self.get_planet_info()
        if planets:
            print("🪐 VISIBLE PLANETS")
            print("-" * 30)
            for planet in planets:
                print(f"{planet.name}: Magnitude {planet.magnitude:.1f}, "
                      f"Distance {planet.distance:.2f} AU")
        else:
            print("🪐 VISIBLE PLANETS")
            print("-" * 30)
            print("No planets currently visible above horizon")
        print()
        
        # Bright stars
        stars = self.get_visible_stars()
        if stars:
            print("⭐ BRIGHTEST VISIBLE STARS")
            print("-" * 30)
            for star in stars[:5]:  # Show top 5
                print(f"{star.name} ({star.constellation}): "
                      f"Magnitude {star.magnitude:.2f}")
        print()
        
        print("=" * 60)
        print("Happy stargazing! 🌟")
        print("=" * 60)
        def main():
    """Main function to run the stargazing app"""
    print("Welcome to the Stargazing Information App!")
    print()
    
    # Get user location (optional)
    try:
        lat = float(input("Enter your latitude (or press Enter for New York City): ") or "40.7128")
        lon = float(input("Enter your longitude (or press Enter for New York City): ") or "-74.0060")
    except ValueError:
        print("Invalid input. Using default location (New York City).")
        lat, lon = 40.7128, -74.0060
    
    # Create app instance
    app = StargazingApp(lat, lon)
    
    # Print comprehensive report
    app.print_stargazing_report()
    
    # Interactive menu
    while True:
        print("\nOptions:")
        print("1. View current report")
        print("2. Get moon phase info")
        print("3. Get planet positions")
        print("4. Get visible stars")
        print("5. Get observing conditions")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            app.print_stargazing_report()
        elif choice == '2':
            moon = app.get_moon_phase()
            print(f"\nMoon Phase: {moon['phase_name']}")
            print(f"Illumination: {moon['illumination']}%")
            print(f"Altitude: {moon['altitude']:.1f}°")
        elif choice == '3':
            planets = app.get_planet_info()
            if planets:
                print("\nVisible Planets:")
                for planet in planets:
                    print(f"{planet.name}: Mag {planet.magnitude:.1f}")
            else:
                print("\nNo planets currently visible")
        elif choice == '4':
            stars = app.get_visible_stars()
            print(f"\nVisible Bright Stars ({len(stars)} total):")
            for star in stars[:10]:
                print(f"{star.name} ({star.constellation}): Mag {star.magnitude:.2f}")
        elif choice == '5':
            conditions = app.get_observing_conditions()
            print(f"\nObserving Conditions: {conditions['conditions']}")
            print(f"Recommendation: {conditions['recommendation']}")
        elif choice == '6':
            print("Thank you for using the Stargazing App! 🌟")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()