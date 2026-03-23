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
tabs = ['🧮 计算', '📷 AI拍照', '🏠 房贷', '🔄 换算', '❤️ 健康']
selected_tab = st.radio("", tabs, horizontal=True, index=0)
tab_map = {'🧮 计算': 'calc', '📷 AI拍照': 'ai', '🏠 房贷': 'loan', '🔄 换算': 'unit', '❤️ 健康': 'health'}
st.session_state.active_tab = tab_map[selected_tab]

# ========== 计算器 ==========
if st.session_state.active_tab == 'calc':
    # 选择计算器模式
    calc_mode = st.radio("模式", ["🧮 基础", "🔬 科学"], horizontal=True, key="calc_mode")
    
    if calc_mode == "🔬 科学":
        # 科学计算器按钮
        st.markdown(f'<div class="display">{st.session_state.display}</div>', unsafe_allow_html=True)
        
        # 第一行：三角函数
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("sin", use_container_width=True):
                try:
                    val = float(st.session_state.display)
                    st.session_state.display = str(round(math.sin(math.radians(val)), 10))
                except: st.session_state.display = "Error"
                st.rerun()
        with col2:
            if st.button("cos", use_container_width=True):
                try:
                    val = float(st.session_state.display)
                    st.session_state.display = str(round(math.cos(math.radians(val)), 10))
                except: st.session_state.display = "Error"
                st.rerun()
        with col3:
            if st.button("tan", use_container_width=True):
                try:
                    val = float(st.session_state.display)
                    st.session_state.display = str(round(math.tan(math.radians(val)), 10))
                except: st.session_state.display = "Error"
                st.rerun()
        with col4:
            if st.button("log", use_container_width=True):
                try:
                    val = float(st.session_state.display)
                    st.session_state.display = str(round(math.log10(val), 10))
                except: st.session_state.display = "Error"
                st.rerun()
        
        # 第二行
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("ln", use_container_width=True):
                try:
                    val = float(st.session_state.display)
                    st.session_state.display = str(round(math.log(val), 10))
                except: st.session_state.display = "Error"
                st.rerun()
        with col2:
            if st.button("√", use_container_width=True):
                try:
                    val = float(st.session_state.display)
                    st.session_state.display = str(round(math.sqrt(val), 10))
                except: st.session_state.display = "Error"
                st.rerun()
        with col3:
            if st.button("x²", use_container_width=True):
                try:
                    val = float(st.session_state.display)
                    st.session_state.display = str(val ** 2)
                except: st.session_state.display = "Error"
                st.rerun()
        with col4:
            if st.button("xⁿ", use_container_width=True):
                st.session_state.operator = '^'
                st.session_state.prev_input = st.session_state.display
                st.session_state.current_input = ''
                st.rerun()
        
        # 第三行：基础运算
        cols = st.columns(4)
        buttons = [
            ('AC', 'gray'), ('⌫', 'gray'), ('(', ''), (')', ''),
            ('7', ''), ('8', ''), ('9', ''), ('÷', 'orange'),
            ('4', ''), ('5', ''), ('6', ''), ('×', 'orange'),
            ('1', ''), ('2', ''), ('3', ''), ('-', 'orange'),
            ('0', ''), ('.', ''), ('π', ''), ('+', 'orange'),
        ]
        
        for i, (btn, btn_type) in enumerate(buttons):
            with cols[i % 4]:
                if st.button(btn, key=f"sci_{btn}", use_container_width=True):
                    if btn == 'AC':
                        st.session_state.display = '0'
                        st.session_state.current_input = ''
                        st.session_state.operator = ''
                        st.session_state.prev_input = ''
                    elif btn == '⌫':
                        if st.session_state.current_input:
                            st.session_state.current_input = st.session_state.current_input[:-1]
                            st.session_state.display = st.session_state.current_input or '0'
                    elif btn == 'π':
                        st.session_state.current_input += str(math.pi)
                        st.session_state.display = st.session_state.current_input
                    elif btn in ['+', '-', '×', '÷', '^']:
                        st.session_state.prev_input = st.session_state.current_input or st.session_state.display
                        st.session_state.current_input = ''
                        st.session_state.operator = btn
                    elif btn in ['(', ')']:
                        st.session_state.current_input += btn
                        st.session_state.display = st.session_state.current_input
                    elif btn == '=':
                        try:
                            expr = st.session_state.current_input or st.session_state.display
                            result = eval(expr)
                            st.session_state.display = str(int(result)) if result == int(result) else str(result)
                            st.session_state.current_input = ''
                        except:
                            st.session_state.display = 'Error'
                    else:
                        st.session_state.current_input += btn
                        st.session_state.display = st.session_state.current_input
                    st.rerun()
        
        # 等号按钮
        if st.button("＝", use_container_width=True, key="sci_equal"):
            try:
                expr = st.session_state.current_input or st.session_state.display
                result = eval(expr)
                st.session_state.display = str(int(result)) if result == int(result) else str(result)
                st.session_state.current_input = ''
            except:
                st.session_state.display = 'Error'
            st.rerun()
    
    else:
        # 基础计算器
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

