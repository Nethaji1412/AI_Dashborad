import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Smart Data Dashboard - Auto Insights & Visualizations",
    page_icon="📊",
    layout="wide"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>

.main-title{
font-size:110px;     /* MUCH bigger title */
font-weight:900;
text-align:center;
background: linear-gradient(90deg,#ff4b4b,#ffb347,#00c6ff,#43e97b);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
margin-top:20px;
margin-bottom:20px;
letter-spacing:3px;
}

.sub-title{
text-align:center;
font-size:30px;
color:gray;
margin-bottom:30px;
}

.kpi-card{
background: linear-gradient(135deg,#6a11cb,#2575fc);
padding:20px;
border-radius:12px;
color:white;
text-align:center;
font-size:20px;
}

</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown('<p class="main-title">📊 AI Smart Data Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Upload any CSV / Excel file and explore beautiful insights instantly</p>', unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.title("📂 Upload Data")

file = st.sidebar.file_uploader(
    "Upload CSV / Excel file",
    type=["csv","xlsx","xls"]
)

# ================= HOME PAGE =================
if file is None:

    st.header("🏠 Dashboard Home")

    col1,col2,col3 = st.columns(3)

    col1.info("📊 **Auto Visualizations**")
    col2.info("⚡ **Instant Insights**")
    col3.info("🎨 **Interactive Charts**")

    st.write("Upload a dataset to generate automatic charts and analytics.")

# ================= DATA PROCESS =================
if file is not None:

    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)

        else:
            df = pd.read_excel(file)

    except:
        st.error("❌ Error reading file")
        st.stop()

    # ================= DATA PREVIEW =================
    st.subheader("🔍 Dataset Preview")
    st.dataframe(df, use_container_width=True)

    # ================= BASIC INFO =================
    st.subheader("📌 Dataset Overview")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Rows",df.shape[0])
    c2.metric("Columns",df.shape[1])
    c3.metric("Missing",df.isnull().sum().sum())
    c4.metric("Duplicates",df.duplicated().sum())

    # ================= COLUMN TYPES =================
    numeric_cols = df.select_dtypes(include=['int64','float64']).columns
    categorical_cols = df.select_dtypes(include='object').columns

    # ================= FILTER =================
    st.sidebar.header("🎛 Filters")

    filtered_df = df.copy()

    for col in categorical_cols:
        values = st.sidebar.multiselect(f"{col}", df[col].dropna().unique())

        if values:
            filtered_df = filtered_df[filtered_df[col].isin(values)]

    # ================= KPI =================
    if len(numeric_cols) > 0:

        st.subheader("📈 KPI Metrics")

        metric_col = st.selectbox("Select numeric column",numeric_cols)

        k1,k2,k3,k4 = st.columns(4)

        k1.metric("Mean", round(filtered_df[metric_col].mean(),2))
        k2.metric("Max", filtered_df[metric_col].max())
        k3.metric("Min", filtered_df[metric_col].min())
        k4.metric("Sum", round(filtered_df[metric_col].sum(),2))

    # ================= VISUALIZATION =================
    st.subheader("📊 Data Visualizations")

    selected = st.selectbox("Select Column",df.columns)

    # -------- NUMERIC --------
    if selected in numeric_cols:

        c1,c2 = st.columns(2)

        with c1:
            fig = px.histogram(
                filtered_df,
                x=selected,
                color_discrete_sequence=['#ff4b4b']
            )
            st.plotly_chart(fig,use_container_width=True)

        with c2:
            fig = px.box(
                filtered_df,
                y=selected,
                color_discrete_sequence=['#00c6ff']
            )
            st.plotly_chart(fig,use_container_width=True)

        c3,c4 = st.columns(2)

        with c3:
            fig = px.line(
                filtered_df,
                y=selected,
                color_discrete_sequence=['#00ff87']
            )
            st.plotly_chart(fig,use_container_width=True)

        with c4:
            fig = px.scatter(
                filtered_df,
                y=selected,
                color_discrete_sequence=['#f7971e']
            )
            st.plotly_chart(fig,use_container_width=True)

        # Area Chart
        fig = px.area(filtered_df,y=selected)
        st.plotly_chart(fig,use_container_width=True)

        # Violin Plot
        fig = go.Figure()
        fig.add_trace(go.Violin(
            y=filtered_df[selected],
            box_visible=True,
            meanline_visible=True
        ))

        fig.update_layout(title="Violin Distribution")
        st.plotly_chart(fig,use_container_width=True)

    # -------- CATEGORICAL --------
    elif selected in categorical_cols:

        counts = filtered_df[selected].value_counts().reset_index()
        counts.columns = [selected,"Count"]

        c1,c2 = st.columns(2)

        with c1:
            fig = px.bar(
                counts,
                x=selected,
                y="Count",
                text="Count",
                color=selected
            )
            st.plotly_chart(fig,use_container_width=True)

        with c2:
            fig = px.pie(
                counts,
                names=selected,
                values="Count",
                hole=0.4
            )
            st.plotly_chart(fig,use_container_width=True)

        # Treemap
        fig = px.treemap(counts,path=[selected],values="Count")
        st.plotly_chart(fig,use_container_width=True)

    # ================= CORRELATION =================
    if len(numeric_cols) > 1:

        st.subheader("🔗 Correlation Heatmap")

        corr = filtered_df[numeric_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="rainbow"
        )

        st.plotly_chart(fig,use_container_width=True)

    # ================= SCATTER MATRIX =================
    if len(numeric_cols) > 1:

        st.subheader("📊 Custom Scatter Plot")

        col1, col2, col3 = st.columns(3)

        with col1:
            x_col = st.selectbox("Select X-axis", numeric_cols)

        with col2:
            y_col = st.selectbox("Select Y-axis", numeric_cols)

        with col3:
            color_col = st.selectbox("Color by (optional)", ["None"] + list(categorical_cols))

        if color_col == "None":
            fig = px.scatter(
                filtered_df,
                x=x_col,
                y=y_col,
                title=f"{x_col} vs {y_col}",
                color_discrete_sequence=["#ff4b4b"]
            )
        else:
            fig = px.scatter(
                filtered_df,
                x=x_col,
                y=y_col,
                color=color_col,
                title=f"{x_col} vs {y_col}"
            )

        st.plotly_chart(fig, use_container_width=True)