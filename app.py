import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="计算器", page_icon="🧮", layout="centered")

# 现代简洁风格 CSS
st.markdown("""
<style>
    .stApp { 
        background: #f5f5f7; 
        padding: 0;
    }
    
    /* 计算器区域 */
    .calc-section {
        background: white;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 10px;
    }
    
    .calc-display {
        background: white;
        padding: 30px 20px;
        text-align: right;
        font-size: 64px;
        font-weight: 300;
        color: #1c1c1e;
        min-height: 120px;
        display: flex;
        align-items: flex-end;
        justify-content: flex-end;
        word-break: break-all;
    }
    
    .calc-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1px;
        background: #d1d1d6;
    }
    
    .calc-btn {
        border: none;
        font-size: 28px;
        height: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: background 0.1s;
    }
    
    .calc-btn:active { opacity: 0.6; }
    
    /* 数字按钮 - 白色 */
    .num-btn { background: white; color: #1c1c1e; }
    
    /* 操作符按钮 - 蓝色 */
    .op-btn { background: #007aff; color: white; }
    
    /* 功能按钮 - 浅灰 */
    .func-btn { background: #a5a5a5; color: #1c1c1e; }
    
    /* 0 按钮 */
    .zero-btn { 
        grid-column: span 2; 
        justify-content: flex-start;
        padding-left: 30px;
    }
    
    /* 功能页签 */
    .tab-bar {
        display: flex;
        background: #f5f5f7;
        padding: 10px;
        gap: 10px;
    }
    
    .tab-item {
        flex: 1;
        padding: 12px;
        text-align: center;
        border-radius: 12px;
        font-size: 14px;
        color: #8e8e93;
        background: white;
    }
    
    .tab-item.active {
        background: #007aff;
        color: white;
    }
    
    /* 卡片样式 */
    .content-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 1px 5px rgba(0,0,0,0.05);
    }
    
    .card-title {
        font-size: 18px;
        font-weight: 600;
        color: #1c1c1e;
        margin-bottom: 15px;
    }
    
    .input-ios {
        background: #f5f5f7;
        border: none;
        border-radius: 10px;
        color: #1c1c1e;
        padding: 14px;
        font-size: 16px;
        width: 100%;
    }
    
    .select-ios {
        background: #f5f5f7;
        border: none;
        border-radius: 10px;
        color: #1c1c1e;
        padding: 14px;
        font-size: 16px;
    }
    
    .btn-blue {
        background: #007aff;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px;
        font-size: 16px;
        width: 100%;
    }
    
    .result-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
    }
    
    .result-card {
        background: #f5f5f7;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }
    
    .result-label { font-size: 12px; color: #8e8e93; }
    .result-value { font-size: 20px; font-weight: 600; color: #007aff; margin-top: 5px; }
    
    .result-big {
        background: #f5f5f7;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-top: 15px;
    }
    
    .result-big-value { font-size: 28px; font-weight: 600; color: #34c759; }
</style>
""", unsafe_allow_html=True)

# 初始化
if 'display' not in st.session_state:
    st.session_state.display = '0'
if 'expression' not in st.session_state:
    st.session_state.expression = ''
if 'rates' not in st.session_state:
    st.session_state.rates = {'CNY': 1, 'USD': 7.2, 'EUR': 0.95, 'JPY': 150, 'HKD': 0.9, 'GBP': 0.85, 'KRW': 190}
if 'loan_result' not in st.session_state:
    st.session_state.loan_result = None
if 'health_result' not in st.session_state:
    st.session_state.health_result = None

# Tab 选择
tab = st.radio("", ["🧮", "🏠", "🔄", "❤️"], horizontal=True, index=0, key="tab_main")
tab_map = {'🧮': 'calc', '🏠': 'loan', '🔄': 'unit', '❤️': 'health'}

