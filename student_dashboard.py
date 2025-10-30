


import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# ========================
# Load Cleaned Dataset
# ========================
cleaned_file_path = r"C:\Users\USER\Downloads\cleaned_student_data.csv"
df = pd.read_csv(cleaned_file_path)

# ========================
# Page Config
# ========================
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")
st.title("🎓 Student Performance Dashboard")
st.markdown("### Analyze the factors that influence students' exam performance")

# ========================
# Sidebar Filters
# ========================
st.sidebar.header("🎛️ Filter Data")

attendance_range = st.sidebar.slider(
    "Attendance Range", int(df['Attendance'].min()), int(df['Attendance'].max()),
    (int(df['Attendance'].min()), int(df['Attendance'].max()))
)
hours_range = st.sidebar.slider(
    "Hours Studied Range", int(df['Hours_Studied'].min()), int(df['Hours_Studied'].max()),
    (int(df['Hours_Studied'].min()), int(df['Hours_Studied'].max()))
)
teacher_quality_filter = st.sidebar.multiselect(
    "Teacher Quality", df['Teacher_Quality'].unique(), df['Teacher_Quality'].unique()
)
school_type_filter = st.sidebar.multiselect(
    "School Type", df['School_Type'].unique(), df['School_Type'].unique()
)
gender_filter = st.sidebar.multiselect(
    "Gender", df['Gender'].unique(), df['Gender'].unique()
)

filtered_df = df[
    (df['Attendance'] >= attendance_range[0]) & (df['Attendance'] <= attendance_range[1]) &
    (df['Hours_Studied'] >= hours_range[0]) & (df['Hours_Studied'] <= hours_range[1]) &
    (df['Teacher_Quality'].isin(teacher_quality_filter)) &
    (df['School_Type'].isin(school_type_filter)) &
    (df['Gender'].isin(gender_filter))
]

# ========================
# KPI Section
# ========================
st.markdown("---")
st.subheader("📈 Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Exam Score", f"{filtered_df['Exam_Score'].mean():.2f}")
col2.metric("Avg Hours Studied", f"{filtered_df['Hours_Studied'].mean():.2f}")
col3.metric("Avg Attendance", f"{filtered_df['Attendance'].mean():.2f}")
col4.metric("Avg Sleep Hours", f"{filtered_df['Sleep_Hours'].mean():.2f}")
st.markdown("---")

# ========================
# Correlation Section
# ========================
st.subheader("📊 Correlation Analysis")

numeric_cols = ['Attendance', 'Hours_Studied', 'Previous_Scores',
                'Tutoring_Sessions', 'Physical_Activity', 'Sleep_Hours']
numeric_corr = filtered_df[numeric_cols + ['Exam_Score']].corr()['Exam_Score'].sort_values(ascending=False)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("**Correlation with Exam Score**")
    st.dataframe(numeric_corr)

with col2:
    st.markdown("**Interactive Heatmap**")
    fig = px.imshow(filtered_df[numeric_cols + ['Exam_Score']].corr(),
                    text_auto=True, color_continuous_scale='Viridis',
                    title="Heatmap of Numeric Correlations")
    st.plotly_chart(fig, use_container_width=True)

# ========================
# Category-Wise Analysis
# ========================
st.markdown("---")
st.subheader("🎨 Category-wise Exam Score Comparison")

categorical_cols = ['Teacher_Quality', 'Parental_Education_Level',
                    'School_Type', 'Gender', 'Distance_from_Home']

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
          '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']

for i, col in enumerate(categorical_cols):
    group_mean = filtered_df.groupby(col)['Exam_Score'].mean().reset_index()
    chart = alt.Chart(group_mean).mark_bar(color=colors[i % len(colors)]).encode(
        x=alt.X(col, sort='-y'),
        y=alt.Y('Exam_Score', title='Average Exam Score'),
        tooltip=[col, 'Exam_Score']
    ).properties(title=f"Average Exam Score by {col}", height=350).interactive()
    st.altair_chart(chart, use_container_width=True)

# ========================
# Top Performing Categories
# ========================
st.markdown("---")
st.subheader("🏆 Top Performing Categories")

for col in categorical_cols:
    best = filtered_df.groupby(col)['Exam_Score'].mean().idxmax()
    best_score = filtered_df.groupby(col)['Exam_Score'].mean().max()
    st.markdown(f"- **{col}** → *{best}* (Avg Score: {best_score:.2f})")

# ========================
# Footer
# ========================
st.markdown("---")
st.caption("👩‍💻 Designed by [Krishnapriya tc] | Powered by Streamlit, Altair & Plotly")