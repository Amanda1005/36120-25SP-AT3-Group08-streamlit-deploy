import streamlit as st
import sys
import os
import requests

# === PATH SETUP ===
# Get the absolute path of current file
current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
parent_dir = os.path.dirname(current_dir)

# Add parent directory to Python path
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# === IMPORT CRYPTO PAGES ===
try:
    from students.bitcoin import show_bitcoin_page
    from students.ethereum import show_ethereum_page
    from students.xrp import show_xrp_page
    from students.solana import show_solana_page
except ImportError as e:
    st.error(f"❌ Failed to import student modules: {e}")
    st.info(f"Current directory: {current_dir}")
    st.info(f"Parent directory: {parent_dir}")
    st.info(f"Looking for: {os.path.join(parent_dir, 'students')}")
    if os.path.exists(os.path.join(parent_dir, 'students')):
        st.info(f"Files in students/: {os.listdir(os.path.join(parent_dir, 'students'))}")
    st.stop()

# === STREAMLIT SETUP ===
st.set_page_config(page_title="Crypto Next-Day High Dashboard", layout="wide")

# === CSS STYLING ===
st.markdown("""
<style>
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }
.stApp {
    background: linear-gradient(135deg, #FAF8F3, #F5F1E8);
    color: #2C2C2C;
    font-family: 'Pretendard', 'Noto Sans KR', sans-serif;
}
.ticker {
    width: 100%;
    background: linear-gradient(90deg, #E8E4D9, #DED9CC);
    border-bottom: 1px solid rgba(0,0,0,0.08);
    overflow: hidden;
    white-space: nowrap;
    height: 36px;
    line-height: 36px;
}
.ticker span {
    display: inline-block;
    animation: ticker-scroll 30s linear infinite;
    padding-right: 2rem;
}
@keyframes ticker-scroll { 
    0% {transform:translateX(100%);} 
    100% {transform:translateX(-100%);} 
}
h1 {
    color: #1A1A1A !important; 
    font-weight: 700;
}
h2, h3, h4 {
    color: #3A3A3A !important; 
    font-weight: 600;
}
div[data-testid="stButton"] button {
    background: #FFFFFF !important;
    border: 1px solid rgba(0,0,0,0.15) !important;
    color: #333333 !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 0.5rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
}
div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #C9A57B, #A68B6A) !important;
    color: white !important;
}
div[data-testid="stButton"] button:active {
    transform: scale(0.97);
}
</style>
""", unsafe_allow_html=True)

# === LIVE PRICES TICKER ===
@st.cache_data(ttl=60)
def get_crypto_prices():
    """Fetch live cryptocurrency prices from CoinGecko API"""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum,ripple,solana", 
        "vs_currencies": "usd", 
        "include_24hr_change": "true"
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        parts = []
        for coin, info in data.items():
            symbol = {
                "bitcoin": "BTC", 
                "ethereum": "ETH", 
                "ripple": "XRP", 
                "solana": "SOL"
            }[coin]
            price = info.get("usd", 0)
            change = info.get("usd_24h_change", 0)
            arrow = "▲" if change >= 0 else "▼"
            color = "#2D9F4F" if change >= 0 else "#D9534F"
            parts.append(
                f"<span style='color:#2C2C2C;font-weight:600'>{symbol}/USD</span> "
                f"<span style='color:#5A5A5A'>{price:,.2f}</span> "
                f"<span style='color:{color};font-weight:600'>{arrow}{abs(change):.2f}%</span>"
            )
        return "  ".join(parts)
    except Exception as e:
        # Fallback data if API fails
        return "BTC/USD 67,450 ▲1.25% ETH/USD 3,120 ▲0.84% XRP/USD 0.512 ▼0.34% SOL/USD 102.4 ▲2.02%"

# Display ticker
prices_html = get_crypto_prices()
st.markdown(f"<div class='ticker'><span>{prices_html}</span></div>", unsafe_allow_html=True)

# === TITLE ===
st.title("Crypto Next-Day High Price Prediction Dashboard")

# === NAVIGATION BUTTONS ===
st.markdown("### Select Cryptocurrency")

col1, col2, col3, col4 = st.columns(4)

# Initialize session state
if "selected_coin" not in st.session_state:
    st.session_state.selected_coin = None

# Create buttons
with col1:
    if st.button("Bitcoin", use_container_width=True):
        st.session_state.selected_coin = "Bitcoin"
with col2:
    if st.button("Ethereum", use_container_width=True):
        st.session_state.selected_coin = "Ethereum"
with col3:
    if st.button("XRP", use_container_width=True):
        st.session_state.selected_coin = "XRP"
with col4:
    if st.button("Solana", use_container_width=True):
        st.session_state.selected_coin = "Solana"

st.markdown("---")

# === DISPLAY SELECTED PAGE ===
try:
    if st.session_state.selected_coin == "Bitcoin":
        show_bitcoin_page()
    elif st.session_state.selected_coin == "Ethereum":
        show_ethereum_page()
    elif st.session_state.selected_coin == "XRP":
        show_xrp_page()
    elif st.session_state.selected_coin == "Solana":
        show_solana_page()
    else:
        st.markdown(
            "<p style='text-align:center;color:#777;'>"
            "Please select a cryptocurrency above to view predictions and charts."
            "</p>", 
            unsafe_allow_html=True
        )
except Exception as e:
    st.error(f"❌ Error loading {st.session_state.selected_coin} page: {e}")
    st.exception(e)

# === FOOTER ===
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #8B7355; padding: 1rem; font-size: 13px;'>
    <p>Data Sources: <strong>CoinGecko API</strong> & <strong>Kraken API</strong> | Group 8 Project AT3</p>
    <p><em>⚠️ This tool is developed solely for academic purposes and should not be used for financial or investment decisions.</em></p>
</div>
""", unsafe_allow_html=True)