# ========== 计算器 ==========
if tab_map[tab] == 'calc':
    st.markdown('<div class="calc-section">', unsafe_allow_html=True)
    st.markdown(f'<div class="calc-display">{st.session_state.display}</div>', unsafe_allow_html=True)
    st.markdown('<div class="calc-grid">', unsafe_allow_html=True)
    
    # 第一行
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("AC", key="ac"):
            st.session_state.display = '0'
            st.session_state.expression = ''
            st.rerun()
    with c2:
        if st.button("±", key="neg"):
            if st.session_state.expression:
                st.session_state.expression = '-' + st.session_state.expression
                st.session_state.display = st.session_state.expression
            st.rerun()
    with c3:
        if st.button("%", key="pct"):
            st.session_state.expression += '%'
            st.session_state.display = st.session_state.expression
            st.rerun()
    with c4:
        if st.button("÷", key="div"):
            st.session_state.expression += '÷'
            st.session_state.display = st.session_state.expression
            st.rerun()
    
    # 第二行
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("7", key="7"): 
            st.session_state.expression += '7'
            st.session_state.display = st.session_state.expression
            st.rerun()
    with c2: 
        if st.button("8", key="8"): 
            st.session_state.expression += '8'
            st.session_state.display = st.session_state.expression
            st.rerun()
    with c3: 
        if st.button("9", key="9"): 
            st.session_state.expression += '9'
            st.session_state.display = st.session_state.expression
            st.rerun()
    with c4:
        if st.button("×", key="mul"):
            st.session_state.expression += '×'
            st.session_state.display = st.session_state.expression
            st.rerun()
    
    # 第三行
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("4", key="4"): 
            st.session_state.expression += '4'
            st.session_state.display = st.session_state.expression
            st.rerun()
    with c2: 
        if st.button("5", key="5"): 
            st.session_state.expression += '5'
            st.session_state.display = st.session_state.expression
            st.rerun()
    with c3: 
        if st.button("6", key="6"): 
            st.session_state.expression += '6'
            st.session_state.display = st.session_state.expression
            st.rerun()
    with c4:
        if st.button("-", key="sub"):
            st.session_state.expression += '-'
            st.session_state.display = st.session_state.expression
            st.rerun()
    
    # 第四行
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("1", key="1"): 
            st.session_state.expression += '1'
            st.session_state.display = st.session_state.expression
            st.rerun()
    with c2: 
        if st.button("2", key="2"): 
            st.session_state.expression += '2'
            st.session_state.display = st.session_state.expression
            st.rerun()
    with c3: 
        if st.button("3", key="3"): 
            st.session_state.expression += '3'
            st.session_state.display = st.session_state.expression
            st.rerun()
    with c4:
        if st.button("+", key="add"):
            st.session_state.expression += '+'
            st.session_state.display = st.session_state.expression
            st.rerun()
    
    # 第五行
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="calc-btn num-btn zero-btn">0</div>', unsafe_allow_html=True)
        if st.button("0", key="0"):
            st.session_state.expression += '0'
            st.session_state.display = st.session_state.expression
            st.rerun()
    with c2: 
        if st.button(".", key="dot"):
            st.session_state.expression += '.'
            st.session_state.display = st.session_state.expression
            st.rerun()
    with c3: pass
    with c4:
        if st.button("=", key="eq"):
            try:
                expr = st.session_state.expression.replace('×', '*').replace('÷', '/')
                result = eval(expr)
                st.session_state.display = str(int(result)) if result == int(result) else str(round(result, 10))
                st.session_state.expression = st.session_state.display
            except:
                st.session_state.display = 'Error'
                st.session_state.expression = ''
            st.rerun()
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# ========== 房贷 ==========
elif tab_map[tab] == 'loan':
    st.markdown('<div class="content-card"><div class="card-title">🏠 房贷计算器</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        amount = st.number_input("贷款金额（万元）", value=100.0, key="loan_amt")
    with c2:
        rate = st.number_input("年利率（%）", value=3.5, step=0.1, key="loan_rate")
    years = st.selectbox("贷款年限", [5, 10, 15, 20, 25, 30], index=3, key="loan_years")
    
    if st.button("计算", key="calc_loan"):
        m = amount * 10000
        r = rate / 100 / 12
        n = years * 12
        monthly = m * r * (1+r)**n / ((1+r)**n - 1)
        st.session_state.loan_result = {'monthly': monthly, 'total': monthly*n, 'interest': monthly*n - m}
    
    if st.session_state.loan_result:
        r = st.session_state.loan_result
        st.markdown(f'''
        <div class="result-grid">
            <div class="result-card"><div class="result-label">月供</div><div class="result-value">{r['monthly']:.2f}</div></div>
            <div class="result-card"><div class="result-label">总利息</div><div class="result-value" style="color:#ff9500">{r['interest']:.0f}</div></div>
            <div class="result-card"><div class="result-label">总还款</div><div class="result-value" style="color:#34c759">{r['total']:.0f}</div></div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== 换算 ==========
elif tab_map[tab] == 'unit':
    st.markdown('<div class="content-card"><div class="card-title">🔄 单位换算</div>', unsafe_allow_html=True)
    
    unit_type = st.selectbox("类型", ["💱 货币", "📏 长度", "⚖️ 重量", "🌡️ 温度"], key="unit_type")
    
    if unit_type == "💱 货币":
        if st.button("🔄 刷新汇率", key="refresh_rate"):
            try:
                resp = urllib.request.urlopen('https://api.frankfurter.dev/v1/latest?base=CNY', timeout=5)
                data = json.loads(resp.read().decode())
                if data.get('rates'):
                    st.session_state.rates = {'CNY': 1, **data['rates']}
                    st.rerun()
            except: st.error("获取失败")
        
        c1, c2, c3 = st.columns(3)
        with c1: amt = st.number_input("金额", value=1.0, key="curr_amt")
        with c2: frm = st.selectbox("从", ['CNY', 'USD', 'EUR', 'JPY', 'HKD', 'GBP', 'KRW'], key="curr_from")
        with c3: to = st.selectbox("到", ['CNY', 'USD', 'EUR', 'JPY', 'HKD', 'GBP', 'KRW'], index=1, key="curr_to")
        
        fr = st.session_state.rates.get(frm, 1)
        tr = st.session_state.rates.get(to, 1)
        res = (amt / fr) * tr
        names = {'CNY': '人民币', 'USD': '美元', 'EUR': '欧元', 'JPY': '日元', 'HKD': '港币', 'GBP': '英镑', 'KRW': '韩元'}
        st.markdown(f'<div class="result-big"><div class="result-label">{names[to]}</div><div class="result-big-value">{res:.4f}</div></div>', unsafe_allow_html=True)
    
    elif unit_type == "📏 长度":
        u = {"米": 1, "厘米": 0.01, "毫米": 0.001, "千米": 1000, "英尺": 0.3048, "英寸": 0.0254}
        c1, c2, c3 = st.columns(3)
        with c1: val = st.number_input("数值", value=1.0, key="len_val")
        with c2: frm = st.selectbox("从", list(u.keys()), key="len_from")
        with c3: to = st.selectbox("到", list(u.keys()), index=1, key="len_to")
        st.markdown(f'<div class="result-big"><div class="result-big-value">{val*u[frm]/u[to]:.6f}</div></div>', unsafe_allow_html=True)
    
    elif unit_type == "⚖️ 重量":
        u = {"公斤": 1, "克": 0.001, "斤": 0.5, "磅": 0.453592, "盎司": 0.0283495}
        c1, c2, c3 = st.columns(3)
        with c1: val = st.number_input("数值", value=1.0, key="wgt_val")
        with c2: frm = st.selectbox("从", list(u.keys()), key="wgt_from")
        with c3: to = st.selectbox("到", list(u.keys()), index=1, key="wgt_to")
        st.markdown(f'<div class="result-big"><div class="result-big-value">{val*u[frm]/u[to]:.6f}</div></div>', unsafe_allow_html=True)
    
    elif unit_type == "🌡️ 温度":
        c1, c2 = st.columns(2)
        with c1: val = st.number_input("温度", value=0.0, key="temp_val")
        with c2: frm = st.selectbox("从", ["摄氏度", "华氏度", "开尔文"], key="temp_from")
        to = st.selectbox("到", ["摄氏度", "华氏度", "开尔文"], index=1, key="temp_to")
        
        c = val if frm=="摄氏度" else (val-32)*5/9 if frm=="华氏度" else val-273.15
        res = c if to=="摄氏度" else c*9/5+32 if to=="华氏度" else c+273.15
        st.markdown(f'<div class="result-big"><div class="result-big-value">{res:.2f}°</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== 健康 ==========
elif tab_map[tab] == 'health':
    st.markdown('<div class="content-card"><div class="card-title">❤️ 健康计算</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1: h = st.number_input("身高(cm)", value=170, key="health_h")
    with c2: w = st.number_input("体重(kg)", value=65, key="health_w")
    c3, c4 = st.columns(2)
    with c3: age = st.number_input("年龄", value=30, key="health_age")
    with c4: gender = st.selectbox("性别", ["男", "女"], key="health_gender")
    act = st.selectbox("运动量", ["久坐(1.2)", "轻度(1.375)", "中度(1.55)", "重度(1.725)"], key="health_act")
    
    if st.button("计算", key="calc_health"):
        bmi = w / ((h/100)**2)
        cat = "偏瘦" if bmi < 18.5 else "正常" if bmi < 24 else "偏胖" if bmi < 28 else "肥胖"
        color = "#ff9500" if bmi < 18.5 else "#34c759" if bmi < 24 else "#ff9500" if bmi < 28 else "#ff3b30"
        bmr = 10*w + 6.25*h - 5*age + (5 if gender=="男" else -161)
        tdee = bmr * float(act.split("(")[1].split(")")[0])
        st.session_state.health_result = {'bmi': bmi, 'cat': cat, 'color': color, 'bmr': bmr, 'tdee': tdee}
    
    if st.session_state.health_result:
        r = st.session_state.health_result
        st.markdown(f'''
        <div style="text-align:center;">
            <div style="font-size:56px; font-weight:600; color:{r['color']};">{r['bmi']:.1f}</div>
            <div style="font-size:20px; color:{r['color']}; margin-bottom:15px;">{r['cat']}</div>
            <div class="result-grid">
                <div class="result-card"><div class="result-label">基础代谢</div><div class="result-value">{r['bmr']:.0f}</div></div>
                <div class="result-card"><div class="result-label">每日消耗</div><div class="result-value">{r['tdee']:.0f}</div></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)