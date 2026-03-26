import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="超级计算器", page_icon="🧮", layout="centered")

# 主题配置 - iOS风格
THEMES = {
    "深空黑": {"bg": "#000000", "display": "#000000", "btn_bg": "#333333", "orange": "#ff9f0a", "func": "#a5a5a5", "sci": "#505050", "sci_text": "#ff9f0a", "text": "#ffffff", "expr": "#888888"},
    "海洋蓝": {"bg": "#001f3f", "display": "#001f3f", "btn_bg": "#003366", "orange": "#0074d9", "func": "#004080", "sci": "#004080", "sci_text": "#7fdbff", "text": "#ffffff", "expr": "#7fdbff"},
    "极光紫": {"bg": "#1a0a2e", "display": "#1a0a2e", "btn_bg": "#2d1b4e", "orange": "#9b59b6", "func": "#3d2066", "sci": "#3d2066", "sci_text": "#d4a5ff", "text": "#ffffff", "expr": "#9b59b6"},
    "荧光绿": {"bg": "#0a1a0a", "display": "#0a1a0a", "btn_bg": "#1a3a1a", "orange": "#2ecc40", "func": "#1e4d2b", "sci": "#1e4d2b", "sci_text": "#7dff7d", "text": "#ffffff", "expr": "#2ecc40"},
    "烈焰红": {"bg": "#1a0a0a", "display": "#1a0a0a", "btn_bg": "#3a1a1a", "orange": "#e74c3c", "func": "#4a2020", "sci": "#4a2020", "sci_text": "#ff6b6b", "text": "#ffffff", "expr": "#e74c3c"},
    "香槟金": {"bg": "#1a150a", "display": "#1a150a", "btn_bg": "#3a3020", "orange": "#f39c12", "func": "#4a4025", "sci": "#4a4025", "sci_text": "#ffd700", "text": "#ffffff", "expr": "#f39c12"},
}

# 初始化session_state
for k, v in [('calc_expr', ''), ('calc_result', '0'), ('pending_num', None), ('pending_op', None), ('is_2nd', False), ('is_deg', True), ('has_result', False), ('rates', {'CNY':1,'USD':7.2,'EUR':0.95,'JPY':150,'HKD':0.9,'GBP':0.85,'KRW':190}), ('loan_result', None), ('health_result', None)]:
    if k not in st.session_state: st.session_state[k] = v

# 侧边栏主题选择
with st.sidebar:
    st.markdown("### 🎨 配色主题")
    theme_name = st.selectbox("选择主题", list(THEMES.keys()), index=0, key="theme_select")
    theme = THEMES[theme_name]
    t_bg = theme['bg']
    t_display = theme['display']
    t_btn_bg = theme['btn_bg']
    t_orange = theme['orange']
    t_func = theme['func']
    t_sci = theme['sci']
    t_sci_text = theme['sci_text']
    t_text = theme['text']
    t_expr = theme['expr']

# 计算器函数
def format_num(n):
    if n is None: return '0'
    try:
        n = float(n)
        if n != n: return 'Error'  # NaN
        if not abs(n) < float('inf'): return '∞' if n > 0 else '-∞'
        if abs(n) > 1e12: return f'{n:.2e}'
        if n == int(n): return str(int(n))
        return f'{n:.10g}'
    except: return 'Error'

def calc_eval(a, b, op):
    try:
        a, b = float(a), float(b)
        if op == '+': return a + b
        elif op == '-': return a - b
        elif op == '×': return a * b
        elif op == '÷': return 0 if b == 0 else a / b
        elif op == '^': return a ** b
        return b
    except: return 'Error'

def to_rad(d): return d * 3.14159265 / 180 if st.session_state.is_deg else d
def to_deg(r): return r * 180 / 3.14159265 if st.session_state.is_deg else r

def handle_num(n):
    if st.session_state.has_result:
        st.session_state.pending_num = None
        st.session_state.has_result = False
    if st.session_state.pending_num is None:
        st.session_state.pending_num = '0.' if n == '.' else n
    else:
        if n == '.' and '.' in st.session_state.pending_num: return
        if len(st.session_state.pending_num) < 12:
            st.session_state.pending_num += n
    st.session_state.calc_result = st.session_state.pending_num

def handle_op(op):
    if st.session_state.pending_num is None: return
    if st.session_state.pending_op and not st.session_state.has_result:
        result = calc_eval(st.session_state.pending_num, st.session_state.pending_num, st.session_state.pending_op)
        st.session_state.pending_num = format_num(result)
    st.session_state.calc_expr = f"{st.session_state.pending_num} {op}"
    st.session_state.pending_op = op
    st.session_state.has_result = False

