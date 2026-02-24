import streamlit as st
import requests
from datetime import datetime

# Function to fetch Bitcoin data (cached to improve performance)
@st.cache(ttl=300)  # Cache the data for 5 minutes to reduce API calls
def get_bitcoin_data():
    """
    Fetch Bitcoin data from CoinGecko API.
    Returns:
        dict: A dictionary with the current price, 24-hour change, and percentage change.
    """
    try:
        # API Endpoint
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        response = requests.get(url, params=params)

        # Check for rate limit error (status code 429)
        if response.status_code == 429:
            st.warning("API 请求过于频繁，请稍后重试。")
            return None

        # Raise an exception for bad responses
        response.raise_for_status()

        # Parse response
        data = response.json()
        return {
            "current_price": data['bitcoin']['usd'],
            "price_change_24h": data['bitcoin']['usd_24h_change'],
            "percent_change_24h": (data['bitcoin']['usd_24h_change'] / data['bitcoin']['usd']) * 100
        }
    except requests.exceptions.RequestException as e:
        st.error(f"网络请求失败，请稍后重试: {e}")
        return None


# Function to render Bitcoin price information on the page
def render_price_info(data):
    """
    Display Bitcoin price information on the app.
    Args:
        data (dict): Contains current price, price change, and percentage change.
    """
    st.metric(
        label="Bitcoin Price (USD)",
        value=f"${data['current_price']:,.2f}",
        delta=f"${data['price_change_24h']:,.2f} ({data['percent_change_24h']:.2f}%)",
        delta_color="inverse" if data['price_change_24h'] < 0 else "normal"
    )


# Main application function
def main():
    # Configure the Streamlit app page
    st.set_page_config(page_title="Bitcoin Price Tracker", page_icon="₿", layout="centered")

    # App Title and Description
    st.title("📈 Bitcoin Price Tracker")
    st.write("实时比特币 (₿) 价格和涨跌幅跟踪工具")

    # Fetch and display data
    with st.spinner("加载最新比特币数据..."):
        bitcoin_data = get_bitcoin_data()

    if bitcoin_data:
        # Render price info
        render_price_info(bitcoin_data)
        # Show last update time
        st.caption(f"最后更新时间: {datetime.now():%Y-%m-%d %H:%M:%S}")

        # Refresh button logic
        if st.button("🔄 刷新数据"):
            with st.spinner("正在刷新数据..."):
                bitcoin_data = get_bitcoin_data()
                if bitcoin_data:
                    render_price_info(bitcoin_data)
                    st.caption(f"最后更新时间: {datetime.now():%Y-%m-%d %H:%M:%S}")
                else:
                    st.error("刷新数据失败，请稍后重试。")
    else:
        st.error("无法获取比特币数据，请检查网络连接或稍后重试。")


# Run the application
if __name__ == "__main__":
    main()