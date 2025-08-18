import folium
import pandas as pd
from typing import Dict, List, Any, Optional

def create_interactive_map(
    data: Dict[str, Any],
    layer_type: str = "all",
    style: str = "OpenStreetMap",
    show_heatmap: bool = True,
    show_clusters: bool = False
) -> folium.Map:
    """Create interactive map with mining data"""
    
    # Default center (Indonesia)
    center_lat, center_lon = -2.5, 118.0
    
    # Create base map
    if style == "Satellite":
        tiles = 'Esri.WorldImagery'
    elif style == "Terrain":
        tiles = 'OpenTopoMap'
    else:
        tiles = 'OpenStreetMap'
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=5,
        tiles=tiles
    )
    
    # Process GeoJSON data
    if data and data.get("features"):
        features = data["features"]
        
        # Add markers for each feature
        for feature in features:
            if feature.get("geometry") and feature["geometry"].get("coordinates"):
                coords = feature["geometry"]["coordinates"]
                props = feature.get("properties", {})
                
                # Reverse coordinates for folium (lat, lon)
                if len(coords) >= 2:
                    lat, lon = coords[1], coords[0]
                    
                    # Create popup content
                    popup_content = f"""
                    <b>{props.get('name', 'Mining Site')}</b><br>
                    Type: {props.get('type', 'Unknown')}<br>
                    Location: {props.get('kabupaten', 'Unknown')}<br>
                    Coordinates: {lat:.6f}, {lon:.6f}
                    """
                    
                    # Choose marker color based on type
                    color = _get_marker_color(props.get('type', ''))
                    
                    folium.Marker(
                        location=[lat, lon],
                        popup=folium.Popup(popup_content, max_width=300),
                        tooltip=props.get('name', 'Mining Site'),
                        icon=folium.Icon(color=color, icon='info-sign')
                    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add fullscreen button
    from folium.plugins import Fullscreen
    Fullscreen().add_to(m)
    
    return m

def _get_marker_color(feature_type: str) -> str:
    """Get marker color based on feature type"""
    
    color_map = {
        'illegal_mining': 'red',
        'production_sites': 'blue', 
        'iup_boundaries': 'green',
        'all_layers': 'purple'
    }
    
    return color_map.get(feature_type.lower(), 'gray')

def create_heatmap_layer(coordinates: List[List[float]]) -> folium.plugins.HeatMap:
    """Create heatmap layer from coordinates"""
    
    from folium.plugins import HeatMap
    
    if not coordinates:
        return None
    
    return HeatMap(
        coordinates,
        min_opacity=0.4,
        max_zoom=18,
        radius=25,
        blur=15
    )

def create_cluster_layer(data: List[Dict[str, Any]]) -> folium.plugins.MarkerCluster:
    """Create marker cluster layer"""
    
    from folium.plugins import MarkerCluster
    
    if not data:
        return None
    
    cluster = MarkerCluster()
    
    for item in data:
        if item.get('lat') and item.get('lng'):
            folium.Marker(
                location=[item['lat'], item['lng']],
                popup=item.get('name', 'Mining Site')
            ).add_to(cluster)
    
    return cluster
