import streamlit as st
import urllib.request
import json
import math

st.set_page_config(page_title="超级计算器", page_icon="🧮", layout="centered")

THEMES = {
    "深空黑": {"bg": "#000000", "btn_bg": "#333333", "orange": "#ff9f0a", "func": "#a5a5a5", "sci": "#505050", "sci_text": "#ff9f0a", "text": "#ffffff", "display_bg": "#000000"},
    "海洋蓝": {"bg": "#001f3f", "btn_bg": "#003366", "orange": "#0074d9", "func": "#004080", "sci": "#004080", "sci_text": "#7fdbff", "text": "#ffffff", "display_bg": "#001f3f"},
    "极光紫": {"bg": "#1a0a2e", "btn_bg": "#2d1b4e", "orange": "#9b59b6", "func": "#3d2066", "sci": "#3d2066", "sci_text": "#d4a5ff", "text": "#ffffff", "display_bg": "#1a0a2e"},
    "荧光绿": {"bg": "#0a1a0a", "btn_bg": "#1a3a1a", "orange": "#2ecc40", "func": "#1e4d2b", "sci": "#1e4d2b", "sci_text": "#7dff7d", "text": "#ffffff", "display_bg": "#0a1a0a"},
    "烈焰红": {"bg": "#1a0a0a", "btn_bg": "#3a1a1a", "orange": "#e74c3c", "func": "#4a2020", "sci": "#4a2020", "sci_text": "#ff6b6b", "text": "#ffffff", "display_bg": "#1a0a0a"},
    "香槟金": {"bg": "#1a150a", "btn_bg": "#3a3020", "orange": "#f39c12", "func": "#4a4025", "sci": "#4a4025", "sci_text": "#ffd700", "text": "#ffffff", "display_bg": "#1a150a"},
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
    st.markdown("### 🎨 配色主题")
    theme_name = st.selectbox("选择", list(THEMES.keys()), index=0, key="ts")
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

# 按钮样式
def btn(text, key, cls="num"):
    colors = {
        "num": f"background:{t['btn_bg']};color:{t['text']};",
        "orange": f"background:{t['orange']};color:#fff;",
        "func": f"background:{t['func']};color:#000;",
        "sci": f"background:{t['sci']};color:{t['sci_text']};",
    }
    return f'''<button onclick="handleBtn('{key}')" style="
        flex:1;height:52px;border:none;border-radius:50%;
        font-size:16px;font-weight:500;cursor:pointer;margin:0 3px;
        {colors.get(cls, colors['num'])}">{text}</button>'''

tab = st.radio("", ["🧮 计算", "🏠 房贷", "🔄 换算", "❤️ 健康"], horizontal=True, key="t1")
tm = {'🧮 计算': 0, '🏠 房贷': 1, '🔄 换算': 2, '❤️ 健康': 3}

if tm[tab] == 0:
    # JS处理
    st.markdown('''<script>
    function handleBtn(key) {
        window.parent.postMessage({type: 'calc_btn', key: key}, '*');
    }
    window.addEventListener('message', function(e) {
        if (e.data.type === 'update_display') {
            document.getElementById('calc_result').textContent = e.data.result;
            document.getElementById('calc_expr').textContent = e.data.expr || '';
        }
    });
    </script>''', unsafe_allow_html=True)

    # HTML布局
    st.markdown(f'''
    <style>
        .stApp {{ background: {t['bg']}; }}
        .wrap {{ max-width: 340px; margin: 0 auto; }}
        .display {{ background: {t['display_bg']}; padding: 20px; min-height: 110px; border-radius: 15px 15px 0 0; display: flex; flex-direction: column; justify-content: flex-end; }}
        .expr {{ font-size: 16px; color: #888; margin-bottom: 5px; text-align: right; }}
        .result {{ font-size: 48px; color: {t['text']}; text-align: right; letter-spacing: -2px; }}
        .buttons {{ background: {t['display_bg']}; padding: 8px; border-radius: 0 0 15px 15px; }}
        .row {{ display: flex; margin-bottom: 6px; justify-content: center; }}
    </style>
    <div class="wrap">
        <div class="display">
            <div class="expr" id="calc_expr">{st.session_state.expr}</div>
            <div class="result" id="calc_result">{st.session_state.display}</div>
        </div>
        <div class="buttons">
            <div class="row">
                <button onclick="handleBtn('2nd')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:14px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['sci']};color:{t['sci_text']};">2nd</button>
                <button onclick="handleBtn('deg')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:14px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['sci']};color:{t['sci_text']};">{'DEG' if st.session_state.is_deg else 'RAD'}</button>
                <button onclick="handleBtn('sin')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:14px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['sci']};color:{t['sci_text']};">sin</button>
                <button onclick="handleBtn('cos')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:14px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['sci']};color:{t['sci_text']};">cos</button>
            </div>
            <div class="row">
                <button onclick="handleBtn('tan')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:14px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['sci']};color:{t['sci_text']};">tan</button>
                <button onclick="handleBtn('x2')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:14px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['sci']};color:{t['sci_text']};">x²</button>
                <button onclick="handleBtn('sqrt')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:14px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['sci']};color:{t['sci_text']};">√</button>
                <button onclick="handleBtn('pow')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:14px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['sci']};color:{t['sci_text']};">xʸ</button>
            </div>
            <div class="row">
                <button onclick="handleBtn('pi')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:16px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['sci']};color:{t['sci_text']};">π</button>
                <button onclick="handleBtn('e')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:16px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['sci']};color:{t['sci_text']};">e</button>
                <button onclick="handleBtn('fact')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:16px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['sci']};color:{t['sci_text']};">n!</button>
                <button onclick="handleBtn('ln')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:14px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['sci']};color:{t['sci_text']};">ln</button>
            </div>
            <div class="row">
                <button onclick="handleBtn('log')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:14px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['sci']};color:{t['sci_text']};">log</button>
                <button onclick="handleBtn('exp')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:14px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['sci']};color:{t['sci_text']};">EXP</button>
                <button onclick="handleBtn('%')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:16px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['func']};color:#000;">%</button>
                <button onclick="handleBtn('/')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['orange']};color:#fff;">÷</button>
            </div>
            <div class="row">
                <button onclick="handleBtn('7')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['btn_bg']};color:{t['text']};">7</button>
                <button onclick="handleBtn('8')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['btn_bg']};color:{t['text']};">8</button>
                <button onclick="handleBtn('9')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['btn_bg']};color:{t['text']};">9</button>
                <button onclick="handleBtn('*')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['orange']};color:#fff;">×</button>
            </div>
            <div class="row">
                <button onclick="handleBtn('4')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['btn_bg']};color:{t['text']};">4</button>
                <button onclick="handleBtn('5')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['btn_bg']};color:{t['text']};">5</button>
                <button onclick="handleBtn('6')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['btn_bg']};color:{t['text']};">6</button>
                <button onclick="handleBtn('-')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['orange']};color:#fff;">-</button>
            </div>
            <div class="row">
                <button onclick="handleBtn('1')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['btn_bg']};color:{t['text']};">1</button>
                <button onclick="handleBtn('2')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['btn_bg']};color:{t['text']};">2</button>
                <button onclick="handleBtn('3')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['btn_bg']};color:{t['text']};">3</button>
                <button onclick="handleBtn('+')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['orange']};color:#fff;">+</button>
            </div>
            <div class="row">
                <button onclick="handleBtn('ac')" style="flex:2;height:52px;border:none;border-radius:26px;font-size:16px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['func']};color:#000;">AC</button>
                <button onclick="handleBtn('neg')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:16px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['func']};color:#000;">±</button>
                <button onclick="handleBtn('=')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['orange']};color:#fff;">=</button>
            </div>
            <div class="row">
                <button onclick="handleBtn('0')" style="flex:2;height:52px;border:none;border-radius:26px;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['btn_bg']};color:{t['text']};">0</button>
                <button onclick="handleBtn('.')" style="flex:1;height:52px;border:none;border-radius:50%;font-size:18px;font-weight:500;cursor:pointer;margin:0 3px;background:{t['btn_bg']};color:{t['text']};">.</button>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # 隐藏的Streamlit按钮用于状态更新
    btn_keys = ['2nd','deg','sin','cos','tan','x2','sqrt','pow','pi','e','fact','ln','log','exp','%','/','7','8','9','*','4','5','6','-','1','2','3','+','ac','neg','=','0','.']
    for key in btn_keys:
        if st.button(key, key=f"btn_{key}", hidden=True):
            s = st.session_state
            curr = float(s.display) if s.display else 0
            p2 = s.is_2nd

            if key == '2nd':
                s.is_2nd = not p2
            elif key == 'deg':
                s.is_deg = not s.is_deg
            elif key in ['sin','cos','tan']:
                if key == 'sin': r = to_deg(math.asin(curr)) if p2 else math.sin(to_rad(curr))
                elif key == 'cos': r = to_deg(math.acos(curr)) if p2 else math.cos(to_rad(curr))
                else: r = to_deg(math.atan(curr)) if p2 else math.tan(to_rad(curr))
                s.expr = f"{key}⁻¹({curr})" if p2 else f"{key}({curr})"
                s.display = fmt(r)
                s.is_2nd = False
            elif key == 'x2':
                s.expr = f"{curr}²"; s.display = fmt(curr * curr)
            elif key == 'sqrt':
                r = curr ** 0.25 if p2 else math.sqrt(curr)
                s.expr = f"∜({curr})" if p2 else f"√({curr})"
                s.display = fmt(r)
            elif key == 'pow':
                if s.operator and not s.new_num:
                    result = do_calc(s.prev_val, s.display, s.operator)
                    s.display = fmt(result); s.prev_val = result
                else: s.prev_val = float(s.display)
                s.operator = '^'; s.expr = f"{s.prev_val} ^"; s.new_num = True
            elif key == 'pi': s.expr = "π"; s.display = fmt(math.pi)
            elif key == 'e': s.expr = "e"; s.display = fmt(math.e)
            elif key == 'fact':
                f = 1
                for i in range(2, min(int(curr), 170) + 1): f *= i
                s.expr = f"{curr}!"; s.display = fmt(f)
            elif key == 'ln':
                r = math.exp(curr) if p2 else math.log(curr)
                s.expr = f"e^{curr}" if p2 else f"ln({curr})"
                s.display = fmt(r); s.is_2nd = False
            elif key == 'log':
                r = 10 ** curr if p2 else math.log10(curr)
                s.expr = f"10^{curr}" if p2 else f"log({curr})"
                s.display = fmt(r); s.is_2nd = False
            elif key == 'exp':
                s.prev_val = curr; s.operator = 'EXP'; s.expr = f"{curr} × 10^"; s.new_num = True
            elif key == '%':
                s.expr = f"{curr}%"; s.display = fmt(curr / 100)
            elif key == 'ac':
                s.display = '0'; s.expr = ''; s.prev_val = None; s.operator = None; s.new_num = True
            elif key == 'neg':
                s.display = fmt(float(s.display) * -1)
            elif key in '0123456789.':
                num = key
                if s.new_num or s.display == '0':
                    s.display = '0.' if num == '.' else num; s.new_num = False
                else:
                    if num == '.' and '.' in s.display: pass
                    elif len(s.display) < 12: s.display += num
            elif key in ['+','-','*','/']:
                op = key
                if s.operator and not s.new_num:
                    result = do_calc(s.prev_val, s.display, s.operator)
                    s.display = fmt(result); s.prev_val = result
                else: s.prev_val = float(s.display)
                s.operator = op.replace('*','×').replace('/','÷'); s.expr = f"{s.prev_val} {s.operator}"; s.new_num = True
            elif key == '=':
                if s.operator and s.prev_val is not None:
                    if s.operator == 'EXP':
                        result = s.prev_val * (10 ** float(s.display))
                        s.expr = f"{s.prev_val} × 10^{s.display}"
                    else:
                        result = do_calc(s.prev_val, s.display, s.operator)
                        s.expr = f"{s.prev_val} {s.operator} {s.display} ="
                    s.display = fmt(result); s.prev_val = None; s.operator = None; s.new_num = True
            st.rerun()

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
