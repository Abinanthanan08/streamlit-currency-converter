import streamlit as st
import requests


st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="centered")


API_KEY = "6b4c4a941dfa530c2755a444"
API_URL = f"https://v6.exchangerate-api.com/v6/6b4c4a941dfa530c2755a444/latest/"


@st.cache_data
def get_exchange_rates(base_currency):
    response = requests.get(f"{API_URL}{base_currency}")
    if response.status_code == 200:
        return response.json()["conversion_rates"]
    else:
        return None


currency_dict = {
    "USD 🇺🇸": "USD", "INR 🇮🇳": "INR", "EUR 🇪🇺": "EUR",
    "GBP 🇬🇧": "GBP", "JPY 🇯🇵": "JPY", "AUD 🇦🇺": "AUD",
    "CAD 🇨🇦": "CAD", "CNY 🇨🇳": "CNY", "SGD 🇸🇬": "SGD"
}



st.title("💱 Currency Converter 🌎")
st.write("Convert currencies in real-time using exchange rates.")


st.sidebar.header("🔄 Currency Settings")


if "history" not in st.session_state:
    st.session_state.history = []


from_currency = st.sidebar.selectbox("🟢 From Currency:", list(currency_dict.keys()), index=0)
to_currency = st.sidebar.selectbox("🔵 To Currency:", list(currency_dict.keys()), index=1)


amount = st.number_input("💰 Enter amount:", min_value=0.0, value=1.0, format="%.2f")


if st.button("🔄 Convert Now"):
    with st.spinner("Fetching latest exchange rates..."):
        exchange_rates = get_exchange_rates(currency_dict[from_currency])

    if exchange_rates and currency_dict[to_currency] in exchange_rates:
        rate = exchange_rates[currency_dict[to_currency]]
        converted_amount = round(amount * rate, 2)

     
        st.success(f"💸 {amount} {from_currency} = {converted_amount} {to_currency} 🎉")

       
        st.session_state.history.append({
            "From": from_currency,
            "To": to_currency,
            "Amount": amount,
            "Converted": converted_amount
        })
    else:
        st.error("❌ Error fetching exchange rates. Please try again.")


if st.session_state.history:
    st.subheader("📜 Conversion History")
    st.table(st.session_state.history)
