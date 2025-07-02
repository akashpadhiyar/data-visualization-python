import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import time

col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    st.title("📊 Upload Data and Generate Awesome Graph.")
st.set_page_config(layout="wide")

col1, col2, col3, col4, col5 = st.columns([1, 2, 5, 7, 9])
with col4:
    file_type = st.radio("", ["Select file type : ", "CSV", "XLSX"], horizontal=True)

uploaded_file = st.file_uploader("Upload your file here", type=["csv", "xlsx"])
if uploaded_file:
    if file_type == "Select file type : ":
        st.error(" ⚠️ Oops you forgot to select file type .")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    graph_type = st.radio("", ["Select graph type : ", "Bar", "Plot", "Scatter", "Histogram", "Pie"], horizontal=True)

def info():
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.info("🎉 Done! Your data has been transformed into a graph.")

def graph():
    st.pyplot(fig, use_container_width=True)

def message():
    if graph_type == "Select graph type : ":
        st.info(f" 📌 You have selected a {file_type} file and not graph type now.")
    elif graph_type != "Select graph type : ":
        st.info(f" 📌 You have selected a {file_type} file and {graph_type} graph type.")

if file_type == "CSV":
    message()
if file_type == "XLSX":
    message()

df = None
if file_type is not "Select file type : ":
    if uploaded_file is not None:
        if file_type == "CSV":
            if not uploaded_file.name.endswith(".csv"):
                st.error(" 🔎 oops you select CSV file type but you try to give XLSX file.")
            else:
                df = pd.read_csv(uploaded_file)

        elif file_type == "XLSX":
            if not uploaded_file.name.endswith(".xlsx"):
                st.error(" 🔎 oops you select XLSX file type but you try to give CSV file.")
            else:
                df = pd.read_excel(uploaded_file)
        st.success(" 👉 Preview of your data:")
        st.write(df)

def show_progress_bar(graph_type, df):
    if graph_type != "Select graph type : " and df is not None:
        st.subheader("Progress Bar")
        progress_bar = st.progress(0)
        with st.spinner("Wait for it..."):
            for percent_complete in range(101):
                time.sleep(0.04)
                progress_bar.progress(percent_complete)
    else:
        st.error("The file must contain at least two columns.")

