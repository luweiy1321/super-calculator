import streamlit as st
import urllib.request
import json
import math

st.set_page_config(page_title="超级计算器", page_icon="🧮", layout="centered")

THEMES = {
    "深空黑": {"bg": "#000000", "btn_bg": "#333333", "orange": "#ff9f0a", "func": "#a5a5a5", "sci": "#505050", "sci_text": "#ff9f0a", "text": "#fff"},
    "海洋蓝": {"bg": "#001f3f", "btn_bg": "#003366", "orange": "#0074d9", "func": "#004080", "sci": "#004080", "sci_text": "#7fdbff", "text": "#fff"},
    "极光紫": {"bg": "#1a0a2e", "btn_bg": "#2d1b4e", "orange": "#9b59b6", "func": "#3d2066", "sci": "#3d2066", "sci_text": "#d4a5ff", "text": "#fff"},
    "荧光绿": {"bg": "#0a1a0a", "btn_bg": "#1a3a1a", "orange": "#2ecc40", "func": "#1e4d2b", "sci": "#1e4d2b", "sci_text": "#7dff7d", "text": "#fff"},
    "烈焰红": {"bg": "#1a0a0a", "btn_bg": "#3a1a1a", "orange": "#e74c3c", "func": "#4a2020", "sci": "#4a2020", "sci_text": "#ff6b6b", "text": "#fff"},
    "香槟金": {"bg": "#1a150a", "btn_bg": "#3a3020", "orange": "#f39c12", "func": "#4a4025", "sci": "#4a4025", "sci_text": "#ffd700", "text": "#fff"},
}

defaults = {
    'display': '0', 'expr': '', 'operator': None,
    'prev_val': None, 'is_deg': True, 'is_2nd': False,
    'new_num': True, 'rates': {'CNY':1,'USD':7.2,'EUR':0.95,'JPY':150,'HKD':0.9,'GBP':0.85,'KRW':190},
    'loan_result': None, 'health_result': None
}
for k, v in defaults.items():
    if k not in st.session_state: st.session_state[k] = v

with st.sidebar:
    st.markdown("### 🎨 配色")
    theme_name = st.selectbox("主题", list(THEMES.keys()), index=0, key="ts")
    t = THEMES[theme_name]

def fmt(n):
    try:
        n = float(n)
        if math.isnan(n): return 'Error'
        if math.isinf(n): return '∞' if n > 0 else '-∞'
        if abs(n) > 1e12: return f'{n:.2e}'
        if n == int(n): return str(int(n))
        return f'{n:.10g}'
    except: return 'Error'

def do_calc(a, b, op):
    try:
        a, b = float(a), float(b)
        if op == '+': return a + b
        elif op == '-': return a - b
        elif op == '×': return a * b
        elif op == '÷': return 0 if b == 0 else a / b
        elif op == '^': return a ** b
        return b
    except: return 'Error'

def to_rad(d): return d * math.pi / 180 if st.session_state.is_deg else d
def to_deg(r): return r * 180 / math.pi if st.session_state.is_deg else r

