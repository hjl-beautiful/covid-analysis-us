# 美国新冠肺炎疫情数据分析

> 基于美国各县公开疫情数据的可视化分析平台 | Pandas + Streamlit + Plotly

## 数据源

- **来源**: [The New York Times COVID-19 Data](https://github.com/nytimes/covid-19-data)（美国各县疫情公开数据）
- **范围**: 2020-01-21 至 2020-05-19
- **字段**: date, county, state, fips, cases, deaths

## 核心功能

- **首页概览**: 累计确诊、累计死亡、统计州数、全美病死率
- **累计趋势**: 全美每日累计确诊/死亡人数柱状图
- **新增趋势**: 每日新增确诊/死亡趋势及 7 日移动平均
- **各州数据**: 分州疫情分布与对比
- **Top10 分析**: 确诊最多、病死率最高的州排名
- **病死率分析**: 各州病死率分布与统计

## 技术栈

- Python 3.10+
- Pandas（数据处理）
- Streamlit（可视化部署）
- Plotly（交互图表）

## 运行方式

```bash
pip install -r requirements.txt
streamlit run covid-analysis-us/app.py
```

## 项目定位

本项目为**数据可视化分析项目**，重点展示：
- 大规模时序数据的聚合与清洗
- 多维度交互式可视化
- 疫情数据的业务解读与风险指标计算
