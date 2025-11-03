# 36120-25SP-AT3-Group08-Streamlit

A **Streamlit application** for presenting cryptocurrency information and predicting next-day high prices.  
This repository forms part of **Group 08’s AT3 submission** for the subject *36120 Advanced Machine Learning Application*.

> **Disclaimer:** This Streamlit application is developed solely for **academic purposes**.  
> It is **not intended for financial or investment use**.

---

## Repository Structure
```
36120-25SP-AT3-Group08-Streamlit/
├── app/
│   └── main.py                
├── students/
│   ├── __init__.py
│   ├── bitcoin.py              # Fang Yee Tan
│   ├── solana.py               # Nian-Ya Weng  
│   ├── ripple.py               # Siqi Zhang
│   └── ethereum.py             # Alesh Shrestha
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── github.txt                  
└── README.md

```
---

## Contributors

| Name               | Component |
|--------------------|------------|
| **Fang Yee Tan**   | Bitcoin    |
| **Nian-Ya Weng**   | Solana     |
| **Siqi Zhang**     | Ripple     |
| **Alesh Shrestha** | Ethereum   |

---

## Data Sources

This application retrieves cryptocurrency data from two trusted public APIs:

Kraken API
 — for historical OHLC (Open, High, Low, Close) market data used in candlestick visualisations and model evaluation.

CoinGecko API
 — for real-time cryptocurrency prices and 24-hour market changes.

Both sources are combined to ensure data reliability, completeness, and up-to-date market insights across multiple coins.

---

## License & Academic Use

This project is developed for **academic purposes** under the  
**University of Technology Sydney (UTS)**.  
© 2025 Group 08 — All rights reserved.




