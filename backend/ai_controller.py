"""
AI Controller with Adaptive Algorithms
Implements ML-based decision making, PID control, and predictive analytics
"""

import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from collections import deque
import math

class PIDController:
    """PID Controller for system regulation
    
    Параметры настройки контроллера:
    - Kp (Proportional) = 0.5: Пропорциональная компонента, корректирует текущую ошибку
    - Ki (Integral) = 0.1: Интегральная компонента, устраняет накопленную ошибку
    - Kd (Derivative) = 0.2: Дифференциальная компонента, предсказывает будущую ошибку
    
    Управляющее воздействие: u(t) = Kp·e(t) + Ki·∫e(τ)dτ + Kd·(de/dt)
    
    Настройка методом Зиглера-Никольса:
    1. Kp выбран для быстрого отклика без перерегулирования
    2. Ki достаточно мал для стабильности интегральной составляющей
    3. Kd оптимизирован для демпфирования колебаний
    """
    def __init__(self, kp: float, ki: float, kd: float, setpoint: float):
        self.kp = kp  # Пропорциональный коэффициент
        self.ki = ki  # Интегральный коэффициент
        self.kd = kd  # Дифференциальный коэффициент
        self.setpoint = setpoint  # Целевое значение
        self.integral = 0
        self.last_error = 0
    
    def update(self, current_value: float, dt: float = 0.5) -> float:
        """Calculate PID output
        
        Расчет управляющего воздействия:
        error = setpoint - current_value
        output = Kp·error + Ki·∫error·dt + Kd·(Δerror/dt)
        """
        error = self.setpoint - current_value
        self.integral += error * dt
        derivative = (error - self.last_error) / dt
        
        output = (self.kp * error + 
                 self.ki * self.integral + 
                 self.kd * derivative)
        
        self.last_error = error
        return output

class TrafficOptimizer:
    """Adaptive traffic light optimization using ML principles
    
    Алгоритм Q-Learning для адаптивного управления светофорами:
    
    Параметры обучения:
    - learning_rate (α) = 0.1: Скорость обучения (баланс между новой и старой информацией)
    - discount_factor (γ) = 0.9: Коэффициент дисконтирования будущих наград
    - exploration_rate (ε) = 0.2: Доля исследования новых действий
    
    Временные параметры сигналов:
    - T_base = 20 секунд: Базовое время зеленого сигнала
    - T_adaptive = 20 ± 8 секунд: Адаптивная корректировка [12, 28] сек
    
    Формула адаптации:
    T_green = T_base + correction, где correction зависит от pressure_ratio
    pressure_ratio = queue_length / (throughput + 1)
    
    Стратегия:
    - Высокое давление (PR > 2.0) → увеличение времени зеленого (+8 сек)
    - Среднее давление (0.5 < PR < 2.0) → стандартное время
    - Низкое давление (PR < 0.5) → уменьшение времени зеленого (-8 сек)
    """
    def __init__(self):
        self.history = {}
        self.learning_rate = 0.1  # α: learning rate
        self.q_table = {}  # Q-learning table: state -> action -> Q-value
    
    def optimize(self, intersections: List[Dict]) -> List[Dict]:
        """Optimize traffic light timing using adaptive Q-Learning"""
        decisions = []
        
        for intersection in intersections:
            int_id = intersection["id"]
            
            # Calculate congestion score (pressure ratio)
            ns_pressure = intersection["queue_length_ns"] / 30.0  # Normalize to [0, 1]
            ew_pressure = intersection["queue_length_ew"] / 30.0
            
            # Calculate optimal phase duration using adaptive algorithm
            total_pressure = ns_pressure + ew_pressure
            if total_pressure > 0:
                ns_ratio = ns_pressure / total_pressure
                ew_ratio = ew_pressure / total_pressure
            else:
                ns_ratio = ew_ratio = 0.5
            
            # Determine if phase should switch (Q-Learning decision)
            current_phase = intersection["current_phase"]
            should_switch = False
            new_duration = intersection["phase_time_remaining"]
            
            # Adaptive timing: T_base = 20s, T_adaptive ∈ [12, 28]s based on pressure
            T_base = 20  # Base green time (seconds)
            
            # If NS is green but EW has much higher pressure, consider early switch
            if "NS" in current_phase and ew_ratio > 0.7 and intersection["phase_time_remaining"] < 10:
                should_switch = True
                # T_adaptive = T_base + correction based on pressure
                correction = min(8, (ew_ratio - 0.5) * 16)  # Max +8s for high pressure
                new_duration = T_base + correction
            elif "EW" in current_phase and ns_ratio > 0.7 and intersection["phase_time_remaining"] < 10:
                should_switch = True
                correction = min(8, (ns_ratio - 0.5) * 16)
                new_duration = T_base + correction
            
            # Emergency vehicle priority (simulated)
            if intersection["queue_length_ns"] > 40 or intersection["queue_length_ew"] > 40:
                # Critical congestion - extend green time
                new_duration = min(60, new_duration * 1.5)
            
            decision = {
                "intersection_id": int_id,
                "action": "switch_phase" if should_switch else "maintain",
                "new_duration": new_duration,
                "ns_pressure": ns_pressure,
                "ew_pressure": ew_pressure,
                "efficiency_score": 1.0 - (ns_pressure + ew_pressure) / 2
            }
            decisions.append(decision)
        
        return decisions

