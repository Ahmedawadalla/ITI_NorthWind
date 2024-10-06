
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load CSV files
profit_month_df = pd.read_csv("Profit by Month.csv")
profit_employee_df = pd.read_csv("Profit by Employee.csv")
profit_product_df = pd.read_csv("Profit by ProductName.csv")
profit_supplier_df = pd.read_csv("Profit by Suppliers.csv")
profit_category_df = pd.read_csv("Profit by CategoryName.csv")
profit_shippers_df = pd.read_csv("Profit by Shippers.csv")
scateer_avgshio_df = pd.read_csv("Total Orders and Avg Delivery Time by ShipName.csv")
profit_country_df = pd.read_csv("Profit by Country.csv")
Profit_customer_df = pd.read_csv("Top Customer by Profit.csv")

# Set the page configuration
st.set_page_config(page_title="NorthWind Dashboard", layout="wide")

# Load KPI data from card.csv
kpi_data = pd.read_csv('card.csv')
# # Extract KPI values
total_cost = kpi_data['Total Cost'][0]
total_sales = kpi_data['Total Sales'][0]
profit = kpi_data['Profit'][0]
total_freight = kpi_data['Total Freight'][0]
total_discount = kpi_data['Total Discount'][0]
total_orders = kpi_data['Total Orders'][0]
total_stock_unit = kpi_data['Total Stock Unit'][0]


# Define a custom card template using HTML and inline CSS
def card(title, value, background_color="#f0f2f6", color="black"):
    return f"""
    <div style="background-color: {background_color}; padding: 1px; border-radius: 10px; margin-bottom: 10px; text-align: center; color: {color}; font-weight: bold;">
        <h3 style="color: {color};">{title}</h3>
        <p style="font-size: 24px;">{value}</p>
    </div>
    """
# Create 7 columns for the KPIs
logo, kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6, kpi_col7 = st.columns(8)

# Display each KPI with custom styling using HTML
with logo :
    chart = st.image("nwrc-1600px-color.png", width=300)
with kpi_col1:
    st.markdown(card("Total Cost", total_cost, background_color="#D95B43", color="white"), unsafe_allow_html=True)
with kpi_col2:
    st.markdown(card("Total Sales", total_sales, background_color="#4B8BBE", color="white"), unsafe_allow_html=True)
with kpi_col3:
    st.markdown(card("Profit", profit, background_color="#EBCB8B", color="black" ), unsafe_allow_html=True)
with kpi_col4:
    st.markdown(card("Total Freight", total_freight, background_color="#8fbc8f", color="white"), unsafe_allow_html=True)
with kpi_col5:
    st.markdown(card("Total Discount", total_discount, background_color="#FFD700", color="black"), unsafe_allow_html=True)
with kpi_col6:
    st.markdown(card("Total Orders", total_orders, background_color="#FF6347", color="white"), unsafe_allow_html=True)
with kpi_col7:
    st.markdown(card("Total Stock Unit", total_stock_unit, background_color="#4682B4", color="white"), unsafe_allow_html=True)

# Define a professional color scheme
color_scheme = ['#4B8BBE', '#EBCB8B', '#D95B43']

