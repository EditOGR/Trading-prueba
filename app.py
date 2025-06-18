import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Trading con Derivadas", layout="centered")

st.title("📈 Estrategia de Trading con Derivadas")
ticker = st.text_input("Símbolo de la acción (ej: AAPL, TSLA, MSFT):", "AAPL")
umbral = st.slider("Umbral de cambio (derivada):", min_value=0.1, max_value=5.0, value=1.0, step=0.1)

if ticker:
    data = yf.download(ticker, period='6mo')
    data['Derivada'] = data['Close'].diff()
    data['Señal'] = 0
    data.loc[data['Derivada'] > umbral, 'Señal'] = 1
    data.loc[data['Derivada'] < -umbral, 'Señal'] = -1

    st.subheader(f"Gráfico de señales para {ticker}")

    fig, ax = plt.subplots()
    ax.plot(data['Close'], label='Precio', color='blue')
    ax.plot(data[data['Señal'] == 1].index, data['Close'][data['Señal'] == 1], '^', color='green', label='Compra')
    ax.plot(data[data['Señal'] == -1].index, data['Close'][data['Señal'] == -1], 'v', color='red', label='Venta')
    ax.set_title(f'Precio y señales de trading para {ticker}')
    ax.legend()
    ax.grid()
    st.pyplot(fig)