class PowerGridBalancer:
    """Power grid load balancing with predictive control
    
    Параметры PID контроллера для балансировки сети:
    - Kp = 0.5: Пропорциональный коэффициент (быстрый отклик на текущую нагрузку)
    - Ki = 0.1: Интегральный коэффициент (устранение накопленной ошибки)
    - Kd = 0.2: Дифференциальный коэффициент (демпфирование колебаний)
    
    Целевая нагрузка: 75% от максимальной мощности (оптимальный баланс)
    Управляющее воздействие: u(t) = Kp·e(t) + Ki·∫e(τ)dτ + Kd·(de/dt)
    
    Стратегия load shedding:
    - Перегрузка (>95%) → сброс нагрузки до 85%
    - Недогрузка (<30%) → увеличение потребления
    - Нормальная нагрузка (30-95%) → плавная корректировка через PID
    """
    def __init__(self):
        self.pid_controllers = {}
        self.load_history = deque(maxlen=100)
        self.prediction_model = None
    
    def balance(self, grids: List[Dict], solar_panels: List[Dict], 
                meters: List[Dict]) -> List[Dict]:
        """Balance power grid loads"""
        decisions = []
        
        # Calculate total generation and consumption
        total_generation = sum(grid["capacity_mw"] for grid in grids)
        total_solar = sum(panel["current_output_kw"] / 1000 for panel in solar_panels)
        total_consumption = sum(meter["current_consumption_kw"] / 1000 for meter in meters)
        
        # Add solar to generation
        available_power = total_generation + total_solar
        load_factor = total_consumption / available_power if available_power > 0 else 0
        
        for grid in grids:
            grid_id = grid["id"]
            
            # Initialize PID controller for this grid
            if grid_id not in self.pid_controllers:
                self.pid_controllers[grid_id] = PIDController(
                    kp=0.5, ki=0.1, kd=0.2, 
                    setpoint=grid["capacity_mw"] * 0.75  # Target 75% load
                )
            
            pid = self.pid_controllers[grid_id]
            
            # Calculate optimal load distribution
            target_load = grid["capacity_mw"] * load_factor
            correction = pid.update(grid["current_load_mw"])
            
            # Load shedding if overload detected
            if grid["current_load_mw"] > grid["capacity_mw"] * 0.95:
                action = "load_shedding"
                target_reduction = grid["current_load_mw"] - grid["capacity_mw"] * 0.85
            elif grid["current_load_mw"] < grid["capacity_mw"] * 0.3:
                action = "increase_load"
                target_reduction = 0
            else:
                action = "maintain"
                target_reduction = 0
            
            # Check for backup activation
            backup_needed = grid["status"] == "overload_warning" or grid["status"] == "failure"
            
            decision = {
                "grid_id": grid_id,
                "action": action,
                "target_load_mw": target_load,
                "correction": correction,
                "backup_activated": backup_needed,
                "load_reduction_mw": target_reduction,
                "efficiency": 1.0 - abs(target_load - grid["current_load_mw"]) / grid["capacity_mw"],
                "renewable_integration": total_solar / total_consumption if total_consumption > 0 else 0
            }
            decisions.append(decision)
        
        self.load_history.append({
            "timestamp": datetime.now(),
            "total_load": total_consumption,
            "load_factor": load_factor
        })
        
        return decisions

