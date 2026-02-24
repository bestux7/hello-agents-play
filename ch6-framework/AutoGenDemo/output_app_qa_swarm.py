import streamlit as st
import requests
from requests.exceptions import HTTPError, ConnectionError

# 定义 CoinGecko API
BASE_API_URL = "https://api.coingecko.com/api/v3/simple/price"

# 缓存的价格获取函数
@st.cache_data(ttl=60)  # 设置缓存有效期为60秒
def fetch_price_data(currency="usd"):
    """
    从 CoinGecko 使用参数化的币种获取比特币价格和24小时变化数据。
    """
    url = f"{BASE_API_URL}?ids=bitcoin&vs_currencies={currency}&include_24hr_change=true"
    try:
        response = requests.get(url, timeout=5)  # 防止请求等待时间过长
        response.raise_for_status()  # 如果 HTTP 响应错误，则引发异常
        data = response.json()
        change_raw = data["bitcoin"].get(f"{currency}_24hr_change")
        change_raw = change_raw if change_raw is not None else 0.0
        return {
            "price": data["bitcoin"].get(currency),
            "change_24h": round(change_raw, 2),
        }
    except HTTPError as http_err:
        st.error(f"服务错误: {http_err}")
        return None
    except ConnectionError as conn_err:
        st.error(f"网络连接错误: {conn_err}. 请检查您的网络状态。")
        return None
    except ValueError:
        st.error("无法解析响应数据，请稍后再试。")
        return None

def format_trend(change_24h):
    """
    格式化趋势指标（减号/加号）
    """
    trend = "涨幅 📈" if change_24h >= 0 else "跌幅 📉"
    return trend


# Streamlit 主应用结构
st.title("比特币价格显示应用")
st.markdown("""
实时显示比特币价格，并展示24小时变化趋势。
支持 USD 货币单位，代码结构已支持未来扩展多币种功能。
""")

# 显示刷新区域的 Placeholder
placeholder = st.empty()

def render_data(currency="usd"):
    """
    渲染价格变化数据至前端显示。
    """
    data = fetch_price_data(currency)
    if data:
        price = round(data["price"], 2)
        change_24h = data["change_24h"]
        trend = format_trend(change_24h)

        # 将内容动态更新到页面
        placeholder.markdown(f"""
        ### 当前比特币价格： ${price} {currency.upper()}
        ---
        ### 24小时价格变化：{trend}
        涨跌幅: {change_24h}%
        涨跌额: ${round(price * (change_24h / 100), 2)}
        """)

def auto_refresh(interval_sec=3, currency="usd"):
    """
    改进的自动刷新机制
    """
    import time
    while True:
        # 动态更新内容并等待指定间隔
        render_data(currency)
        time.sleep(interval_sec)

# 手动刷新按钮
if st.button("手动刷新"):
    with st.spinner("正在手动刷新数据..."):
        render_data()

# 初次渲染页面数据
render_data(currency="usd")

# 自动刷新功能
with st.sidebar.info("自动刷新数据间隔为每3秒。请更新以获取最新数据。"):
    auto_refresh(3, currency="usd")