# 处理按钮点击
def handle_button(key):
    s = st.session_state

    # 数字和小数点
    if key in ['b7','b8','b9','b4','b5','b6','b1','b2','b3','b0','bdot']:
        num = key[1] if key != 'bdot' else '.'
        if s.new_num or s.display == '0':
            s.display = '0.' if num == '.' else num
            s.new_num = False
        else:
            if num == '.' and '.' in s.display: return
            if len(s.display) < 12: s.display += num
        return

    # 运算符
    if key in ['badd','bsub','bmul','bdiv','bpow']:
        op = {'badd':'+','bsub':'-','bmul':'×','bdiv':'÷','bpow':'^'}[key]
        if s.operator and not s.new_num:
            result = do_calc(s.prev_val, s.display, s.operator)
            s.display = fmt(result)
            s.prev_val = result
        else:
            s.prev_val = float(s.display)
            s.new_num = True
        s.operator = op
        s.expr = f"{s.prev_val} {op}"
        return

    # 等于
    if key == 'beq':
        if s.operator and s.prev_val is not None:
            result = do_calc(s.prev_val, s.display, s.operator)
            s.expr = f"{s.prev_val} {s.operator} {s.display} ="
            s.display = fmt(result)
            s.prev_val = None
            s.operator = None
            s.new_num = True
        return

    # 清除
    if key == 'bac':
        s.display = '0'
        s.expr = ''
        s.prev_val = None
        s.operator = None
        s.new_num = True
        return

    # 取反
    if key == 'bneg':
        s.display = fmt(float(s.display) * -1)
        return

    # 删除
    if key == 'bdel':
        if len(s.display) > 1:
            s.display = s.display[:-1]
        else:
            s.display = '0'
        return

    # 科学函数
    curr = float(s.display) if s.display else 0
    p2 = s.is_2nd
    s.is_2nd = False

    if key == 'b2nd':
        s.is_2nd = not p2
        return
    if key == 'bdeg':
        s.is_deg = not s.is_deg
        return
    if key == 'bsin':
        r = to_deg(math.asin(curr)) if p2 else math.sin(to_rad(curr))
        s.expr = f"sin⁻¹({curr})" if p2 else f"sin({curr})"
    elif key == 'bcos':
        r = to_deg(math.acos(curr)) if p2 else math.cos(to_rad(curr))
        s.expr = f"cos⁻¹({curr})" if p2 else f"cos({curr})"
    elif key == 'btan':
        r = to_deg(math.atan(curr)) if p2 else math.tan(to_rad(curr))
        s.expr = f"tan⁻¹({curr})" if p2 else f"tan({curr})"
    elif key == 'bx2':
        r, s.expr = curr * curr, f"{curr}²"
    elif key == 'bsqrt':
        r = curr ** 0.25 if p2 else math.sqrt(curr)
        s.expr = f"∜({curr})" if p2 else f"√({curr})"
    elif key == 'bpow':
        if s.operator and not s.new_num:
            result = do_calc(s.prev_val, s.display, s.operator)
            s.display = fmt(result)
            s.prev_val = result
        else:
            s.prev_val = float(s.display)
            s.new_num = True
        s.operator = '^'
        s.expr = f"{s.prev_val} ^"
        return
    elif key == 'bpi':
        r, s.expr = math.pi, "π"
    elif key == 'be':
        r, s.expr = math.e, "e"
    elif key == 'bfact':
        f = 1
        for i in range(2, min(int(curr), 170) + 1): f *= i
        r, s.expr = f, f"{curr}!"
    elif key == 'bln':
        r = math.exp(curr) if p2 else math.log(curr)
        s.expr = f"e^{curr}" if p2 else f"ln({curr})"
    elif key == 'blog':
        r = 10 ** curr if p2 else math.log10(curr)
        s.expr = f"10^{curr}" if p2 else f"log({curr})"
    elif key == 'bpct':
        r, s.expr = curr / 100, f"{curr}%"
    elif key == 'bexp':
        s.prev_val = curr
        s.operator = 'EXP'
        s.expr = f"{curr} × 10^"
        s.new_num = True
        return
    else:
        return

    s.display = fmt(r)
    s.new_num = True

# 检查按钮状态
for key in ['b7','b8','b9','b4','b5','b6','b1','b2','b3','b0','bdot',
            'badd','bsub','bmul','bdiv','bpow','beq','bac','bneg','bdel',
            'b2nd','bdeg','bsin','bcos','btan','bx2','bsqrt',
            'bpi','be','bfact','bln','blog','bpct','bexp']:
    if st.session_state.get(key):
        st.session_state[key] = False
        handle_button(key)
        st.rerun()

# UI
tab = st.radio("", ["🧮 计算", "🏠 房贷", "🔄 换算", "❤️ 健康"], horizontal=True, key="t1")
tm = {'🧮 计算': 0, '🏠 房贷': 1, '🔄 换算': 2, '❤️ 健康': 3}

