import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="美国新冠肺炎疫情数据分析",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv('us-counties.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

try:
    df = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"数据加载失败: {e}")
    st.info("请确保 us-counties.csv 文件与 app.py 在同一目录")
    data_loaded = False

if data_loaded:
    # 侧边栏导航
    st.sidebar.title("📊 功能导航")
    st.sidebar.markdown("选择分析模块")

    menu = st.sidebar.radio(
        "",
        ["🏠 首页概览", "📈 累计趋势", "📉 新增趋势", "🗺️ 各州数据", 
         "🏆 Top10分析", "📊 病死率分析", "📋 原始数据"]
    )

    # 数据预处理
    daily_total = df.groupby('date').agg({
        'cases': 'sum',
        'deaths': 'sum'
    }).reset_index()
    daily_total['new_cases'] = daily_total['cases'].diff().fillna(0)
    daily_total['new_deaths'] = daily_total['deaths'].diff().fillna(0)

    latest_date = df['date'].max()
    state_latest = df[df['date'] == latest_date].groupby('state').agg({
        'cases': 'sum',
        'deaths': 'sum'
    }).reset_index()
    state_latest['death_rate'] = (state_latest['deaths'] / state_latest['cases'] * 100).round(2)
    state_latest = state_latest.sort_values('cases', ascending=False)

    # 首页概览
    if menu == "🏠 首页概览":
        st.markdown('<div class="main-header">美国新冠肺炎疫情数据分析</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">美国疫情数据可视化分析 | Pandas + Streamlit + Plotly</div>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("累计确诊", f"{daily_total['cases'].max():,.0f}")
        col2.metric("累计死亡", f"{daily_total['deaths'].max():,.0f}")
        col3.metric("统计州数", f"{state_latest.shape[0]}")
        death_rate_us = (daily_total['deaths'].max() / daily_total['cases'].max() * 100)
        col4.metric("全美病死率", f"{death_rate_us:.2f}%")

        st.markdown("---")

        st.subheader("📅 数据概览")
        col1, col2 = st.columns(2)
        col1.info(f"**数据起始日期:** {df['date'].min().strftime('%Y-%m-%d')}")
        col2.info(f"**数据截止日期:** {df['date'].max().strftime('%Y-%m-%d')}")

        st.subheader("📋 数据样例")
        st.dataframe(df.head(10), use_container_width=True)

        st.markdown("---")
        st.subheader("📌 关于本项目")
        st.markdown("""
        基于美国各县疫情公开数据，构建疫情数据可视化分析平台，支持累计/新增趋势、各州分布、Top10 排名及病死率统计。

        **技术栈:** Python | Pandas | Streamlit | Plotly

        **分析模块:**
        - 累计趋势分析
        - 新增趋势分析
        - 各州疫情数据
        - Top10 排名分析
        - 病死率统计分析
        """)

    # 累计趋势
    elif menu == "📈 累计趋势":
        st.header("📈 美国每日累计确诊和死亡人数")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=daily_total['date'],
            y=daily_total['cases'],
            name='累计确诊',
            marker_color='#1f77b4',
            opacity=0.8
        ))
        fig.add_trace(go.Bar(
            x=daily_total['date'],
            y=daily_total['deaths'],
            name='累计死亡',
            marker_color='#ff7f0e',
            opacity=0.8
        ))
        fig.update_layout(
            barmode='group',
            xaxis_title="日期",
            yaxis_title="人数",
            height=500,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📋 累计数据明细")
        st.dataframe(daily_total[['date', 'cases', 'deaths']].sort_values('date', ascending=False), 
                     use_container_width=True)

    # 新增趋势
    elif menu == "📉 新增趋势":
        st.header("📉 美国每日新增确诊和死亡人数")

        tab1, tab2 = st.tabs(["新增确诊", "新增死亡"])

        with tab1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_total['date'],
                y=daily_total['new_cases'],
                mode='lines',
                name='新增确诊',
                line=dict(color='#e74c3c', width=2),
                fill='tozeroy'
            ))
            fig.add_trace(go.Scatter(
                x=daily_total['date'],
                y=[daily_total['new_cases'].mean()] * len(daily_total),
                mode='lines',
                name='平均值',
                line=dict(color='#3498db', width=2, dash='dash')
            ))
            fig.update_layout(
                xaxis_title="日期",
                yaxis_title="新增确诊人数",
                height=450,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=daily_total['date'],
                y=daily_total['new_deaths'],
                mode='lines',
                name='新增死亡',
                line=dict(color='#9b59b6', width=2),
                fill='tozeroy'
            ))
            fig.add_trace(go.Scatter(
                x=daily_total['date'],
                y=[daily_total['new_deaths'].mean()] * len(daily_total),
                mode='lines',
                name='平均值',
                line=dict(color='#3498db', width=2, dash='dash')
            ))
            fig.update_layout(
                xaxis_title="日期",
                yaxis_title="新增死亡人数",
                height=450,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)

    # 各州数据
    elif menu == "🗺️ 各州数据":
        st.header("🗺️ 美国各州疫情一览")

        search_state = st.text_input("🔍 搜索州名", "")
        if search_state:
            filtered = state_latest[state_latest['state'].str.contains(search_state, case=False)]
        else:
            filtered = state_latest

        st.dataframe(
            filtered[['state', 'cases', 'deaths', 'death_rate']].rename(columns={
                'state': '州名',
                'cases': '累计确诊',
                'deaths': '累计死亡',
                'death_rate': '病死率(%)'
            }).sort_values('累计确诊', ascending=False),
            use_container_width=True
        )

        st.subheader("📊 各州确诊人数分布")
        fig = px.bar(
            state_latest.head(20),
            x='cases',
            y='state',
            orientation='h',
            color='cases',
            color_continuous_scale='Reds',
            labels={'cases': '累计确诊', 'state': '州名'}
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

    # Top10分析
    elif menu == "🏆 Top10分析":
        st.header("🏆 美国各州疫情Top10分析")

        tab1, tab2, tab3, tab4 = st.tabs([
            "确诊Top10", "死亡Top10", "确诊最少10州", "死亡最少10州"
        ])

        with tab1:
            top10_cases = state_latest.nlargest(10, 'cases')
            fig = px.bar(
                top10_cases,
                x='cases',
                y='state',
                orientation='h',
                color='cases',
                color_continuous_scale='Blues',
                labels={'cases': '累计确诊', 'state': '州名'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            top10_deaths = state_latest.nlargest(10, 'deaths')
            fig = px.bar(
                top10_deaths,
                x='deaths',
                y='state',
                orientation='h',
                color='deaths',
                color_continuous_scale='Reds',
                labels={'deaths': '累计死亡', 'state': '州名'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            bottom10_cases = state_latest.nsmallest(10, 'cases')
            fig = px.bar(
                bottom10_cases,
                x='cases',
                y='state',
                orientation='h',
                color='cases',
                color_continuous_scale='Greens',
                labels={'cases': '累计确诊', 'state': '州名'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with tab4:
            bottom10_deaths = state_latest.nsmallest(10, 'deaths')
            fig = px.bar(
                bottom10_deaths,
                x='deaths',
                y='state',
                orientation='h',
                color='deaths',
                color_continuous_scale='Oranges',
                labels={'deaths': '累计死亡', 'state': '州名'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    # 病死率分析
    elif menu == "📊 病死率分析":
        st.header("📊 美国各州病死率分析")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("全美病死率")
            us_death_rate = daily_total['deaths'].max() / daily_total['cases'].max()
            fig = go.Figure(data=[go.Pie(
                labels=['病死', '未病死'],
                values=[us_death_rate * 100, (1 - us_death_rate) * 100],
                hole=0.4,
                marker_colors=['#e74c3c', '#2ecc71']
            )])
            fig.update_layout(
                annotations=[dict(text=f'{us_death_rate*100:.2f}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("各州病死率Top10")
            top10_rate = state_latest.nlargest(10, 'death_rate')
            fig = px.bar(
                top10_rate,
                x='death_rate',
                y='state',
                orientation='h',
                color='death_rate',
                color_continuous_scale='Reds',
                labels={'death_rate': '病死率(%)', 'state': '州名'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("📋 各州病死率明细")
        st.dataframe(
            state_latest[['state', 'cases', 'deaths', 'death_rate']].rename(columns={
                'state': '州名',
                'cases': '累计确诊',
                'deaths': '累计死亡',
                'death_rate': '病死率(%)'
            }).sort_values('病死率(%)', ascending=False),
            use_container_width=True
        )

    # 原始数据
    elif menu == "📋 原始数据":
        st.header("📋 原始数据")

        col1, col2 = st.columns(2)
        with col1:
            selected_state = st.multiselect(
                "选择州",
                options=sorted(df['state'].unique()),
                default=[]
            )
        with col2:
            date_range = st.date_input(
                "选择日期范围",
                value=[df['date'].min(), df['date'].max()],
                min_value=df['date'].min(),
                max_value=df['date'].max()
            )

        filtered_df = df.copy()
        if selected_state:
            filtered_df = filtered_df[filtered_df['state'].isin(selected_state)]
        if len(date_range) == 2:
            filtered_df = filtered_df[
                (filtered_df['date'] >= pd.Timestamp(date_range[0])) &
                (filtered_df['date'] <= pd.Timestamp(date_range[1]))
            ]

        st.dataframe(filtered_df, use_container_width=True)

        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 下载筛选数据",
            data=csv,
            file_name='filtered_covid_data.csv',
            mime='text/csv'
        )

else:
    st.error("请上传 us-counties.csv 数据文件")
