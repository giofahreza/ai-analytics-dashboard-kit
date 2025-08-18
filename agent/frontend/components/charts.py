import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any
import pandas as pd

def create_production_chart(data: List[Dict[str, Any]]) -> go.Figure:
    """Create production trends chart"""
    
    if not data:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    df = pd.DataFrame(data)
    
    fig = px.line(
        df, 
        x='date', 
        y='production',
        title='Production Trends Over Time',
        labels={'date': 'Date', 'production': 'Production (tons)'}
    )
    
    fig.update_layout(
        hovermode='x unified',
        showlegend=False
    )
    
    return fig

def create_mining_heatmap(data: List[Dict[str, Any]]) -> go.Figure:
    """Create mining activity heatmap"""
    
    if not data:
        return go.Figure()
    
    # Process data for heatmap
    df = pd.DataFrame(data)
    
    # Create heatmap based on kabupaten and mining types
    if 'kabupaten' in df.columns and 'jenis_tambang' in df.columns:
        heatmap_data = df.groupby(['kabupaten', 'jenis_tambang']).size().reset_index(name='count')
        pivot_data = heatmap_data.pivot(index='kabupaten', columns='jenis_tambang', values='count').fillna(0)
        
        fig = px.imshow(
            pivot_data,
            title="Mining Activity Heatmap by Region and Type",
            labels=dict(x="Mining Type", y="Region", color="Activity Count"),
            aspect="auto"
        )
        
        return fig
    
    return go.Figure()

def create_risk_score_gauge(score: float) -> go.Figure:
    """Create risk score gauge chart"""
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Score"},
        delta = {'reference': 5.0},
        gauge = {
            'axis': {'range': [None, 10]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 3], 'color': "lightgreen"},
                {'range': [3, 7], 'color': "yellow"},
                {'range': [7, 10], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 8
            }
        }
    ))
    
    return fig

def create_distribution_pie_chart(data: Dict[str, int], title: str) -> go.Figure:
    """Create pie chart for data distribution"""
    
    if not data:
        fig = go.Figure()
        fig.add_annotation(text="No data available", 
                          xref="paper", yref="paper",
                          x=0.5, y=0.5, showarrow=False)
        return fig
    
    fig = px.pie(
        values=list(data.values()),
        names=list(data.keys()),
        title=title
    )
    
    return fig

def create_timeline_chart(data: List[Dict[str, Any]]) -> go.Figure:
    """Create timeline chart for activities"""
    
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    if 'timestamp' not in df.columns:
        return go.Figure()
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    fig = px.scatter(
        df,
        x='timestamp',
        y='type',
        color='location',
        title='Activity Timeline',
        hover_data=['details']
    )
    
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig
