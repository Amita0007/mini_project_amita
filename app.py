import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("supermarket_sales.csv", parse_dates=['Date'])
    df = df.drop(columns=['Invoice ID'])
    return df


df = load_data()
st.title("Data analystic dashboard")
cat_cols = df.select_dtypes(exclude='number').columns
num_cols = df.select_dtypes(include='number').columns


with st.expander("View Numerical data"):
    st.dataframe(df[num_cols])
with st.expander("View Categorical data"):
    st.dataframe(df[cat_cols])

st.subheader("Visualize categorical data")
col = st.selectbox("Select a cateogory", cat_cols)
count_df = df[col].value_counts().reset_index()
fig = px.pie(count_df, col, 'count', title=f'{col} distribution in supermarket dataset', hole=.7)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Visualize numerical data")
col = st.selectbox("Select a numerical column", num_cols)
fig = px.density_contour(df, col)
fig2 = px.histogram(df, col)
st.plotly_chart(fig, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

st.subheader('Relation b/w Columns')
x = st.selectbox("Select a x column", num_cols, key='xcol')
y = st.selectbox("Select a y column", num_cols, key='ycol')
cat = st.selectbox("Select a cateogory", ["No Category"]+cat_cols.to_list(), key='catcolor')
if cat == 'No Category':
    fig = px.scatter(df, x, y)
else:
    fig =px.scatter(df, x, y, color=cat)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Grouped data")
grp = st.selectbox("Select a group", cat_cols)
total = st.selectbox("Select a column to calculate on", num_cols)
sales_by_product_line = df.groupby(by=[grp])[total].sum().reset_index().sort_values(total)

st.dataframe(sales_by_product_line, use_container_width=True)
fig_product_sales = px.bar(
    sales_by_product_line,
    x = grp,
    y = total,
    title=f"<b>{grp} Distribution on sum of {total}",
    template="plotly_white",
    log_y=True,
)
st.plotly_chart(fig_product_sales, use_container_width=True)