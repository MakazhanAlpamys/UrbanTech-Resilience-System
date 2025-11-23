"""
Sensor Network Simulation
Simulates realistic sensor data for all three categories
"""

import random
import math
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import numpy as np

class SensorNetwork:
    """Manages all sensor simulations"""
    
    def __init__(self):
        self.start_time = time.time()
        self.time_step = 0
        
        # Category A: Emergency Infrastructure
        self.power_grids = self._initialize_power_grids()
        self.water_systems = self._initialize_water_systems()
        self.emergency_detectors = self._initialize_emergency_detectors()
        
        # Category B: Smart Mobility
        self.traffic_intersections = self._initialize_traffic_intersections()
        self.road_sensors = self._initialize_road_sensors()
        self.parking_zones = self._initialize_parking_zones()
        
        # Category C: Energy & Ecology
        self.air_quality_sensors = self._initialize_air_quality()
        self.solar_panels = self._initialize_solar_panels()
        self.smart_meters = self._initialize_smart_meters()
        
        # Emergency scenarios
        self.active_emergencies = []
        
        # Configuration
        self.config = {
            "noise_level": 0.1,
            "failure_probability": 0.001,
            "rush_hour_enabled": True,
            "weather_simulation": True
        }
    
    def _initialize_power_grids(self) -> List[Dict]:
        """Initialize power grid sensors"""
        grids = []
        for i in range(5):
            grids.append({
                "id": f"GRID_{i+1}",
                "name": f"Power Grid Zone {i+1}",
                "location": {"x": random.uniform(0, 100), "y": random.uniform(0, 100)},
                "capacity_mw": random.uniform(50, 200),
                "current_load_mw": 0,
                "voltage": 220.0,
                "frequency": 50.0,
                "status": "operational",
                "backup_available": True,
                "transformer_temp": 45.0
            })
        return grids
    
    def _initialize_water_systems(self) -> List[Dict]:
        """Initialize water supply sensors"""
        systems = []
        for i in range(4):
            systems.append({
                "id": f"WATER_{i+1}",
                "name": f"Water District {i+1}",
                "location": {"x": random.uniform(0, 100), "y": random.uniform(0, 100)},
                "pressure_bar": 4.5,
                "flow_rate_m3h": random.uniform(100, 500),
                "quality_index": 0.95,
                "tank_level_percent": 80.0,
                "status": "operational",
                "leak_detected": False
            })
        return systems
    
    def _initialize_emergency_detectors(self) -> List[Dict]:
        """Initialize emergency detection sensors"""
        detectors = []
        for i in range(10):
            detectors.append({
                "id": f"EMG_{i+1}",
                "type": random.choice(["fire", "flood", "gas", "structural"]),
                "location": {"x": random.uniform(0, 100), "y": random.uniform(0, 100)},
                "status": "normal",
                "last_trigger": None,
                "sensitivity": 0.8
            })
        return detectors
    
    def _initialize_traffic_intersections(self) -> List[Dict]:
        """Initialize traffic light intersections"""
        intersections = []
        for i in range(8):
            intersections.append({
                "id": f"INT_{i+1}",
                "name": f"Intersection {i+1}",
                "location": {"x": random.uniform(0, 100), "y": random.uniform(0, 100)},
                "current_phase": "NS_GREEN",
                "phase_time_remaining": 30,
                "vehicle_count_ns": 0,
                "vehicle_count_ew": 0,
                "queue_length_ns": 0,
                "queue_length_ew": 0,
                "avg_wait_time": 0,
                "throughput": 0,
                "adaptive_mode": True
            })
        return intersections
    
    def _initialize_road_sensors(self) -> List[Dict]:
        """Initialize road condition sensors"""
        sensors = []
        for i in range(15):
            sensors.append({
                "id": f"ROAD_{i+1}",
                "location": {"x": random.uniform(0, 100), "y": random.uniform(0, 100)},
                "vehicle_speed_kmh": 50.0,
                "vehicle_count": 0,
                "occupancy_percent": 0,
                "congestion_level": "low",
                "surface_condition": "dry",
                "incident_detected": False
            })
        return sensors
    
    def _initialize_parking_zones(self) -> List[Dict]:
        """Initialize smart parking zones"""
        zones = []
        for i in range(6):
            capacity = random.randint(50, 200)
            zones.append({
                "id": f"PARK_{i+1}",
                "name": f"Parking Zone {i+1}",
                "location": {"x": random.uniform(0, 100), "y": random.uniform(0, 100)},
                "capacity": capacity,
                "occupied": random.randint(0, capacity),
                "ev_charging_stations": random.randint(2, 10),
                "ev_charging_available": 0
            })
        return zones
    
    def _initialize_air_quality(self) -> List[Dict]:
        """Initialize air quality sensors"""
        sensors = []
        for i in range(12):
            sensors.append({
                "id": f"AIR_{i+1}",
                "location": {"x": random.uniform(0, 100), "y": random.uniform(0, 100)},
                "pm25": 15.0,
                "pm10": 25.0,
                "co2_ppm": 400.0,
                "no2": 20.0,
                "o3": 50.0,
                "aqi": 50,
                "quality_level": "good"
            })
        return sensors
    
    def _initialize_solar_panels(self) -> List[Dict]:
        """Initialize solar panel arrays"""
        panels = []
        for i in range(5):
            panels.append({
                "id": f"SOLAR_{i+1}",
                "name": f"Solar Array {i+1}",
                "location": {"x": random.uniform(0, 100), "y": random.uniform(0, 100)},
                "capacity_kw": random.uniform(100, 500),
                "current_output_kw": 0,
                "efficiency": 0.18,
                "panel_temp": 25.0,
                "status": "operational"
            })
        return panels
    
    def _initialize_smart_meters(self) -> List[Dict]:
        """Initialize smart energy meters"""
        meters = []
        for i in range(20):
            meters.append({
                "id": f"METER_{i+1}",
                "type": random.choice(["residential", "commercial", "industrial"]),
                "location": {"x": random.uniform(0, 100), "y": random.uniform(0, 100)},
                "current_consumption_kw": 0,
                "daily_consumption_kwh": 0,
                "peak_demand_kw": 0,
                "power_factor": 0.95
            })
        return meters
    
    def update(self) -> Dict:
        """Update all sensors - called every simulation step"""
        self.time_step += 1
        current_time = datetime.now()
        hour = current_time.hour
        
        # Simulate time-based patterns
        is_rush_hour = hour in [7, 8, 9, 17, 18, 19] if self.config["rush_hour_enabled"] else False
        is_night = hour < 6 or hour > 22
        
        # Weather simulation (affects multiple systems)
        if self.config["weather_simulation"]:
            weather = self._simulate_weather()
        else:
            weather = {"condition": "clear", "temp": 20, "solar_intensity": 0.8}
        
        # Update all sensor categories
        self._update_power_grids(is_night, weather)
        self._update_water_systems()
        self._update_emergency_detectors()
        self._update_traffic(is_rush_hour)
        self._update_roads(is_rush_hour)
        self._update_parking()
        self._update_air_quality(is_rush_hour, weather)
        self._update_solar_panels(weather)
        self._update_smart_meters(is_night)
        
        # Check for random failures
        if random.random() < self.config["failure_probability"]:
            self._trigger_random_failure()
        
        return self.get_all_data()
    
    def _simulate_weather(self) -> Dict:
        """Simulate weather conditions"""
        hour = datetime.now().hour
        
        # Solar intensity based on time of day
        if 6 <= hour <= 18:
            base_intensity = math.sin((hour - 6) * math.pi / 12)
        else:
            base_intensity = 0
        
        return {
            "condition": random.choice(["clear", "clear", "clear", "cloudy", "rainy"]),
            "temp": 15 + 10 * math.sin(hour * math.pi / 12) + random.gauss(0, 2),
            "solar_intensity": max(0, base_intensity + random.gauss(0, 0.1)),
            "humidity": random.uniform(40, 80),
            "wind_speed": random.uniform(0, 15)
        }
    
    def _update_power_grids(self, is_night: bool, weather: Dict):
        """Update power grid sensors with realistic patterns"""
        for grid in self.power_grids:
            # Base load varies by time of day
            base_load_factor = 0.5 if is_night else 0.8
            
            # Add noise
            noise = random.gauss(0, self.config["noise_level"])
            grid["current_load_mw"] = grid["capacity_mw"] * (base_load_factor + noise)
            grid["current_load_mw"] = max(0, min(grid["capacity_mw"], grid["current_load_mw"]))
            
            # Voltage stability (should be close to 220V)
            grid["voltage"] = 220 + random.gauss(0, 2)
            grid["frequency"] = 50 + random.gauss(0, 0.05)
            
            # Temperature increases with load
            load_factor = grid["current_load_mw"] / grid["capacity_mw"]
            grid["transformer_temp"] = 30 + load_factor * 40 + weather["temp"] * 0.3
            
            # Check for overload
            if load_factor > 0.95:
                grid["status"] = "overload_warning"
            elif grid["transformer_temp"] > 80:
                grid["status"] = "overheat_warning"
            else:
                grid["status"] = "operational"
    
    def _update_water_systems(self):
        """Update water system sensors"""
        for system in self.water_systems:
            # Pressure varies slightly
            system["pressure_bar"] = 4.5 + random.gauss(0, 0.2)
            
            # Flow rate with noise
            base_flow = 200 + 100 * math.sin(self.time_step * 0.01)
            system["flow_rate_m3h"] = max(0, base_flow + random.gauss(0, 20))
            
            # Tank level decreases with flow
            system["tank_level_percent"] -= system["flow_rate_m3h"] * 0.001
            system["tank_level_percent"] = max(0, min(100, system["tank_level_percent"]))
            
            # Refill when low
            if system["tank_level_percent"] < 20:
                system["tank_level_percent"] += 5
            
            # Quality should stay high
            system["quality_index"] = 0.95 + random.gauss(0, 0.02)
            system["quality_index"] = max(0, min(1, system["quality_index"]))
            
            # Random leak detection
            if random.random() < 0.0001:
                system["leak_detected"] = True
                system["status"] = "leak_detected"
            elif system["pressure_bar"] < 3.0:
                system["status"] = "low_pressure"
            else:
                system["leak_detected"] = False
                system["status"] = "operational"
    
    def _update_emergency_detectors(self):
        """Update emergency detection sensors"""
        for detector in self.emergency_detectors:
            # Most of the time, status is normal
            if random.random() < 0.9999:
                detector["status"] = "normal"
            else:
                # Rare emergency detection
                detector["status"] = "alert"
                detector["last_trigger"] = datetime.now().isoformat()
    
    def _update_traffic(self, is_rush_hour: bool):
        """Update traffic intersection sensors"""
        for intersection in self.traffic_intersections:
            # Vehicle arrival rate depends on rush hour
            arrival_rate = 8 if is_rush_hour else 3
            
            # Simulate vehicle arrivals (Poisson process)
            intersection["vehicle_count_ns"] += np.random.poisson(arrival_rate * 0.5)
            intersection["vehicle_count_ew"] += np.random.poisson(arrival_rate * 0.5)
            
            # Vehicles leave based on green light
            if "GREEN" in intersection["current_phase"]:
                if "NS" in intersection["current_phase"]:
                    departed = min(intersection["vehicle_count_ns"], 10)
                    intersection["vehicle_count_ns"] -= departed
                    intersection["throughput"] += departed
                else:
                    departed = min(intersection["vehicle_count_ew"], 10)
                    intersection["vehicle_count_ew"] -= departed
                    intersection["throughput"] += departed
            
            # Update queue lengths
            intersection["queue_length_ns"] = intersection["vehicle_count_ns"]
            intersection["queue_length_ew"] = intersection["vehicle_count_ew"]
            
            # Calculate average wait time
            total_vehicles = intersection["vehicle_count_ns"] + intersection["vehicle_count_ew"]
            if total_vehicles > 0:
                intersection["avg_wait_time"] = (
                    intersection["queue_length_ns"] * 2 + 
                    intersection["queue_length_ew"] * 2
                ) / total_vehicles
            else:
                intersection["avg_wait_time"] = 0
            
            # Phase timing countdown
            intersection["phase_time_remaining"] -= 0.5
            if intersection["phase_time_remaining"] <= 0:
                # Switch phase
                if intersection["current_phase"] == "NS_GREEN":
                    intersection["current_phase"] = "EW_GREEN"
                else:
                    intersection["current_phase"] = "NS_GREEN"
                
                # Adaptive timing based on queue length
                if intersection["adaptive_mode"]:
                    if intersection["current_phase"] == "NS_GREEN":
                        ratio = intersection["queue_length_ns"] / max(1, intersection["queue_length_ew"])
                    else:
                        ratio = intersection["queue_length_ew"] / max(1, intersection["queue_length_ns"])
                    
                    intersection["phase_time_remaining"] = 20 + 20 * min(ratio, 2)
                else:
                    intersection["phase_time_remaining"] = 30
    
    def _update_roads(self, is_rush_hour: bool):
        """Update road sensor data"""
        for sensor in self.road_sensors:
            # Speed and volume inversely related
            if is_rush_hour:
                sensor["vehicle_count"] = random.randint(20, 50)
                sensor["vehicle_speed_kmh"] = random.uniform(20, 40)
                sensor["occupancy_percent"] = random.uniform(60, 90)
            else:
                sensor["vehicle_count"] = random.randint(5, 20)
                sensor["vehicle_speed_kmh"] = random.uniform(40, 70)
                sensor["occupancy_percent"] = random.uniform(20, 50)
            
            # Determine congestion level
            if sensor["occupancy_percent"] > 80:
                sensor["congestion_level"] = "high"
            elif sensor["occupancy_percent"] > 50:
                sensor["congestion_level"] = "medium"
            else:
                sensor["congestion_level"] = "low"
            
            # Random incidents
            sensor["incident_detected"] = random.random() < 0.0001
    
    def _update_parking(self):
        """Update parking zone data"""
        for zone in self.parking_zones:
            # Random parking/leaving
            change = random.randint(-3, 5)
            zone["occupied"] = max(0, min(zone["capacity"], zone["occupied"] + change))
            
            # EV charging
            max_charging = min(zone["ev_charging_stations"], zone["occupied"])
            zone["ev_charging_available"] = zone["ev_charging_stations"] - random.randint(0, max_charging)
    
    def _update_air_quality(self, is_rush_hour: bool, weather: Dict):
        """Update air quality sensors"""
        for sensor in self.air_quality_sensors:
            # Traffic affects air quality
            traffic_factor = 1.5 if is_rush_hour else 1.0
            
            # Weather affects dispersion
            if weather["condition"] == "rainy":
                weather_factor = 0.7
            elif weather["wind_speed"] > 10:
                weather_factor = 0.8
            else:
                weather_factor = 1.0
            
            # Update pollutants
            sensor["pm25"] = max(0, 10 + 15 * traffic_factor * weather_factor + random.gauss(0, 3))
            sensor["pm10"] = sensor["pm25"] * 1.5 + random.gauss(0, 5)
            sensor["co2_ppm"] = 400 + 100 * traffic_factor + random.gauss(0, 20)
            sensor["no2"] = 15 + 25 * traffic_factor * weather_factor + random.gauss(0, 5)
            sensor["o3"] = 50 + random.gauss(0, 10)
            
            # Calculate AQI (simplified)
            aqi_components = [
                sensor["pm25"] * 2,
                sensor["pm10"] * 1,
                (sensor["co2_ppm"] - 400) * 0.1,
                sensor["no2"] * 1.5
            ]
            sensor["aqi"] = int(max(aqi_components))
            
            # Quality level
            if sensor["aqi"] < 50:
                sensor["quality_level"] = "good"
            elif sensor["aqi"] < 100:
                sensor["quality_level"] = "moderate"
            elif sensor["aqi"] < 150:
                sensor["quality_level"] = "unhealthy_sensitive"
            else:
                sensor["quality_level"] = "unhealthy"
    
    def _update_solar_panels(self, weather: Dict):
        """Update solar panel data"""
        for panel in self.solar_panels:
            # Output based on solar intensity and weather
            if weather["condition"] == "rainy":
                intensity_factor = 0.2
            elif weather["condition"] == "cloudy":
                intensity_factor = 0.5
            else:
                intensity_factor = 1.0
            
            panel["current_output_kw"] = (
                panel["capacity_kw"] * 
                panel["efficiency"] * 
                weather["solar_intensity"] * 
                intensity_factor
            )
            
            # Panel temperature affects efficiency
            panel["panel_temp"] = weather["temp"] + weather["solar_intensity"] * 30
            
            # Adjust efficiency based on temperature (decreases with heat)
            if panel["panel_temp"] > 25:
                temp_loss = (panel["panel_temp"] - 25) * 0.004
                panel["efficiency"] = max(0.10, 0.18 - temp_loss)
    
    def _update_smart_meters(self, is_night: bool):
        """Update smart meter data"""
        for meter in self.smart_meters:
            # Consumption patterns by type
            if meter["type"] == "residential":
                if is_night:
                    base_consumption = random.uniform(0.5, 2)
                else:
                    base_consumption = random.uniform(2, 5)
            elif meter["type"] == "commercial":
                if is_night:
                    base_consumption = random.uniform(1, 3)
                else:
                    base_consumption = random.uniform(10, 30)
            else:  # industrial
                base_consumption = random.uniform(50, 150)
            
            meter["current_consumption_kw"] = base_consumption
            meter["daily_consumption_kwh"] += base_consumption * 0.5 / 3600  # 0.5s timestep
            
            # Track peak demand
            if meter["current_consumption_kw"] > meter["peak_demand_kw"]:
                meter["peak_demand_kw"] = meter["current_consumption_kw"]
            
            # Power factor varies slightly
            meter["power_factor"] = 0.95 + random.gauss(0, 0.02)
            meter["power_factor"] = max(0.8, min(1.0, meter["power_factor"]))
    
    def _trigger_random_failure(self):
        """Simulate random system failure"""
        failure_type = random.choice(["power", "water", "traffic"])
        
        if failure_type == "power":
            grid = random.choice(self.power_grids)
            grid["status"] = "failure"
            grid["current_load_mw"] = 0
        elif failure_type == "water":
            system = random.choice(self.water_systems)
            system["leak_detected"] = True
            system["status"] = "leak_detected"
        else:
            sensor = random.choice(self.road_sensors)
            sensor["incident_detected"] = True
    
    def trigger_emergency(self, emergency_type: str, location: Dict) -> Dict:
        """Manually trigger emergency for testing"""
        emergency = {
            "id": f"EMG_{len(self.active_emergencies)+1}",
            "type": emergency_type,
            "location": location,
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        }
        self.active_emergencies.append(emergency)
        return emergency
    
    def get_all_data(self) -> Dict:
        """Get all sensor data"""
        return {
            "timestamp": datetime.now().isoformat(),
            "power_grids": self.power_grids,
            "water_systems": self.water_systems,
            "emergency_detectors": self.emergency_detectors,
            "traffic_intersections": self.traffic_intersections,
            "road_sensors": self.road_sensors,
            "parking_zones": self.parking_zones,
            "air_quality_sensors": self.air_quality_sensors,
            "solar_panels": self.solar_panels,
            "smart_meters": self.smart_meters,
            "active_emergencies": self.active_emergencies
        }
    
    def get_sensor_count(self) -> int:
        """Get total number of sensors"""
        return (len(self.power_grids) + len(self.water_systems) + 
                len(self.emergency_detectors) + len(self.traffic_intersections) +
                len(self.road_sensors) + len(self.parking_zones) +
                len(self.air_quality_sensors) + len(self.solar_panels) +
                len(self.smart_meters))
    
    def get_config(self) -> Dict:
        """Get current configuration"""
        return self.config
    
    def update_config(self, config: Dict):
        """Update configuration"""
        self.config.update(config)
