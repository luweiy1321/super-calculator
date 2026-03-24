import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="计算器", page_icon="🧮", layout="centered")

# iOS 风格 CSS
st.markdown("""
<style>
    .stApp { 
        background: #000000; 
        padding: 0;
    }
    
    /* iOS 风格计算器 */
    .ios-display {
        background: #000000;
        padding: 20px 20px 60px;
        text-align: right;
        font-size: 80px;
        font-weight: 300;
        color: white;
        min-height: 200px;
        display: flex;
        align-items: flex-end;
        justify-content: flex-end;
        word-break: break-all;
        padding-right: 30px;
    }
    
    .ios-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        padding: 12px;
        background: #000000;
    }
    
    .ios-btn {
        border-radius: 50%;
        border: none;
        font-size: 32px;
        font-weight: 400;
        height: 80px;
        width: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        cursor: pointer;
    }
    
    .ios-btn:active {
        opacity: 0.6;
    }
    
    /* 数字按钮 */
    .num-btn {
        background: #333333;
        color: white;
    }
    
    /* 操作符按钮 */
    .op-btn {
        background: #ff9500;
        color: white;
    }
    
    /* 功能按钮 */
    .func-btn {
        background: #a5a5a5;
        color: black;
    }
    
    /* 等号按钮 */
    .eq-btn {
        background: #ff9500;
        color: white;
    }
    
    /* 0 按钮 - 长条形 */
    .zero-btn {
        grid-column: span 2;
        width: 100%;
        border-radius: 40px;
        justify-content: flex-start;
        padding-left: 30px;
    }
    
    /* 底部卡片样式 */
    .card-dark {
        background: #1c1c1e;
        border-radius: 20px;
        padding: 20px;
        margin: 10px;
    }
    
    .card-title {
        font-size: 20px;
        font-weight: 600;
        color: white;
        margin-bottom: 15px;
    }
    
    .input-ios {
        background: #2c2c2e;
        border: none;
        border-radius: 10px;
        color: white;
        padding: 15px;
        font-size: 18px;
        width: 100%;
    }
    
    .select-ios {
        background: #2c2c2e;
        border: none;
        border-radius: 10px;
        color: white;
        padding: 15px;
        font-size: 18px;
    }
    
    .btn-ios {
        background: #ff9500;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 15px;
        font-size: 18px;
        width: 100%;
    }
    
    .result-ios {
        background: #2c2c2e;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    
    .result-label {
        font-size: 14px;
        color: #8e8e93;
    }
    
    .result-value {
        font-size: 24px;
        font-weight: 600;
        color: white;
        margin-top: 5px;
    }
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

# Tab
tabs = ['🧮 计算', '🏠 房贷', '🔄 换算', '❤️ 健康']
tab = st.radio("", tabs, horizontal=True, index=0, key="tab_radio")
tab_map = {'🧮 计算': 'calc', '🏠 房贷': 'loan', '🔄 换算': 'unit', '❤️ 健康': 'health'}

# ========== 计算器 ==========
if tab_map[tab] == 'calc':
    st.markdown(f'<div class="ios-display">{st.session_state.display}</div>', unsafe_allow_html=True)
    
    # iOS 风格按钮网格
    st.markdown('<div class="ios-grid">', unsafe_allow_html=True)
    
    # 第一行：功能按钮
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("AC", key="ac"):
            st.session_state.display = '0'
            st.session_state.expression = ''
            st.rerun()
    with c2:
        if st.button("±", key="neg"):
            if st.session_state.expression:
                if st.session_state.expression.startswith('-'):
                    st.session_state.expression = st.session_state.expression[1:]
                else:
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
    
    # 第二行：7,8,9,×
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
    
    # 第三行：4,5,6,-
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
    
    # 第四行：1,2,3,+
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
    
    # 第五行：0,.,=
    c1, c2 = st.columns([2, 1])
    with c1:
        if st.button("0", key="0"):
            st.session_state.expression += '0'
            st.session_state.display = st.session_state.expression
            st.rerun()
    with c2:
        if st.button(".", key="dot"):
            if '.' not in st.session_state.expression.split()[-1] if st.session_state.expression else True:
                st.session_state.expression += '.'
                st.session_state.display = st.session_state.expression
            st.rerun()
    with c2:
        if st.button("=", key="eq"):
            try:
                expr = st.session_state.expression.replace('×', '*').replace('÷', '/').replace(' ', '')
                result = eval(expr)
                st.session_state.display = str(int(result)) if result == int(result) else str(round(result, 10))
                st.session_state.expression = st.session_state.display
            except:
                st.session_state.display = 'Error'
                st.session_state.expression = ''
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== 房贷 ==========
elif tab_map[tab] == 'loan':
    st.markdown('<div class="card-dark"><div class="card-title">🏠 房贷计算器</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        amount = st.number_input("贷款金额（万元）", value=100.0, key="loan_amt")
    with c2:
        rate = st.number_input("年利率（%）", value=3.5, step=0.1, key="loan_rate")
    years = st.selectbox("贷款年限", [5, 10, 15, 20, 25, 30], index=3, key="loan_years")
    
    if st.button("计算月供", key="calc_loan"):
        m = amount * 10000
        r = rate / 100 / 12
        n = years * 12
        monthly = m * r * (1+r)**n / ((1+r)**n - 1)
        st.session_state.loan_result = {'monthly': monthly, 'total': monthly*n, 'interest': monthly*n - m}
    
    if st.session_state.loan_result:
        r = st.session_state.loan_result
        st.markdown(f'''
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:15px; margin-top:20px;">
            <div class="result-ios"><div class="result-label">月供</div><div class="result-value" style="color:#ff9500">{r['monthly']:.2f}</div></div>
            <div class="result-ios"><div class="result-label">总利息</div><div class="result-value" style="color:#ff9500">{r['interest']:.0f}</div></div>
            <div class="result-ios"><div class="result-label">总还款</div><div class="result-value" style="color:#34c759">{r['total']:.0f}</div></div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== 换算 ==========
elif tab_map[tab] == 'unit':
    st.markdown('<div class="card-dark"><div class="card-title">🔄 单位换算</div>', unsafe_allow_html=True)
    
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
        st.markdown(f'<div class="result-ios" style="margin-top:20px;"><div class="result-label">{names[to]}</div><div class="result-value" style="color:#34c759; font-size:32px;">{res:.4f}</div></div>', unsafe_allow_html=True)
    
    elif unit_type == "📏 长度":
        u = {"米": 1, "厘米": 0.01, "毫米": 0.001, "千米": 1000, "英尺": 0.3048, "英寸": 0.0254}
        c1, c2, c3 = st.columns(3)
        with c1: val = st.number_input("数值", value=1.0, key="len_val")
        with c2: frm = st.selectbox("从", list(u.keys()), key="len_from")
        with c3: to = st.selectbox("到", list(u.keys()), index=1, key="len_to")
        st.markdown(f'<div class="result-ios" style="margin-top:20px;"><div class="result-value" style="color:#34c759;">{val*u[frm]/u[to]:.6f}</div></div>', unsafe_allow_html=True)
    
    elif unit_type == "⚖️ 重量":
        u = {"公斤": 1, "克": 0.001, "斤": 0.5, "磅": 0.453592, "盎司": 0.0283495}
        c1, c2, c3 = st.columns(3)
        with c1: val = st.number_input("数值", value=1.0, key="wgt_val")
        with c2: frm = st.selectbox("从", list(u.keys()), key="wgt_from")
        with c3: to = st.selectbox("到", list(u.keys()), index=1, key="wgt_to")
        st.markdown(f'<div class="result-ios" style="margin-top:20px;"><div class="result-value" style="color:#34c759;">{val*u[frm]/u[to]:.6f}</div></div>', unsafe_allow_html=True)
    
    elif unit_type == "🌡️ 温度":
        c1, c2 = st.columns(2)
        with c1: val = st.number_input("温度", value=0.0, key="temp_val")
        with c2: frm = st.selectbox("从", ["摄氏度", "华氏度", "开尔文"], key="temp_from")
        to = st.selectbox("到", ["摄氏度", "华氏度", "开尔文"], index=1, key="temp_to")
        
        c = val if frm=="摄氏度" else (val-32)*5/9 if frm=="华氏度" else val-273.15
        res = c if to=="摄氏度" else c*9/5+32 if to=="华氏度" else c+273.15
        st.markdown(f'<div class="result-ios" style="margin-top:20px;"><div class="result-value" style="color:#34c759;">{res:.2f}°</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== 健康 ==========
elif tab_map[tab] == 'health':
    st.markdown('<div class="card-dark"><div class="card-title">❤️ 健康计算</div>', unsafe_allow_html=True)
    
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
        <div style="text-align:center; margin-top:20px;">
            <div style="font-size:64px; font-weight:300; color:{r['color']};">{r['bmi']:.1f}</div>
            <div style="font-size:24px; color:{r['color']};">{r['cat']}</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px; margin-top:20px;">
                <div class="result-ios"><div class="result-label">基础代谢</div><div class="result-value">{r['bmr']:.0f} 千卡</div></div>
                <div class="result-ios"><div class="result-label">每日消耗</div><div class="result-value">{r['tdee']:.0f} 千卡</div></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)