import streamlit as st
import asyncio
import json
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import st_folium
import folium

from services.api_client import TinsigAPIClient
from components.charts import create_production_chart, create_mining_heatmap
from components.maps import create_interactive_map
from components.chat import render_chat_interface
from utils.constants import KABUPATEN_OPTIONS, CHART_THEMES

# Page config
st.set_page_config(
    page_title="TINSIG AI Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize API client
@st.cache_resource
def get_api_client():
    return TinsigAPIClient()

api_client = get_api_client()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🏗️ TINSIG AI Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Filters & Settings")
        
        # Date range filter
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            max_value=datetime.now()
        )
        
        # Location filter
        selected_kabupaten = st.multiselect(
            "Select Kabupaten",
            options=KABUPATEN_OPTIONS,
            default=KABUPATEN_OPTIONS[:2] if len(KABUPATEN_OPTIONS) > 2 else KABUPATEN_OPTIONS
        )
        
        # Refresh data button
        if st.button("🔄 Refresh Data", type="primary"):
            st.cache_data.clear()
            st.rerun()
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🗺️ Interactive Maps", "🤖 AI Assistant", "⚙️ Settings"])
    
    with tab1:
        render_overview_tab(selected_kabupaten, date_range)
    
    with tab2:
        render_maps_tab(selected_kabupaten)
    
    with tab3:
        render_ai_chat_tab()
    
    with tab4:
        render_settings_tab()