if tm[tab] == 0:
    st.markdown(f"""
    <style>
        .stApp {{ background: {t['bg']}; }}
        .wrap {{ max-width: 340px; margin: 0 auto; }}
        .display {{ background: {t['bg']}; padding: 20px; min-height: 100px; border-radius: 15px 15px 0 0; display: flex; flex-direction: column; justify-content: flex-end; }}
        .expr {{ font-size: 16px; color: #888; margin-bottom: 5px; text-align: right; }}
        .result {{ font-size: 48px; color: {t['text']}; text-align: right; letter-spacing: -2px; }}
        .buttons {{ background: {t['bg']}; padding: 8px; border-radius: 0 0 15px 15px; }}
        .row {{ display: flex; margin-bottom: 6px; justify-content: center; }}
        .btn {{ flex: 1; height: 52px; border: none; border-radius: 50%; font-size: 16px; font-weight: 500; cursor: pointer; display: flex; align-items: center; justify-content: center; margin: 0 3px; transition: transform 0.1s; }}
        .btn:active {{ transform: scale(0.92); }}
        .num {{ background: {t['btn_bg']}; color: {t['text']}; }}
        .orange {{ background: {t['orange']}; color: white; }}
        .func {{ background: {t['func']}; color: {t['text']}; }}
        .sci {{ background: {t['sci']}; color: {t['sci_text']}; }}
        .wide {{ flex: 2; }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="wrap">', unsafe_allow_html=True)
    st.markdown(f'<div class="display"><div class="expr">{st.session_state.expr}</div><div class="result">{st.session_state.display}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="buttons">', unsafe_allow_html=True)

    # 科学函数
    st.columns(4)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("2nd", key="b2nd", help="第二功能")
    with c2: st.button("DEG" if st.session_state.is_deg else "RAD", key="bdeg", help="角度/弧度")
    with c3: st.button("sin", key="bsin")
    with c4: st.button("cos", key="bcos")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("tan", key="btan")
    with c2: st.button("x²", key="bx2")
    with c3: st.button("√", key="bsqrt")
    with c4: st.button("xʸ", key="bpow")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("π", key="bpi")
    with c2: st.button("e", key="be")
    with c3: st.button("n!", key="bfact")
    with c4: st.button("ln", key="bln")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("log", key="blog")
    with c2: st.button("%", key="bpct")
    with c3: st.button("EXP", key="bexp")
    with c4: st.button(" ", key="bspace", disabled=True)

    st.markdown('---', unsafe_allow_html=True)

    # 基础运算
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("AC", key="bac")
    with c2: st.button("±", key="bneg")
    with c3: st.button("⌫", key="bdel")
    with c4: st.button("÷", key="bdiv")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("7", key="b7")
    with c2: st.button("8", key="b8")
    with c3: st.button("9", key="b9")
    with c4: st.button("×", key="bmul")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("4", key="b4")
    with c2: st.button("5", key="b5")
    with c3: st.button("6", key="b6")
    with c4: st.button("-", key="bsub")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("1", key="b1")
    with c2: st.button("2", key="b2")
    with c3: st.button("3", key="b3")
    with c4: st.button("+", key="badd")

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("0", key="b0")
    with c2: st.button(".", key="bdot")
    with (c3): st.button("", key="bempty", disabled=True)
    with c4: st.button("=", key="beq")

    st.markdown('</div></div>', unsafe_allow_html=True)

elif tm[tab] == 1:
    st.markdown('<div style="max-width:340px;margin:0 auto;background:#2a2a2a;padding:20px;border-radius:15px;"><div style="font-size:20px;margin-bottom:15px;">🏠 房贷计算器</div></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: amt = st.number_input("贷款(万)", 100.0, key="la1")
    with c2: rt = st.number_input("利率(%)", 3.5, step=0.1, key="lr1")
    yr = st.selectbox("年限", [5,10,15,20,25,30], index=3, key="ly1")
    if st.button("计算", key="calc1"):
        m = amt * 10000; r = rt / 100 / 12; n = yr * 12
        mp = m * r * (1+r)**n / ((1+r)**n - 1)
        st.session_state.loan_result = {'m': mp, 't': mp*n, 'i': mp*n - m}
    if st.session_state.loan_result:
        r = st.session_state.loan_result
        st.markdown(f'<div style="max-width:340px;margin:15px auto;display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;"><div style="background:#3a3a3a;padding:15px;border-radius:10px;text-align:center;"><div style="font-size:12px;color:#888;">月供</div><div style="font-size:18px;color:#007AFF;">{r["m"]:.2f}</div></div><div style="background:#3a3a3a;padding:15px;border-radius:10px;text-align:center;"><div style="font-size:12px;color:#888;">利息</div><div style="font-size:18px;color:#ff9500;">{r["i"]:.0f}</div></div><div style="background:#3a3a3a;padding:15px;border-radius:10px;text-align:center;"><div style="font-size:12px;color:#888;">总额</div><div style="font-size:18px;color:#34c759;">{r["t"]:.0f}</div></div></div>', unsafe_allow_html=True)

elif tm[tab] == 2:
    st.markdown('<div style="max-width:340px;margin:0 auto;background:#2a2a2a;padding:20px;border-radius:15px;"><div style="font-size:20px;margin-bottom:15px;">🔄 单位换算</div></div>', unsafe_allow_html=True)
    ut = st.selectbox("类型", ["💱 货币", "📏 长度", "⚖️ 重量", "🌡️ 温度"], key="ut1")
    if ut == "💱 货币":
        if st.button("🔄 更新汇率", key="rf1"):
            try: st.session_state.rates = {'CNY':1,**json.loads(urllib.request.urlopen('https://api.frankfurter.dev/v1/latest?base=CNY',timeout=5).read().decode())['rates']}
            except: pass
        c1, c2, c3 = st.columns(3)
        with c1: amt = st.number_input("金额", 1.0, key="ca1")
        with c2: frm = st.selectbox("从", ['CNY','USD','EUR','JPY','HKD','GBP','KRW'], key="cf1")
        with c3: to = st.selectbox("到", ['CNY','USD','EUR','JPY','HKD','GBP','KRW'], index=1, key="ct1")
        res = (amt / st.session_state.rates.get(frm,1)) * st.session_state.rates.get(to,1)
        names = {'CNY':'人民币','USD':'美元','EUR':'欧元','JPY':'日元','HKD':'港币','GBP':'英镑','KRW':'韩元'}
        st.markdown(f'<div style="max-width:340px;margin:15px auto;background:#3a3a3a;padding:15px;border-radius:10px;text-align:center;font-size:20px;">{names[to]} {res:.4f}</div>', unsafe_allow_html=True)
    elif ut == "📏 长度":
        u = {"米":1,"厘米":0.01,"毫米":0.001,"千米":1000,"英尺":0.3048,"英寸":0.0254}
        c1, c2, c3 = st.columns(3)
        with c1: v = st.number_input("数值", 1.0, key="lv1")
        with c2: f = st.selectbox("从", list(u.keys()), key="lf1")
        with c3: t = st.selectbox("到", list(u.keys()), index=1, key="lt1")
        st.markdown(f'<div style="max-width:340px;margin:15px auto;background:#3a3a3a;padding:15px;border-radius:10px;text-align:center;font-size:20px;">{v*u[f]/u[t]:.6f}</div>', unsafe_allow_html=True)
    elif ut == "⚖️ 重量":
        u = {"公斤":1,"克":0.001,"斤":0.5,"磅":0.453592,"盎司":0.0283495}
        c1, c2, c3 = st.columns(3)
        with c1: v = st.number_input("数值", 1.0, key="wv1")
        with c2: f = st.selectbox("从", list(u.keys()), key="wf1")
        with c3: t = st.selectbox("到", list(u.keys()), index=1, key="wt1")
        st.markdown(f'<div style="max-width:340px;margin:15px auto;background:#3a3a3a;padding:15px;border-radius:10px;text-align:center;font-size:20px;">{v*u[f]/u[t]:.6f}</div>', unsafe_allow_html=True)
    elif ut == "🌡️ 温度":
        c1, c2 = st.columns(2)
        with c1: v = st.number_input("温度", 0.0, key="tv1")
        with c2: f = st.selectbox("从", ["摄氏度","华氏度","开尔文"], key="tf1")
        t2 = st.selectbox("到", ["摄氏度","华氏度","开尔文"], index=1, key="tt1")
        c = v if f=="摄氏度" else (v-32)*5/9 if f=="华氏度" else v-273.15
        res = c if t2=="摄氏度" else c*9/5+32 if t2=="华氏度" else c+273.15
        st.markdown(f'<div style="max-width:340px;margin:15px auto;background:#3a3a3a;padding:15px;border-radius:10px;text-align:center;font-size:20px;">{res:.2f}°</div>', unsafe_allow_html=True)

elif tm[tab] == 3:
    st.markdown('<div style="max-width:340px;margin:0 auto;background:#2a2a2a;padding:20px;border-radius:15px;"><div style="font-size:20px;margin-bottom:15px;">❤️ 健康计算</div></div>', unsafe_allow_html=True)
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
        st.markdown(f'<div style="max-width:340px;margin:15px auto;text-align:center;"><div style="font-size:56px;font-weight:bold;color:{color};">{r["b"]:.1f}</div><div style="font-size:20px;color:{color};">{r["c"]}</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:15px;"><div style="background:#3a3a3a;padding:15px;border-radius:10px;text-align:center;"><div style="font-size:12px;color:#888;">基础代谢</div><div style="font-size:18px;">{r["bmr"]:.0f}</div></div><div style="background:#3a3a3a;padding:15px;border-radius:10px;text-align:center;"><div style="font-size:12px;color:#888;">每日消耗</div><div style="font-size:18px;">{r["tdee"]:.0f}</div></div></div></div>', unsafe_allow_html=True)