def handle_sci(func):
    current = float(st.session_state.pending_num) if st.session_state.pending_num else 0
    prev_2nd = st.session_state.is_2nd
    result = None
    expr = ""

    if func == '2nd':
        st.session_state.is_2nd = not st.session_state.is_2nd
        return
    elif func == 'sin':
        result = to_deg(math.asin(current)) if prev_2nd else math.sin(to_rad(current))
        expr = f"sin⁻¹({current})" if prev_2nd else f"sin({current})"
    elif func == 'cos':
        result = to_deg(math.acos(current)) if prev_2nd else math.cos(to_rad(current))
        expr = f"cos⁻¹({current})" if prev_2nd else f"cos({current})"
    elif func == 'tan':
        result = to_deg(math.atan(current)) if prev_2nd else math.tan(to_rad(current))
        expr = f"tan⁻¹({current})" if prev_2nd else f"tan({current})"
    elif func == 'x2':
        result = current * current
        expr = f"{current}²"
    elif func == 'sqrt':
        result = current ** 0.25 if prev_2nd else math.sqrt(current)
        expr = f"∜({current})" if prev_2nd else f"√({current})"
    elif func == 'pow':
        handle_op('^')
        return
    elif func == 'pi':
        result = 3.14159265
        expr = "π"
    elif func == 'e':
        result = 2.71828183
        expr = "e"
    elif func == 'fact':
        f = 1
        for i in range(2, min(int(current), 170) + 1): f *= i
        result = f
        expr = f"{current}!"
    elif func == '(':
        st.session_state.calc_expr += '('
        return
    elif func == ')':
        st.session_state.calc_expr += ')'
        return
    elif func == 'ln':
        result = math.exp(current) if prev_2nd else math.log(current)
        expr = f"e^({current})" if prev_2nd else f"ln({current})"
    elif func == 'log':
        result = 10 ** current if prev_2nd else math.log10(current)
        expr = f"10^({current})" if prev_2nd else f"log({current})"
    elif func == '%':
        result = current / 100
        expr = f"{current}%"
    elif func == 'exp':
        st.session_state.calc_expr = f"{current} × 10^"
        st.session_state.pending_op = 'EXP'
        st.session_state.has_result = False
        st.session_state.is_2nd = False
        return

    if result is not None:
        st.session_state.calc_expr = expr
        st.session_state.calc_result = format_num(result)
        st.session_state.pending_num = format_num(result)
        st.session_state.has_result = True
    st.session_state.is_2nd = False

def handle_calc():
    if st.session_state.pending_num is None or st.session_state.pending_op is None:
        st.session_state.calc_expr = f"{st.session_state.calc_result} ="
        return
    a = float(st.session_state.pending_num) if not st.session_state.has_result else float(st.session_state.calc_result)
    b = float(st.session_state.pending_num)
    op = st.session_state.pending_op

    if op == 'EXP':
        result = a * (10 ** b)
        expr = f"{a} × 10^{b}"
    elif op == '^':
        result = a ** b
        expr = f"{a}^{b}"
    else:
        result = calc_eval(a, b, op)
        expr = f"{a} {op} {b}"

    st.session_state.calc_expr = f"{expr} ="
    st.session_state.calc_result = format_num(result)
    st.session_state.pending_num = None
    st.session_state.pending_op = None
    st.session_state.has_result = True

def handle_clear():
    st.session_state.calc_expr = ''
    st.session_state.calc_result = '0'
    st.session_state.pending_num = None
    st.session_state.pending_op = None
    st.session_state.has_result = False
    st.session_state.is_2nd = False

def handle_negate():
    if st.session_state.pending_num:
        val = format_num(float(st.session_state.pending_num) * -1)
        st.session_state.pending_num = val
        st.session_state.calc_result = val

def toggle_deg():
    st.session_state.is_deg = not st.session_state.is_deg

# 页面
tab = st.radio("", ["🧮 计算", "🏠 房贷", "🔄 换算", "❤️ 健康"], horizontal=True, index=0, key="t1")
tm = {'🧮 计算': 0, '🏠 房贷': 1, '🔄 换算': 2, '❤️ 健康': 3}

