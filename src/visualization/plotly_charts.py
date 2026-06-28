import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def plot_candlestick_with_features(df: pd.DataFrame, title: str = "BTCUSDT Price Action & CVD") -> go.Figure:
    """Generates an interactive Plotly chart with Candlestick price, volume, and CVD.
    
    Overlays liquidity sweeps and key levels.
    """
    # Create subplots: Row 1 = Candlesticks, Row 2 = Volume & Delta, Row 3 = CVD
    fig = make_subplots(
        rows=3, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.03, 
        row_heights=[0.6, 0.2, 0.2]
    )
    
    # Row 1: Candlesticks
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Price"
        ),
        row=1, col=1
    )
    
    # Overlay liquidity sweeps
    if "bullish_sweep_24h" in df:
        sweeps = df[df["bullish_sweep_24h"]]
        fig.add_trace(
            go.Scatter(
                x=sweeps.index,
                y=sweeps["low"] - 100,
                mode="markers",
                marker=dict(symbol="triangle-up", size=10, color="green"),
                name="Bullish Sweep"
            ),
            row=1, col=1
        )
        
    if "bearish_sweep_24h" in df:
        sweeps = df[df["bearish_sweep_24h"]]
        fig.add_trace(
            go.Scatter(
                x=sweeps.index,
                y=sweeps["high"] + 100,
                mode="markers",
                marker=dict(symbol="triangle-down", size=10, color="red"),
                name="Bearish Sweep"
            ),
            row=1, col=1
        )

    # Row 2: Volume
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["volume"],
            marker_color="blue",
            name="Volume"
        ),
        row=2, col=1
    )
    
    # Row 3: CVD
    if "cvd" in df:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["cvd"],
                mode="lines",
                line=dict(color="orange", width=2),
                name="CVD"
            ),
            row=3, col=1
        )
        
    fig.update_layout(
        title=title,
        xaxis_rangeslider_visible=False,
        height=800,
        template="plotly_dark"
    )
    
    return fig
