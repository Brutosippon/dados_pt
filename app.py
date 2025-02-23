#working app.py
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import requests
from dash_bootstrap_components.themes import BOOTSTRAP

app = Dash(__name__, title="Pro-Statistics", external_stylesheets=[BOOTSTRAP])
server = app.server  # For Heroku deployment

# Fetch GDP data from Eurostat (Portugal, 1995–2023, in million euros)
url_gdp = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp?format=JSON&geo=PT&unit=CP_MEUR&na_item=B1GQ"
response_gdp = requests.get(url_gdp).json()
print("GDP Response:", response_gdp)

# Extract years and values for GDP
all_years = list(response_gdp["dimension"]["time"]["category"]["index"].keys())
gdp_data = response_gdp["value"]
gdp_years = [year for i, year in enumerate(all_years) if str(i) in gdp_data]
gdp_values = [gdp_data[str(i)] for i, year in enumerate(all_years) if str(i) in gdp_data]
print("GDP Years:", gdp_years)
print("GDP Values:", gdp_values)

# Fetch inflation data (Portugal, annual average, 1996–2024)
url_inflation = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_aind?format=JSON&geo=PT&unit=RCH_A_AVG&coicop=CP00"
response_inflation = requests.get(url_inflation).json()
print("Inflation Response:", response_inflation)

# Extract years and values for inflation
inflation_years = list(response_inflation["dimension"]["time"]["category"]["index"].keys())
inflation_data = response_inflation["value"]
inflation_years_with_data = [year for i, year in enumerate(inflation_years) if str(i) in inflation_data]
inflation_values = [inflation_data[str(i)] for i, year in enumerate(inflation_years) if str(i) in inflation_data]
print("Inflation Years:", inflation_years_with_data)
print("Inflation Values:", inflation_values)

# Create DataFrame using overlapping years for GDP and Inflation
common_years = sorted(set(gdp_years) & set(inflation_years_with_data))
print("Common Years (GDP & Inflation):", common_years)

df = pd.DataFrame({
    "Year": common_years,
    "GDP": [gdp_data[str(all_years.index(year))] for year in common_years if str(all_years.index(year)) in gdp_data],
    "Inflation": [inflation_data[str(inflation_years.index(year))] for year in common_years if str(inflation_years.index(year)) in inflation_data]
})
print("DataFrame:", df)

# Ensure Year is treated as a categorical variable
df["Year"] = df["Year"].astype(str)

# Dropdown options
dropdown_options = ["GDP", "Inflation"]  # Only include available stats

# Initial charts
fig1 = px.bar(df, x="Year", y="GDP", color="Inflation", barmode="group")

# For scatter plot, use absolute value of Inflation for size to avoid negative values
fig2 = px.scatter(df, x="Year", y="GDP", size=df["Inflation"].abs(), color="Inflation", log_x=True, size_max=60)

# App layout with CSS classes
app.layout = html.Div(
    className="app-div black text-white text-center",
    children=[
        html.H1("Pro-Statistics"),
        html.H3("Dashboard: Access key statistical data for Portugal with just a few clicks."),
        html.H3("Simplifying statistics for everyday use."),
        html.Hr(className="black"),  # Using your hr styling
        html.H4("Portugal DataFrame (1996–2023)"),
        
        # Chart 1: Bar chart
        html.Div("1st Chart: Bar Chart", className="tabs-group"),
        dcc.Graph(id="graph1", figure=fig1),
        
        # Chart 2: Scatter plot
        html.Div("2nd Chart: Scatter Plot", className="tabs-group"),
        dcc.Graph(id="graph2", figure=fig2),
        
        # Configuration section with grid layout for dropdowns
        html.H3("Chart Configuration", className="tabs-group"),
        html.Div(
            className="dropdown-container",
            children=[
                html.Label("Y-Axis for Charts", className="budget-label"),
                dcc.Dropdown(
                    dropdown_options, "GDP", id="y_axis_column", 
                    className="dropdown-button bg-black text-black"
                ),
                html.Label("Color Axis for Chart 1", className="budget-label"),
                dcc.Dropdown(
                    dropdown_options, "Inflation", id="color_axis_fig1", 
                    className="dropdown-button bg-black text-black"
                ),
                html.Label("Size Axis for Chart 2", className="budget-label"),
                dcc.Dropdown(
                    dropdown_options, "Inflation", id="size_axis_fig2", 
                    className="dropdown-button bg-black text-black"
                ),
                html.Label("Color Axis for Chart 2", className="budget-label"),
                dcc.Dropdown(
                    dropdown_options, "Inflation", id="color_axis_fig2", 
                    className="dropdown-button bg-black text-black"
                ),
            ]
        ),
        
        html.Hr(className="black"),
        html.H4("Copyright 2022. All Rights Reserved João Fidalgo. Data Source: Eurostat.", className="tabs-group"),
    ]
)

# Callback for updating bar chart (Chart 1)
@app.callback(
    Output("graph1", "figure"),
    [Input("y_axis_column", "value"), Input("color_axis_fig1", "value")]
)
def update_bar_chart(y_axis, color_axis):
    fig1 = px.bar(df, x="Year", y=y_axis, color=color_axis, barmode="group")
    return fig1

# Callback for updating scatter plot (Chart 2)
@app.callback(
    Output("graph2", "figure"),
    [Input("y_axis_column", "value"), Input("size_axis_fig2", "value"), Input("color_axis_fig2", "value")]
)
def update_scatter_chart(y_axis, size_axis, color_axis):
    # Use absolute value for size to handle negative inflation
    size_values = df[size_axis].abs() if size_axis == "Inflation" else df[size_axis]
    fig2 = px.scatter(df, x="Year", y=y_axis, size=size_values, color=color_axis, log_x=True, size_max=60)
    return fig2

if __name__ == "__main__":
    app.run_server(debug=True)