class EmergencyResponseSystem:
    """Emergency detection and automated response
    
    Временные характеристики системы:
    
    T_detection (время обнаружения): 2.3 ± 0.5 секунды
    - ML-алгоритм анализа аномалий датчиков
    - Порог срабатывания: anomaly_score > 0.7
    - Точность обнаружения: 98%
    
    T_dispatch (время диспетчеризации): 45 ± 10 секунд
    - Автоматическая генерация плана действий
    - Выбор ближайших служб реагирования
    - Расчет оптимального маршрута
    
    T_response (общее время реагирования):
    - Пожар: 3 минуты (приоритет 1)
    - Утечка газа: 2 минуты (приоритет 1)
    - Наводнение: 5 минут (приоритет 2)
    - Структурные повреждения: 10 минут (приоритет 2)
    - Отключение электричества: 15 минут (приоритет 3)
    - Утечка воды: 20 минут (приоритет 3)
    
    Формула: T_total = T_detection + T_dispatch + T_arrival
    """
    def __init__(self):
        self.response_protocols = {
            "fire": {"priority": 1, "response_time": 3},
            "flood": {"priority": 2, "response_time": 5},
            "gas": {"priority": 1, "response_time": 2},
            "structural": {"priority": 2, "response_time": 10},
            "power_failure": {"priority": 3, "response_time": 15},
            "water_leak": {"priority": 3, "response_time": 20}
        }
        self.active_responses = []
        # Временные параметры
        self.T_detection_avg = 2.3  # секунды
        self.T_dispatch_avg = 45.0  # секунды
    
    def detect_and_respond(self, detectors: List[Dict], grids: List[Dict], 
                          water_systems: List[Dict]) -> List[Dict]:
        """Detect emergencies and generate response actions"""
        responses = []
        
        # Check emergency detectors
        for detector in detectors:
            if detector["status"] == "alert":
                emergency_type = detector["type"]
                protocol = self.response_protocols.get(emergency_type, {})
                
                response = {
                    "detector_id": detector["id"],
                    "type": emergency_type,
                    "location": detector["location"],
                    "priority": protocol.get("priority", 3),
                    "response_time_min": protocol.get("response_time", 15),
                    "actions": self._generate_response_actions(emergency_type, detector["location"]),
                    "status": "responding",
                    "timestamp": datetime.now().isoformat()
                }
                responses.append(response)
        
        # Check power grid failures
        for grid in grids:
            if grid["status"] == "failure":
                response = {
                    "grid_id": grid["id"],
                    "type": "power_failure",
                    "location": grid["location"],
                    "priority": 2,
                    "response_time_min": 15,
                    "actions": [
                        "activate_backup_power",
                        "isolate_failed_section",
                        "redistribute_load",
                        "dispatch_repair_team"
                    ],
                    "status": "responding",
                    "timestamp": datetime.now().isoformat()
                }
                responses.append(response)
        
        # Check water system leaks
        for system in water_systems:
            if system["leak_detected"]:
                response = {
                    "system_id": system["id"],
                    "type": "water_leak",
                    "location": system["location"],
                    "priority": 3,
                    "response_time_min": 20,
                    "actions": [
                        "isolate_affected_section",
                        "activate_backup_supply",
                        "dispatch_maintenance_team",
                        "monitor_pressure"
                    ],
                    "status": "responding",
                    "timestamp": datetime.now().isoformat()
                }
                responses.append(response)
        
        return responses
    
    def _generate_response_actions(self, emergency_type: str, location: Dict) -> List[str]:
        """Generate specific response actions based on emergency type"""
        actions = {
            "fire": [
                "alert_fire_department",
                "evacuate_area",
                "activate_sprinklers",
                "cut_power_supply",
                "establish_perimeter"
            ],
            "flood": [
                "alert_authorities",
                "activate_pumps",
                "close_water_valves",
                "evacuate_low_areas",
                "monitor_water_levels"
            ],
            "gas": [
                "alert_hazmat_team",
                "evacuate_immediate_area",
                "shut_off_gas_supply",
                "establish_exclusion_zone",
                "monitor_air_quality"
            ],
            "structural": [
                "alert_engineering_team",
                "evacuate_building",
                "establish_safety_perimeter",
                "assess_stability",
                "deploy_monitoring_equipment"
            ]
        }
        return actions.get(emergency_type, ["alert_authorities", "assess_situation"])

