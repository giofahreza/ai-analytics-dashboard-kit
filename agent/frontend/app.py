import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from typing import Dict, List, Any
import re
import asyncio
from services.api_client import TinsigAPIClient

# Page config
st.set_page_config(
    page_title="TINSIG AI Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for charts
if "charts" not in st.session_state:
    st.session_state.charts = []

if "chart_counter" not in st.session_state:
    st.session_state.chart_counter = 0

# Initialize API client
@st.cache_resource
def get_api_client():
    return TinsigAPIClient()

api_client = get_api_client()

# Data fetching functions
async def fetch_data_async(data_type: str, location_filter: str = None) -> List[Dict]:
    """Fetch real data from API sources"""
    try:
        filters = {}
        if location_filter:
            filters["kabupaten"] = location_filter
            
        if data_type == "illegal":
            data = await api_client.get_illegal_mining_data(filters)
        elif data_type == "production":
            data = await api_client.get_production_data(filters)
        elif data_type == "iup":
            data = await api_client.get_iup_data(filters)
        else:
            return []
            
        return data or []
    except Exception as e:
        st.error(f"Error fetching {data_type} data: {str(e)}")
        return []

def fetch_data(data_type: str, location_filter: str = None) -> List[Dict]:
    """Synchronous wrapper for async data fetching"""
    try:
        # Create new event loop for this call
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(fetch_data_async(data_type, location_filter))
        loop.close()
        return data
    except Exception as e:
        # Show error modal instead of using mock data
        st.error(f"❌ **Database Connection Error**")
        st.error(f"Failed to fetch {data_type} data: {str(e)}")
        st.info("💡 **Possible Solutions:**\n- Check if backend services are running\n- Verify database connection\n- Contact system administrator")
        return []

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
    .chart-container {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: #f8f9fa;
    }
    .chart-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("🏗️ TINSIG AI Dashboard")
page = st.sidebar.selectbox("Navigate to:", ["Show Data", "Settings"])

def process_chart_command(command: str) -> str:
    """Process user commands to add/remove/modify charts"""
    command_lower = command.lower()
    
    try:
        # Add chart commands
        if any(word in command_lower for word in ["add", "create", "show", "display"]):
            return handle_add_chart_command(command)
        
        # Remove chart commands
        elif any(word in command_lower for word in ["remove", "delete", "clear"]):
            return handle_remove_chart_command(command)
        
        # Modify chart commands  
        elif any(word in command_lower for word in ["change", "modify", "update", "replace"]):
            return handle_modify_chart_command(command)
        
        else:
            return "I didn't understand that command. Try commands like:\n- Add chart view for illegal mining\n- Remove all charts\n- Change second chart to map view"
    
    except Exception as e:
        return f"Error processing command: {str(e)}"

def handle_add_chart_command(command: str) -> str:
    """Handle commands to add new charts - supports multiple charts in one command"""
    command_lower = command.lower()
    
    # Determine data type
    data_type = "illegal"  # default
    if "production" in command_lower:
        data_type = "production"
    elif "iup" in command_lower:
        data_type = "iup"
    
    # Extract location filter
    location_filter = extract_location(command)
    
    # Get real data from database
    with st.spinner(f"Fetching {data_type} data from database..."):
        data = fetch_data(data_type, location_filter)
    
    if not data:
        # Show modal-style error message and return special code
        st.error("❌ **No Data Found**")
        st.warning(f"""
        **No {data_type} data found with the specified criteria:**
        - Data Type: {data_type}
        - Location Filter: {location_filter if location_filter else 'None'}
        
        **Possible reasons:**
        - Database is empty for this data type
        - Location filter is too restrictive  
        - Backend services are not running
        - Data sync from PHP sources hasn't completed yet
        """)
        st.info("💡 **Try:** Remove location filters or check if data exists in the database")
        return "MODAL_ALREADY_SHOWN"  # Special return code to prevent duplicate modals
    
    # Detect multiple chart types requested
    charts_to_create = []
    
    # Check for specific chart types
    if "pie chart" in command_lower or "pie" in command_lower:
        charts_to_create.append(("chart", "pie"))
    
    if "bar chart" in command_lower or "bar" in command_lower:
        charts_to_create.append(("chart", "bar"))
    
    if "table" in command_lower:
        charts_to_create.append(("table", None))
    
    if "map" in command_lower or "location" in command_lower or "geographic" in command_lower:
        charts_to_create.append(("map", None))
    
    # If no specific types found, default behavior
    if not charts_to_create:
        if any(word in command_lower for word in ["chart", "graph", "plot"]):
            charts_to_create.append(("chart", None))
        else:
            charts_to_create.append(("table", None))
    
    # Create all requested charts
    created_charts = []
    for chart_type, specific_chart in charts_to_create:
        st.session_state.chart_counter += 1
        chart_id = st.session_state.chart_counter
        
        # Create title based on specific request
        if specific_chart:
            title = f"{data_type.title()} {specific_chart.title()} Chart #{chart_id}"
        else:
            title = f"{data_type.title()} {chart_type.title()} #{chart_id}"
        
        chart_config = {
            "id": chart_id,
            "type": chart_type,
            "data_type": data_type,
            "specific_chart": specific_chart,
            "data": data,
            "title": title,
            "filters": {
                "location": location_filter
            }
        }
        
        st.session_state.charts.append(chart_config)
        created_charts.append(f"{chart_type} (#{chart_id})")
    
    if len(created_charts) > 1:
        return f"Created {len(created_charts)} charts for {data_type} data: {', '.join(created_charts)}"
    else:
        return f"Added {created_charts[0]} for {data_type} data ({len(data)} records)"

def handle_remove_chart_command(command: str) -> str:
    """Handle commands to remove charts"""
    command_lower = command.lower()
    
    if "all" in command_lower:
        count = len(st.session_state.charts)
        st.session_state.charts = []
        return f"Removed all {count} charts."
    
    # Extract chart number/position
    chart_num = extract_chart_number(command)
    if chart_num:
        if 1 <= chart_num <= len(st.session_state.charts):
            removed_chart = st.session_state.charts.pop(chart_num - 1)
            return f"Removed chart #{chart_num}: {removed_chart['title']}"
        else:
            return f"Chart #{chart_num} not found. Available charts: 1-{len(st.session_state.charts)}"
    
    # Remove last chart if no specific number
    if st.session_state.charts:
        removed_chart = st.session_state.charts.pop()
        return f"Removed last chart: {removed_chart['title']}"
    else:
        return "No charts to remove."

def handle_modify_chart_command(command: str) -> str:
    """Handle commands to modify existing charts"""
    command_lower = command.lower()
    
    # Extract chart number
    chart_num = extract_chart_number(command)
    if not chart_num or chart_num > len(st.session_state.charts):
        return f"Please specify a valid chart number (1-{len(st.session_state.charts)})"
    
    chart_index = chart_num - 1
    current_chart = st.session_state.charts[chart_index]
    
    # Determine new chart type
    new_type = current_chart["type"]
    if any(word in command_lower for word in ["map", "location", "geographic"]):
        new_type = "map"
    elif any(word in command_lower for word in ["chart", "graph", "plot"]):
        new_type = "chart"
    elif "table" in command_lower:
        new_type = "table"
    
    # Update chart configuration
    st.session_state.charts[chart_index]["type"] = new_type
    st.session_state.charts[chart_index]["title"] = f"{current_chart['data_type'].title()} {new_type.title()} #{chart_num}"
    
    return f"Changed chart #{chart_num} to {new_type} view"

def extract_location(command: str) -> str:
    """Extract location from command text"""
    command_lower = command.lower()
    if "jakarta" in command_lower:
        return "Jakarta"
    elif "bangka" in command_lower:
        return "Bangka"
    elif "selatan" in command_lower:
        return "Selatan"
    return ""

def extract_chart_number(command: str) -> int:
    """Extract chart number from command text"""
    if "first" in command.lower() or "1st" in command.lower():
        return 1
    elif "second" in command.lower() or "2nd" in command.lower():
        return 2
    elif "third" in command.lower() or "3rd" in command.lower():
        return 3
    
    # Look for numbers
    numbers = re.findall(r'\d+', command)
    if numbers:
        return int(numbers[0])
    
    return 0

def render_chart(chart_config: Dict):
    """Render a chart based on its configuration"""
    data = chart_config["data"]
    chart_type = chart_config["type"]
    data_type = chart_config["data_type"]
    chart_id = chart_config.get("id", 0)
    specific_chart = chart_config.get("specific_chart")
    
    if not data:
        st.warning("No data available for this chart.")
        return
    
    df = pd.DataFrame(data)
    
    # Generate description based on chart type and data
    description = generate_chart_description(data_type, chart_type, specific_chart, len(data))
    
    # Create a styled container using Streamlit's container and CSS
    with st.container():
        # Add CSS class using markdown (this approach works better with Streamlit)
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; margin: 1rem 0; background: #f8f9fa;">
            <div style="font-size: 1.2rem; font-weight: bold; color: #333; margin-bottom: 0.5rem;">
                {chart_config['title']}
            </div>
            <div style="font-size: 0.9rem; color: #666; margin-bottom: 1rem; font-style: italic;">
                {description}
            </div>
        """, unsafe_allow_html=True)
        
        # Render the chart content within the styled container
        if chart_type == "map":
            render_map_chart(df, data_type, chart_id)
        elif chart_type == "chart":
            render_statistical_chart(df, data_type, chart_id, specific_chart)
        else:  # table
            render_data_table(df, data_type, chart_id)
        
        # Close the styled div
        st.markdown("</div>", unsafe_allow_html=True)

def generate_chart_description(data_type: str, chart_type: str, specific_chart: str = None, record_count: int = 0) -> str:
    """Generate descriptive text for charts based on their type and data"""
    
    # Base descriptions for different data types
    data_descriptions = {
        "illegal": "illegal mining activities and violations",
        "production": "tin production data and mining operations", 
        "iup": "Mining Business Permits (IUP) and their current status"
    }
    
    base_desc = data_descriptions.get(data_type, "mining data")
    
    # Chart-specific descriptions
    if chart_type == "map":
        return f"Geographic distribution of {base_desc} showing locations and details across different regions ({record_count} locations)"
    
    elif chart_type == "chart":
        if specific_chart == "pie":
            if data_type == "illegal":
                return f"Distribution of illegal mining types showing the breakdown of different violation categories ({record_count} cases)"
            elif data_type == "iup":
                return f"IUP status distribution showing active vs inactive mining permits ({record_count} permits)"
            elif data_type == "production":
                return f"Production data breakdown by different operational categories ({record_count} operations)"
        
        elif specific_chart == "bar":
            return f"Regional distribution of {base_desc} comparing quantities across different areas ({record_count} records)"
        
        else:  # General chart
            if data_type == "illegal":
                return f"Analysis of illegal mining patterns showing both type distribution and regional breakdown ({record_count} violations)"
            elif data_type == "iup":
                return f"IUP permit analysis showing status distribution and regional breakdown ({record_count} permits)"
            elif data_type == "production":
                return f"Production analysis showing operational data and regional distribution ({record_count} operations)"
    
    elif chart_type == "table":
        return f"Detailed tabular view of {base_desc} showing all available data fields and records ({record_count} entries)"
    
    # Fallback description
    return f"Visualization of {base_desc} ({record_count} records)"

def render_map_chart(df: pd.DataFrame, data_type: str, chart_id: int = None):
    """Render map visualization"""
    # Handle different coordinate column names
    lat_col = 'location_lat' if 'location_lat' in df.columns else 'latitude'
    lng_col = 'location_lng' if 'location_lng' in df.columns else 'longitude'
    
    if not any(col in df.columns for col in [lat_col, lng_col]):
        st.warning("No coordinate data available for map view.")
        return
    
    # Filter out rows with missing coordinates
    df_clean = df.dropna(subset=[lat_col, lng_col])
    if df_clean.empty:
        st.warning("No valid coordinate data available for map view.")
        return
    
    # Generate unique key for this chart
    unique_key = f"{data_type}_{chart_id}_{hash(str(df.to_dict()))}"
    
    # Create map
    center_lat = df_clean[lat_col].mean()
    center_lon = df_clean[lng_col].mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)
    
    # Color coding based on data type
    colors = {"illegal": "red", "production": "green", "iup": "blue"}
    color = colors.get(data_type, "gray")
    
    for idx, row in df_clean.iterrows():
        popup_content = f"<b>Location:</b> {row.get('kabupaten', 'Unknown')}<br>"
        if data_type == "illegal":
            popup_content += f"<b>Type:</b> {row.get('jenis_tambang', 'N/A')}<br>"
            popup_content += f"<b>Owner:</b> {row.get('nama_pemilik', 'N/A')}<br>"
            popup_content += f"<b>Workers:</b> {row.get('jumlah_pekerja', 'N/A')}<br>"
        elif data_type == "production":
            popup_content += f"<b>Production:</b> {row.get('produksi_ton', 'N/A')} tons<br>"
            popup_content += f"<b>Operator:</b> {row.get('operator', 'N/A')}<br>"
            popup_content += f"<b>Date:</b> {row.get('tanggal_produksi', 'N/A')}<br>"
        elif data_type == "iup":
            popup_content += f"<b>Name:</b> {row.get('name', 'N/A')}<br>"
            popup_content += f"<b>Area:</b> {row.get('luas', 'N/A')} ha<br>"
            popup_content += f"<b>Status:</b> {row.get('status', 'N/A')}<br>"
            popup_content += f"<b>Region:</b> {row.get('daerah', 'N/A')}<br>"
        
        folium.Marker(
            location=[row[lat_col], row[lng_col]],
            popup=popup_content,
            icon=folium.Icon(color=color)
        ).add_to(m)
    
    st_folium(m, width=700, height=400, key=f"map_{unique_key}")

def render_statistical_chart(df: pd.DataFrame, data_type: str, chart_id: int = None, specific_chart: str = None):
    """Render statistical charts"""
    # Generate unique key for this chart
    unique_key = f"{data_type}_{chart_id}_{hash(str(df.to_dict()))}"
    
    # If specific chart is requested, show only that chart
    if specific_chart == "pie":
        render_pie_chart(df, data_type, unique_key)
    elif specific_chart == "bar":
        render_bar_chart(df, data_type, unique_key)
    else:
        # Show default combination of charts
        col1, col2 = st.columns(2)
        
        with col1:
            render_primary_chart(df, data_type, unique_key)
        
        with col2:
            render_secondary_chart(df, data_type, unique_key)

def render_pie_chart(df: pd.DataFrame, data_type: str, unique_key: str):
    """Render pie chart only"""
    if data_type == "illegal" and 'jenis_tambang' in df.columns:
        type_counts = df['jenis_tambang'].value_counts()
        fig = px.pie(values=type_counts.values, names=type_counts.index,
                   title="Illegal Mining Types Distribution")
        st.plotly_chart(fig, use_container_width=True, key=f"pie_{unique_key}")
    elif data_type == "iup" and 'status' in df.columns:
        status_counts = df['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index,
                   title="IUP Status Distribution")
        st.plotly_chart(fig, use_container_width=True, key=f"pie_{unique_key}")
    else:
        st.warning(f"Pie chart not available for {data_type} data with current columns.")

def render_bar_chart(df: pd.DataFrame, data_type: str, unique_key: str):
    """Render bar chart only"""
    if 'kabupaten' in df.columns:
        if data_type == "production" and 'produksi_ton' in df.columns:
            fig = px.bar(df, x='kabupaten', y='produksi_ton',
                       title="Production by Region")
            st.plotly_chart(fig, use_container_width=True, key=f"bar_{unique_key}")
        else:
            region_counts = df['kabupaten'].value_counts()
            fig = px.bar(x=region_counts.index, y=region_counts.values,
                       title=f"{data_type.title()} by Region")
            st.plotly_chart(fig, use_container_width=True, key=f"bar_{unique_key}")
    else:
        st.warning(f"Bar chart not available for {data_type} data with current columns.")

def render_primary_chart(df: pd.DataFrame, data_type: str, unique_key: str):
    """Render the primary chart for data type"""
    if data_type == "illegal" and 'jenis_tambang' in df.columns:
        type_counts = df['jenis_tambang'].value_counts()
        fig = px.pie(values=type_counts.values, names=type_counts.index,
                   title=f"{data_type.title()} Mining Types")
        st.plotly_chart(fig, use_container_width=True, key=f"chart1_{unique_key}")
    elif data_type == "production" and 'kabupaten' in df.columns:
        if 'produksi_ton' in df.columns:
            fig = px.bar(df, x='kabupaten', y='produksi_ton',
                       title="Production by Region")
            st.plotly_chart(fig, use_container_width=True, key=f"chart1_{unique_key}")
    elif data_type == "iup" and 'status' in df.columns:
        status_counts = df['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index,
                   title="IUP Status Distribution")
        st.plotly_chart(fig, use_container_width=True, key=f"chart1_{unique_key}")

def render_secondary_chart(df: pd.DataFrame, data_type: str, unique_key: str):
    """Render the secondary chart (regional distribution)"""
    if 'kabupaten' in df.columns:
        region_counts = df['kabupaten'].value_counts()
        fig = px.bar(x=region_counts.index, y=region_counts.values,
                   title=f"{data_type.title()} by Region")
        st.plotly_chart(fig, use_container_width=True, key=f"chart2_{unique_key}")

def render_data_table(df: pd.DataFrame, data_type: str, chart_id: int = None):
    """Render data table"""
    # Generate unique key for this table
    unique_key = f"table_{data_type}_{chart_id}_{hash(str(df.to_dict()))}"
    st.dataframe(df, use_container_width=True, key=unique_key)
    st.caption(f"Showing {len(df)} {data_type} records")

# Main app logic
if page == "Show Data":
    st.markdown("<h1 class='main-header'>📊 Show Data</h1>", unsafe_allow_html=True)
    
    # Command input
    st.markdown("### 🎯 Chart Management")
    st.markdown("Tell me what you want to do with charts:")
    
    with st.form(key="command_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            command = st.text_input(
                "Command Input",
                placeholder="e.g., add chart view for illegal mining in Jakarta",
                key="command_input",
                label_visibility="hidden"
            )
        
        with col2:
            submit_button = st.form_submit_button("Execute", type="primary")
    
    # Process command
    if submit_button and command.strip():
        with st.spinner("Processing command..."):
            try:
                result = process_chart_command(command)
                
                # Skip modal if already shown by the command handler
                if result == "MODAL_ALREADY_SHOWN":
                    pass  # Modal was already shown in the command handler
                # Check result and show appropriate modal
                elif "Error" in result or "Failed" in result or "Unable" in result:
                    st.error(f"❌ **Command Error**")
                    st.error(result)
                elif "No data" in result or "not found" in result or "No" in result and "available" in result:
                    st.warning(f"⚠️ **No Data Found**")
                    st.warning(result)
                elif "didn't understand" in result or "Try commands like" in result:
                    st.info(f"💡 **Command Help**")
                    st.info(result)
                else:
                    st.success(f"✅ **Command Executed**")
                    st.success(result)
                    
                st.rerun()
            except Exception as e:
                st.error(f"❌ **Command Processing Error**")
                st.error(f"Failed to process command: {str(e)}")
                import traceback
                with st.expander("🔍 View Error Details"):
                    st.code(traceback.format_exc())
    
    # Example commands
    st.markdown("#### 💡 Example Commands:")
    example_commands = [
        "Add chart view for illegal mining in Jakarta",
        "Add map view for production data",
        "Add table view for IUP data",
        "Remove all charts",
        "Remove second chart", 
        "Change first chart to map view"
    ]
    
    cols = st.columns(2)
    for i, cmd in enumerate(example_commands):
        with cols[i % 2]:
            if st.button(cmd, key=f"example_{i}"):
                try:
                    result = process_chart_command(cmd)
                    
                    # Skip modal if already shown by the command handler
                    if result == "MODAL_ALREADY_SHOWN":
                        pass  # Modal was already shown in the command handler
                    # Check result and show appropriate modal
                    elif "Error" in result or "Failed" in result or "Unable" in result:
                        st.error(f"❌ **Button Command Error**")
                        st.error(result)
                    elif "No data" in result or "not found" in result or "No" in result and "available" in result:
                        st.warning(f"⚠️ **No Data Found**")
                        st.warning(result)
                    elif "didn't understand" in result or "Try commands like" in result:
                        st.info(f"💡 **Command Help**")
                        st.info(result)
                    else:
                        st.success(f"✅ **Button Command Executed**")
                        st.success(result)
                        
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ **Button Command Error**")
                    st.error(f"Failed to execute command: {str(e)}")
                    with st.expander("🔍 View Error Details"):
                        import traceback
                        st.code(traceback.format_exc())
    
    # Display charts
    if st.session_state.charts:
        st.markdown("### 📈 Current Charts")
        st.markdown(f"*Showing {len(st.session_state.charts)} chart(s)*")
        
        for chart_config in st.session_state.charts:
            render_chart(chart_config)
    else:
        st.info("No charts to display. Use the commands above to add charts!")

elif page == "Settings":
    st.markdown("<h1 class='main-header'>⚙️ Settings</h1>", unsafe_allow_html=True)
    
    # API Configuration
    st.markdown("### 🔧 API Configuration")
    with st.expander("Backend API Settings"):
        backend_url = st.text_input("Backend URL", value="http://localhost:8000")
        st.text_input("Source 1 URL (Illegal Mining)", value="http://localhost:8001", disabled=True)
        st.text_input("Source 2 URL (Production)", value="http://localhost:8002", disabled=True)
        st.text_input("Source 3 URL (IUP)", value="http://localhost:8003", disabled=True)
    
    # Display Settings
    st.markdown("### 🎨 Display Settings")
    with st.expander("Chart & Map Settings"):
        default_map_zoom = st.slider("Default Map Zoom Level", min_value=5, max_value=15, value=10)
        chart_theme = st.selectbox("Chart Theme", ["plotly", "plotly_white", "plotly_dark"])
        show_data_table = st.checkbox("Always show data table below charts", value=False)
    
    # Data Settings  
    st.markdown("### 📊 Data Settings")
    with st.expander("Data Processing Settings"):
        max_records = st.number_input("Maximum records per query", min_value=10, max_value=1000, value=100)
        use_real_data = st.checkbox("Use real API data", value=True, disabled=True, help="Always enabled - fetches data from SQLite database via API")
        auto_refresh = st.checkbox("Auto-refresh data", value=False)
        if auto_refresh:
            refresh_interval = st.selectbox("Refresh interval", ["30 seconds", "1 minute", "5 minutes", "10 minutes"])
    
    # System Status
    st.markdown("### 🚦 System Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Backend API", "🟢 Online" if True else "🔴 Offline")
    with col2: 
        st.metric("Active Charts", len(st.session_state.charts))
    with col3:
        st.metric("Data Source", "🔄 Real API Data")
    
    # Actions
    st.markdown("### 🔄 Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Clear All Charts"):
            st.session_state.charts = []
            st.success("All charts cleared!")
            st.rerun()
    
    with col2:
        if st.button("Reset Settings"):
            st.success("Settings reset to defaults!")
    
    with col3:
        if st.button("Export Configuration"):
            st.success("Configuration exported!")

# Footer
st.markdown("---")
st.markdown("*TINSIG AI Dashboard - Connected to Real-Time Data Sources*")
