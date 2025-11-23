import { useState, useEffect } from 'react';
import { Activity, AlertTriangle } from 'lucide-react';

interface SensorData {
  timestamp: string;
  power_grids: any[];
  water_systems: any[];
  traffic_intersections: any[];
  road_sensors: any[];
  air_quality_sensors: any[];
  solar_panels: any[];
  smart_meters: any[];
  emergency_detectors: any[];
  parking_zones: any[];
}

interface KPIs {
  avg_vehicle_wait_time: number;
  traffic_throughput: number;
  congestion_reduction: number;
  grid_reliability: number;
  load_balance_efficiency: number;
  renewable_energy_ratio: number;
  avg_response_time_minutes: number;
  avg_aqi: number;
  overall_efficiency: number;
  cost_savings_percent: number;
  resilience_score: number;
}

interface Alert {
  type: string;
  severity: string;
  message: string;
  location: any;
}

const Dashboard = () => {
  const [connected, setConnected] = useState(false);
  const [sensorData, setSensorData] = useState<SensorData | null>(null);
  const [kpis, setKpis] = useState<KPIs | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [activeTab, setActiveTab] = useState<'overview' | 'traffic' | 'power' | 'emergency' | 'environment'>('overview');
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    // Connect to WebSocket
    const connectWebSocket = () => {
      const websocket = new WebSocket('ws://localhost:8000/ws');
      
      websocket.onopen = () => {
        console.log('Connected to UrbanTech System');
        setConnected(true);
      };
      
      websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'initial') {
          setSensorData(data.sensors);
          setKpis(data.kpis);
        } else {
          setSensorData(data.sensors);
          setKpis(data.kpis);
          setAlerts(data.alerts || []);
        }
      };
      
      websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnected(false);
      };
      
      websocket.onclose = () => {
        console.log('Disconnected from UrbanTech System');
        setConnected(false);
        // Attempt to reconnect after 3 seconds
        setTimeout(connectWebSocket, 3000);
      };
      
      setWs(websocket);
    };
    
    connectWebSocket();
    
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  const renderOverview = () => (
    <>
      {/* KPI Summary */}
      <div className="status-bar">
        <div className="status-card">
          <h3>System Efficiency</h3>
          <div className="status-value">{((kpis?.overall_efficiency || 0) * 100).toFixed(1)}%</div>
          <div className="status-label">Overall Performance</div>
        </div>
        <div className="status-card">
          <h3>Cost Savings</h3>
          <div className="status-value">${(kpis?.cost_savings_percent || 0).toFixed(0)}K</div>
          <div className="status-label">Annual Estimate</div>
        </div>
        <div className="status-card">
          <h3>Resilience Score</h3>
          <div className="status-value">{((kpis?.resilience_score || 0) * 100).toFixed(1)}%</div>
          <div className="status-label">System Stability</div>
        </div>
        <div className="status-card">
          <h3>Active Sensors</h3>
          <div className="status-value">{sensorData ? 
            (sensorData.power_grids?.length || 0) +
            (sensorData.traffic_intersections?.length || 0) +
            (sensorData.air_quality_sensors?.length || 0) +
            (sensorData.water_systems?.length || 0) : 0
          }</div>
          <div className="status-label">Monitoring Points</div>
        </div>
      </div>

      {/* Alerts */}
      {alerts && alerts.length > 0 && (
        <div className="alerts-section">
          <h2>
            <AlertTriangle size={24} />
            Active Alerts ({alerts.length})
          </h2>
          {alerts.slice(0, 5).map((alert, idx) => (
            <div key={idx} className={`alert-item severity-${alert.severity}`}>
              <div className="alert-info">
                <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
                  {alert.type.replace(/_/g, ' ').toUpperCase()}
                </div>
                <div>{alert.message}</div>
              </div>
              <span className="alert-severity">{alert.severity}</span>
            </div>
          ))}
        </div>
      )}

      {/* Main Metrics Grid */}
      <div className="grid">
        {/* Traffic Metrics */}
        <div className="card">
          <h3>
            Traffic Management
          </h3>
          <div className="kpi-grid">
            <div className="kpi-item">
              <div className="kpi-label">Avg Wait Time</div>
              <div className="kpi-value">{(kpis?.avg_vehicle_wait_time || 0).toFixed(1)}s</div>
            </div>
            <div className="kpi-item">
              <div className="kpi-label">Throughput</div>
              <div className="kpi-value">{kpis?.traffic_throughput || 0}</div>
            </div>
            <div className="kpi-item">
              <div className="kpi-label">Congestion ↓</div>
              <div className="kpi-value">{(kpis?.congestion_reduction || 0).toFixed(1)}%</div>
            </div>
            <div className="kpi-item">
              <div className="kpi-label">Intersections</div>
              <div className="kpi-value">{sensorData?.traffic_intersections?.length || 0}</div>
            </div>
          </div>
        </div>

        {/* Power Grid Metrics */}
        <div className="card">
          <h3>
            Power Grid
          </h3>
          <div className="kpi-grid">
            <div className="kpi-item">
              <div className="kpi-label">Reliability</div>
              <div className="kpi-value">{((kpis?.grid_reliability || 0) * 100).toFixed(1)}%</div>
            </div>
            <div className="kpi-item">
              <div className="kpi-label">Balance Efficiency</div>
              <div className="kpi-value">{((kpis?.load_balance_efficiency || 0) * 100).toFixed(1)}%</div>
            </div>
            <div className="kpi-item">
              <div className="kpi-label">Renewable %</div>
              <div className="kpi-value">{((kpis?.renewable_energy_ratio || 0) * 100).toFixed(1)}%</div>
            </div>
            <div className="kpi-item">
              <div className="kpi-label">Solar Output</div>
              <div className="kpi-value">
                {(sensorData?.solar_panels?.reduce((sum, p) => sum + p.current_output_kw, 0) || 0).toFixed(0)}kW
              </div>
            </div>
          </div>
        </div>

        {/* Emergency Response */}
        <div className="card">
          <h3>
            Emergency Response
          </h3>
          <div className="kpi-grid">
            <div className="kpi-item">
              <div className="kpi-label">Avg Response</div>
              <div className="kpi-value">{(kpis?.avg_response_time_minutes || 0).toFixed(1)}min</div>
            </div>
            <div className="kpi-item">
              <div className="kpi-label">Active Alerts</div>
              <div className="kpi-value">{alerts?.length || 0}</div>
            </div>
            <div className="kpi-item">
              <div className="kpi-label">Water Systems</div>
              <div className="kpi-value">{sensorData?.water_systems?.filter(w => w.status === 'operational').length || 0}/{sensorData?.water_systems?.length || 0}</div>
            </div>
            <div className="kpi-item">
              <div className="kpi-label">Detectors</div>
              <div className="kpi-value">{sensorData?.emergency_detectors?.length || 0}</div>
            </div>
          </div>
        </div>

        {/* Air Quality */}
        <div className="card">
          <h3>
            Air Quality
          </h3>
          <div className="kpi-grid">
            <div className="kpi-item">
              <div className="kpi-label">Avg AQI</div>
              <div className="kpi-value" style={{
                background: (kpis?.avg_aqi || 50) > 100 ? 
                  'linear-gradient(90deg, #ef4444 0%, #f59e0b 100%)' :
                  'linear-gradient(90deg, #34d399 0%, #3b82f6 100%)'
              }}>
                {(kpis?.avg_aqi || 0).toFixed(0)}
              </div>
            </div>
            <div className="kpi-item">
              <div className="kpi-label">Quality Level</div>
              <div className="kpi-value" style={{ fontSize: '1.2rem' }}>
                {(kpis?.avg_aqi || 50) < 50 ? 'Good' :
                 (kpis?.avg_aqi || 50) < 100 ? 'Moderate' : 'Unhealthy'}
              </div>
            </div>
            <div className="kpi-item">
              <div className="kpi-label">Sensors</div>
              <div className="kpi-value">{sensorData?.air_quality_sensors?.length || 0}</div>
            </div>
            <div className="kpi-item">
              <div className="kpi-label">Hotspots</div>
              <div className="kpi-value">
                {sensorData?.air_quality_sensors?.filter(s => s.aqi > 100).length || 0}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );

  const renderTrafficView = () => (
    <div className="grid">
      {sensorData?.traffic_intersections?.map((intersection) => (
        <div key={intersection.id} className={`card sensor-item ${
          intersection.queue_length_ns > 30 || intersection.queue_length_ew > 30 ? 'status-warning' : 'status-good'
        }`}>
          <div className="sensor-header">
            <span className="sensor-name">
              {intersection.name}
            </span>
            <span className={`sensor-status ${intersection.adaptive_mode ? 'operational' : 'warning'}`}>
              {intersection.adaptive_mode ? 'ADAPTIVE' : 'MANUAL'}
            </span>
          </div>
          <div className="sensor-metrics">
            <div className="metric">
              <span>Current Phase</span>
              <span className="metric-value">{intersection.current_phase}</span>
            </div>
            <div className="metric">
              <span>Time Remaining</span>
              <span className="metric-value">{intersection.phase_time_remaining.toFixed(0)}s</span>
            </div>
            <div className="metric">
              <span>Queue NS</span>
              <span className="metric-value">{intersection.queue_length_ns}</span>
            </div>
            <div className="metric">
              <span>Queue EW</span>
              <span className="metric-value">{intersection.queue_length_ew}</span>
            </div>
            <div className="metric">
              <span>Avg Wait</span>
              <span className="metric-value">{intersection.avg_wait_time.toFixed(1)}s</span>
            </div>
            <div className="metric">
              <span>Throughput</span>
              <span className="metric-value">{intersection.throughput}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );

  const renderPowerView = () => (
    <div className="grid">
      {sensorData?.power_grids?.map((grid) => (
        <div key={grid.id} className={`card sensor-item ${
          grid.status === 'operational' ? 'status-good' :
          grid.status.includes('warning') ? 'status-warning' : 'status-critical'
        }`}>
          <div className="sensor-header">
            <span className="sensor-name">
              {grid.name}
            </span>
            <span className={`sensor-status ${
              grid.status === 'operational' ? 'operational' : 'warning'
            }`}>
              {grid.status}
            </span>
          </div>
          <div className="sensor-metrics">
            <div className="metric">
              <span>Load:</span>
              <span className="metric-value">{grid.current_load_mw.toFixed(1)} MW</span>
            </div>
            <div className="metric">
              <span>Capacity:</span>
              <span className="metric-value">{grid.capacity_mw.toFixed(1)} MW</span>
            </div>
            <div className="metric">
              <span>Utilization:</span>
              <span className="metric-value">{((grid.current_load_mw / grid.capacity_mw) * 100).toFixed(1)}%</span>
            </div>
            <div className="metric">
              <span>Voltage:</span>
              <span className="metric-value">{grid.voltage.toFixed(1)}V</span>
            </div>
            <div className="metric">
              <span>Frequency:</span>
              <span className="metric-value">{grid.frequency.toFixed(2)}Hz</span>
            </div>
            <div className="metric">
              <span>Temp:</span>
              <span className="metric-value">{grid.transformer_temp.toFixed(1)}°C</span>
            </div>
          </div>
        </div>
      ))}

      {sensorData?.solar_panels?.map((panel) => (
        <div key={panel.id} className="card sensor-item status-good">
          <div className="sensor-header">
            <span className="sensor-name">{panel.name}</span>
            <span className="sensor-status operational">GENERATING</span>
          </div>
          <div className="sensor-metrics">
            <div className="metric">
              <span>Output:</span>
              <span className="metric-value">{panel.current_output_kw.toFixed(1)} kW</span>
            </div>
            <div className="metric">
              <span>Capacity:</span>
              <span className="metric-value">{panel.capacity_kw.toFixed(1)} kW</span>
            </div>
            <div className="metric">
              <span>Efficiency:</span>
              <span className="metric-value">{(panel.efficiency * 100).toFixed(1)}%</span>
            </div>
            <div className="metric">
              <span>Panel Temp:</span>
              <span className="metric-value">{panel.panel_temp.toFixed(1)}°C</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );

  const renderEmergencyView = () => (
    <div className="grid">
      {sensorData?.water_systems?.map((system) => (
        <div key={system.id} className={`card sensor-item ${
          system.leak_detected ? 'status-critical' :
          system.status === 'operational' ? 'status-good' : 'status-warning'
        }`}>
          <div className="sensor-header">
            <span className="sensor-name">
              {system.name}
            </span>
            <span className={`sensor-status ${
              system.status === 'operational' ? 'operational' : 'critical'
            }`}>
              {system.status}
            </span>
          </div>
          <div className="sensor-metrics">
            <div className="metric">
              <span>Pressure:</span>
              <span className="metric-value">{system.pressure_bar.toFixed(2)} bar</span>
            </div>
            <div className="metric">
              <span>Flow Rate:</span>
              <span className="metric-value">{system.flow_rate_m3h.toFixed(1)} m³/h</span>
            </div>
            <div className="metric">
              <span>Tank Level:</span>
              <span className="metric-value">{system.tank_level_percent.toFixed(1)}%</span>
            </div>
            <div className="metric">
              <span>Quality:</span>
              <span className="metric-value">{(system.quality_index * 100).toFixed(1)}%</span>
            </div>
            <div className="metric">
              <span>Leak:</span>
              <span className="metric-value" style={{ color: system.leak_detected ? '#ef4444' : '#10b981' }}>
                {system.leak_detected ? 'DETECTED' : 'None'}
              </span>
            </div>
          </div>
        </div>
      ))}

      {sensorData?.emergency_detectors?.slice(0, 6).map((detector) => (
        <div key={detector.id} className={`card sensor-item ${
          detector.status === 'alert' ? 'status-critical' : 'status-good'
        }`}>
          <div className="sensor-header">
            <span className="sensor-name">
              {detector.id} - {detector.type.toUpperCase()}
            </span>
            <span className={`sensor-status ${
              detector.status === 'alert' ? 'critical' : 'operational'
            }`}>
              {detector.status}
            </span>
          </div>
          <div className="sensor-metrics">
            <div className="metric">
              <span>Type:</span>
              <span className="metric-value">{detector.type}</span>
            </div>
            <div className="metric">
              <span>Sensitivity:</span>
              <span className="metric-value">{(detector.sensitivity * 100).toFixed(0)}%</span>
            </div>
            <div className="metric">
              <span>Location:</span>
              <span className="metric-value">
                {detector.location.x.toFixed(0)}, {detector.location.y.toFixed(0)}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );

  const renderEnvironmentView = () => (
    <div className="grid">
      {sensorData?.air_quality_sensors?.map((sensor) => (
        <div key={sensor.id} className={`card sensor-item ${
          sensor.aqi > 150 ? 'status-critical' :
          sensor.aqi > 100 ? 'status-warning' : 'status-good'
        }`}>
          <div className="sensor-header">
            <span className="sensor-name">
              {sensor.id}
            </span>
            <span className={`sensor-status ${
              sensor.aqi < 50 ? 'operational' :
              sensor.aqi < 100 ? 'warning' : 'critical'
            }`}>
              {sensor.quality_level}
            </span>
          </div>
          <div className="sensor-metrics">
            <div className="metric">
              <span>AQI:</span>
              <span className="metric-value">{sensor.aqi}</span>
            </div>
            <div className="metric">
              <span>PM2.5:</span>
              <span className="metric-value">{sensor.pm25.toFixed(1)} µg/m³</span>
            </div>
            <div className="metric">
              <span>PM10:</span>
              <span className="metric-value">{sensor.pm10.toFixed(1)} µg/m³</span>
            </div>
            <div className="metric">
              <span>CO2:</span>
              <span className="metric-value">{sensor.co2_ppm.toFixed(0)} ppm</span>
            </div>
            <div className="metric">
              <span>NO2:</span>
              <span className="metric-value">{sensor.no2.toFixed(1)} µg/m³</span>
            </div>
            <div className="metric">
              <span>O3:</span>
              <span className="metric-value">{sensor.o3.toFixed(1)} µg/m³</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );

  return (
    <div className="dashboard">
      {/* Connection Status */}
      <div className={`connection-status ${connected ? 'connected' : 'disconnected'}`}>
        <div className={`status-dot ${connected ? 'connected' : 'disconnected'}`}></div>
        {connected ? 'Connected to UrbanTech System' : 'Connecting...'}
      </div>

      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <h1>UrbanTech Resilience System</h1>
          <p>Integrated Infrastructure Management | Engineering Hackathon 2025</p>
          <p style={{ fontSize: '0.875rem', opacity: 0.7 }}>
            Category A: Emergency Response | Category B: Smart Mobility | Category C: Energy & Ecology
          </p>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="tabs">
        <button 
          className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={`tab-button ${activeTab === 'traffic' ? 'active' : ''}`}
          onClick={() => setActiveTab('traffic')}
        >
          Traffic Management
        </button>
        <button 
          className={`tab-button ${activeTab === 'power' ? 'active' : ''}`}
          onClick={() => setActiveTab('power')}
        >
          Power Grid
        </button>
        <button 
          className={`tab-button ${activeTab === 'emergency' ? 'active' : ''}`}
          onClick={() => setActiveTab('emergency')}
        >
          Emergency Systems
        </button>
        <button 
          className={`tab-button ${activeTab === 'environment' ? 'active' : ''}`}
          onClick={() => setActiveTab('environment')}
        >
          Environment
        </button>
      </div>

      {/* Content */}
      {!connected && (
        <div className="no-data">
          <Activity size={48} style={{ marginBottom: '20px', opacity: 0.5 }} />
          <div>Connecting to UrbanTech System...</div>
          <div style={{ marginTop: '10px', fontSize: '0.9rem' }}>
            Make sure the backend server is running on port 8000
          </div>
        </div>
      )}

      {connected && (
        <>
          {activeTab === 'overview' && renderOverview()}
          {activeTab === 'traffic' && renderTrafficView()}
          {activeTab === 'power' && renderPowerView()}
          {activeTab === 'emergency' && renderEmergencyView()}
          {activeTab === 'environment' && renderEnvironmentView()}
        </>
      )}
    </div>
  );
};

export default Dashboard;