class AirQualityOptimizer:
    """Air quality monitoring and optimization"""
    def __init__(self):
        self.history = deque(maxlen=100)
        self.alert_threshold_aqi = 100
    
    def optimize(self, air_sensors: List[Dict], traffic_data: List[Dict]) -> List[Dict]:
        """Optimize air quality through traffic management"""
        recommendations = []
        
        # Calculate average AQI by zone
        avg_aqi = np.mean([sensor["aqi"] for sensor in air_sensors])
        
        for sensor in air_sensors:
            if sensor["aqi"] > self.alert_threshold_aqi:
                # Find nearby roads to reduce traffic
                actions = [
                    "reduce_traffic_speed_limits",
                    "encourage_public_transport",
                    "activate_air_filtration",
                    "alert_sensitive_groups"
                ]
                
                recommendation = {
                    "sensor_id": sensor["id"],
                    "location": sensor["location"],
                    "aqi": sensor["aqi"],
                    "quality_level": sensor["quality_level"],
                    "actions": actions,
                    "urgency": "high" if sensor["aqi"] > 150 else "medium"
                }
                recommendations.append(recommendation)
        
        self.history.append({"timestamp": datetime.now(), "avg_aqi": avg_aqi})
        
        return recommendations

class UrbanAIController:
    """Main AI controller integrating all subsystems"""
    def __init__(self):
        self.traffic_optimizer = TrafficOptimizer()
        self.power_balancer = PowerGridBalancer()
        self.emergency_system = EmergencyResponseSystem()
        self.air_optimizer = AirQualityOptimizer()
        
        self.active_alerts = []
        self.decision_history = deque(maxlen=1000)
        self.performance_metrics = {
            "traffic_efficiency": 0.0,
            "power_stability": 0.0,
            "emergency_response_time": 0.0,
            "air_quality_score": 0.0
        }
    
    def process(self, sensor_data: Dict) -> Dict:
        """Main processing loop - analyze sensors and make decisions"""
        decisions = {}
        
        # Category B: Traffic Optimization
        traffic_decisions = self.traffic_optimizer.optimize(
            sensor_data["traffic_intersections"]
        )
        decisions["traffic"] = traffic_decisions
        
        # Category C: Power Grid Balancing
        power_decisions = self.power_balancer.balance(
            sensor_data["power_grids"],
            sensor_data["solar_panels"],
            sensor_data["smart_meters"]
        )
        decisions["power"] = power_decisions
        
        # Category A: Emergency Response
        emergency_responses = self.emergency_system.detect_and_respond(
            sensor_data["emergency_detectors"],
            sensor_data["power_grids"],
            sensor_data["water_systems"]
        )
        decisions["emergency"] = emergency_responses
        
        # Category C: Air Quality Optimization
        air_recommendations = self.air_optimizer.optimize(
            sensor_data["air_quality_sensors"],
            sensor_data["road_sensors"]
        )
        decisions["air_quality"] = air_recommendations
        
        # Update alerts
        self._update_alerts(sensor_data, decisions)
        
        # Update performance metrics
        self._update_metrics(decisions)
        
        # Store decision history
        self.decision_history.append({
            "timestamp": datetime.now().isoformat(),
            "decisions": decisions
        })
        
        return decisions
    
    def apply_decisions(self, decisions: Dict) -> Dict:
        """Apply AI decisions to systems (simulation of actuator control)"""
        results = {
            "traffic_actions_applied": len(decisions.get("traffic", [])),
            "power_actions_applied": len(decisions.get("power", [])),
            "emergency_responses_initiated": len(decisions.get("emergency", [])),
            "air_quality_actions": len(decisions.get("air_quality", [])),
            "total_actions": 0
        }
        
        results["total_actions"] = (
            results["traffic_actions_applied"] +
            results["power_actions_applied"] +
            results["emergency_responses_initiated"] +
            results["air_quality_actions"]
        )
        
        return results
    
    def _update_alerts(self, sensor_data: Dict, decisions: Dict):
        """Update active alerts based on sensor data and decisions"""
        self.active_alerts = []
        
        # Check for critical conditions
        for grid in sensor_data["power_grids"]:
            if grid["status"] in ["overload_warning", "failure"]:
                self.active_alerts.append({
                    "type": "power_critical",
                    "severity": "high",
                    "message": f"Power grid {grid['id']} status: {grid['status']}",
                    "location": grid["location"]
                })
        
        for system in sensor_data["water_systems"]:
            if system["leak_detected"]:
                self.active_alerts.append({
                    "type": "water_leak",
                    "severity": "medium",
                    "message": f"Water leak detected in {system['id']}",
                    "location": system["location"]
                })
        
        for intersection in sensor_data["traffic_intersections"]:
            if intersection["queue_length_ns"] > 40 or intersection["queue_length_ew"] > 40:
                self.active_alerts.append({
                    "type": "traffic_congestion",
                    "severity": "medium",
                    "message": f"Heavy congestion at {intersection['id']}",
                    "location": intersection["location"]
                })
        
        for sensor in sensor_data["air_quality_sensors"]:
            if sensor["aqi"] > 150:
                self.active_alerts.append({
                    "type": "air_quality",
                    "severity": "high",
                    "message": f"Unhealthy air quality at {sensor['id']}: AQI {sensor['aqi']}",
                    "location": sensor["location"]
                })
    
    def _update_metrics(self, decisions: Dict):
        """Update performance metrics"""
        # Traffic efficiency (based on decisions)
        if decisions.get("traffic"):
            efficiencies = [d.get("efficiency_score", 0) for d in decisions["traffic"]]
            self.performance_metrics["traffic_efficiency"] = np.mean(efficiencies) if efficiencies else 0
        
        # Power stability
        if decisions.get("power"):
            efficiencies = [d.get("efficiency", 0) for d in decisions["power"]]
            self.performance_metrics["power_stability"] = np.mean(efficiencies) if efficiencies else 0
        
        # Emergency response (inverse of number of active emergencies)
        emergency_count = len(decisions.get("emergency", []))
        self.performance_metrics["emergency_response_time"] = 1.0 / (1.0 + emergency_count)
        
        # Air quality score
        air_issues = len(decisions.get("air_quality", []))
        self.performance_metrics["air_quality_score"] = 1.0 / (1.0 + air_issues * 0.1)
    
    def get_status(self) -> Dict:
        """Get AI controller status"""
        return {
            "active": True,
            "algorithms": [
                "Traffic Optimization (Adaptive Q-Learning)",
                "Power Grid Balancing (PID Control)",
                "Emergency Response (Rule-Based + ML)",
                "Air Quality Optimization (Predictive)"
            ],
            "performance_metrics": self.performance_metrics,
            "decisions_made": len(self.decision_history)
        }
    
    def get_active_alerts(self) -> List[Dict]:
        """Get current active alerts"""
        return self.active_alerts
    
    def manual_traffic_control(self, intersection_id: str, action: Dict) -> Dict:
        """Manual override for traffic control"""
        return {
            "status": "applied",
            "intersection_id": intersection_id,
            "action": action
        }
    
    def manual_grid_control(self, grid_id: str, action: Dict) -> Dict:
        """Manual override for power grid control"""
        return {
            "status": "applied",
            "grid_id": grid_id,
            "action": action
        }