def render_overview_tab(kabupaten_filter, date_range):
    """Render the main overview dashboard"""
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Fetch illegal mining count
        try:
            illegal_count = asyncio.run(api_client.get_illegal_mining_count(kabupaten_filter))
        except:
            illegal_count = 0
        st.metric(
            label="🚨 Illegal Mining Sites",
            value=illegal_count,
            delta="12 new this month"
        )
    
    with col2:
        # Fetch production total
        try:
            production_total = asyncio.run(api_client.get_production_total(kabupaten_filter))
        except:
            production_total = 0.0
        st.metric(
            label="⛏️ Total Production (tons)",
            value=f"{production_total:.1f}",
            delta="5.2% vs last month"
        )
    
    with col3:
        # Active IUPs
        try:
            active_iups = asyncio.run(api_client.get_active_iups_count())
        except:
            active_iups = 0
        st.metric(
            label="📋 Active IUPs",
            value=active_iups,
            delta="2 renewed"
        )
    
    with col4:
        # Risk score (calculated)
        risk_score = 7.3  # TODO: Calculate from AI model
        st.metric(
            label="⚠️ Risk Score",
            value=f"{risk_score}/10",
            delta="-0.5 improved"
        )
    
    st.markdown("---")
    
    # Charts row
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Production Trends")
        # Production chart
        try:
            production_data = asyncio.run(api_client.get_production_trends(kabupaten_filter))
            if production_data:
                chart = create_production_chart(production_data)
                st.plotly_chart(chart, use_container_width=True)
            else:
                st.info("No production data available for selected filters")
        except Exception as e:
            st.error(f"Failed to load production data: {e}")
    
    with col2:
        st.subheader("🏗️ Mining Types Distribution")
        # Mining types pie chart
        try:
            mining_types = asyncio.run(api_client.get_mining_types_distribution())
            if mining_types:
                fig = px.pie(
                    values=list(mining_types.values()),
                    names=list(mining_types.keys()),
                    title="Illegal Mining Types"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No mining type data available")
        except Exception as e:
            st.error(f"Failed to load mining types: {e}")
    
    # Recent activities
    st.subheader("🕒 Recent Activities")
    try:
        recent_data = asyncio.run(api_client.get_recent_activities(limit=10))
        if recent_data:
            df = pd.DataFrame(recent_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No recent activities available")
    except Exception as e:
        st.error(f"Failed to load recent activities: {e}")

def render_maps_tab(kabupaten_filter):
    """Render interactive maps"""
    
    st.subheader("🗺️ Interactive Mining Data Map")
    
    # Map controls
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        map_layer = st.selectbox(
            "Select Layer",
            ["Illegal Mining", "Production Sites", "IUP Boundaries", "All Layers"]
        )
    
    with col2:
        map_style = st.selectbox(
            "Map Style", 
            ["OpenStreetMap", "Satellite", "Terrain"]
        )
    
    with col3:
        show_heatmap = st.checkbox("Show Heatmap", value=True)
        show_clusters = st.checkbox("Show Clusters", value=False)
    
    # Generate map
    try:
        map_data = asyncio.run(api_client.get_map_data(
            layer=map_layer.lower().replace(" ", "_"),
            kabupaten=kabupaten_filter
        ))
        
        if map_data:
            # Create interactive map
            m = create_interactive_map(
                data=map_data,
                layer_type=map_layer,
                style=map_style,
                show_heatmap=show_heatmap,
                show_clusters=show_clusters
            )
            
            # Display map
            map_data_return = st_folium(m, width=1200, height=600)
            
            # Show selected feature info
            if map_data_return.get('last_object_clicked'):
                st.subheader("📍 Selected Location Details")
                selected_data = map_data_return['last_object_clicked']
                st.json(selected_data)
        else:
            st.info("No map data available for selected filters")
            
    except Exception as e:
        st.error(f"Failed to load map data: {e}")

def render_ai_chat_tab():
    """Render AI assistant chat interface"""
    
    st.subheader("🤖 AI Mining Data Assistant")
    st.markdown("Ask questions about mining data, get insights, and generate reports using natural language.")
    
    # Chat interface
    render_chat_interface(api_client)

def render_settings_tab():
    """Render settings and configuration"""
    
    st.subheader("⚙️ Dashboard Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Data Source Configuration**")
        
        # API endpoints status
        st.write("Source API Status:")
        
        # Check API health
        try:
            source1_status = asyncio.run(api_client.check_source_health("source1"))
            source2_status = asyncio.run(api_client.check_source_health("source2")) 
            source3_status = asyncio.run(api_client.check_source_health("source3"))
            
            st.success(f"Source 1 (Illegal Mining): {'✅ Online' if source1_status else '❌ Offline'}")
            st.success(f"Source 2 (Production): {'✅ Online' if source2_status else '❌ Offline'}")
            st.success(f"Source 3 (IUP): {'✅ Online' if source3_status else '❌ Offline'}")
        except Exception as e:
            st.error(f"Failed to check API status: {e}")
        
        # Data sync settings
        st.write("**Data Synchronization**")
        auto_sync = st.checkbox("Auto-sync every hour", value=True)
        
        if st.button("🔄 Sync Now"):
            with st.spinner("Syncing data from source APIs..."):
                try:
                    result = asyncio.run(api_client.trigger_data_sync())
                    if result:
                        st.success("Data sync completed successfully!")
                    else:
                        st.error("Data sync failed. Check logs for details.")
                except Exception as e:
                    st.error(f"Data sync error: {e}")
    
    with col2:
        st.write("**AI Model Settings**")
        
        # Model selection
        selected_model = st.selectbox(
            "AI Model",
            ["Gemini 1.5 Pro", "Gemini 1.0 Pro", "GPT-4 (Fallback)"]
        )
        
        # Temperature setting
        temperature = st.slider("Response Creativity", 0.0, 1.0, 0.1, 0.1)
        
        # Max tokens
        max_tokens = st.number_input("Max Response Length", 100, 4000, 1000)
        
        st.write("**Chart Preferences**")
        
        # Theme selection
        chart_theme = st.selectbox("Chart Theme", CHART_THEMES)
        
        # Color palette
        color_palette = st.selectbox(
            "Color Palette",
            ["Default", "Viridis", "Plasma", "Inferno", "Magma"]
        )
        
        if st.button("💾 Save Settings"):
            # TODO: Implement settings persistence
            st.success("Settings saved successfully!")

if __name__ == "__main__":
    main()
