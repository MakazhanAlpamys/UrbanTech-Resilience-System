"""
UrbanTech Resilience System - Main Backend API
Integrated system combining:
- Emergency Infrastructure Response (Category A)
- Adaptive Smart Mobility (Category B)
- Energy Efficiency & Ecological Control (Category C)
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import json
from datetime import datetime
from typing import Dict, List
import uvicorn

from sensors import SensorNetwork
from ai_controller import UrbanAIController
from analytics import SystemAnalytics

# Global instances
sensor_network = None
ai_controller = None
analytics = None
active_connections: List[WebSocket] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global sensor_network, ai_controller, analytics
    
    # Initialize systems
    sensor_network = SensorNetwork()
    ai_controller = UrbanAIController()
    analytics = SystemAnalytics()
    
    # Start background tasks
    asyncio.create_task(simulation_loop())
    
    yield
    
    # Cleanup
    pass

app = FastAPI(
    title="UrbanTech Resilience System",
    description="Integrated urban infrastructure management system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def simulation_loop():
    """Main simulation loop - runs continuously"""
    while True:
        try:
            # Update sensor data
            sensor_data = sensor_network.update()
            
            # AI processing and decision making
            decisions = ai_controller.process(sensor_data)
            
            # Apply decisions to systems
            results = ai_controller.apply_decisions(decisions)
            
            # Update analytics
            analytics.update(sensor_data, decisions, results)
            
            # Broadcast to all connected clients
            message = {
                "timestamp": datetime.now().isoformat(),
                "sensors": sensor_data,
                "decisions": decisions,
                "results": results,
                "kpis": analytics.get_kpis(),
                "alerts": ai_controller.get_active_alerts()
            }
            
            await broadcast_message(message)
            
            # Run at 2Hz (every 0.5 seconds for real-time feel)
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"Simulation error: {e}")
            await asyncio.sleep(1)

async def broadcast_message(message: dict):
    """Broadcast message to all connected WebSocket clients"""
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except:
            disconnected.append(connection)
    
    # Remove disconnected clients
    for connection in disconnected:
        if connection in active_connections:
            active_connections.remove(connection)

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "UrbanTech Resilience System",
        "version": "1.0.0",
        "status": "operational",
        "categories": [
            "Emergency Infrastructure Response",
            "Adaptive Smart Mobility",
            "Energy Efficiency & Ecological Control"
        ]
    }

@app.get("/api/status")
async def get_status():
    """Get current system status"""
    return {
        "timestamp": datetime.now().isoformat(),
        "active_sensors": sensor_network.get_sensor_count(),
        "ai_status": ai_controller.get_status(),
        "alerts": ai_controller.get_active_alerts(),
        "uptime": analytics.get_uptime()
    }

@app.get("/api/sensors")
async def get_sensors():
    """Get all sensor data"""
    return sensor_network.get_all_data()

@app.get("/api/kpis")
async def get_kpis():
    """Get Key Performance Indicators"""
    return analytics.get_kpis()

@app.get("/api/analytics")
async def get_analytics():
    """Get detailed analytics"""
    return analytics.get_detailed_analytics()

@app.post("/api/control/traffic-light/{intersection_id}")
async def control_traffic_light(intersection_id: str, action: dict):
    """Manual control of traffic light"""
    result = ai_controller.manual_traffic_control(intersection_id, action)
    return result

@app.post("/api/control/power-grid/{grid_id}")
async def control_power_grid(grid_id: str, action: dict):
    """Manual control of power grid"""
    result = ai_controller.manual_grid_control(grid_id, action)
    return result

@app.post("/api/emergency/trigger")
async def trigger_emergency(emergency_type: str, location: dict):
    """Trigger emergency scenario for testing"""
    result = sensor_network.trigger_emergency(emergency_type, location)
    return result

@app.get("/api/simulation/config")
async def get_simulation_config():
    """Get simulation configuration"""
    return sensor_network.get_config()

@app.post("/api/simulation/config")
async def update_simulation_config(config: dict):
    """Update simulation configuration"""
    sensor_network.update_config(config)
    return {"status": "updated", "config": config}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Send initial data
        initial_data = {
            "type": "initial",
            "sensors": sensor_network.get_all_data(),
            "kpis": analytics.get_kpis(),
            "config": sensor_network.get_config()
        }
        await websocket.send_json(initial_data)
        
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            # Handle client messages if needed
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
