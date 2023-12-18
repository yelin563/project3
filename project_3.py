# 기본 설정
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import base64
import io

# 앱에서 사용할 기능 함수 정의 (그래프를 이미지 파일로 저장하는 작업)
def save_graph_to_image(fig):
    img_data = io.BytesIO()
    fig.savefig(img_data, format='png')
    img_data.seek(0)
    return img_data
def create_download_link(data, filename, text):
    b64_ori = base64.b64encode(data).decode()
    href = f'<a href="data:file/png;base64,{b64_ori}" download="{filename}">{text}</a>'
    return href

# Streamlit 앱의 제목 설정
st.title("내가 바로 미래의 기자!")

# 통계자료 파일 업로드
st.subheader("통계자료 준비하기")
uploaded_file = st.file_uploader("기사 작성에 사용할 통계자료 파일을 업로드하세요.", type=["xlsx", "xls"])


if uploaded_file is not None:
    # 엑셀 파일을 데이터프레임으로 읽기
    df = pd.read_excel(uploaded_file, header=0, index_col=0)
    st.write('다음은 업로드한 파일의 일부입니다. 통계자료 파일이 잘 업로드되었는지 확인하세요.', df)

    # 데이터프레임의 행/열 목록 가져오기
    col_list = df.columns.tolist()
    row_list = df.index.tolist()

    # 엑셀 파일의 전체 데이터를 한 번에 그래프로 그리기 (option : 막대그래프,꺾은선그래프,원그래프,히스토그램)
    st.subheader("업로드한 전체 통계자료를 시각화해봅시다.")
    df_all = df
    fig_all, ax = plt.subplots()
    graph_option = ["그래프 선택하기","막대그래프", "꺾은선그래프", "원그래프", "히스토그램"]
    graph_selected_opt = st.selectbox("어떤 그래프로 나타낼까요?", graph_option, key="graph_selected_opt")
    
    if st.session_state.get('graph_selected_opt') is None:
        st.session_state['graph_selected_opt'] = graph_selected_opt  # 위젯 생성 전에 session_state에 저장

    if graph_selected_opt == "히스토그램":
        df_all = df.astype(float) # 숫자 데이터를 실수형으로 변환(정수->실수 or 실수->실수)
        value_m = int(min(df_all.values.flatten()))
        value_M = int(max(df_all.values.flatten())) # 다시 정수형으로 변환
        bin_size = st.slider("계급의 크기를 선택하세요.", min_value=value_m, max_value=value_M, value=round(value_M/20), step=1) #value:초기값
        df_all.plot(kind="hist", bins=range(value_m, value_M + bin_size, bin_size), ax=ax)
    else:
        if graph_selected_opt == "막대그래프":
            df_all.plot(kind="bar", ax=ax)
        elif graph_selected_opt == "꺾은선그래프":
            df_all.plot(kind="line", ax=ax, marker="o")
        elif graph_selected_opt == "원그래프":
            df_all.plot.pie(y=df_all.columns[0], ax=ax)
            ax.legend(bbox_to_anchor=(1, 1))
    ax.set_xlabel("")
    ax.set_ylabel("")
    if graph_selected_opt != "그래프 선택하기":
        st.pyplot(fig_all)
        # 그래프를 이미지로 변환하여 다운로드 링크 생성
        graph_image_all = save_graph_to_image(fig_all)
        download_link_all = create_download_link(graph_image_all.getvalue(), f"전체 통계자료.png", "여기를 눌러 그래프를 다운로드하세요.")
        st.markdown(download_link_all, unsafe_allow_html=True) 

    # 메인 페이지에서의 주요 변수를 session_state에 저장
    st.session_state['df'] = df
    st.session_state['col_list'] = col_list
    st.session_state['row_list'] = row_list
    st.session_state['graph_option'] = graph_option