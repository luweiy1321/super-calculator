import streamlit as st
import urllib.request
import json
import math

st.set_page_config(
    page_title="超级计算器",
    page_icon="🧮",
    layout="centered"
)

# CSS 样式
st.markdown("""
<style>
    @media (max-width: 768px) {
        .stApp { padding: 10px !important; }
    }
    .stApp { background: #1a1a1a; }
    .display {
        background: #2a2a2a;
        padding: 15px;
        text-align: right;
        font-size: 36px;
        border-radius: 15px 15px 0 0;
        word-break: break-all;
    }
    .calc-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        padding: 10px;
        background: #2a2a2a;
        border-radius: 0 0 15px 15px;
    }
    .calc-btn {
        padding: 16px;
        font-size: 18px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        background: #444;
        color: white;
    }
    .calc-btn.orange { background: #ff9500; }
    .calc-btn.gray { background: #a5a5a5; color: black; }
    .calc-btn.blue { background: #007AFF; }
    .result-highlight {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        padding: 15px;
        background: #007AFF;
        border-radius: 10px;
    }
    .info-card {
        background: #2a2a2a;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
    }
    .info-card .label { font-size: 11px; color: #888; }
    .info-card .value { font-size: 16px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 初始化
if 'display' not in st.session_state:
    st.session_state.display = '0'
if 'expression' not in st.session_state:
    st.session_state.expression = ''
if 'rates' not in st.session_state:
    st.session_state.rates = {'CNY': 1, 'USD': 7.2, 'EUR': 0.95, 'JPY': 150, 'HKD': 0.9, 'GBP': 0.85, 'KRW': 190}
if 'rate_time' not in st.session_state:
    st.session_state.rate_time = ''
if 'loan_result' not in st.session_state:
    st.session_state.loan_result = None
if 'health_result' not in st.session_state:
    st.session_state.health_result = None

# Tab 导航
tabs = ['🧮 计算', '📷 AI拍照', '🏠 房贷', '🔄 换算', '❤️ 健康']
selected_tab = st.radio("", tabs, horizontal=True, index=0)
tab_map = {'🧮 计算': 'calc', '📷 AI拍照': 'ai', '🏠 房贷': 'loan', '🔄 换算': 'unit', '❤️ 健康': 'health'}
tab = tab_map[selected_tab]

# ========== 计算器 ==========
if tab == 'calc':
    st.markdown(f'<div class="display">{st.session_state.display}</div>', unsafe_allow_html=True)
    
    # 使用 HTML 按钮
    buttons = [
        ('AC', 'gray'), ('⌫', 'gray'), ('%', ''), ('÷', 'orange'),
        ('7', ''), ('8', ''), ('9', ''), ('×', 'orange'),
        ('4', ''), ('5', ''), ('6', ''), ('-', 'orange'),
        ('1', ''), ('2', ''), ('3', ''), ('+', 'orange'),
    ]
    
    cols = st.columns(4)
    for i, (btn, btn_type) in enumerate(buttons):
        with cols[i % 4]:
            cls = f"calc-btn {btn_type}" if btn_type else "calc-btn"
            if st.button(btn, key=f"btn_{btn}", use_container_width=True):
                if btn == 'AC':
                    st.session_state.display = '0'
                    st.session_state.expression = ''
                elif btn == '⌫':
                    if st.session_state.expression:
                        st.session_state.expression = st.session_state.expression[:-1]
                        st.session_state.display = st.session_state.expression or '0'
                elif btn in ['+', '-', '×', '÷', '%']:
                    st.session_state.expression += btn
                    st.session_state.display = st.session_state.expression
                else:
                    st.session_state.expression += btn
                    st.session_state.display = st.session_state.expression
                st.rerun()
    
    # 等号按钮
    if st.button("＝", use_container_width=True, key="btn_eq"):
        try:
            expr = st.session_state.expression.replace('×', '*').replace('÷', '/')
            result = eval(expr)
            st.session_state.display = str(int(result)) if result == int(result) else str(result)
            st.session_state.expression = st.session_state.display
        except:
            st.session_state.display = 'Error'
            st.session_state.expression = ''
        st.rerun()

# ========== AI拍照 ==========
elif tab == 'ai':
    st.subheader("📷 AI拍照解题")
    uploaded = st.file_uploader("上传数学题图片", type=['jpg', 'jpeg', 'png'])
    if uploaded:
        st.image(uploaded, use_container_width=True)
        st.info("📝 需要配置 AI API 才能使用")

# ========== 房贷 ==========
elif tab == 'loan':
    st.subheader("🏠 房贷计算器")
    c1, c2 = st.columns(2)
    with c1:
        amount = st.number_input("贷款金额（万元）", value=100.0, min_value=0.0)
    with c2:
        rate = st.number_input("年利率（%）", value=3.5, min_value=0.0, step=0.1)
    years = st.selectbox("年限", [5, 10, 15, 20, 25, 30], index=3)
    
    if st.button("计算"):
        m = amount * 10000
        r = rate / 100 / 12
        n = years * 12
        monthly = m * r * (1+r)**n / ((1+r)**n - 1)
        total = monthly * n
        interest = total - m
        st.session_state.loan_result = {'monthly': monthly, 'total': total, 'interest': interest}
    
    if st.session_state.loan_result:
        r = st.session_state.loan_result
        st.markdown(f"""
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-top:20px;">
            <div class="info-card"><div class="label">月供</div><div class="value" style="color:#007AFF">{r['monthly']:.2f}</div></div>
            <div class="info-card"><div class="label">总利息</div><div class="value" style="color:#ff9500">{r['interest']:.0f}</div></div>
            <div class="info-card"><div class="label">总还款</div><div class="value" style="color:#34c759">{r['total']:.0f}</div></div>
        </div>
        """, unsafe_allow_html=True)

# ========== 单位换算 ==========
elif tab == 'unit':
    st.subheader("🔄 单位换算")
    unit_type = st.selectbox("类型", ["📏 长度", "⚖️ 重量", "🌡️ 温度", "💱 货币"])
    
    if unit_type == "💱 货币":
        if st.button("🔄 刷新汇率"):
            try:
                resp = urllib.request.urlopen('https://api.frankfurter.dev/v1/latest?base=CNY', timeout=5)
                data = json.loads(resp.read().decode())
                if data.get('rates'):
                    st.session_state.rates = {'CNY': 1, **data['rates']}
                    st.session_state.rate_time = data.get('date', '')
                    st.rerun()
            except: st.error("获取汇率失败")
        
        if st.session_state.rate_time:
            st.caption(f"汇率时间: {st.session_state.rate_time}")
        
        c1, c2, c3 = st.columns(3)
        with c1: amt = st.number_input("金额", value=1.0, min_value=0.0)
        with c2: frm = st.selectbox("从", ['CNY', 'USD', 'EUR', 'JPY', 'HKD', 'GBP', 'KRW'])
        with c3: to = st.selectbox("到", ['CNY', 'USD', 'EUR', 'JPY', 'HKD', 'GBP', 'KRW'], index=1)
        
        fr = st.session_state.rates.get(frm, 1)
        tr = st.session_state.rates.get(to, 1)
        res = (amt / fr) * tr
        names = {'CNY': '人民币', 'USD': '美元', 'EUR': '欧元', 'JPY': '日元', 'HKD': '港币', 'GBP': '英镑', 'KRW': '韩元'}
        st.markdown(f'<div class="result-highlight">{names[to]}: {res:.4f}</div>', unsafe_allow_html=True)
    
    elif unit_type == "📏 长度":
        units = {"米": 1, "厘米": 0.01, "毫米": 0.001, "千米": 1000, "英尺": 0.3048, "英寸": 0.0254}
        c1, c2, c3 = st.columns(3)
        with c1: val = st.number_input("数值", value=1.0, min_value=0.0)
        with c2: frm = st.selectbox("从", list(units.keys()))
        with c3: to = st.selectbox("到", list(units.keys()), index=1)
        res = val * units[frm] / units[to]
        st.markdown(f'<div class="result-highlight">{to}: {res:.6f}</div>', unsafe_allow_html=True)
    
    elif unit_type == "⚖️ 重量":
        units = {"公斤": 1, "克": 0.001, "斤": 0.5, "磅": 0.453592, "盎司": 0.0283495}
        c1, c2, c3 = st.columns(3)
        with c1: val = st.number_input("数值", value=1.0, min_value=0.0)
        with c2: frm = st.selectbox("从", list(units.keys()))
        with c3: to = st.selectbox("到", list(units.keys()), index=1)
        res = val * units[frm] / units[to]
        st.markdown(f'<div class="result-highlight">{to}: {res:.6f}</div>', unsafe_allow_html=True)
    
    elif unit_type == "🌡️ 温度":
        c1, c2 = st.columns(2)
        with c1: val = st.number_input("温度", value=0.0)
        with c2: frm = st.selectbox("从", ["摄氏度", "华氏度", "开尔文"])
        to = st.selectbox("到", ["摄氏度", "华氏度", "开尔文"], index=1)
        
        if frm == "摄氏度": c = val
        elif frm == "华氏度": c = (val - 32) * 5/9
        else: c = val - 273.15
        
        if to == "摄氏度": res = c
        elif to == "华氏度": res = c * 9/5 + 32
        else: res = c + 273.15
        
        st.markdown(f'<div class="result-highlight">{to}: {res:.2f}</div>', unsafe_allow_html=True)

# ========== 健康 ==========
elif tab == 'health':
    st.subheader("❤️ 健康计算")
    c1, c2 = st.columns(2)
    with c1: h = st.number_input("身高(cm)", value=170, min_value=50, max_value=250)
    with c2: w = st.number_input("体重(kg)", value=65, min_value=20, max_value=300)
    c3, c4 = st.columns(2)
    with c3: age = st.number_input("年龄", value=30, min_value=1, max_value=150)
    with c4: gender = st.selectbox("性别", ["男", "女"])
    act = st.selectbox("运动量", ["久坐(1.2)", "轻度(1.375)", "中度(1.55)", "重度(1.725)"])
    act_map = {"久坐(1.2)": 1.2, "轻度(1.375)": 1.375, "中度(1.55)": 1.55, "重度(1.725)": 1.725}
    
    if st.button("计算"):
        bmi = w / ((h/100) ** 2)
        cat = "偏瘦" if bmi < 18.5 else "正常" if bmi < 24 else "偏胖" if bmi < 28 else "肥胖"
        color = "#007AFF" if bmi < 18.5 else "#34c759" if bmi < 24 else "#ff9500" if bmi < 28 else "#ff3b30"
        bmr = 10*w + 6.25*h - 5*age + (5 if gender=="男" else -161)
        tdee = bmr * act_map[act]
        st.session_state.health_result = {'bmi': bmi, 'cat': cat, 'color': color, 'bmr': bmr, 'tdee': tdee}
    
    if st.session_state.health_result:
        r = st.session_state.health_result
        st.markdown(f"""
        <div style="text-align:center; margin-top:20px;">
            <div style="font-size:48px; font-weight:bold; color:{r['color']};">{r['bmi']:.1f}</div>
            <div style="font-size:18px; color:{r['color']};">{r['cat']}</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:15px;">
                <div class="info-card"><div class="label">基础代谢</div><div style="font-size:16px;">{r['bmr']:.0f} 千卡</div></div>
                <div class="info-card"><div class="label">每日消耗</div><div style="font-size:16px;">{r['tdee']:.0f} 千卡</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)