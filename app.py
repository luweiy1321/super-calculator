import streamlit as st
import urllib.request
import json

st.set_page_config(page_title="计算器", page_icon="🧮", layout="centered")

# 主题
THEMES = {
    "💜 紫罗蓝": {"bg": "#1c1c1e", "num": "#505050", "func": "#a0a0a0", "op": "#ff9f0a", "eq": "#ff9f0a"},
    "🌸 樱花粉": {"bg": "#2d1f2d", "num": "#6d5d6d", "func": "#c0a0b0", "op": "#ff6b9d", "eq": "#ff6b9d"},
    "🌊 海洋蓝": {"bg": "#0d1f2d", "num": "#3d5f7d", "func": "#80a0b0", "op": "#4ecdc4", "eq": "#4ecdc4"},
    "🍋 柠檬黄": {"bg": "#1f1f1f", "num": "#5d5d4d", "func": "#c0c080", "op": "#f39c12", "eq": "#f39c12"},
    "🖤 经典黑": {"bg": "#000000", "num": "#333333", "func": "#a5a5a5", "op": "#ff9500", "eq": "#ff9500"},
}

# 主题选择
if 'saved_theme' not in st.session_state:
    st.session_state.saved_theme = "🖤 经典黑"
theme_name = st.selectbox("🎨 主题", list(THEMES.keys()), index=list(THEMES.keys()).index(st.session_state.saved_theme), key="tp")
if theme_name != st.session_state.saved_theme:
    st.session_state.saved_theme = theme_name
theme = THEMES[theme_name]
t_num, t_func, t_op, t_eq, t_bg = theme['num'], theme['func'], theme['op'], theme['eq'], theme['bg']

# CSS
st.markdown(f"""
<style>
    .stApp {{ background: {t_bg}; }}
    .wrap {{ max-width: 320px; margin: 0 auto; }}
    .display {{ background: {t_num}; color: white; padding: 20px; font-size: 36px; text-align: right; border-radius: 15px; margin-bottom: 10px; }}
    .card {{ background: {t_num}; border-radius: 15px; padding: 15px; margin: 10px auto; max-width: 320px; }}
    .title {{ font-size: 16px; font-weight: 600; color: white; margin-bottom: 12px; }}
</style>
""", unsafe_allow_html=True)

# 初始化
for k, v in [('display','0'),('expression',''),('rates',{'CNY':1,'USD':7.2,'EUR':0.95,'JPY':150,'HKD':0.9,'GBP':0.85,'KRW':190}),('loan_result',None),('health_result',None)]:
    if k not in st.session_state: st.session_state[k] = v

tab = st.radio("", ["🧮", "🏠", "🔄", "❤️"], horizontal=True, index=0, key="t1")
tm = {'🧮': 0, '🏠': 1, '🔄': 2, '❤️': 3}

# 计算器
if tm[tab] == 0:
    st.markdown('<div class="wrap">', unsafe_allow_html=True)
    st.markdown(f'<div class="display">{st.session_state.display}</div>', unsafe_allow_html=True)
    
    # 4列x5行按钮
    cols = st.columns(4)
    with cols[0]:
        if st.button("AC", key="ac1"):
            st.session_state.display='0'; st.session_state.expression=''
            st.rerun()
    with cols[1]:
        if st.button("±", key="pm1"):
            if st.session_state.expression: st.session_state.expression='-'+st.session_state.expression; st.session_state.display=st.session_state.expression
            st.rerun()
    with cols[2]:
        if st.button("%", key="pct1"):
            st.session_state.expression+='%'; st.session_state.display=st.session_state.expression
            st.rerun()
    with cols[3]:
        if st.button("÷", key="div1"):
            st.session_state.expression+='÷'; st.session_state.display=st.session_state.expression
            st.rerun()
    
    cols = st.columns(4)
    with cols[0]:
        if st.button("7", key="7_1"): st.session_state.expression+='7'; st.session_state.display=st.session_state.expression; st.rerun()
    with cols[1]:
        if st.button("8", key="8_1"): st.session_state.expression+='8'; st.session_state.display=st.session_state.expression; st.rerun()
    with cols[2]:
        if st.button("9", key="9_1"): st.session_state.expression+='9'; st.session_state.display=st.session_state.expression; st.rerun()
    with cols[3]:
        if st.button("×", key="mul1"): st.session_state.expression+='×'; st.session_state.display=st.session_state.expression; st.rerun()
    
    cols = st.columns(4)
    with cols[0]:
        if st.button("4", key="4_1"): st.session_state.expression+='4'; st.session_state.display=st.session_state.expression; st.rerun()
    with cols[1]:
        if st.button("5", key="5_1"): st.session_state.expression+='5'; st.session_state.display=st.session_state.expression; st.rerun()
    with cols[2]:
        if st.button("6", key="6_1"): st.session_state.expression+='6'; st.session_state.display=st.session_state.expression; st.rerun()
    with cols[3]:
        if st.button("-", key="sub1"): st.session_state.expression+='-'; st.session_state.display=st.session_state.expression; st.rerun()
    
    cols = st.columns(4)
    with cols[0]:
        if st.button("1", key="1_1"): st.session_state.expression+='1'; st.session_state.display=st.session_state.expression; st.rerun()
    with cols[1]:
        if st.button("2", key="2_1"): st.session_state.expression+='2'; st.session_state.display=st.session_state.expression; st.rerun()
    with cols[2]:
        if st.button("3", key="3_1"): st.session_state.expression+='3'; st.session_state.display=st.session_state.expression; st.rerun()
    with cols[3]:
        if st.button("+", key="add1"): st.session_state.expression+='+'; st.session_state.display=st.session_state.expression; st.rerun()
    
    cols = st.columns(4)
    with cols[0]:
        if st.button("0", key="0_1"): st.session_state.expression+='0'; st.session_state.display=st.session_state.expression; st.rerun()
    with cols[1]:
        if st.button(".", key="dot1"): st.session_state.expression+='.'; st.session_state.display=st.session_state.expression; st.rerun()
    with cols[3]:
        if st.button("=", key="eq1"):
            try:
                result = eval(st.session_state.expression.replace('×','*').replace('÷','/'))
                st.session_state.display = str(int(result)) if result == int(result) else str(round(result,10))
                st.session_state.expression = st.session_state.display
            except:
                st.session_state.display = 'Error'
                st.session_state.expression = ''
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

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
        st.markdown(f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px;"><div style="background:{t_func}; padding:12px; border-radius:10px; text-align:center;"><div style="font-size:11px; color:#888;">月供</div><div style="font-size:16px; color:{t_op};">{r["m"]:.2f}</div></div><div style="background:{t_func}; padding:12px; border-radius:10px; text-align:center;"><div style="font-size:11px; color:#888;">利息</div><div style="font-size:16px; color:{t_op};">{r["i"]:.0f}</div></div><div style="background:{t_func}; padding:12px; border-radius:10px; text-align:center;"><div style="font-size:11px; color:#888;">总额</div><div style="font-size:16px; color:{t_op};">{r["t"]:.0f}</div></div></div>', unsafe_allow_html=True)
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