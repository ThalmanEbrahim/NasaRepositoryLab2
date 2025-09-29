#!/usr/bin/env python3
"""
Stargazing Information App
A comprehensive tool for astronomy enthusiasts to get stargazing information
"""

# import all needed modules
import datetime
import math
import json
from typing import Dict, List, Tuple, Optional
import ephem
from dataclasses import dataclass
import pytz
from timezonefinder import TimezoneFinder

# class to store star information
@dataclass
class StarInfo:
    name: str
    magnitude: float
    constellation: str
    ra: float  # Right ascension in hours
    dec: float  # Declination in degrees

# class to store planet information
@dataclass
class PlanetInfo:
    name: str
    magnitude: float
    phase: float
    distance: float  # Distance from Earth in AU
    elongation: float  # Angular distance from Sun

# main app class
class StargazingApp:
    def __init__(self, latitude: float = 26.0, longitude: float = 50.0):
        """
        Initialize the stargazing app with observer location
        
        Args:
            latitude: Observer's latitude in degrees (default: Bahrain)
            longitude: Observer's longitude in degrees (default: Bahrain)
        """
        # store location coordinates
        self.latitude = latitude
        self.longitude = longitude
        
        # create observer object for calculations
        self.observer = ephem.Observer()
        self.observer.lat = str(latitude)
        self.observer.lon = str(longitude)
        
        # setup timezone for location
        self.tf = TimezoneFinder()
        self.timezone_str = self.tf.timezone_at(lat=latitude, lng=longitude)
        self.timezone = pytz.timezone(self.timezone_str) if self.timezone_str else pytz.UTC
        
        # list of bright stars with their data
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
        
        # list of planets to track
        self.planets = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
        
    # get current time in local timezone
    def get_current_time(self) -> datetime.datetime:
        """Get current time in the location's timezone"""
        utc_now = datetime.datetime.now(datetime.timezone.utc)
        local_time = utc_now.astimezone(self.timezone)
        return local_time
    
    # get current utc time for calculations
    def get_current_time_utc(self) -> datetime.datetime:
        """Get current UTC time (for ephem calculations)"""
        return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    
    # get timezone information
    def get_timezone_info(self) -> Dict:
        """Get timezone information for the current location"""
        current_time = self.get_current_time()
        utc_time = self.get_current_time_utc()
        
        return {
            'timezone_name': self.timezone_str or 'UTC',
            'timezone_abbreviation': current_time.strftime('%Z'),
            'utc_offset': current_time.strftime('%z'),
            'local_time': current_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
            'utc_time': utc_time.strftime('%Y-%m-%d %H:%M:%S UTC'),
            'is_dst': bool(current_time.dst())
        }
    
    # calculate moon phase information
    def get_moon_phase(self, date: Optional[datetime.datetime] = None) -> Dict:
        """
        Calculate moon phase information
        
        Args:
            date: Date to calculate for (default: current time)
            
        Returns:
            Dictionary with moon phase information
        """
        # use current time if no date given
        if date is None:
            date = self.get_current_time_utc()
            
        # setup observer and calculate moon position
        self.observer.date = date
        moon = ephem.Moon()
        moon.compute(self.observer)
        
        # get moon illumination percentage
        illumination_fraction = moon.moon_phase
        illumination = illumination_fraction * 100
        
        # calculate sun position for phase determination
        sun = ephem.Sun()
        sun.compute(self.observer)
        
        # get coordinates for both moon and sun
        moon_ra = moon.ra
        moon_dec = moon.dec
        sun_ra = sun.ra
        sun_dec = sun.dec
        
        # calculate angle between moon and sun
        elongation = math.degrees(ephem.separation((moon_ra, moon_dec), (sun_ra, sun_dec)))
        
        # determine if moon is getting brighter or dimmer
        is_waxing = elongation < 180
        
        # figure out phase name based on brightness
        if illumination < 1:
            phase_name = "New Moon"
        elif illumination < 25:
            phase_name = "Waxing Crescent" if is_waxing else "Waning Crescent"
        elif illumination < 50:
            phase_name = "First Quarter" if is_waxing else "Last Quarter"
        elif illumination < 75:
            phase_name = "Waxing Gibbous" if is_waxing else "Waning Gibbous"
        elif illumination < 100:
            phase_name = "Full Moon"
        else:
            phase_name = "Full Moon"
        
        return {
            'phase': illumination_fraction,
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
            date = self.get_current_time_utc()
            
        self.observer.date = date
        planet_info = []
        
        for planet_name in self.planets:
            try:
                planet = getattr(ephem, planet_name)()
                planet.compute(self.observer)
                
                # Only include planets that are above horizon
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
        current_time = self.get_current_time_utc()
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
    
    def get_observing_conditions(self) -> Dict:
        """
        Get current observing conditions based on location, time, and moon phase
        
        Returns:
            Dictionary with observing conditions
        """
        current_time = self.get_current_time_utc()
        moon_info = self.get_moon_phase(current_time)
        
        # Calculate location-based factors
        light_pollution = self._estimate_light_pollution()
        moon_altitude = moon_info['altitude']
        sun_altitude = self._get_sun_altitude()
        
        # Determine base conditions from moon phase
        base_score = self._get_moon_impact_score(moon_info['illumination'], moon_altitude)
        
        # Adjust for light pollution
        light_pollution_penalty = self._get_light_pollution_penalty(light_pollution)
        
        # Adjust for time of day (sun altitude)
        time_penalty = self._get_time_penalty(sun_altitude)
        
        # Calculate final observing score (0-100, higher is better)
        final_score = max(0, base_score - light_pollution_penalty - time_penalty)
        
        # Determine conditions based on final score
        if final_score >= 80:
            conditions = "Excellent - Dark sky, minimal interference"
        elif final_score >= 65:
            conditions = "Very Good - Good visibility with minor interference"
        elif final_score >= 50:
            conditions = "Good - Decent conditions with some interference"
        elif final_score >= 35:
            conditions = "Fair - Moderate interference from light/moon"
        elif final_score >= 20:
            conditions = "Poor - Significant interference"
        else:
            conditions = "Very Poor - Heavy interference, not recommended"
        
        return {
            'conditions': conditions,
            'score': round(final_score, 1),
            'moon_illumination': moon_info['illumination'],
            'moon_phase': moon_info['phase_name'],
            'moon_altitude': round(moon_altitude, 1),
            'light_pollution': light_pollution,
            'sun_altitude': round(sun_altitude, 1),
            'recommendation': self.get_observing_recommendation(final_score)
        }
    
    def _estimate_light_pollution(self) -> str:
        """Estimate light pollution based on location"""
        # Simple estimation based on latitude/longitude patterns
        # This is a simplified model - in reality, you'd use actual light pollution data
        
        # Major cities and their approximate light pollution levels
        major_cities = {
            (26.0, 50.0): "Medium",            # Bahrain
            (40.7128, -74.0060): "Very High",  # NYC
            (34.0522, -118.2437): "Very High",  # LA
            (41.8781, -87.6298): "Very High",  # Chicago
            (29.7604, -95.3698): "High",       # Houston
            (33.4484, -112.0740): "High",      # Phoenix
            (39.7392, -104.9903): "High",      # Denver
            (47.6062, -122.3321): "High",      # Seattle
            (25.7617, -80.1918): "High",       # Miami
        }
        
        # Check if we're near a major city
        for (lat, lon), pollution in major_cities.items():
            if abs(self.latitude - lat) < 0.5 and abs(self.longitude - lon) < 0.5:
                return pollution
        
        # Estimate based on general patterns
        if abs(self.latitude) < 30:  # Tropical/subtropical
            return "Medium"
        elif abs(self.latitude) < 60:  # Temperate
            return "Low"
        else:  # Polar
            return "Very Low"
    
    def _get_sun_altitude(self) -> float:
        """Get current sun altitude in degrees"""
        sun = ephem.Sun()
        sun.compute(self.observer)
        return math.degrees(sun.alt)
    
    def _get_moon_impact_score(self, illumination: float, moon_altitude: float) -> float:
        """Calculate moon impact on observing conditions (0-100, higher is better)"""
        # Base score starts at 100 (perfect conditions)
        base_score = 100
        
        # Moon illumination impact (0-50 points penalty)
        illumination_penalty = (illumination / 100) * 50
        
        # Moon altitude impact (moon below horizon = no impact)
        if moon_altitude < 0:
            altitude_penalty = 0
        else:
            # Moon above horizon reduces score more when higher
            altitude_penalty = (moon_altitude / 90) * 20
        
        return base_score - illumination_penalty - altitude_penalty
    
    def _get_light_pollution_penalty(self, light_pollution: str) -> float:
        """Get penalty points for light pollution"""
        penalties = {
            "Very Low": 0,
            "Low": 5,
            "Medium": 15,
            "High": 30,
            "Very High": 45
        }
        return penalties.get(light_pollution, 20)
    
    def _get_time_penalty(self, sun_altitude: float) -> float:
        """Get penalty for time of day (sun altitude)"""
        if sun_altitude < -18:  # Astronomical twilight
            return 0
        elif sun_altitude < -12:  # Nautical twilight
            return 5
        elif sun_altitude < -6:   # Civil twilight
            return 15
        elif sun_altitude < 0:    # Sun below horizon
            return 25
        else:  # Sun above horizon
            return 50
    
    def get_observing_recommendation(self, score: float) -> str:
        """Get observing recommendations based on overall score"""
        if score >= 80:
            return "Perfect for deep sky objects, galaxies, and nebulae"
        elif score >= 65:
            return "Great for deep sky objects and faint star clusters"
        elif score >= 50:
            return "Good for planets, bright star clusters, and double stars"
        elif score >= 35:
            return "Best for planets, bright stars, and lunar observation"
        elif score >= 20:
            return "Only bright planets and lunar observation recommended"
        else:
            return "Only lunar observation and very bright planets visible"
    
    def print_stargazing_report(self):
        """Print a comprehensive stargazing report"""
        timezone_info = self.get_timezone_info()
        print("=" * 60)
        print("🌟 STARGAZING REPORT 🌟")
        print("=" * 60)
        print(f"Location: {self.latitude:.2f}°N, {self.longitude:.2f}°W")
        print(f"Timezone: {timezone_info['timezone_name']} ({timezone_info['utc_offset']})")
        print(f"Local Time: {timezone_info['local_time']}")
        print(f"UTC Time: {timezone_info['utc_time']}")
        print()
        
        # Observing conditions
        conditions = self.get_observing_conditions()
        print("🌙 OBSERVING CONDITIONS")
        print("-" * 30)
        print(f"Overall Score: {conditions['score']}/100")
        print(f"Conditions: {conditions['conditions']}")
        print(f"Moon Phase: {conditions['moon_phase']} ({conditions['moon_illumination']}% illuminated)")
        print(f"Moon Altitude: {conditions['moon_altitude']}°")
        print(f"Sun Altitude: {conditions['sun_altitude']}°")
        print(f"Light Pollution: {conditions['light_pollution']}")
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
        lat = float(input("Enter your latitude (or press Enter for Bahrain): ") or "26.0")
        lon = float(input("Enter your longitude (or press Enter for Bahrain): ") or "50.0")
    except ValueError:
        print("Invalid input. Using default location (Bahrain).")
        lat, lon = 26.0, 50.0
    
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
            print(f"Overall Score: {conditions['score']}/100")
            print(f"Light Pollution: {conditions['light_pollution']}")
            print(f"Moon Altitude: {conditions['moon_altitude']}°")
            print(f"Sun Altitude: {conditions['sun_altitude']}°")
            print(f"Recommendation: {conditions['recommendation']}")
        elif choice == '6':
            print("Thank you for using the Stargazing App! 🌟")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()