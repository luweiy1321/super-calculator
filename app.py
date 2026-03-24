import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="计算器", page_icon="🧮", layout="centered")

# 主题配置
THEMES = {
    "💜 紫罗蓝": {"bg": "#1c1c1e", "display": "#000000", "display_text": "#ffffff", "keypad": "#1c1c1e", "num": "#2c2c2e", "num_text": "#ffffff", "func": "#636366", "func_text": "#000000", "op": "#a8a8b3", "op_text": "#000000", "eq": "#ff9f0a", "eq_text": "#ffffff"},
    "🌸 樱花粉": {"bg": "#2d1f2d", "display": "#1a1a1a", "display_text": "#ffffff", "keypad": "#2d1f2d", "num": "#3d2d3d", "num_text": "#ffffff", "func": "#5d4d5d", "func_text": "#ffffff", "op": "#d4a5b9", "op_text": "#1a1a1a", "eq": "#ff6b9d", "eq_text": "#ffffff"},
    "🌊 海洋蓝": {"bg": "#0d1f2d", "display": "#0a1520", "display_text": "#ffffff", "keypad": "#0d1f2d", "num": "#1d2f3d", "num_text": "#ffffff", "func": "#3d5a6d", "func_text": "#ffffff", "op": "#5da4b4", "op_text": "#0a1520", "eq": "#4ecdc4", "eq_text": "#0a1520"},
    "🍋 柠檬黄": {"bg": "#1f1f1f", "display": "#000000", "display_text": "#ffffff", "keypad": "#1f1f1f", "num": "#2d2d2d", "num_text": "#ffffff", "func": "#4d4d4d", "func_text": "#ffffff", "op": "#f7dc6f", "op_text": "#1f1f1f", "eq": "#f39c12", "eq_text": "#ffffff"},
    "🖤 经典黑": {"bg": "#000000", "display": "#000000", "display_text": "#ffffff", "keypad": "#000000", "num": "#333333", "num_text": "#ffffff", "func": "#a5a5a5", "func_text": "#000000", "op": "#ff9500", "op_text": "#ffffff", "eq": "#ff9500", "eq_text": "#ffffff"},
}

theme_name = st.selectbox("🎨 主题", list(THEMES.keys()), index=4, key="theme_sel")
theme = THEMES[theme_name]

# 使用 session_state 保存主题选择
if 'current_theme' not in st.session_state or st.session_state.get('theme_key') != 'theme_sel':
    st.session_state.current_theme = theme
    st.session_state.theme_key = 'theme_sel'

# 获取当前主题（每次选择后更新）
if 'theme_sel' in st.session_state and st.session_state.get('last_theme') != st.session_state.theme_sel:
    st.session_state.current_theme = THEMES.get(st.session_state.theme_sel, THEMES["🖤 经典黑"])
    st.session_state.last_theme = st.session_state.theme_sel
    
theme = st.session_state.get('current_theme', THEMES["🖤 经典黑"])

