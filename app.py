import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="计算器", page_icon="🧮", layout="centered")

# 主题
THEMES = {
    "💜 紫罗蓝": {"bg": "#1c1c1e", "num": "#2c2c2e", "func": "#636366", "op": "#a8a8b3", "eq": "#ff9f0a"},
    "🌸 樱花粉": {"bg": "#2d1f2d", "num": "#3d2d3d", "func": "#5d4d5d", "op": "#d4a5b9", "eq": "#ff6b9d"},
    "🌊 海洋蓝": {"bg": "#0d1f2d", "num": "#1d2f3d", "func": "#3d5a6d", "op": "#5da4b4", "eq": "#4ecdc4"},
    "🍋 柠檬黄": {"bg": "#1f1f1f", "num": "#2d2d2d", "func": "#4d4d4d", "op": "#f7dc6f", "eq": "#f39c12"},
    "🖤 经典黑": {"bg": "#000000", "num": "#333333", "func": "#a5a5a5", "op": "#ff9500", "eq": "#ff9500"},
}

theme_name = st.selectbox("🎨 主题", list(THEMES.keys()), index=4)
theme = THEMES[theme_name]
t_func = theme['func']
t_eq = theme['eq']
t_num = theme['num']

# CSS - 强制4列
st.markdown(f"""
<style>
    .stApp {{ background: {theme['bg']}; }}
    .wrap {{ max-width: 350px; margin: 0 auto; }}
    .display {{ background: {t_num}; color: white; padding: 20px; font-size: 42px; text-align: right; border-radius: 20px 20px 0 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; padding: 10px; background: {theme['bg']}; border-radius: 0 0 20px 20px; }}
    .card {{ background: {t_num}; border-radius: 16px; padding: 15px; margin: 10px auto; max-width: 350px; }}
    .title {{ font-size: 16px; font-weight: 600; color: white; margin-bottom: 12px; }}
    
    /* 强制4列 */
    [data-testid="stHorizontalBlock"] {{
        display: grid !important;
        grid-template-columns: repeat(4, 1fr) !important;
        gap: 8px !important;
    }}
    [data-testid="stColumn"] {{
        min-width: auto !important;
        width: auto !important;
    }}
    [data-testid="stColumn"]:nth-child(n+5) {{
        display: none !important;
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

tab = st.radio("", ["🧮", "🏠", "🔄", "❤️"], horizontal=True, index=0, key="tab1")
tm = {'🧮': 0, '🏠': 1, '🔄': 2, '❤️': 3}

# 计算器
if tm[tab] == 0:
    st.markdown('<div class="wrap">', unsafe_allow_html=True)
    st.markdown(f'<div class="display">{st.session_state.display}</div>', unsafe_allow_html=True)
    st.markdown('<div class="grid">', unsafe_allow_html=True)
    
    # 用唯一的key
    btns = [
        ('AC',0,'func'),('±',1,'func'),('%',2,'func'),('÷',3,'op'),
        ('7',4,'num'),('8',5,'num'),('9',6,'num'),('×',7,'op'),
        ('4',8,'num'),('5',9,'num'),('6',10,'num'),('-',11,'op'),
        ('1',12,'num'),('2',13,'num'),('3',14,'num'),('+',15,'op'),
        ('0',16,'num'),('.',17,'num'),('=',18,'eq')
    ]
    
    cols = st.columns(4)
    for lbl, idx, typ in btns:
        with cols[idx % 4]:
            if st.button(lbl, key=f"b{idx}", use_container_width=True):
                if lbl == 'AC':
                    st.session_state.display = '0'
                    st.session_state.expression = ''
                elif lbl == '±':
                    if st.session_state.expression:
                        st.session_state.expression = '-' + st.session_state.expression
                        st.session_state.display = st.session_state.expression
                elif lbl == '=':
                    try:
                        result = eval(st.session_state.expression.replace('×','*').replace('÷','/'))
                        st.session_state.display = str(int(result)) if result == int(result) else str(round(result,10))
                        st.session_state.expression = st.session_state.display
                    except:
                        st.session_state.display = 'Error'
                        st.session_state.expression = ''
                else:
                    st.session_state.expression += lbl
                    st.session_state.display = st.session_state.expression
                st.rerun()
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# 房贷
elif tm[tab] == 1:
    st.markdown(f'<div class="card"><div class="title">🏠 房贷计算器</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: amt = st.number_input("贷款(万)", 100.0, key="la1")
    with c2: rt = st.number_input("利率(%)", 3.5, step=0.1, key="lr1")
    yr = st.selectbox("年限", [5,10,15,20,25,30], index=3, key="ly1")
    
    if st.button("计算", key="calc1"):
        m = amt*10000; r = rt/100/12; n = yr*12; mp = m*r*(1+r)**n/((1+r)**n-1)
        st.session_state.loan_result = {'m':mp,'t':mp*n,'i':mp*n-m}
    
    if st.session_state.loan_result:
        r = st.session_state.loan_result
        st.markdown(f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px;"><div style="background:{t_func}; padding:12px; border-radius:10px; text-align:center;"><div style="font-size:11px; color:#888;">月供</div><div style="font-size:16px; color:{theme["op"]};">{r["m"]:.2f}</div></div><div style="background:{t_func}; padding:12px; border-radius:10px; text-align:center;"><div style="font-size:11px; color:#888;">利息</div><div style="font-size:16px; color:{theme["op"]};">{r["i"]:.0f}</div></div><div style="background:{t_func}; padding:12px; border-radius:10px; text-align:center;"><div style="font-size:11px; color:#888;">总额</div><div style="font-size:16px; color:{theme["op"]};">{r["t"]:.0f}</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 换算
elif tm[tab] == 2:
    st.markdown(f'<div class="card"><div class="title">🔄 单位换算</div>', unsafe_allow_html=True)
    ut = st.selectbox("类型", ["💱 货币","📏 长度","⚖️ 重量","🌡️ 温度"], key="ut1")
    
    if ut == "💱 货币":
        if st.button("🔄", key="rf1"): 
            try: st.session_state.rates = {'CNY':1,**json.loads(urllib.request.urlopen('https://api.frankfurter.dev/v1/latest?base=CNY',timeout=5).read().decode())['rates']}
            except: pass
        
        c1,c2,c3 = st.columns(3)
        with c1: amt = st.number_input("金额", 1.0, key="ca1")
        with c2: frm = st.selectbox("从", ['CNY','USD','EUR','JPY','HKD','GBP','KRW'], key="cf1")
        with c3: to = st.selectbox("到", ['CNY','USD','EUR','JPY','HKD','GBP','KRW'], index=1, key="ct1")
        
        res = (amt/st.session_state.rates.get(frm,1))*st.session_state.rates.get(to,1)
        names = {'CNY':'人民币','USD':'美元','EUR':'欧元','JPY':'日元','HKD':'港币','GBP':'英镑','KRW':'韩元'}
        st.markdown(f'<div style="background:{t_func}; padding:15px; border-radius:10px; text-align:center; margin-top:12px;"><div style="font-size:22px; color:{t_eq};">{names[to]} {res:.4f}</div></div>', unsafe_allow_html=True)
    
    elif ut == "📏 长度":
        u = {"米":1,"厘米":0.01,"毫米":0.001,"千米":1000,"英尺":0.3048,"英寸":0.0254}
        c1,c2,c3 = st.columns(3)
        with c1: v = st.number_input("数值", 1.0, key="lv1")
        with c2: f = st.selectbox("从", list(u.keys()), key="lf1")
        with c3: t = st.selectbox("到", list(u.keys()), index=1, key="lt1")
        st.markdown(f'<div style="background:{t_func}; padding:15px; border-radius:10px; text-align:center; margin-top:12px;"><div style="font-size:22px;">{v*u[f]/u[t]:.6f}</div></div>', unsafe_allow_html=True)
    
    elif ut == "⚖️ 重量":
        u = {"公斤":1,"克":0.001,"斤":0.5,"磅":0.453592,"盎司":0.0283495}
        c1,c2,c3 = st.columns(3)
        with c1: v = st.number_input("数值", 1.0, key="wv1")
        with c2: f = st.selectbox("从", list(u.keys()), key="wf1")
        with c3: t = st.selectbox("到", list(u.keys()), index=1, key="wt1")
        st.markdown(f'<div style="background:{t_func}; padding:15px; border-radius:10px; text-align:center; margin-top:12px;"><div style="font-size:22px;">{v*u[f]/u[t]:.6f}</div></div>', unsafe_allow_html=True)
    
    elif ut == "🌡️ 温度":
        c1,c2 = st.columns(2)
        with c1: v = st.number_input("温度", 0.0, key="tv1")
        with c2: f = st.selectbox("从", ["摄氏度","华氏度","开尔文"], key="tf1")
        t = st.selectbox("到", ["摄氏度","华氏度","开尔文"], index=1, key="tt1")
        c = v if f=="摄氏度" else (v-32)*5/9 if f=="华氏度" else v-273.15
        res = c if t=="摄氏度" else c*9/5+32 if t=="华氏度" else c+273.15
        st.markdown(f'<div style="background:{t_func}; padding:15px; border-radius:10px; text-align:center; margin-top:12px;"><div style="font-size:22px;">{res:.2f}°</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 健康
elif tm[tab] == 3:
    st.markdown(f'<div class="card"><div class="title">❤️ 健康计算</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: h = st.number_input("身高(cm)", 170, key="hh1")
    with c2: w = st.number_input("体重(kg)", 65, key="hw1")
    c3,c4 = st.columns(2)
    with c3: age = st.number_input("年龄", 30, key="ha1")
    with c4: g = st.selectbox("性别", ["男","女"], key="hg1")
    act = st.selectbox("运动", ["久坐(1.2)","轻度(1.375)","中度(1.55)","重度(1.725)"], key="hac1")
    
    if st.button("计算", key="hc1"):
        bmi = w/((h/100)**2)
        cat = "偏瘦" if bmi<18.5 else "正常" if bmi<24 else "偏胖" if bmi<28 else "肥胖"
        bmr = 10*w+6.25*h-5*age+(5 if g=="男" else -161)
        tdee = bmr*float(act.split("(")[1].split(")")[0])
        st.session_state.health_result = {'b':bmi,'c':cat,'bmr':bmr,'tdee':tdee}
    
    if st.session_state.health_result:
        r = st.session_state.health_result
        st.markdown(f'<div style="text-align:center;"><div style="font-size:48px; font-weight:600; color:{t_eq};">{r["b"]:.1f}</div><div style="font-size:18px; color:{t_eq};">{r["c"]}</div><div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:12px;"><div style="background:{t_func}; padding:12px; border-radius:10px; text-align:center;"><div style="font-size:11px; color:#888;">基础代谢</div><div style="font-size:16px;">{r["bmr"]:.0f}</div></div><div style="background:{t_func}; padding:12px; border-radius:10px; text-align:center;"><div style="font-size:11px; color:#888;">每日消耗</div><div style="font-size:16px;">{r["tdee"]:.0f}</div></div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)