# ========== AI拍照解题 ==========
elif st.session_state.active_tab == 'ai':
    st.subheader("📷 AI拍照解题")
    
    uploaded_file = st.file_uploader("上传数学题图片", type=['jpg', 'jpeg', 'png', 'gif', 'webp'])
    
    if uploaded_file:
        st.image(uploaded_file, caption="上传的图片", use_container_width=True)
        
        # 显示说明
        st.info("📝 AI拍照解题功能需要配置 API Key 才能使用。")
        st.markdown("""
        **功能说明：**
        - 上传包含数学题的图片
        - AI 自动识别题目并给出解答
        - 支持代数、几何等多种题型
        
        **注意：** 此功能需要后端 AI API 支持。
        """)
        
        # 显示模拟结果（示例）
        with st.expander("示例效果预览"):
            st.markdown("""
            **输入：** 上传一张包含 `2x + 5 = 15` 的图片
            
            **输出：**
            ```
            解答步骤：
            1. 两边同时减去 5
            2x = 15 - 5
            2x = 10
            
            2. 两边同时除以 2
            x = 10 ÷ 2
            x = 5
            
            答案：x = 5
            ```
            """)

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

# ========== 单位换算 ==========
elif st.session_state.active_tab == 'unit':
    st.subheader("🔄 单位换算")
    
    # 选择换算类型
    unit_type = st.selectbox("选择类型", ["📏 长度", "⚖️ 重量", "🌡️ 温度", "💱 货币"])
    
    # 长度换算
    if unit_type == "📏 长度":
        length_units = {
            "米": 1, "厘米": 0.01, "毫米": 0.001, 
            "千米": 1000, "英尺": 0.3048, "英寸": 0.0254, "英里": 1609.344
        }
        col1, col2, col3 = st.columns(3)
        with col1:
            length_val = st.number_input("数值", value=1.0, min_value=0.0, key="length_val")
        with col2:
            length_from = st.selectbox("从", list(length_units.keys()), key="length_from")
        with col3:
            length_to = st.selectbox("到", list(length_units.keys()), index=1, key="length_to")
        
        result = length_val * length_units[length_from] / length_units[length_to]
        st.markdown(f"""
        <div class="result-highlight" style="margin-top:20px;">
            {length_to}: {result:.6f}
        </div>
        """, unsafe_allow_html=True)
    
    # 重量换算
    elif unit_type == "⚖️ 重量":
        weight_units = {
            "公斤": 1, "克": 0.001, "毫克": 0.000001,
            "斤": 0.5, "磅": 0.453592, "盎司": 0.0283495, "吨": 1000
        }
        col1, col2, col3 = st.columns(3)
        with col1:
            weight_val = st.number_input("数值", value=1.0, min_value=0.0, key="weight_val")
        with col2:
            weight_from = st.selectbox("从", list(weight_units.keys()), key="weight_from")
        with col3:
            weight_to = st.selectbox("到", list(weight_units.keys()), index=1, key="weight_to")
        
        result = weight_val * weight_units[weight_from] / weight_units[weight_to]
        st.markdown(f"""
        <div class="result-highlight" style="margin-top:20px;">
            {weight_to}: {result:.6f}
        </div>
        """, unsafe_allow_html=True)
    
    # 温度换算
    elif unit_type == "🌡️ 温度":
        st.markdown("**温度转换公式：**")
        st.latex(r"C = (F - 32) \times \frac{5}{9}")
        st.latex(r"K = C + 273.15")
        
        col1, col2 = st.columns(2)
        with col1:
            temp_val = st.number_input("输入温度", value=0.0, key="temp_val")
        with col2:
            temp_from = st.selectbox("从", ["摄氏度(°C)", "华氏度(°F)", "开尔文(K)"], key="temp_from")
        
        temp_to = st.selectbox("到", ["摄氏度(°C)", "华氏度(°F)", "开尔文(K)"], index=1, key="temp_to")
        
        # 转换为摄氏度
        if temp_from == "摄氏度(°C)":
            celsius = temp_val
        elif temp_from == "华氏度(°F)":
            celsius = (temp_val - 32) * 5/9
        else:  # 开尔文
            celsius = temp_val - 273.15
        
        # 从摄氏度转换为目标
        if temp_to == "摄氏度(°C)":
            result = celsius
        elif temp_to == "华氏度(°F)":
            result = celsius * 9/5 + 32
        else:  # 开尔文
            result = celsius + 273.15
        
        st.markdown(f"""
        <div class="result-highlight" style="margin-top:20px;">
            {temp_to.split('(')[0]}: {result:.2f}
        </div>
        """, unsafe_allow_html=True)
    
    # 货币换算
    elif unit_type == "💱 货币":
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
            amount = st.number_input("金额", value=1.0, min_value=0.0, key="currency_val")
        with col2:
            from_curr = st.selectbox("从", ['CNY', 'USD', 'EUR', 'JPY', 'HKD', 'GBP', 'KRW'], index=0, key="curr_from")
        with col3:
            to_curr = st.selectbox("到", ['CNY', 'USD', 'EUR', 'JPY', 'HKD', 'GBP', 'KRW'], index=1, key="curr_to")
        
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