# CSS - 使用 CSS Grid 确保移动端布局
st.markdown(f"""
<style>
    .stApp {{ background: {theme['bg']}; padding: 10px; }}
    
    .calc-wrapper {{
        max-width: 400px;
        margin: 0 auto;
    }}
    
    .calc-display {{
        background: {theme['display']};
        color: {theme['display_text']};
        padding: 20px;
        font-size: 48px;
        font-weight: 300;
        text-align: right;
        min-height: 80px;
        border-radius: 20px 20px 0 0;
        word-break: break-all;
    }}
    
    .calc-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        padding: 10px;
        background: {theme['keypad']};
        border-radius: 0 0 20px 20px;
    }}
    
    .calc-btn {{
        border: none;
        border-radius: 50%;
        font-size: 24px;
        height: 70px;
        width: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        margin: 0 auto;
    }}
    
    .calc-btn:active {{ opacity: 0.7; }}
    
    .btn-num {{ background: {theme['num']}; color: {theme['num_text']}; }}
    .btn-func {{ background: {theme['func']}; color: {theme['func_text']}; }}
    .btn-op {{ background: {theme['op']}; color: {theme['op_text']}; }}
    .btn-eq {{ background: {theme['eq']}; color: {theme['eq_text']}; }}
    
    .btn-zero {{
        grid-column: span 2;
        width: 100%;
        border-radius: 35px;
        justify-content: flex-start;
        padding-left: 28px;
    }}
    
    .card {{ background: {theme['num']}; border-radius: 16px; padding: 15px; margin: 10px auto; max-width: 400px; }}
    .title {{ font-size: 16px; font-weight: 600; color: {theme['num_text']}; margin-bottom: 12px; }}
    .input {{ background: {theme['func']}; border: none; border-radius: 10px; color: {theme['num_text']}; padding: 12px; font-size: 15px; width: 100%; }}
    .btn-action {{ background: {theme['op']}; color: {theme['op_text']}; border: none; border-radius: 10px; padding: 12px; font-size: 15px; width: 100%; }}
    .result-card {{ background: {theme['func']}; border-radius: 10px; padding: 12px; text-align: center; }}
    .result-label {{ font-size: 11px; color: {theme['num_text']}99; }}
    .result-value {{ font-size: 18px; font-weight: 600; color: {theme['op']}; margin-top: 3px; }}
    
    /* 强制使用 CSS Grid 布局 */
    [data-testid="stHorizontalBlock"] {{
        display: grid !important;
        grid-template-columns: repeat(4, 1fr) !important;
        gap: 8px !important;
    }}
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
tab = st.radio("", ["🧮", "🏠", "🔄", "❤️"], horizontal=True, index=0, key="tab_main", label_visibility="collapsed")
tab_map = {'🧮': 'calc', '🏠': 'loan', '🔄': 'unit', '❤️': 'health'}

# ========== 计算器 ==========
if tab_map[tab] == 'calc':
    st.markdown('<div class="calc-wrapper">', unsafe_allow_html=True)
    st.markdown(f'<div class="calc-display">{st.session_state.display}</div>', unsafe_allow_html=True)
    
    # 使用 HTML 渲染按钮 - 强制 Grid 布局
    buttons_html = f'''
    <div class="calc-grid">
        <button class="calc-btn btn-func" onclick="parent.postMessage({{type:'set_theme',theme:'AC'}}, '*')">AC</button>
        <button class="calc-btn btn-func" onclick="parent.postMessage({{type:'set_theme',theme:'±'}}, '*')">±</button>
        <button class="calc-btn btn-func" onclick="parent.postMessage({{type:'set_theme',theme:'%'}}, '*')">%</button>
        <button class="calc-btn btn-op" onclick="parent.postMessage({{type:'set_theme',theme:'÷'}}, '*')">÷</button>
        
        <button class="calc-btn btn-num" onclick="parent.postMessage({{type:'set_theme',theme:'7'}}, '*')">7</button>
        <button class="calc-btn btn-num" onclick="parent.postMessage({{type:'set_theme',theme:'8'}}, '*')">8</button>
        <button class="calc-btn btn-num" onclick="parent.postMessage({{type:'set_theme',theme:'9'}}, '*')">9</button>
        <button class="calc-btn btn-op" onclick="parent.postMessage({{type:'set_theme',theme:'×'}}, '*')">×</button>
        
        <button class="calc-btn btn-num" onclick="parent.postMessage({{type:'set_theme',theme:'4'}}, '*')">4</button>
        <button class="calc-btn btn-num" onclick="parent.postMessage({{type:'set_theme',theme:'5'}}, '*')">5</button>
        <button class="calc-btn btn-num" onclick="parent.postMessage({{type:'set_theme',theme:'6'}}, '*')">6</button>
        <button class="calc-btn btn-op" onclick="parent.postMessage({{type:'set_theme',theme:'-'}}, '*')">-</button>
        
        <button class="calc-btn btn-num" onclick="parent.postMessage({{type:'set_theme',theme:'1'}}, '*')">1</button>
        <button class="calc-btn btn-num" onclick="parent.postMessage({{type:'set_theme',theme:'2'}}, '*')">2</button>
        <button class="calc-btn btn-num" onclick="parent.postMessage({{type:'set_theme',theme:'3'}}, '*')">3</button>
        <button class="calc-btn btn-op" onclick="parent.postMessage({{type:'set_theme',theme:'+'}}, '*')">+</button>
        
        <button class="calc-btn btn-num btn-zero" onclick="parent.postMessage({{type:'set_theme',theme:'0'}}, '*')">0</button>
        <button class="calc-btn btn-num" onclick="parent.postMessage({{type:'set_theme',theme:'.'}}, '*')">.</button>
        <button class="calc-btn btn-num"></button>
        <button class="calc-btn btn-eq" onclick="parent.postMessage({{type:'set_theme',theme:'='}}, '*')">=</button>
    </div>
    '''
    
    st.markdown(buttons_html, unsafe_allow_html=True)
    
    # 使用隐藏的 Streamlit 按钮处理点击
    for btn in ['AC', '±', '%', '÷', '×', '-', '+', '=', '7', '8', '9', '4', '5', '6', '1', '2', '3', '0', '.']:
        if st.button(btn, key=f"btn_{btn}"):
            if btn == 'AC':
                st.session_state.display = '0'
                st.session_state.expression = ''
            elif btn == '±':
                if st.session_state.expression:
                    st.session_state.expression = '-' + st.session_state.expression
                    st.session_state.display = st.session_state.expression
            elif btn in ['÷', '×', '-', '+', '%']:
                st.session_state.expression += btn
                st.session_state.display = st.session_state.expression
            elif btn == '=':
                try:
                    expr = st.session_state.expression.replace('×', '*').replace('÷', '/')
                    result = eval(expr)
                    st.session_state.display = str(int(result)) if result == int(result) else str(round(result, 10))
                    st.session_state.expression = st.session_state.display
                except:
                    st.session_state.display = 'Error'
                    st.session_state.expression = ''
            else:
                st.session_state.expression += btn
                st.session_state.display = st.session_state.expression
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== 房贷 ==========
elif tab_map[tab] == 'loan':
    st.markdown('<div class="card"><div class="title">🏠 房贷计算器</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: amount = st.number_input("贷款(万元)", value=100.0, key="la")
    with c2: rate = st.number_input("利率(%)", value=3.5, step=0.1, key="lr")
    years = st.selectbox("年限", [5, 10, 15, 20, 25, 30], index=3, key="ly")
    
    if st.button("计算", key="calc_ln"):
        m = amount * 10000; r = rate / 100 / 12; n = years * 12
        monthly = m * r * (1+r)**n / ((1+r)**n - 1)
        st.session_state.loan_result = {'monthly': monthly, 'total': monthly*n, 'interest': monthly*n - m}
    
    if st.session_state.loan_result:
        r = st.session_state.loan_result
        st.markdown(f'''
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; margin-top:12px;">
            <div class="result-card"><div class="result-label">月供</div><div class="result-value">{r['monthly']:.2f}</div></div>
            <div class="result-card"><div class="result-label">利息</div><div class="result-value">{r['interest']:.0f}</div></div>
            <div class="result-card"><div class="result-label">总额</div><div class="result-value">{r['total']:.0f}</div></div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ========== 换算 ==========
elif tab_map[tab] == 'unit':
    st.markdown('<div class="card"><div class="title">🔄 单位换算</div>', unsafe_allow_html=True)
    unit_type = st.selectbox("类型", ["💱 货币", "📏 长度", "⚖️ 重量", "🌡️ 温度"], key="ut")
    
    if unit_type == "💱 货币":
        if st.button("🔄", key="ref_rate"):
            try:
                resp = urllib.request.urlopen('https://api.frankfurter.dev/v1/latest?base=CNY', timeout=5)
                data = json.loads(resp.read().decode())
                if data.get('rates'): st.session_state.rates = {'CNY': 1, **data['rates']}
            except: st.error("失败")
        
        c1, c2, c3 = st.columns(3)
        with c1: amt = st.number_input("金额", value=1.0, key="ca")
        with c2: frm = st.selectbox("从", ['CNY','USD','EUR','JPY','HKD','GBP','KRW'], key="cf")
        with c3: to = st.selectbox("到", ['CNY','USD','EUR','JPY','HKD','GBP','KRW'], index=1, key="ct")
        
        fr = st.session_state.rates.get(frm, 1)
        tr = st.session_state.rates.get(to, 1)
        res = (amt / fr) * tr
        names = {'CNY':'人民币','USD':'美元','EUR':'欧元','JPY':'日元','HKD':'港币','GBP':'英镑','KRW':'韩元'}
        st.markdown(f'<div class="result-card" style="margin-top:12px;"><div class="result-value" style="font-size:24px;">{names[to]} {res:.4f}</div></div>', unsafe_allow_html=True)
    
    elif unit_type == "📏 长度":
        u = {"米":1,"厘米":0.01,"毫米":0.001,"千米":1000,"英尺":0.3048,"英寸":0.0254}
        c1, c2, c3 = st.columns(3)
        with c1: val = st.number_input("数值", value=1.0, key="lv")
        with c2: frm = st.selectbox("从", list(u.keys()), key="lf")
        with c3: to = st.selectbox("到", list(u.keys()), index=1, key="lt")
        st.markdown(f'<div class="result-card" style="margin-top:12px;"><div class="result-value">{val*u[frm]/u[to]:.6f}</div></div>', unsafe_allow_html=True)
    
    elif unit_type == "⚖️ 重量":
        u = {"公斤":1,"克":0.001,"斤":0.5,"磅":0.453592,"盎司":0.0283495}
        c1, c2, c3 = st.columns(3)
        with c1: val = st.number_input("数值", value=1.0, key="wv")
        with c2: frm = st.selectbox("从", list(u.keys()), key="wf")
        with c3: to = st.selectbox("到", list(u.keys()), index=1, key="wt")
        st.markdown(f'<div class="result-card" style="margin-top:12px;"><div class="result-value">{val*u[frm]/u[to]:.6f}</div></div>', unsafe_allow_html=True)
    
    elif unit_type == "🌡️ 温度":
        c1, c2 = st.columns(2)
        with c1: val = st.number_input("温度", value=0.0, key="tv")
        with c2: frm = st.selectbox("从", ["摄氏度","华氏度","开尔文"], key="tf")
        to = st.selectbox("到", ["摄氏度","华氏度","开尔文"], index=1, key="tt")
        c = val if frm=="摄氏度" else (val-32)*5/9 if frm=="华氏度" else val-273.15
        res = c if to=="摄氏度" else c*9/5+32 if to=="华氏度" else c+273.15
        st.markdown(f'<div class="result-card" style="margin-top:12px;"><div class="result-value">{res:.2f}°</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== 健康 ==========
elif tab_map[tab] == 'health':
    st.markdown('<div class="card"><div class="title">❤️ 健康计算</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: h = st.number_input("身高(cm)", value=170, key="hh")
    with c2: w = st.number_input("体重(kg)", value=65, key="hw")
    c3, c4 = st.columns(2)
    with c3: age = st.number_input("年龄", value=30, key="ha")
    with c4: gender = st.selectbox("性别", ["男","女"], key="hg")
    act = st.selectbox("运动量", ["久坐(1.2)","轻度(1.375)","中度(1.55)","重度(1.725)"], key="hac")
    
    if st.button("计算", key="calc_h"):
        bmi = w / ((h/100)**2)
        cat = "偏瘦" if bmi < 18.5 else "正常" if bmi < 24 else "偏胖" if bmi < 28 else "肥胖"
        bmr = 10*w + 6.25*h - 5*age + (5 if gender=="男" else -161)
        tdee = bmr * float(act.split("(")[1].split(")")[0])
        st.session_state.health_result = {'bmi': bmi, 'cat': cat, 'bmr': bmr, 'tdee': tdee}
    
    if st.session_state.health_result:
        r = st.session_state.health_result
        st.markdown(f'''
        <div style="text-align:center;">
            <div style="font-size:48px; font-weight:600; color:{theme['op']};">{r['bmi']:.1f}</div>
            <div style="font-size:18px; color:{theme['op']};">{r['cat']}</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:12px;">
                <div class="result-card"><div class="result-label">基础代谢</div><div class="result-value">{r['bmr']:.0f}</div></div>
                <div class="result-card"><div class="result-label">每日消耗</div><div class="result-value">{r['tdee']:.0f}</div></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)