if df is not None and df.shape[1] >= 2:
    x_column = st.selectbox("Select X-axis column", df.columns)
    y_column = st.selectbox("Select Y-axis column", df.columns, index=1 if len(df.columns) > 1 else 0)
    x = df[x_column]
    y = df[y_column]

    if df[x_column].dropna().apply(type).nunique() > 1:
        st.error(f"❌ X-axis column '{x_column}' contains mixed data types.")
        st.stop()

    if df[y_column].dropna().apply(type).nunique() > 1:
        st.error(f"❌ Y-axis column '{y_column}' contains mixed data types.")
        st.stop()

    if y.empty or x.empty:
        st.warning("Data columns are empty. Please upload valid data.")
    elif graph_type in ["Bar", "Plot", "Scatter", "Histogram"] and not pd.api.types.is_numeric_dtype(y):
        st.warning("Y-axis data must be numeric for this graph type.")
    elif graph_type == "Histogram" and not pd.api.types.is_numeric_dtype(x):
        st.warning("Histogram requires numeric data in the first column.")
    elif graph_type == "Pie":
        if not pd.api.types.is_numeric_dtype(y):
            st.warning("Pie chart requires numeric values in the second column.")
        elif any(y < 0):
            st.warning("Pie chart cannot display negative values.")
        else:
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                generate_graph = st.button("Generate graph")
            if generate_graph:
                show_progress_bar(graph_type, df)
                info()
                colors = ['#3498db', '#e74c3c', '#2ecc71', '#f1c40f',
                        '#9b59b6', '#1abc9c', '#e67e22', '#34495e']
                fig, ax = plt.subplots(figsize=(5, 5) )
                wedges, texts, autotexts = ax.pie(
                    y,  
                    labels=x,
                    autopct='%1.1f%%',
                    startangle=140,
                    colors=colors[:len(y)],
                    shadow=True,
                    wedgeprops={'edgecolor': 'black'},
                    textprops={'fontsize': 10}
                )
                ax.set_title("Stylish Pie Chart", fontsize=8, fontweight='bold', color='#2c3e50')
                col1, col2, col3 = st.columns([1, 4, 1])
                with col2:
                    graph()
                plt.clf()

    elif graph_type == "Bar":
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            generate_graph = st.button(" 🛠️ Generate graph !")
        if generate_graph:
            show_progress_bar(graph_type, df)
            info()
            plt.style.use("fivethirtyeight")
            fig, ax = plt.subplots(figsize=(7, 4))
            bars = ax.bar(x, y, color="#1f77b4", edgecolor="black", linewidth=2)
            ax.set_title("Bar Graph Visualization", fontsize=16, fontweight='bold', color="#333")
            ax.set_xlabel(df.columns[0], fontsize=12, fontweight='bold')
            ax.set_ylabel(df.columns[1], fontsize=12, fontweight='bold')
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.set_facecolor('#f9f9f9')
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.2f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 5),
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=10)
            col1, col2, col3 = st.columns([1, 4, 1])
            with col2:
                graph()
            plt.clf()

    elif graph_type == "Plot":
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            generate_graph = st.button("Generate graph !")
        if generate_graph:
            show_progress_bar(graph_type, df)
            info()
            fig, ax = plt.subplots(figsize=(7, 4))
            ax.plot(
                x, y,
                marker='o',
                color='#e74c3c',
                linewidth=2.5,
                markersize=8,
                label='Data Line'
            )
            ax.set_title("Trend Line Plot", fontsize=16, fontweight='bold', color="#2c3e50")
            ax.set_xlabel(df.columns[0], fontsize=12, fontweight='bold')
            ax.set_ylabel(df.columns[1], fontsize=12, fontweight='bold')
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
            for i in range(len(x)):
                ax.annotate(f"{y[i]:.2f}",
                            (x[i], y[i]),
                            textcoords="offset points",
                            xytext=(0, 10),
                            ha='center',
                            fontsize=9)
            ax.set_facecolor('#fefefe')
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.legend(loc="upper left", fontsize=10)
            col1, col2, col3 = st.columns([1, 4, 1])
            with col2:
                graph()
            plt.clf()

    elif graph_type == "Scatter":
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            generate_graph = st.button("Generate graph !")
        if generate_graph:
            show_progress_bar(graph_type, df)
            info()
            fig, ax = plt.subplots(figsize=(7, 4))
            scatter = ax.scatter(
                x, y,
                color="#8e44ad",
                edgecolor='black',
                s=100,
                alpha=0.8,
                label='Data Points'
            )
            ax.set_title("Stylish Scatter Plot", fontsize=16, fontweight='bold', color="#2c3e50")
            ax.set_xlabel(df.columns[0], fontsize=12, fontweight='bold')
            ax.set_ylabel(df.columns[1], fontsize=12, fontweight='bold')
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
            for i in range(len(x)):
                ax.annotate(f"{y[i]:.2f}",
                            (x[i], y[i]),
                            textcoords="offset points",
                            xytext=(0, 8),
                            ha='center',
                            fontsize=9)
            ax.set_facecolor('#fafafa')
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.legend(loc="upper left", fontsize=10)
            col1, col2, col3 = st.columns([1, 4, 1])
            with col2:
                graph()
            plt.clf()

    elif graph_type == "Histogram":
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            generate_graph = st.button("Generate graph !")
        if generate_graph:
            show_progress_bar(graph_type, df)
            info()
            plt.style.use("ggplot")
            fig, ax = plt.subplots(figsize=(7, 4))
            counts, bins, patches = ax.hist(
                x,
                bins=10,
                color='#3498db',
                edgecolor='black',
                alpha=0.85,
                label='Frequency'
            )
            ax.set_title("Stylish Histogram", fontsize=16, fontweight='bold', color='#2c3e50')
            ax.set_xlabel(df.columns[0], fontsize=12, fontweight='bold')
            ax.set_ylabel("Frequency", fontsize=12, fontweight='bold')
            for count, bin_edge in zip(counts, bins[:-1]):
                ax.annotate(f'{int(count)}',
                            xy=(bin_edge + (bins[1] - bins[0]) / 2, count),
                            xytext=(0, 5),
                            textcoords='offset points',
                            ha='center', fontsize=9)
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.set_facecolor('#fefefe')
            ax.legend(loc="upper right", fontsize=10)
            col1, col2, col3 = st.columns([1, 4, 1])
            with col2:
                graph()
            plt.clf()