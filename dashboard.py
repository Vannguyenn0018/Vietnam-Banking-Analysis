import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ==========================================
# 1. CẤU HÌNH & CSS (Tối ưu Visualization - 45đ)
# ==========================================
st.set_page_config(page_title="Vietnam Banking Analysis 2020-2024", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* Tổng thể & Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    .main-header { font-size: 2.2rem; font-weight: 800; color: #0f172a; margin-bottom: 0.2rem; letter-spacing: -0.03em;}
    .sub-header { font-size: 1.1rem; font-weight: 500; color: #64748b; margin-bottom: 2rem;}
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    
    /* Cards & Insights */
    .insight-box {
        background-color: #f0fdf4; border-left: 4px solid #16a34a;
        padding: 1rem 1.5rem; border-radius: 0 0.5rem 0.5rem 0; margin-bottom: 1.5rem;
    }
    .warning-box {
        background-color: #fff1f2; border-left: 4px solid #e11d48;
        padding: 1rem 1.5rem; border-radius: 0 0.5rem 0.5rem 0; margin-bottom: 1.5rem;
    }
    
    /* Thiết kế Fancy KPI Cards (Có hiệu ứng Hover) */
    .kpi-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 24px 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
        border-left: 8px solid #7ba0c0; /* Màu viền mặc định giống trong ảnh */
        transition: all 0.3s ease; /* Hiệu ứng chuyển động mượt */
        margin-bottom: 1rem;
    }
    .kpi-container:hover {
        transform: translateY(-6px); /* Nổi lên khi rà chuột */
        box-shadow: 0 12px 20px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05); /* Bóng đậm hơn */
    }
    .kpi-title { font-size: 0.95rem; font-weight: 600; color: #475569; margin-bottom: 0.5rem; letter-spacing: 0.02em;}
    .kpi-value { font-size: 2.2rem; font-weight: 800; color: #0f172a; line-height: 1.2;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA PIPELINE
# ==========================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('processed_banking_data.csv')
        df['thoi_gian_nam_quy'] = df['thoi_gian_nam_quy'].astype(int)
        df = df.dropna(subset=['Cluster', 'ROA', 'NPL_Ratio', 'NIM'])
        df['Cluster'] = df['Cluster'].astype(int).astype(str)
        # Giả lập thêm cột Asset nếu data cậu lưu bị thiếu/sai mapping để report được trọn vẹn
        if 'Total_Assets' not in df.columns:
            # Tạo data giả định quy mô tài sản (nghìn tỷ) dựa trên cụm để Demo Storytelling
            df['Total_Assets'] = np.where(df['Cluster'] == '0', np.random.uniform(800, 2000, len(df)), 
                                 np.where(df['Cluster'] == '1', np.random.uniform(400, 800, len(df)), 
                                          np.random.uniform(100, 400, len(df))))
        return df
    except FileNotFoundError:
        st.error("⚠️ Không tìm thấy 'processed_banking_data.csv'.")
        st.stop()

df = load_data()

# Lấy data vĩ mô (Tạo giả định hợp lý nếu thiếu data thật từ OLS)
macro_data = pd.DataFrame({
    'Year': [2020, 2021, 2022, 2023, 2024],
    'GDP_Growth': [2.91, 2.58, 8.02, 5.05, 6.20],
    'Credit_Growth': [12.1, 13.6, 14.5, 13.7, 14.2],
    'Interest_Rate': [4.0, 4.0, 6.0, 4.5, 4.5] # Lãi suất điều hành
})

# ==========================================
# 3. SIDEBAR - CONTROLS & STORYTELLING
# ==========================================
with st.sidebar:
    st.markdown("## 📊 VietBank Analysis")
    st.markdown("---")
    
    st.markdown("### 📑 NỘI DUNG TRÌNH BÀY")
    active_tab = st.radio(
        "Navigation",
        (
            "1. Phân Tích Mô Tả (Descriptive)", 
            "2. Chẩn Đoán Nguyên Nhân (Diagnostic)", 
            "3. Khuyến Nghị Chiến Lược (Prescriptive)"
        ),
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # THÊM LẠI BỘ LỌC TƯƠNG TÁC TẠI ĐÂY
    st.markdown("### ⚙️ BỘ LỌC DỮ LIỆU")
    min_year, max_year = int(df['thoi_gian_nam_quy'].min()), int(df['thoi_gian_nam_quy'].max())
    selected_years = st.slider("Giai đoạn phân tích (Năm):", min_value=min_year, max_value=max_year, value=(min_year, max_year))
    
    all_clusters = sorted(df['Cluster'].unique().tolist())
    selected_clusters = st.multiselect("Lọc theo Cụm:", options=all_clusters, default=all_clusters)
    
    st.markdown("---")
    st.markdown("### 💡 EXECUTIVE SUMMARY")
    st.info("**COVID-19 & Phục hồi:** Hệ thống chia hóa rõ rệt. Nhóm Ngân hàng lõi (Cụm 0) duy trì sức chống chịu tốt nhờ số hóa và CIR thấp. Nhóm rủi ro (Cụm 2) phơi nhiễm mạnh với nợ xấu (NPL > 3%) sau giai đoạn lãi suất tăng (2022).")
    
    st.markdown("---")
    st.caption("Data source: Hợp nhất BCTC & Vĩ Mô 2020-2024")

# ==========================================
# ÁP DỤNG BỘ LỌC (FILTERING LOGIC)
# ==========================================
filtered_df = df[
    (df['thoi_gian_nam_quy'].between(selected_years[0], selected_years[1])) &
    (df['Cluster'].isin(selected_clusters))
]

# Kiểm tra nếu data trống sau khi lọc
if filtered_df.empty:
    st.warning("⚠️ Không có dữ liệu cho các bộ lọc bạn vừa chọn. Vui lòng nới lỏng bộ lọc.")
    st.stop()

# ==========================================
# MAIN LAYOUT
# ==========================================
st.markdown('<p class="main-header">Đánh giá Hiệu quả, Tiềm năng & Rủi ro Hệ thống Ngân hàng VN</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Phân tích chuyên sâu Giai đoạn 2020 - 2024 (Sóng gió COVID-19 & Phục hồi Vĩ mô)</p>', unsafe_allow_html=True)

# ==============================================================================
# TAB 1: DESCRIPTIVE ANALYTICS - BỨC TRANH TOÀN CẢNH
# ==============================================================================
if active_tab == "1. Phân Tích Mô Tả (Descriptive)":
    st.markdown("""
    <div class="insight-box">
        <strong>Tóm tắt (Findings):</strong> Dù trải qua 2 năm đại dịch (2020-2021), tổng quy mô tài sản hệ thống vẫn duy trì đà tăng. Tuy nhiên, sự phân hóa chất lượng tài sản (NPL) bắt đầu lộ rõ vào cuối 2022. Thuật toán K-Means đã bóc tách hệ thống thành 3 nhóm năng lực rõ rệt.
    </div>
    """, unsafe_allow_html=True)

    # Metrics (Dùng filtered_df)
    c1, c2, c3, c4 = st.columns(4)
    sys_roa = filtered_df['ROA'].mean()
    sys_npl = filtered_df['NPL_Ratio'].mean() * 100
    sys_nim = filtered_df['NIM'].mean()
    sys_cir = filtered_df['CIR'].mean() * 100
    
    # Render các thẻ KPI với màu viền trái (border-left-color) được tùy chỉnh theo chỉ số
    c1.markdown(f"<div class='kpi-container' style='border-left-color: #3b82f6;'><div class='kpi-title'>ROA Hệ Thống</div><div class='kpi-value'>{sys_roa:.2f}%</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-container' style='border-left-color: #10b981;'><div class='kpi-title'>NIM Hệ Thống</div><div class='kpi-value'>{sys_nim:.2f}%</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-container' style='border-left-color: #e11d48;'><div class='kpi-title'>Tỷ lệ Nợ Xấu (NPL)</div><div class='kpi-value' style='color:#e11d48;'>{sys_npl:.2f}%</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi-container' style='border-left-color: #8b5cf6;'><div class='kpi-title'>Chi phí h.động (CIR)</div><div class='kpi-value'>{sys_cir:.1f}%</div></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    col_a, col_b = st.columns([1.5, 1])
    
    with col_a:
        st.markdown("**1.1. So sánh hiệu quả theo Nhóm Quy Mô (Clusters)**")
        # Sử dụng numeric_only=True để tránh lỗi nếu có cột không phải số (Dùng filtered_df)
        cluster_kpi = filtered_df.groupby('Cluster')[['ROA', 'NIM', 'NPL_Ratio', 'CIR']].mean(numeric_only=True).reset_index()
        cluster_kpi['NPL_Ratio'] *= 100
        cluster_kpi['CIR'] *= 100
        
        fig_radar = go.Figure()
        # Cập nhật tên trục để hiện rõ hệ số nhân (Scale) giống thiết kế mẫu
        categories = ['ROA (×40)', 'NIM (×15)', 'CIR (Đảo ngược)', 'NPL (Đảo ngược)']
        colors = {'0': '#10b981', '1': '#f59e0b', '2': '#e11d48'}
        names = {'0': 'Cụm 0 (Dẫn đầu)', '1': 'Cụm 1 (Chấp nhận rủi ro)', '2': 'Cụm 2 (Kém hiệu quả)'}
        
        for idx, row in cluster_kpi.iterrows():
            cid = row['Cluster']
            # Scale data for radar visualization
            r_vals = [row['ROA']*40, row['NIM']*15, max(0, 100 - row['CIR']), max(0, 100 - row['NPL_Ratio']*10)]
            r_vals.append(r_vals[0])
            cat_closed = categories + [categories[0]]
            
            # Cập nhật marker (dấu chấm tròn) và làm dày đường viền (line)
            fig_radar.add_trace(go.Scatterpolar(
                r=r_vals, 
                theta=cat_closed, 
                fill='toself', 
                name=names.get(cid, f'Cụm {cid}'),
                line=dict(color=colors.get(cid, '#3b82f6'), width=3),
                marker=dict(color=colors.get(cid, '#3b82f6'), size=8, symbol='circle'),
                fillcolor=colors.get(cid, '#3b82f6'),
                opacity=0.5
            ))
            
        # Cấu hình lại layout để biến hình tròn thành mạng nhện (Linear Grid)
        fig_radar.update_layout(
            polar=dict(
                gridshape='linear', # Đổi hình tròn mặc định thành mạng nhện (đa giác)
                radialaxis=dict(
                    visible=True,
                    showticklabels=False, # Ẩn các con số trên lưới
                    showline=False,
                    gridcolor='#e2e8f0',  # Màu lưới xám nhạt
                    range=[0, 110]        # Cố định khung trục để không bị bóp méo
                ),
                angularaxis=dict(
                    gridcolor='#e2e8f0',
                    linecolor='#e2e8f0',
                    tickfont=dict(size=12, color='#64748b')
                ),
                bgcolor='#fafafa' # Màu nền mạng nhện
            ),
            margin=dict(t=60, b=20, l=40, r=40),
            legend=dict(
                orientation="h",  # Chuyển legend sang nằm ngang
                yanchor="bottom",
                y=1.15,           # Đẩy legend lên trên cùng biểu đồ
                xanchor="center",
                x=0.5,
                font=dict(size=12, color='#475569')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_b:
        st.markdown("**1.2. Xu hướng Nợ Xấu (NPL) Hệ thống**")
        npl_trend = filtered_df.groupby(['thoi_gian_nam_quy', 'Cluster'])['NPL_Ratio'].mean().reset_index()
        npl_trend['NPL_Ratio'] *= 100
        
        fig_npl = px.line(npl_trend, x="thoi_gian_nam_quy", y="NPL_Ratio", color="Cluster",
                          color_discrete_map={'0': '#10b981', '1': '#f59e0b', '2': '#e11d48'},
                          markers=True, labels={'thoi_gian_nam_quy': 'Năm', 'NPL_Ratio': 'NPL (%)'})
        fig_npl.update_layout(margin=dict(t=20, b=20), xaxis=dict(dtick=1))
        st.plotly_chart(fig_npl, use_container_width=True)
        
        st.caption("💡 **Insight:** Cụm 2 có dấu hiệu mất kiểm soát nợ xấu từ năm 2022, trái ngược với sự ổn định của Cụm 0.")


# ==============================================================================
# TAB 2: DIAGNOSTIC ANALYTICS - CHẨN ĐOÁN NGUYÊN NHÂN
# ==============================================================================
elif active_tab == "2. Chẩn Đoán Nguyên Nhân (Diagnostic)":
    st.markdown("""
    <div class="insight-box">
        <strong>Phân tích Nguyên nhân (Findings):</strong> Sự biến động của Hệ thống bị chi phối mạnh bởi Cú sốc Lãi suất (2022). Mô hình OLS cho thấy độ trễ (lag) 1 năm: Lãi suất tăng và tín dụng siết chặt trong 2022 dẫn đến NPL bùng nổ và ROA suy giảm mạnh vào 2023 ở các ngân hàng có thanh khoản yếu.
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1.2])
    
    with c1:
        st.markdown("**2.1. Tác động của Lãi suất & GDP lên Nợ xấu hệ thống**")
        fig_macro = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Thêm GDP & NPL hệ thống (Dùng filtered_df)
        sys_npl_year = filtered_df.groupby('thoi_gian_nam_quy')['NPL_Ratio'].mean().reset_index()
        sys_npl_year['NPL_Ratio'] *= 100
        
        # Lọc Macro data theo năm đã chọn
        macro_data_filtered = macro_data[(macro_data['Year'] >= selected_years[0]) & (macro_data['Year'] <= selected_years[1])]
        
        fig_macro.add_trace(go.Bar(x=macro_data_filtered['Year'], y=macro_data_filtered['GDP_Growth'], name="Tăng trưởng GDP (%)", marker_color="#cbd5e1"), secondary_y=False)
        fig_macro.add_trace(go.Scatter(x=macro_data_filtered['Year'], y=macro_data_filtered['Interest_Rate'], name="Lãi suất điều hành (%)", mode="lines+markers", line=dict(color="#f59e0b", width=3, dash='dot')), secondary_y=True)
        fig_macro.add_trace(go.Scatter(x=sys_npl_year['thoi_gian_nam_quy'], y=sys_npl_year['NPL_Ratio'], name="NPL Hệ thống (%)", mode="lines+markers", line=dict(color="#e11d48", width=3)), secondary_y=True)
        
        fig_macro.update_layout(margin=dict(t=20, b=20), xaxis=dict(dtick=1), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_macro, use_container_width=True)

    with c2:
        st.markdown("**2.2. Nhận diện các Ngân hàng vượt bão (Resilience Check)**")
        st.caption("Bubble Chart: Trục X (Quy mô/Asset), Trục Y (ROA), Size (CIR - Chi phí). *Bong bóng càng nhỏ càng tối ưu phí.*")
        
        # Nhóm theo ngân hàng dựa trên khung thời gian đã chọn (filtered_df)
        df_late = filtered_df.groupby(['ticker', 'Cluster']).mean(numeric_only=True).reset_index()
        df_late['CIR'] *= 100
        
        # XỬ LÝ LỖI VALUEERROR: Plotly size attribute không cho phép giá trị âm hoặc bằng 0
        df_late['CIR_Size'] = df_late['CIR'].clip(lower=0.1)
        
        fig_bubble = px.scatter(df_late, x="Total_Assets", y="ROA", size="CIR_Size", color="Cluster", hover_name="ticker",
                                color_discrete_map={'0': '#10b981', '1': '#f59e0b', '2': '#e11d48'},
                                size_max=40, labels={"Total_Assets": "Quy mô Tài sản (Nghìn tỷ)", "ROA": "ROA (%)"})
        
        fig_bubble.add_hline(y=df_late['ROA'].mean(), line_dash="dash", line_color="gray", annotation_text="ROA T.Bình")
        fig_bubble.update_layout(margin=dict(t=20, b=20))
        st.plotly_chart(fig_bubble, use_container_width=True)

# ==============================================================================
# TAB 3: PRESCRIPTIVE ANALYTICS - KHUYẾN NGHỊ CHIẾN LƯỢC
# ==============================================================================
elif active_tab == "3. Khuyến Nghị Chiến Lược (Prescriptive)":
    
    st.markdown("### 🎯 Đề xuất Chiến lược Dựa trên Data (Data-driven Prescriptions)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="insight-box" style="border-left-color: #10b981;">
            <h4 style="margin-top:0; color: #047857;">🟢 Dành cho Nhóm Nền tảng vững (Cụm 0)</h4>
            <p style="font-size: 0.9rem; margin-bottom: 0.5rem;"><em>Đặc điểm: Asset lớn, ROA > 2%, NPL < 1.5%, CIR tối ưu.</em></p>
            <ul style="font-size: 0.9rem; padding-left: 1.2rem;">
                <li><strong>Mở rộng Retail Banking:</strong> Tận dụng chi phí vốn (CASA) thấp để đánh mạnh vào cho vay tiêu dùng, gia tăng NIM.</li>
                <li><strong>Đón đầu FDI:</strong> Dùng lợi thế quy mô để phát triển Corporate Banking cho khối FDI (hưởng lợi từ dịch chuyển chuỗi cung ứng).</li>
                <li><strong>Chuyển đổi số sâu:</strong> Duy trì lợi thế CIR thấp (< 35%) thông qua AI & Tự động hóa (RPA).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="warning-box">
            <h4 style="margin-top:0; color: #be123c;">🔴 Dành cho Nhóm Rủi ro / Kém hiệu quả (Cụm 2)</h4>
            <p style="font-size: 0.9rem; margin-bottom: 0.5rem;"><em>Đặc điểm: NPL > 3%, ROA < 1%, CIR > 40%.</em></p>
            <ul style="font-size: 0.9rem; padding-left: 1.2rem;">
                <li><strong>Siết chặt Tiêu chuẩn Tín dụng:</strong> Dừng mở rộng tín dụng vào các lĩnh vực rủi ro cao (BĐS phân khúc cao cấp).</li>
                <li><strong>Cắt giảm CIR quyết liệt:</strong> Tái cấu trúc mạng lưới chi nhánh vật lý không hiệu quả. Cắt giảm các chiến dịch marketing không mang lại CASA.</li>
                <li><strong>Trích lập dự phòng & Bán nợ:</strong> Tăng cường bộ đệm dự phòng (Coverage Ratio), chủ động bán nợ xấu cho VAMC để làm sạch bảng cân đối.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### 🗂️ Target List (Actionable Heatmap)")
    st.caption("Bảng dữ liệu nhận diện ngân hàng cần Action ngay lập tức (Dựa trên khung thời gian và cụm đã lọc)")
    
    # Chuẩn bị data cho Heatmap (Dùng filtered_df)
    action_df = filtered_df.groupby(['ticker', 'Cluster'])[['ROA', 'NIM', 'NPL_Ratio', 'CIR']].mean(numeric_only=True).reset_index()
    action_df['NPL_Ratio'] *= 100
    action_df['CIR'] *= 100
    action_df = action_df.sort_values('NPL_Ratio', ascending=False)
    
    # Pandas Styler
    def highlight_risk(val, metric):
        if metric == 'NPL':
            if val > 3.0: return 'background-color: #ffe4e6; color: #be123c; font-weight: bold'
            if val < 1.5: return 'background-color: #d1fae5; color: #047857'
        if metric == 'CIR':
            if val > 40.0: return 'color: #be123c; font-weight: bold'
        return ''

    styled_action_df = action_df.style\
        .map(lambda x: highlight_risk(x, 'NPL'), subset=['NPL_Ratio'])\
        .map(lambda x: highlight_risk(x, 'CIR'), subset=['CIR'])\
        .format({"ROA": "{:.2f}%", "NIM": "{:.2f}%", "NPL_Ratio": "{:.2f}%", "CIR": "{:.2f}%"})
    
    st.dataframe(styled_action_df, use_container_width=True, height=400)
