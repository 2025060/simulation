import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import platform

if platform.system() == 'Windows':
    matplotlib.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    matplotlib.rc('font', family='AppleGothic')
else:
    matplotlib.rc('font', family='NanumGothic')  # Linux 서버용

matplotlib.rcParams['axes.unicode_minus'] = False

# 회귀 계수 정의
regression_params = {
    '난연제 무처리': {'slope': -0.01, 'intercept': 6.58, 'color': 'blue'},
    '폴리비닐 알코올 기반 난연제': {'slope': 0.03, 'intercept': 2.67, 'color': 'orange'},
    '알긴산 나트륨 기반 난연제': {'slope': -0.02, 'intercept': 5.71, 'color': 'green'}
}

# 📌 제목 및 설명
st.title("🔥 난연제의 탄화 길이 분석 및 예측")
st.markdown("""
울산과학고 팀(정소연, 최연우, 임지우)이 연소 실험을 통해 측정한 데이터에 기반하여 개발한 **습도 변화에 따른 난연제의 탄화 길이를 분석 및 예측**하는 웹사이트입니다. 난연제 종류를 선택하고 습도 조건을 설정하면 연소 시 탄화 길이를 예측할 수 있습니다.
""")

# 📌 입력 위젯
material = st.selectbox("난연제 종류를 선택하세요:", list(regression_params.keys()))
humidity = st.slider("습도(%)를 선택하세요", 0, 100, 40)

# 📌 예측 계산
selected = regression_params[material]
predicted = selected['slope'] * humidity + selected['intercept']
within_range = 20 <= humidity <= 60

st.markdown(f"""
### 🔍 예측 결과
- **선택한 난연제 종류**: `{material}`
- **습도**: `{humidity}%`
- **예상 탄화 길이**: `{predicted:.2f} cm`
""")

if not within_range:
    st.warning("⚠️ 입력하신 습도는 실험 영역(20~60%)을 벗어나기 때문에 예측값의 신뢰도가 낮을 수 있습니다.")

# 📌 그래프 그리기
x_full = np.linspace(0, 100, 200)
x_valid = np.linspace(20, 60, 200)

fig, ax = plt.subplots(figsize=(7, 5))

for label, params in regression_params.items():
    slope = params['slope']
    intercept = params['intercept']
    color = params['color']

    y_full = slope * x_full + intercept
    y_valid = slope * x_valid + intercept

    ax.plot(x_full, y_full, linestyle='--', color='lightgray')
    ax.plot(x_valid, y_valid, linestyle='--', color=color, label=f'{label} 회귀선')

# 예측점 표시
point_color = 'gray' if humidity < 20 or humidity > 60 else 'red'
ax.scatter(humidity, predicted, color=point_color, label='예측점', zorder=5)

# 그래프 설정
ax.set_xlabel("습도 (%)")
ax.set_ylabel("탄화 길이 (cm)")
ax.set_title("난연제 종류별 탄화 길이 회귀선 및 예측 결과")
ax.grid(True)
ax.legend()
ax.set_xlim(0, 100)
ax.set_ylim(0, 10)

# Streamlit에 그래프 표시
st.pyplot(fig)
