import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Load and preprocess data
df = pd.read_excel('Online Retail.xlsx')

# Data cleaning and feature engineering
df = df.dropna(subset=['CustomerID', 'Description'])
df = df[df['Quantity'] > 0]
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
df['DayOfWeek'] = df['InvoiceDate'].dt.dayofweek
df['Day'] = df['InvoiceDate'].dt.day

# Customer segmentation
customer_spending = df.groupby('CustomerID')['TotalPrice'].sum().reset_index()
customer_spending['Segment'] = pd.cut(customer_spending['TotalPrice'], 
                                      bins=[0, 100, 500, 1000, float('Inf')],
                                      labels=['Low Spenders', 'Medium Spenders', 'High Spenders', 'Very High Spenders'])

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Get unique YearMonth
unique_year_months = df['YearMonth'].sort_values().unique()
date_marks = {i: date for i, date in enumerate(unique_year_months)}

colors = {
    'background': '#111111',
    'text': '#0000FF'  # Changed title color to blue
}

# Layout
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1("Online Retail Dashboard", style={'text-align': 'center', 'color': colors['text']}),

    html.Div([
        dcc.RangeSlider(
            id='date-slider',
            min=0,
            max=len(unique_year_months) - 1,
            value=[0, len(unique_year_months) - 1],
            marks=date_marks,
            className='mb-4'
        )
    ], style={'padding': '10px 5px'}),

    html.Div([
        dcc.Graph(id='sales-over-time')
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in df['Country'].unique()],
            value=['United Kingdom'],
            multi=True,
            className='mb-4'
        ),
        dcc.Graph(id='sales-by-country')
    ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'top'}),

    html.Div([
        dcc.Graph(id='top-products')
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='sales-map')
    ], style={'width': '49%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(id='customer-segmentation')
    ], style={'width': '49%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id='monthly-sales')
    ], style={'width': '49%', 'display': 'inline-block'})
])

# Callbacks
@app.callback(
    Output('sales-over-time', 'figure'),
    Input('date-slider', 'value')
)
def update_sales_over_time(date_range):
    start_date = unique_year_months[date_range[0]]
    end_date = unique_year_months[date_range[1]]
    filtered_df = df[(df['YearMonth'] >= start_date) & (df['YearMonth'] <= end_date)]
    sales_over_time = filtered_df.groupby('InvoiceDate')['TotalPrice'].sum().reset_index()
    fig = px.line(sales_over_time, x='InvoiceDate', y='TotalPrice', title='Sales Over Time')
    fig.update_layout(template='plotly_dark')
    return fig

@app.callback(
    Output('sales-by-country', 'figure'),
    Input('country-dropdown', 'value')
)
def update_sales_by_country(selected_countries):
    if isinstance(selected_countries, str):
        selected_countries = [selected_countries]
    filtered_df = df[df['Country'].isin(selected_countries)]
    sales_by_country = filtered_df.groupby('Country')['TotalPrice'].sum().reset_index()
    fig = px.bar(sales_by_country, x='Country', y='TotalPrice', title='Sales by Country')
    fig.update_layout(template='plotly_dark')
    return fig

@app.callback(
    Output('top-products', 'figure'),
    Input('date-slider', 'value')
)
def update_top_products(date_range):
    start_date = unique_year_months[date_range[0]]
    end_date = unique_year_months[date_range[1]]
    filtered_df = df[(df['YearMonth'] >= start_date) & (df['YearMonth'] <= end_date)]
    top_products = filtered_df.groupby('Description')['TotalPrice'].sum().reset_index().nlargest(10, 'TotalPrice')
    fig = px.bar(top_products, x='Description', y='TotalPrice', title='Top Products')
    fig.update_layout(template='plotly_dark')
    return fig

@app.callback(
    Output('sales-map', 'figure'),
    Input('date-slider', 'value')
)
def update_sales_map(date_range):
    start_date = unique_year_months[date_range[0]]
    end_date = unique_year_months[date_range[1]]
    filtered_df = df[(df['YearMonth'] >= start_date) & (df['YearMonth'] <= end_date)]
    sales_by_country = filtered_df.groupby('Country')['TotalPrice'].sum().reset_index()
    fig = px.choropleth(sales_by_country, locations='Country', locationmode='country names', color='TotalPrice',
                        title='Sales by Country', template='plotly_dark')
    return fig

@app.callback(
    Output('customer-segmentation', 'figure'),
    Input('date-slider', 'value')
)
def update_customer_segmentation(date_range):
    start_date = unique_year_months[date_range[0]]
    end_date = unique_year_months[date_range[1]]
    filtered_df = df[(df['YearMonth'] >= start_date) & (df['YearMonth'] <= end_date)]
    customer_spending = filtered_df.groupby('CustomerID')['TotalPrice'].sum().reset_index()
    customer_spending['Segment'] = pd.cut(customer_spending['TotalPrice'], 
                                          bins=[0, 100, 500, 1000, float('Inf')],
                                          labels=['Low Spenders', 'Medium Spenders', 'High Spenders', 'Very High Spenders'])
    segment_count = customer_spending['Segment'].value_counts().reset_index()
    segment_count.columns = ['Segment', 'Count']
    fig = px.pie(segment_count, values='Count', names='Segment', title='Customer Segmentation')
    fig.update_layout(template='plotly_dark')
    return fig

@app.callback(
    Output('monthly-sales', 'figure'),
    Input('date-slider', 'value')
)
def update_monthly_sales(date_range):
    start_date = unique_year_months[date_range[0]]
    end_date = unique_year_months[date_range[1]]
    filtered_df = df[(df['YearMonth'] >= start_date) & (df['YearMonth'] <= end_date)]
    monthly_sales = filtered_df.groupby('YearMonth')['TotalPrice'].sum().reset_index()
    fig = px.bar(monthly_sales, x='YearMonth', y='TotalPrice', title='Monthly Sales')
    fig.update_layout(template='plotly_dark')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
