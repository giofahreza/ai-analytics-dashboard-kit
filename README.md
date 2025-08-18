# 🏗️ TINSIG AI Dashboard

> **AI-Powered Mining Data Analysis Platform**  
> A comprehensive dashboard for monitoring and analyzing Indonesian mining activities, including illegal mining detection, production tracking, and IUP (Mining Permit) management.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [System Flow](#system-flow)
- [Folder Structure](#folder-structure)
- [Design System](#design-system)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

TINSIG AI Dashboard is a modern web application built to analyze and visualize mining data across Indonesia. The system integrates multiple data sources, provides real-time monitoring capabilities, and offers intuitive data visualization through charts, maps, and tables.

### Key Capabilities:
- **Real-time Data Monitoring**: Live tracking of mining activities
- **Prompt-driven Interface**: Natural language commands for chart generation
- **Multi-source Integration**: Aggregates data from multiple PHP APIs
- **Interactive Visualizations**: Dynamic charts, maps, and data tables
- **Modal Error Handling**: User-friendly error feedback system

---

## ✨ Features

### 🎨 **Interactive Dashboard**
- **2-Page Interface**: Show Data and Settings pages
- **Prompt-driven Charts**: Create visualizations using natural language
- **Dynamic Filtering**: Filter data by location, date, and other criteria
- **Real-time Updates**: Auto-refresh capabilities for live data

### 📊 **Data Visualization**
- **Charts**: Bar charts, pie charts, line graphs
- **Maps**: Interactive geographic visualization using Folium
- **Tables**: Sortable and filterable data tables
- **Multi-chart Support**: Create and manage multiple visualizations

### 🔌 **Data Sources**
- **Illegal Mining**: Detection and tracking of unauthorized mining activities
- **Production Data**: Official mining production statistics
- **IUP Records**: Mining permit and licensing information

### 🚨 **Error Handling**
- **Modal Alerts**: Visual feedback for errors and status updates
- **Connection Monitoring**: Real-time API health checking
- **Graceful Degradation**: Fallback mechanisms for service interruptions

---

## 🏗️ Architecture

### **Technology Stack**

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Interactive web dashboard |
| **Backend API** | FastAPI | RESTful API server |
| **Database** | SQLite + SQLAlchemy | Data persistence |
| **Data Sources** | PHP APIs | External data integration |
| **Visualization** | Plotly + Folium | Charts and maps |
| **HTTP Client** | aiohttp | Async API communication |

### **System Architecture Diagram**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit     │    │    FastAPI       │    │   SQLite DB     │
│   Frontend      │◄──►│    Backend       │◄──►│   + Models      │
│   (Port 8502)   │    │   (Port 8000)    │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │
         │                        │
         ▼                        ▼
┌─────────────────┐    ┌──────────────────┐
│   API Client    │    │  Data Ingestion  │
│   (aiohttp)     │    │     Service      │
└─────────────────┘    └──────────────────┘
         │                        │
         └────────┬─────────────────┘
                  │
                  ▼
     ┌────────────────────────────────┐
     │        PHP APIs                │
     ├────────────┬────────────┬──────┤
     │Source 1    │Source 2    │Source│
     │:8001       │:8002       │3:8003│
     │Illegal     │Production  │IUP   │
     │Mining      │Data        │Data  │
     └────────────┴────────────┴──────┘
```

---

## 🔄 System Flow

### **1. Data Flow**
```
PHP APIs → Data Ingestion → SQLite Database → FastAPI → Streamlit Frontend
```

### **2. User Interaction Flow**
```
User Input → Command Processing → Data Fetching → Visualization → Display
```

### **3. Detailed Process Flow**

1. **Data Ingestion**:
   - PHP APIs serve raw data from three sources
   - Data Ingestion Service fetches and normalizes data
   - Processed data stored in SQLite database

2. **User Interaction**:
   - User enters natural language commands
   - Command processor interprets intent
   - System identifies required data type and filters

3. **Data Retrieval**:
   - API client fetches data from backend
   - Backend queries SQLite database
   - Results returned as JSON to frontend

4. **Visualization**:
   - Data processed into charts/maps/tables
   - Interactive visualizations rendered
   - User can manipulate and explore data

5. **Error Handling**:
   - Modal alerts for connection issues
   - Graceful degradation for missing data
   - User-friendly error messages

---

## 📁 Folder Structure

```
agent/
├── 📱 frontend/                    # Streamlit Web Application
│   ├── app.py                     # Main dashboard application
│   ├── __init__.py               # Python package marker
│   └── services/                 # Frontend services
│       ├── __init__.py          
│       └── api_client.py        # API communication client
│
├── ⚙️ backend/                     # FastAPI Backend Server
│   ├── main.py                   # FastAPI application entry point
│   ├── config.py                 # Application configuration
│   ├── __init__.py              
│   ├── api/                      # API endpoints
│   │   ├── __init__.py          
│   │   ├── data.py              # Data retrieval endpoints
│   │   └── health.py            # Health check endpoint
│   ├── database/                 # Database layer
│   │   ├── __init__.py          
│   │   ├── db.py                # Database connection & session
│   │   ├── models.py            # SQLAlchemy data models
│   │   └── tinsig_db.sqlite     # SQLite database file
│   ├── schemas/                  # Pydantic data schemas
│   │   └── __init__.py          
│   ├── services/                 # Business logic services
│   │   ├── __init__.py          
│   │   └── data_ingestion.py    # Data sync from PHP APIs
│   └── utils/                    # Utility functions
│       ├── __init__.py          
│       └── logger.py            # Logging configuration
│
├── 🛠️ scripts/                     # Utility Scripts
│   ├── setup_db.py              # Database initialization
│   └── ingest_data.py           # Manual data ingestion
│
├── 📄 Configuration Files
│   ├── .env                     # Environment variables (local)
│   ├── .env.example            # Environment variables template
│   ├── .gitignore              # Git ignore rules
│   ├── requirements.txt        # Python dependencies
│   └── setup.sh               # Initial setup script
│
├── 🚀 run_services.sh             # Unified service launcher
└── 🐍 venv/                       # Python virtual environment
```

### **File Descriptions**

| File | Purpose | Key Functions |
|------|---------|---------------|
| `frontend/app.py` | Main dashboard | Command processing, visualization, UI |
| `backend/main.py` | API server | FastAPI app, CORS, route registration |
| `backend/api/data.py` | Data endpoints | GET /illegal-mining, /production, /iup |
| `backend/database/models.py` | Data models | IllegalMining, Production, IUP classes |
| `services/api_client.py` | API client | Async HTTP requests, data fetching |
| `run_services.sh` | Service launcher | Starts all required services |

---

## 🎨 Design System

### **Visual Design Principles**

1. **Clean Interface**: Minimalist design with focus on data
2. **Responsive Layout**: Adapts to different screen sizes
3. **Consistent Styling**: Unified color scheme and typography
4. **Interactive Elements**: Hover effects and smooth transitions

### **Color Palette**

```css
Primary Blue:   #1f77b4  /* Headers, buttons */
Background:     #f8f9fa  /* Card backgrounds */
Success Green:  #28a745  /* Success messages */
Warning Orange: #ffc107  /* Warning alerts */
Error Red:      #dc3545  /* Error messages */
Text Dark:      #333333  /* Primary text */
Text Light:     #666666  /* Secondary text */
Border:         #dddddd  /* Card borders */
```

### **Typography**

- **Headers**: 2.5rem, bold, primary blue
- **Subheaders**: 1.2rem, bold, dark text
- **Body Text**: 1rem, regular, dark text
- **Descriptions**: 0.9rem, italic, light text

### **Component Styling**

#### **Chart Containers**
```css
.chart-container {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 1rem;
    margin: 1rem 0;
    background: #f8f9fa;
}
```

#### **Modal Alerts**
- **Success**: Green background, checkmark icon
- **Warning**: Orange background, warning icon
- **Error**: Red background, X icon
- **Info**: Blue background, info icon

---

## 🚀 Installation

### **Prerequisites**

- **Python 3.13+**
- **PHP 7.4+**
- **Git**

### **Quick Start**

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd ai-agent/agent
   ```

2. **Run Setup Script**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Start All Services**
   ```bash
   chmod +x run_services.sh
   ./run_services.sh
   ```

4. **Access Dashboard**
   - Open: http://localhost:8502

### **Manual Installation**

1. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Database**
   ```bash
   python scripts/setup_db.py
   ```

4. **Ingest Initial Data**
   ```bash
   python scripts/ingest_data.py
   ```

5. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

---

## 📊 Usage

### **Starting the Application**

```bash
./run_services.sh
```

This will start:
- **Frontend Dashboard**: http://localhost:8502
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **PHP Data Sources**: Ports 8001, 8002, 8003

### **Basic Commands**

The dashboard supports natural language commands:

#### **Adding Charts**
```
"Add chart view for illegal mining in Jakarta"
"Add map view for production data"
"Add table view for IUP data"
"Show pie chart for mining types"
"Display bar chart for production by region"
```

#### **Removing Charts**
```
"Remove all charts"
"Remove first chart"
"Remove second chart"
"Clear all visualizations"
```

#### **Modifying Charts**
```
"Change first chart to map view"
"Convert second chart to table"
"Update third chart to pie chart"
```

### **Navigation**

- **Show Data Page**: Main dashboard with charts and commands
- **Settings Page**: Configuration and system status

---

## 🔌 API Endpoints

### **Backend API (Port 8000)**

#### **Health Check**
```
GET /health
Response: {"status": "healthy", "timestamp": "..."}
```

#### **Data Endpoints**
```
GET /api/v1/data/illegal-mining?location={location}
GET /api/v1/data/production?location={location}
GET /api/v1/data/iup?location={location}
```

### **PHP Data Sources**

#### **Source 1 - Illegal Mining (Port 8001)**
```
GET /?location={location}
Response: {"data": {"data": [...mining_records]}}
```

#### **Source 2 - Production (Port 8002)**
```
GET /?location={location}
Response: {"data": {"data": [...production_records]}}
```

#### **Source 3 - IUP (Port 8003)**
```
GET /?location={location}
Response: {"data": {"data": [...iup_records]}}
```

---

## 🔧 Development

### **Adding New Features**

1. **Frontend Changes**: Edit `frontend/app.py`
2. **Backend Changes**: Add endpoints in `backend/api/`
3. **Database Changes**: Update models in `backend/database/models.py`
4. **New Data Sources**: Extend `services/api_client.py`

### **Code Style Guidelines**

- **Python**: Follow PEP 8
- **Comments**: Document complex functions
- **Type Hints**: Use for function parameters and returns
- **Error Handling**: Always include try-catch blocks
- **Async/Await**: Use for I/O operations

### **Testing**

```bash
# Test backend
cd backend
python -m pytest

# Test data ingestion
python scripts/ingest_data.py

# Manual API testing
curl http://localhost:8000/health
```

### **Database Management**

```bash
# Reset database
python scripts/setup_db.py

# Manual data sync
python scripts/ingest_data.py

# View database
sqlite3 backend/database/tinsig_db.sqlite
```

---

## 🚨 Troubleshooting

### **Common Issues**

#### **Services Won't Start**
```bash
# Check if ports are in use
lsof -i :8000  # Backend
lsof -i :8502  # Frontend

# Kill processes if needed
pkill -f uvicorn
pkill -f streamlit
```

#### **Database Connection Errors**
```bash
# Recreate database
rm backend/database/tinsig_db.sqlite
python scripts/setup_db.py
```

#### **No Data in Charts**
1. Check if PHP APIs are running
2. Run data ingestion: `python scripts/ingest_data.py`
3. Verify database has data: `sqlite3 backend/database/tinsig_db.sqlite`

#### **Module Import Errors**
```bash
# Ensure virtual environment is active
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### **Log Files**

- **Backend Logs**: Check terminal running `uvicorn`
- **Frontend Logs**: Check terminal running `streamlit`
- **Application Logs**: Stored in memory (check console)

### **Performance Issues**

1. **Slow Chart Loading**: Reduce data set size with filters
2. **Memory Usage**: Restart services periodically
3. **Network Delays**: Check PHP API response times

---

## 📞 Support

### **Getting Help**

1. **Check Logs**: Review terminal outputs for errors
2. **API Documentation**: Visit http://localhost:8000/docs
3. **Database Inspection**: Use SQLite browser tools
4. **Service Status**: Check http://localhost:8000/health

### **Development Resources**

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Streamlit Documentation**: https://docs.streamlit.io/
- **Plotly Documentation**: https://plotly.com/python/
- **SQLAlchemy Documentation**: https://docs.sqlalchemy.org/

---

## 📄 License

This project is developed for TINSIG AI Dashboard - Mining Data Analysis Platform.

---

**🎉 Happy Mining Data Analysis!**
