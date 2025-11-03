import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.graph_objects as go

# Cached crypto prices
@st.cache_data(ttl=60)
def get_crypto_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,xrp,solana",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


# Fetch OHLC data (default = 30 days)
@st.cache_data(ttl=300)
def get_coin_history_kraken(pair="SOLUSD", interval=1440, days=30):
    """
    Fetch historical OHLC data from Kraken for the given trading pair.
    interval=1440 means daily candles.
    """
    import time
    end_time = int(time.time())
    start_time = end_time - days * 24 * 60 * 60  # seconds

    url = "https://api.kraken.com/0/public/OHLC"
    params = {"pair": pair, "interval": interval, "since": start_time}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Kraken returns nested dict with pair key
        key = list(data["result"].keys())[0]
        ohlc = data["result"][key]

        result = []
        for entry in ohlc:
            ts, o, h, l, c, *_ = entry
            result.append({
                "date": datetime.utcfromtimestamp(ts),
                "open": float(o),
                "high": float(h),
                "low": float(l),
                "close": float(c)
            })

        return result
    except Exception as e:
        st.error(f"Error loading Kraken data: {e}")
        return None


# Plotly Candlestick Chart
def plot_candlestick(data, symbol, days):
    if not data:
        return None

    df = pd.DataFrame(data).sort_values("date")
    df["date_str"] = df["date"].dt.strftime("%b %d")

    # Show every day for 7-day, every 3 days for longer
    dtick_val = 1 if days == 7 else 3

    # Using default hover text (no custom hovertemplate)
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["date_str"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                increasing_line_color="#4CAF50",
                decreasing_line_color="#EF5350",
                whiskerwidth=0.7,
                opacity=1
            )
        ]
    )

    fig.update_layout(
        title=f"{symbol} {days}-Day Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="#FAF8F3",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#3A3A3A", size=10),
        xaxis=dict(
            type="category",
            gridcolor="rgba(0,0,0,0.08)",
            rangeslider=dict(visible=False),
            showline=True,
            linecolor="rgba(0,0,0,0.1)",
            tickmode="linear",
            tick0=0,
            dtick=dtick_val
        ),
        yaxis=dict(
            gridcolor="rgba(0,0,0,0.08)",
            showline=True,
            linecolor="rgba(0,0,0,0.1)",
            tickprefix="$"
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_color="#333",
            bordercolor="rgba(0,0,0,0.1)"
        ),
        showlegend=False
    )

    fig.update_traces(
        selector=dict(type="candlestick"),
        increasing_line_width=2.0,
        decreasing_line_width=2.0
    )

    return fig


# API call for prediction
def predict_solana():
    API_URL = "https://solana-fastapi.onrender.com/predict"
    params = {
        "open": 180.0,
        "high": 185.0,
        "low": 178.0,
        "close": 183.0,
        "volume": 5000000.0,
        "marketCap": 85000000000.0,
        "price_diff": 7.0,
        "daily_range": 7.0,
        "SMA_7": 181.0
    }
    try:
        response = requests.get(API_URL, params=params, timeout=120)
        if response.status_code == 200:
            data = response.json()
            prediction = data.get("predicted_next_day_high")
            if prediction is not None:
                return float(prediction)
            return "No prediction available"
        return f"API Error {response.status_code}: {response.text}"
    except requests.exceptions.Timeout:
        return "API timeout - server is waking up, please try again"
    except Exception as e:
        return f"Error: {e}"


# Streamlit Page Layout
def show_solana_page():
    st.image("https://raw.githubusercontent.com/spothq/cryptocurrency-icons/master/128/color/sol.png", width=50)
    st.header("Solana Next-Day High Price Prediction")

    if st.button("Predict Next-Day High", key="predict_solana_btn"):
        with st.spinner("Fetching prediction..."):
            prediction = predict_solana()
            if isinstance(prediction, (int, float)):
                st.success(f"📈 Predicted Next-Day High: **${prediction:,.2f} USD**")
            else:
                st.error(f"⚠️ {prediction}")

    # Default = 30 days
    days = st.selectbox("Select time range (days):", [7, 30, 60], index=1, key="solana_days")
    data = get_coin_history_kraken("SOLUSD", interval=1440, days=days)

    if data:
        fig = plot_candlestick(data, "Solana", days)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Unable to load Solana data.")