# 计算器页面
if tm[tab] == 0:
    import math

    # CSS样式
    st.markdown(f"""
    <style>
        .stApp {{ background: {t_bg}; }}
        .calc-wrap {{ max-width: 340px; margin: 0 auto; }}
        .display {{ background: {t_display}; padding: 20px; min-height: 100px; border-radius: 15px 15px 0 0; display: flex; flex-direction: column; justify-content: flex-end; }}
        .expr {{ font-size: 16px; color: {t_expr}; margin-bottom: 5px; min-height: 20px; text-align: right; }}
        .result {{ font-size: 48px; color: {t_text}; text-align: right; letter-spacing: -2px; }}
        .btn-row {{ display: flex; margin-bottom: 6px; justify-content: center; }}
        .btn {{ flex: 1; height: 52px; border: none; border-radius: 50%; font-size: 18px; font-weight: 500; cursor: pointer; transition: transform 0.1s; display: flex; align-items: center; justify-content: center; margin: 0 3px; }}
        .btn:active {{ transform: scale(0.92); }}
        .btn-num {{ background: {t_btn_bg}; color: {t_text}; }}
        .btn-orange {{ background: {t_orange}; color: white; }}
        .btn-func {{ background: {t_func}; color: {t_text}; }}
        .btn-sci {{ background: {t_sci}; color: {t_sci_text}; }}
        .btn-wide {{ flex: 2; }}
        .buttons {{ background: {t_display}; padding: 8px; border-radius: 0 0 15px 15px; }}
        .mode-bar {{ display: flex; justify-content: flex-end; padding: 8px 10px; background: {t_display}; }}
        .mode-btn {{ background: {t_sci}; color: {t_sci_text}; border: none; padding: 4px 12px; border-radius: 10px; font-size: 12px; cursor: pointer; }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="calc-wrap">', unsafe_allow_html=True)

    # 显示区
    st.markdown(f'''
    <div class="display">
        <div class="expr">{st.session_state.calc_expr}</div>
        <div class="result">{st.session_state.calc_result}</div>
    </div>
    ''', unsafe_allow_html=True)

    # 模式切换
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("2nd", key="btn_2nd"):
            st.session_state.is_2nd = not st.session_state.is_2nd
            st.rerun()
    with col2:
        if st.button("DEG" if st.session_state.is_deg else "RAD", key="btn_deg"):
            toggle_deg()
            st.rerun()
    with col3:
        if st.button("sin", key="btn_sin"):
            handle_sci('sin')
            st.rerun()
    with col4:
        if st.button("cos", key="btn_cos"):
            handle_sci('cos')
            st.rerun()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("tan", key="btn_tan"):
            handle_sci('tan')
            st.rerun()
    with col2:
        if st.button("x²", key="btn_x2"):
            handle_sci('x2')
            st.rerun()
    with col3:
        if st.button("√", key="btn_sqrt"):
            handle_sci('sqrt')
            st.rerun()
    with col4:
        if st.button("xʸ", key="btn_pow"):
            handle_sci('pow')
            st.rerun()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("π", key="btn_pi"):
            handle_sci('pi')
            st.rerun()
    with col2:
        if st.button("e", key="btn_e"):
            handle_sci('e')
            st.rerun()
    with col3:
        if st.button("n!", key="btn_fact"):
            handle_sci('fact')
            st.rerun()
    with col4:
        if st.button("(", key="btn_lpar"):
            handle_sci('(')
            st.rerun()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button(")", key="btn_rpar"):
            handle_sci(')')
            st.rerun()
    with col2:
        if st.button("ln", key="btn_ln"):
            handle_sci('ln')
            st.rerun()
    with col3:
        if st.button("log", key="btn_log"):
            handle_sci('log')
            st.rerun()
    with col4:
        if st.button("EXP", key="btn_exp"):
            handle_sci('exp')
            st.rerun()

    # 分隔线
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("AC", key="btn_ac"):
            handle_clear()
            st.rerun()
    with col2:
        if st.button("±", key="btn_neg"):
            handle_negate()
            st.rerun()
    with col3:
        if st.button("%", key="btn_pct"):
            handle_sci('%')
            st.rerun()
    with col4:
        if st.button("÷", key="btn_div"):
            handle_op('÷')
            st.rerun()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("7", key="btn_7"):
            handle_num('7')
            st.rerun()
    with col2:
        if st.button("8", key="btn_8"):
            handle_num('8')
            st.rerun()
    with col3:
        if st.button("9", key="btn_9"):
            handle_num('9')
            st.rerun()
    with col4:
        if st.button("×", key="btn_mul"):
            handle_op('×')
            st.rerun()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("4", key="btn_4"):
            handle_num('4')
            st.rerun()
    with col2:
        if st.button("5", key="btn_5"):
            handle_num('5')
            st.rerun()
    with col3:
        if st.button("6", key="btn_6"):
            handle_num('6')
            st.rerun()
    with col4:
        if st.button("-", key="btn_sub"):
            handle_op('-')
            st.rerun()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("1", key="btn_1"):
            handle_num('1')
            st.rerun()
    with col2:
        if st.button("2", key="btn_2"):
            handle_num('2')
            st.rerun()
    with col3:
        if st.button("3", key="btn_3"):
            handle_num('3')
            st.rerun()
    with col4:
        if st.button("+", key="btn_add"):
            handle_op('+')
            st.rerun()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("0", key="btn_0"):
            handle_num('0')
            st.rerun()
    with col2:
        if st.button(".", key="btn_dot"):
            handle_num('.')
            st.rerun()
    with col3:
        if st.button("⌫", key="btn_del"):
            if st.session_state.pending_num and len(st.session_state.pending_num) > 1:
                st.session_state.pending_num = st.session_state.pending_num[:-1]
            else:
                st.session_state.pending_num = '0'
            st.session_state.calc_result = st.session_state.pending_num
            st.rerun()
    with col4:
        if st.button("=", key="btn_eq"):
            handle_calc()
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# 房贷计算
elif tm[tab] == 1:
    st.markdown(f'''
    <div style="max-width: 340px; margin: 0 auto; background: #2a2a2a; padding: 20px; border-radius: 15px;">
        <div style="font-size: 20px; margin-bottom: 15px;">🏠 房贷计算器</div>
    </div>
    ''', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: amt = st.number_input("贷款(万)", 100.0, key="la1")
    with c2: rt = st.number_input("利率(%)", 3.5, step=0.1, key="lr1")
    yr = st.selectbox("年限", [5,10,15,20,25,30], index=3, key="ly1")
    if st.button("计算", key="calc1"):
        m = amt * 10000; r = rt / 100 / 12; n = yr * 12
        mp = m * r * (1+r)**n / ((1+r)**n - 1)
        st.session_state.loan_result = {'m': mp, 't': mp * n, 'i': mp * n - m}
    if st.session_state.loan_result:
        r = st.session_state.loan_result
        st.markdown(f'''
        <div style="max-width: 340px; margin: 15px auto; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
            <div style="background: #3a3a3a; padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 12px; color: #888;">月供</div>
                <div style="font-size: 18px; color: #007AFF;">{r["m"]:.2f}</div>
            </div>
            <div style="background: #3a3a3a; padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 12px; color: #888;">利息</div>
                <div style="font-size: 18px; color: #ff9500;">{r["i"]:.0f}</div>
            </div>
            <div style="background: #3a3a3a; padding: 15px; border-radius: 10px; text-align: center;">
                <div style="font-size: 12px; color: #888;">总额</div>
                <div style="font-size: 18px; color: #34c759;">{r["t"]:.0f}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

# 单位换算
elif tm[tab] == 2:
    st.markdown(f'''
    <div style="max-width: 340px; margin: 0 auto; background: #2a2a2a; padding: 20px; border-radius: 15px;">
        <div style="font-size: 20px; margin-bottom: 15px;">🔄 单位换算</div>
    </div>
    ''', unsafe_allow_html=True)
    ut = st.selectbox("类型", ["💱 货币", "📏 长度", "⚖️ 重量", "🌡️ 温度"], key="ut1")

    if ut == "💱 货币":
        if st.button("🔄 更新汇率", key="rf1"):
            try:
                st.session_state.rates = {'CNY': 1, **json.loads(urllib.request.urlopen('https://api.frankfurter.dev/v1/latest?base=CNY', timeout=5).read().decode())['rates']}
            except:
                pass
        c1, c2, c3 = st.columns(3)
        with c1: amt = st.number_input("金额", 1.0, key="ca1")
        with c2: frm = st.selectbox("从", ['CNY','USD','EUR','JPY','HKD','GBP','KRW'], key="cf1")
        with c3: to = st.selectbox("到", ['CNY','USD','EUR','JPY','HKD','GBP','KRW'], index=1, key="ct1")
        res = (amt / st.session_state.rates.get(frm, 1)) * st.session_state.rates.get(to, 1)
        names = {'CNY':'人民币','USD':'美元','EUR':'欧元','JPY':'日元','HKD':'港币','GBP':'英镑','KRW':'韩元'}
        st.markdown(f'<div style="max-width: 340px; margin: 15px auto; background: #3a3a3a; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px;">{names[to]} {res:.4f}</div>', unsafe_allow_html=True)

    elif ut == "📏 长度":
        u = {"米":1,"厘米":0.01,"毫米":0.001,"千米":1000,"英尺":0.3048,"英寸":0.0254}
        c1, c2, c3 = st.columns(3)
        with c1: v = st.number_input("数值", 1.0, key="lv1")
        with c2: f = st.selectbox("从", list(u.keys()), key="lf1")
        with c3: t = st.selectbox("到", list(u.keys()), index=1, key="lt1")
        st.markdown(f'<div style="max-width: 340px; margin: 15px auto; background: #3a3a3a; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px;">{v*u[f]/u[t]:.6f}</div>', unsafe_allow_html=True)

    elif ut == "⚖️ 重量":
        u = {"公斤":1,"克":0.001,"斤":0.5,"磅":0.453592,"盎司":0.0283495}
        c1, c2, c3 = st.columns(3)
        with c1: v = st.number_input("数值", 1.0, key="wv1")
        with c2: f = st.selectbox("从", list(u.keys()), key="wf1")
        with c3: t = st.selectbox("到", list(u.keys()), index=1, key="wt1")
        st.markdown(f'<div style="max-width: 340px; margin: 15px auto; background: #3a3a3a; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px;">{v*u[f]/u[t]:.6f}</div>', unsafe_allow_html=True)

    elif ut == "🌡️ 温度":
        c1, c2 = st.columns(2)
        with c1: v = st.number_input("温度", 0.0, key="tv1")
        with c2: f = st.selectbox("从", ["摄氏度","华氏度","开尔文"], key="tf1")
        t = st.selectbox("到", ["摄氏度","华氏度","开尔文"], index=1, key="tt1")
        c = v if f=="摄氏度" else (v-32)*5/9 if f=="华氏度" else v-273.15
        res = c if t=="摄氏度" else c*9/5+32 if t=="华氏度" else c+273.15
        st.markdown(f'<div style="max-width: 340px; margin: 15px auto; background: #3a3a3a; padding: 15px; border-radius: 10px; text-align: center; font-size: 20px;">{res:.2f}°</div>', unsafe_allow_html=True)

# 健康计算
elif tm[tab] == 3:
    st.markdown(f'''
    <div style="max-width: 340px; margin: 0 auto; background: #2a2a2a; padding: 20px; border-radius: 15px;">
        <div style="font-size: 20px; margin-bottom: 15px;">❤️ 健康计算</div>
    </div>
    ''', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: h = st.number_input("身高(cm)", 170, key="hh1")
    with c2: w = st.number_input("体重(kg)", 65, key="hw1")
    c3, c4 = st.columns(2)
    with c3: age = st.number_input("年龄", 30, key="ha1")
    with c4: g = st.selectbox("性别", ["男","女"], key="hg1")
    act = st.selectbox("运动", ["久坐(1.2)","轻度(1.375)","中度(1.55)","重度(1.725)"], key="hac1")
    if st.button("计算", key="hc1"):
        bmi = w / ((h/100)**2)
        cat = "偏瘦" if bmi < 18.5 else "正常" if bmi < 24 else "偏胖" if bmi < 28 else "肥胖"
        bmr = 10*w + 6.25*h - 5*age + (5 if g == "男" else -161)
        tdee = bmr * float(act.split("(")[1].split(")")[0])
        st.session_state.health_result = {'b': bmi, 'c': cat, 'bmr': bmr, 'tdee': tdee}
    if st.session_state.health_result:
        r = st.session_state.health_result
        color = '#34c759' if r['b'] < 24 else '#ff9500' if r['b'] < 28 else '#ff3b30'
        st.markdown(f'''
        <div style="max-width: 340px; margin: 15px auto; text-align: center;">
            <div style="font-size: 56px; font-weight: bold; color: {color};">{r["b"]:.1f}</div>
            <div style="font-size: 20px; color: {color};">{r["c"]}</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 15px;">
                <div style="background: #3a3a3a; padding: 15px; border-radius: 10px; text-align: center;">
                    <div style="font-size: 12px; color: #888;">基础代谢</div>
                    <div style="font-size: 18px;">{r["bmr"]:.0f}</div>
                </div>
                <div style="background: #3a3a3a; padding: 15px; border-radius: 10px; text-align: center;">
                    <div style="font-size: 12px; color: #888;">每日消耗</div>
                    <div style="font-size: 18px;">{r["tdee"]:.0f}</div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
