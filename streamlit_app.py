import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Bank Customer Churn Analysis", layout="wide")
st.title("Customer Engagement & Product Utilization Analytics for Retention Strategy")
uploaded_file = st.file_uploader("Upload Customer Dataset (CSV)", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Dataset Overview")
    st.dataframe(df.head())
    # KPIs
    total_customers = len(df)
    churn_rate = round(df["Exited"].mean() * 100, 2)
    active_rate = round(df["IsActiveMember"].mean() * 100, 2)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", total_customers)
    col2.metric("Churn Rate (%)", churn_rate)
    col3.metric("Active Customers (%)", active_rate)
    st.divider()
    # Engagement vs Churn
    st.subheader("Engagement vs Churn")
    engagement = (
        df.groupby("IsActiveMember")["Exited"]
        .mean()
        .reset_index()
    )
    engagement["IsActiveMember"] = engagement["IsActiveMember"].map(
        {0: "Inactive", 1: "Active"}
    )
    fig1 = px.bar(
        engagement,
        x="IsActiveMember",
        y="Exited",
        title="Churn Rate by Activity Status"
    )
    st.plotly_chart(fig1, use_container_width=True)
    # Product Utilization
    st.subheader("Product Utilization Impact")
    product_churn = (
        df.groupby("NumOfProducts")["Exited"]
        .mean()
        .reset_index()
    )
    fig2 = px.line(
        product_churn,
        x="NumOfProducts",
        y="Exited",
        markers=True,
        title="Churn Rate by Number of Products"
    )
    st.plotly_chart(fig2, use_container_width=True)
    # High Value Disengaged Customers
    st.subheader("High-Value Disengaged Customers")
    threshold = st.slider(
        "Balance Threshold",
        int(df["Balance"].min()),
        int(df["Balance"].max()),
        100000
    )
    high_value = df[
        (df["Balance"] > threshold)
        & (df["IsActiveMember"] == 0)
    ]
    st.write(
        f"Customers Found: {len(high_value)}"
    )
    st.dataframe(
        high_value[
            [
                "CustomerId",
                "Age",
                "Balance",
                "NumOfProducts",
                "EstimatedSalary",
                "Exited"
            ]
        ]
    )
    # Relationship Strength Index
    st.subheader("Relationship Strength Assessment")
    df["RelationshipStrength"] = (
        df["IsActiveMember"] * 50
        + df["NumOfProducts"] * 10
    )
    fig3 = px.histogram(
        df,
        x="RelationshipStrength",
        title="Relationship Strength Distribution"
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Upload the bank customer churn dataset to begin analysis.")
