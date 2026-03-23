import streamlit as st
import urllib.request
import json

st.set_page_config(
    page_title="超级计算器",
    page_icon="🧮",
    layout="centered"
)

# CSS 样式
st.markdown("""
<style>
    .stApp {
        background: #1a1a1a;
    }
    .tab-nav {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        overflow-x: auto;
    }
    .tab-btn {
        padding: 10px 20px;
        background: #333;
        border: none;
        border-radius: 20px;
        color: white;
        cursor: pointer;
    }
    .tab-btn.active {
        background: #007AFF;
    }
    .display {
        background: #2a2a2a;
        padding: 20px;
        text-align: right;
        font-size: 48px;
        border-radius: 15px 15px 0 0;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .calculator-buttons {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        padding: 10px;
        background: #2a2a2a;
        border-radius: 0 0 15px 15px;
    }
    .btn {
        padding: 20px;
        font-size: 24px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        background: #444;
        color: white;
    }
    .btn-orange { background: #ff9500; }
    .btn-gray { background: #a5a5a5; color: black; }
    .result-highlight {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        background: #007AFF;
        border-radius: 10px;
    }
    .info-card {
        background: #2a2a2a;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    .info-card .label { font-size: 12px; color: #888; }
    .info-card .value { font-size: 18px; font-weight: bold; margin-top: 5px; }
    .rate-refresh {
        display: inline-block;
        padding: 8px 16px;
        background: #007AFF;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        margin-bottom: 10px;
    }
    .rate-time {
        color: #888;
        font-size: 12px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 初始化 session state
if 'display' not in st.session_state:
    st.session_state.display = '0'
if 'current_input' not in st.session_state:
    st.session_state.current_input = ''
if 'operator' not in st.session_state:
    st.session_state.operator = ''
if 'prev_input' not in st.session_state:
    st.session_state.prev_input = ''
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'calc'

# 汇率数据
if 'rates' not in st.session_state:
    st.session_state.rates = {'CNY': 1, 'USD': 7.2, 'EUR': 0.95, 'JPY': 150, 'HKD': 0.9, 'GBP': 0.85, 'KRW': 190}
if 'rate_time' not in st.session_state:
    st.session_state.rate_time = ''

# 房贷数据
if 'loan_result' not in st.session_state:
    st.session_state.loan_result = None

# 健康数据
if 'health_result' not in st.session_state:
    st.session_state.health_result = None

# Tab 导航
tabs = ['🧮 计算', '🏠 房贷', '🔄 汇率', '❤️ 健康']
selected_tab = st.radio("", tabs, horizontal=True, index=tabs.index('🧮 计算') if st.session_state.active_tab == 'calc' else 0)
tab_map = {'🧮 计算': 'calc', '🏠 房贷': 'loan', '🔄 汇率': 'currency', '❤️ 健康': 'health'}
st.session_state.active_tab = tab_map[selected_tab]

# ========== 计算器 ==========
if st.session_state.active_tab == 'calc':
    st.markdown(f'<div class="display">{st.session_state.display}</div>', unsafe_allow_html=True)
    
    cols = st.columns(4)
    buttons = [
        ('AC', 'gray'), ('⌫', 'gray'), ('%', 'gray'), ('÷', 'orange'),
        ('7', ''), ('8', ''), ('9', ''), ('×', 'orange'),
        ('4', ''), ('5', ''), ('6', ''), ('-', 'orange'),
        ('1', ''), ('2', ''), ('3', ''), ('+', 'orange'),
    ]
    
    for i, (btn, btn_type) in enumerate(buttons):
        with cols[i % 4]:
            btn_class = 'btn-gray' if btn_type == 'gray' else 'btn-orange' if btn_type == 'orange' else 'btn'
            if st.button(btn, key=f"calc_{btn}", use_container_width=True):
                if btn == 'AC':
                    st.session_state.display = '0'
                    st.session_state.current_input = ''
                    st.session_state.operator = ''
                    st.session_state.prev_input = ''
                elif btn == '⌫':
                    if st.session_state.current_input:
                        st.session_state.current_input = st.session_state.current_input[:-1]
                        st.session_state.display = st.session_state.current_input or '0'
                elif btn in ['+', '-', '×', '÷', '%']:
                    st.session_state.prev_input = st.session_state.current_input or st.session_state.display
                    st.session_state.current_input = ''
                    st.session_state.operator = btn
                elif btn == '=':
                    if st.session_state.prev_input and st.session_state.current_input and st.session_state.operator:
                        try:
                            a = float(st.session_state.prev_input)
                            b = float(st.session_state.current_input)
                            if st.session_state.operator == '+':
                                result = a + b
                            elif st.session_state.operator == '-':
                                result = a - b
                            elif st.session_state.operator == '×':
                                result = a * b
                            elif st.session_state.operator == '÷':
                                result = a / b if b != 0 else 0
                            elif st.session_state.operator == '%':
                                result = a % b
                            st.session_state.display = str(int(result)) if result == int(result) else str(result)
                            st.session_state.current_input = ''
                        except:
                            st.session_state.display = 'Error'
                else:
                    st.session_state.current_input += btn
                    st.session_state.display = st.session_state.current_input
                st.rerun()

# ========== 房贷计算 ==========
elif st.session_state.active_tab == 'loan':
    st.subheader("🏠 房贷计算器")
    
    col1, col2 = st.columns(2)
    with col1:
        loan_amount = st.number_input("贷款金额（万元）", value=100.0, min_value=0.0)
    with col2:
        interest_rate = st.number_input("年利率（%）", value=3.5, min_value=0.0, step=0.1)
    
    loan_years = st.selectbox("贷款年限", [5, 10, 15, 20, 25, 30], index=3)
    
    if st.button("计算月供"):
        amount = loan_amount * 10000
        rate = interest_rate / 100 / 12
        months = loan_years * 12
        monthly = amount * rate * (1 + rate) ** months / ((1 + rate) ** months - 1)
        total = monthly * months
        interest = total - amount
        st.session_state.loan_result = {
            'monthly': monthly,
            'total': total,
            'interest': interest
        }
    
    if st.session_state.loan_result:
        st.markdown(f"""
        <div style="margin-top:20px; display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px;">
            <div class="info-card">
                <div class="label">月供</div>
                <div class="value" style="color:#007AFF">{st.session_state.loan_result['monthly']:.2f}</div>
            </div>
            <div class="info-card">
                <div class="label">总利息</div>
                <div class="value" style="color:#ff9500">{st.session_state.loan_result['interest']:.0f}</div>
            </div>
            <div class="info-card">
                <div class="label">总还款</div>
                <div class="value" style="color:#34c759">{st.session_state.loan_result['total']:.0f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ========== 汇率换算 ==========
elif st.session_state.active_tab == 'currency':
    st.subheader("🔄 汇率换算")
    
    if st.button("🔄 刷新汇率"):
        try:
            with st.spinner("正在获取汇率..."):
                response = urllib.request.urlopen('https://api.frankfurter.dev/v1/latest?base=CNY', timeout=5)
                data = json.loads(response.read().decode())
                if data.get('rates'):
                    st.session_state.rates = {'CNY': 1, **data['rates']}
                    st.session_state.rate_time = data.get('date', '')
                    st.success("汇率更新成功！")
        except Exception as e:
            st.error(f"获取汇率失败: {e}")
    
    if st.session_state.rate_time:
        st.caption(f"汇率时间: {st.session_state.rate_time}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        amount = st.number_input("金额", value=1.0, min_value=0.0)
    with col2:
        from_curr = st.selectbox("从", ['CNY', 'USD', 'EUR', 'JPY', 'HKD', 'GBP', 'KRW'], index=0)
    with col3:
        to_curr = st.selectbox("到", ['CNY', 'USD', 'EUR', 'JPY', 'HKD', 'GBP', 'KRW'], index=1)
    
    from_rate = st.session_state.rates.get(from_curr, 1)
    to_rate = st.session_state.rates.get(to_curr, 1)
    result = (amount / from_rate) * to_rate
    
    curr_names = {'CNY': '人民币', 'USD': '美元', 'EUR': '欧元', 'JPY': '日元', 'HKD': '港币', 'GBP': '英镑', 'KRW': '韩元'}
    st.markdown(f"""
    <div class="result-highlight" style="margin-top:20px;">
        {curr_names[to_curr]}: {result:.4f}
    </div>
    """, unsafe_allow_html=True)

# ========== 健康计算 ==========
elif st.session_state.active_tab == 'health':
    st.subheader("❤️ 健康计算")
    
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("身高（cm）", value=170, min_value=50, max_value=250)
    with col2:
        weight = st.number_input("体重（kg）", value=65, min_value=20, max_value=300)
    
    col3, col4 = st.columns(2)
    with col3:
        age = st.number_input("年龄", value=30, min_value=1, max_value=150)
    with col4:
        gender = st.selectbox("性别", ["男", "女"])
    
    activity = st.selectbox("运动量", ["久坐(1.2)", "轻度运动(1.375)", "中度运动(1.55)", "重度运动(1.725)"])
    activity_map = {"久坐(1.2)": 1.2, "轻度运动(1.375)": 1.375, "中度运动(1.55)": 1.55, "重度运动(1.725)": 1.725}
    activity_val = activity_map[activity]
    
    if st.button("计算"):
        bmi = weight / ((height / 100) ** 2)
        
        if bmi < 18.5:
            bmi_cat = "偏瘦"
            bmi_color = "#007AFF"
        elif bmi < 24:
            bmi_cat = "正常"
            bmi_color = "#34c759"
        elif bmi < 28:
            bmi_cat = "偏胖"
            bmi_color = "#ff9500"
        else:
            bmi_cat = "肥胖"
            bmi_color = "#ff3b30"
        
        if gender == "男":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        tdee = bmr * activity_val
        
        st.session_state.health_result = {
            'bmi': bmi,
            'bmi_cat': bmi_cat,
            'bmi_color': bmi_color,
            'bmr': bmr,
            'tdee': tdee
        }
    
    if st.session_state.health_result:
        r = st.session_state.health_result
        st.markdown(f"""
        <div style="text-align:center; margin-top:20px;">
            <div style="font-size:48px; font-weight:bold; color:{r['bmi_color']};">{r['bmi']:.1f}</div>
            <div style="font-size:18px; color:{r['bmi_color']};">{r['bmi_cat']}</div>
            <div style="margin-top:15px; display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                <div class="info-card">
                    <div class="label">基础代谢</div>
                    <div style="font-size:18px;">{r['bmr']:.0f} 千卡</div>
                </div>
                <div class="info-card">
                    <div class="label">每日消耗</div>
                    <div style="font-size:18px;">{r['tdee']:.0f} 千卡</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)