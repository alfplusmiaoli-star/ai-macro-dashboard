import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==========================================
# 1. 網頁基本設定 (Page Configuration)
# ==========================================
st.set_page_config(page_title="AI 財經防護儀表板", layout="wide")
st.title("四維宏觀與動態資產防護儀表板 (4D Macro & DAA Dashboard)")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["一、四維防護系統 (避險)", "二、長期估值濾網 (長線)", "三、動態提領試算 (退休)"])

end_date = datetime.now()
start_date_1y = end_date - timedelta(days=400)
start_date_18m = end_date - timedelta(days=540)

# ==========================================
# 頁籤一：四維防護系統 (4D Protection System)
# ==========================================
with tab1:
    st.subheader("四維緊急煞車與三維動能檢驗")
    if st.button("啟動檢驗 (Run Analysis)"):
        with st.spinner("正在連線抓取即時數據..."):
            try:
                # 嘗試正常連線 FRED
                url_hy = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAMLH0A0HYM2"
                hy_spread = pd.read_csv(url_hy, index_col='DATE', parse_dates=True, na_values='.')
                hy_spread = hy_spread.loc[start_date_1y.strftime('%Y-%m-%d'):end_date.strftime('%Y-%m-%d')].dropna()
                current_spread = float(hy_spread.iloc[-1].values[0])
                spread_1m_ago = float(hy_spread.iloc[-21].values[0])
                spread_change = current_spread - spread_1m_ago

                url_sp500 = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SP500"
                sp500_data = pd.read_csv(url_sp500, index_col='DATE', parse_dates=True, na_values='.')
                sp500_data = sp500_data.apply(pd.to_numeric, errors='coerce').dropna()
                sp500_data = sp500_data.loc[start_date_1y.strftime('%Y-%m-%d'):end_date.strftime('%Y-%m-%d')]
                spy_current = float(sp500_data.iloc[-1].values[0])
                spy_200sma = float(sp500_data.rolling(window=200).mean().iloc[-1].values[0])

            except Exception:
                # 【備援機制啟動】：若被封鎖，立即切換為教學模擬數據
                st.toast('⚠️ 外部網路遭阻擋，已自動切換為【教學模擬模式】', icon='🛡️')
                current_spread = 4.15
                spread_change = 0.05
                spy_current = 5120.30
                spy_200sma = 4850.50

            # 畫面排版與決策輸出 (無論資料來源為何，邏輯皆正常運作)
            col1, col2 = st.columns(2)
            col1.metric("高收益債信用利差 (HY OAS)", f"{current_spread:.2f}%", f"{spread_change:+.2f}% (月變動)", delta_color="inverse")
            col2.metric("標普500 (SP500) 現價 vs 200日均線", f"{spy_current:.2f}", f"均線: {spy_200sma:.2f}")

            if current_spread > 5.0 or spread_change > 1.0:
                st.error("🚨 **警報觸發！實體經濟違約風險過高，啟動強制防禦。**\n\n**決策**：清空所有股票，100% 轉入 BIL。企業主請凍結資本支出！")
            elif spy_current > spy_200sma:
                st.success("✅ **多頭確認：市場流動性與經濟成長健康。**\n\n**決策**：啟動攻擊配置，尋找相對動能強勢板塊。")
            else:
                st.warning("⚠️ **空頭確認：大盤跌破長期均線，資金動能衰退。**\n\n**決策**：防禦配置，資金轉入 IEI 與 BIL。")

# ==========================================
# 頁籤二：長期估值濾網 (Long-term Valuation Filter)
# ==========================================
with tab2:
    st.subheader("20法則 (Rule of 20) 大盤水位評估")
    manual_pe = st.number_input("請查詢並輸入目前的標普500本益比 (P/E Ratio)：", min_value=1.0, value=25.0, step=0.1)

    if st.button("計算估值 (Calculate Valuation)"):
        with st.spinner("正在計算數據..."):
            try:
                url_cpi = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL"
                cpi_data = pd.read_csv(url_cpi, index_col='DATE', parse_dates=True, na_values='.')
                cpi_data = cpi_data.loc[start_date_18m.strftime('%Y-%m-%d'):end_date.strftime('%Y-%m-%d')].dropna()
                cpi_current = float(cpi_data.iloc[-1].values[0])
                cpi_year_ago = float(cpi_data.iloc[-13].values[0])
                cpi_yoy = ((cpi_current - cpi_year_ago) / cpi_year_ago) * 100
            except Exception:
                # 備援機制
                st.toast('⚠️ 外部網路遭阻擋，已自動切換為【教學模擬模式】', icon='🛡️')
                cpi_yoy = 3.15

            pe_ratio = manual_pe
            rule_of_20 = pe_ratio + cpi_yoy
            
            col1, col2, col3 = st.columns(3)
            col1.metric("標普500 本益比 (P/E)", f"{pe_ratio:.2f}")
            col2.metric("核心通膨年增率 (CPI YoY)", f"{cpi_yoy:.2f}%")
            col3.metric("20法則數值", f"{rule_of_20:.2f}")

            if rule_of_20 < 20:
                st.info("💡 **估值狀態：【低估 (Undervalued)】**\n\n建議：長線便宜區間，可加速定期定額佈局。")
            else:
                st.warning("⚠️ **估值狀態：【高估 (Overvalued)】**\n\n建議：大盤不便宜，請勿單筆重壓，保留現金彈性。")

# ==========================================
# 頁籤三：動態安全提領率試算 (Dynamic SWR)
# ==========================================
with tab3:
    st.subheader("退休金動態提領計算機 (Retirement Withdrawal Calculator)")

    col1, col2 = st.columns(2)
    with col1:
        portfolio_value = st.number_input("請輸入預估退休金總額 (萬元):", min_value=100, value=1000, step=100)
        inflation_rate = st.number_input("預估年度通膨率 (%):", min_value=0.0, value=2.0, step=0.1) / 100
    with col2:
        market_status = st.radio("目前系統判定的大盤狀態為：", ("多頭 (Bull Market)", "空頭 (Bear Market)"))

    if st.button("試算本年度提領金 (Calculate SWR)"):
        if market_status == "多頭 (Bull Market)":
            base_swr = 0.045
            withdrawal = portfolio_value * base_swr * (1 + inflation_rate)
            st.success(f"📈 **建議提領率：{base_swr*100}% + 通膨調整**")
            st.info(f"💰 **本年度可安全提領：{withdrawal:.2f} 萬元**")
        else:
            base_swr = 0.03
            withdrawal = portfolio_value * base_swr
            st.error(f"📉 **建議提領率：{base_swr*100}% (凍結通膨調整)**")
            st.warning(f"💰 **本年度可安全提領：{withdrawal:.2f} 萬元**")