# Function to create a consistent plot layout
def create_bar_chart(df, x_col, y_col, orientation='v', title=''):
    fig = px.bar(df, x=x_col, y=y_col, orientation=orientation, color_discrete_sequence=color_scheme)
    fig.update_layout(
        title=title,
        title_font_size=22,
        xaxis_title=x_col,
        yaxis_title=y_col,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12, color="black"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    return fig

# Create bar charts using the function
fig_month = create_bar_chart(profit_month_df, 'Month', 'Profit', title ='Profit by Month' )
fig_employee = create_bar_chart(profit_employee_df, 'Profit', 'Employee', orientation='h', title='Profit by Employee')
fig_product = create_bar_chart(profit_product_df,  'Profit','ProductName',orientation='h', title='Profit by ProductName' )
fig_supplier = create_bar_chart(profit_supplier_df, 'Profit', 'Suppliers', orientation='h', title='Profit by Suppliers')
fig_customer = create_bar_chart(Profit_customer_df, 'Customer', 'Profit', title='Profit by Customer')

# Waterfall chart for Profit by Category
profits = profit_category_df['Profit'].tolist()
category_names = profit_category_df['CategoryName'].tolist()
fig_category = go.Figure(go.Waterfall(
    name="20", orientation="v",
    measure=["relative"] * len(profits) + ["total"],
    x=category_names + ["Total"],
    textposition="outside",
    text=[f"{p:+}" for p in profits] + ["Total"],
    y=profits + [sum(profits)],
    connector={"line": {"color": "rgb(63, 63, 63)"}}
))
fig_category.update_layout(
    title='Profit by Category',
    title_font_size=22,
    xaxis_title='Category',
    yaxis_title='Profit',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    xaxis=dict(showgrid=False, gridcolor='lightgrey'),
    yaxis=dict(showgrid=False, gridcolor='lightgrey')
)

# Pie chart for Profit by Shippers
fig_shippers = px.pie(profit_shippers_df, names='Shippers', values='Profit', hole=0.6)
fig_shippers.update_traces(marker=dict(colors=color_scheme), textposition="inside", text=profit_shippers_df["Shippers"])

# Scatter chart for orders by ship
TotalOrders = scateer_avgshio_df['Total Orders'].tolist()
Ship_Name = scateer_avgshio_df['ShipName'].tolist()

fig_ship = go.FigureWidget([go.Scatter(x=TotalOrders , y=Ship_Name, mode='markers')])
scatter = fig_ship.data[0]
colors = ['#a3a7e4'] * 100
scatter.marker.color = colors
scatter.marker.size = [10] * 100
fig_ship.layout.hovermode = 'closest'

# create our callback function
def update_point(trace, points, selector):
    c = list(scatter.marker.color)
    s = list(scatter.marker.size)
    for i in points.point_inds:
        c[i] = '#bae2be'
        s[i] = 30
        with fig_ship.batch_update():
            scatter.marker.color = c
            scatter.marker.size = s
scatter.on_click(update_point)

# Create a subplot layout for all the charts
part1 , part2 , part3 , part4 , map = st.columns(5)

with part1 :
    fig1 = make_subplots(
        rows=2, cols=1,
        subplot_titles=(
            "Profit by Shippers",
            "Profit by Suppliers"
            "", ""
        ),
        specs=[[{'type': 'domain'}],
            [{'type': 'bar'}]]
    )

    # Add the individual charts to the layout
    fig1.add_trace(fig_shippers.data[0], row=1, col=1)
    fig1.add_trace(fig_supplier.data[0], row=2, col=1)

    # Update the layout
    fig1.update_layout(height=1000, width=1400, showlegend=False)

    # Display the combined chart
    st.write(fig1)

with part2 :
    fig2 = make_subplots(
        rows=2, cols=1,
        subplot_titles=(
             "Profit by Month",
             "Profit by ProductName" 
            "", ""
        ),
        specs=[[{'type': 'bar'}],
            [{'type': 'bar'}]]
    )

    # Add the individual charts to the layout
    fig2.add_trace(fig_month.data[0], row=1, col=1)
    fig2.add_trace(fig_product.data[0], row=2, col=1)

    # Update the layout
    fig2.update_layout(height=1000, width=1400, showlegend=False)

    # Display the combined chart
    st.write(fig2)


with part3 :
    fig3 = make_subplots(
        rows=2, cols=1,
        subplot_titles=(
             "Profit by Employee",
             "Profit by Category"
            "", ""
        ),
        specs=[[{'type': 'bar'}],
            [{'type': 'bar'}]]
    )

    # Add the individual charts to the layout
    fig3.add_trace(fig_employee.data[0], row=1, col=1)
    fig3.add_trace(fig_category.data[0], row=2, col=1)

    # Update the layout
    fig3.update_layout(height=1000, width=1400 , showlegend=False)

    # Display the combined chart
    st.write(fig3)

with part4 :
    fig4 = make_subplots(
        rows=2, cols=1,
        subplot_titles=(
             "Orders by Ship",
             "Top 10 Customers"
            "", ""
        ),
        specs=[[{'type': 'bar'}],
            [{'type': 'bar'}]]
    )

    # Add the individual charts to the layout
    fig4.add_trace(fig_ship.data[0], row=1, col=1)
    fig4.add_trace(fig_customer.data[0], row=2, col=1)

    # Update the layout
    fig4.update_layout(height=1000, width=1400 , showlegend=False)

    # Display the combined chart
    st.write(fig4)

with map :
    st.markdown("## Profit by Country")
    # Use absolute values of profit for marker size (positive sizes only)
    profit_country_df['Profit_Abs'] = profit_country_df['Profit'].abs()

    # Create the scattergeo map plot for Profit by Country, with color based on profit
    fig_country = px.scatter_geo(
        profit_country_df, 
        locations="Country", 
        locationmode='country names',
        color="Profit", 
        hover_name="Country", 
        size="Profit_Abs",  # Use absolute values for sizing
        projection="orthographic",
        color_continuous_scale=[(0, "red"), (0.5, "white"), (1, "green")],  # Red for losses, green for profit
        range_color=[profit_country_df['Profit'].min(), profit_country_df['Profit'].max()]
    )

    # Update layout of the map
    fig_country.update_layout(
        height=800,  
        margin=dict(l=50, r=50, t=50, b=50)
    )

    # Display the country map
    st.write(fig_country)
    