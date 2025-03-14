# Pro-Statistics Dashboard
## Overview
A Dash (Plotly) web app to visualize Portugal’s GDP and Inflation (1996–2023) using Eurostat data. Features interactive bar and scatter charts with customizable configuration via dropdowns. Simplifies statistics for everyday use with a clean, black-and-white design.
## Features

    Interactive bar and scatter plots for GDP and Inflation.
    Customizable Y-axis, color, and size via dropdowns.
    Real-time data from Eurostat API.
    Responsive, black-background layout.

## Prerequisites

    Python 3.8+
    Required packages: dash, dash-bootstrap-components, plotly, pandas, requests

## Installation

### Clone the repo:
    git clone https://github.com/Brutosippon/dados_cv.git
    cd dados_cv

### Create a virtual environment (optional):

    python -m venv env_dados
    source env_dados/bin/activate  # On Windows: env_dados\Scripts\activate

### Install dependencies:

    pip install -r requirements.txt

### Usage
Run the app:
    
    python app.py

    Open http://127.0.0.1:8050/ in your browser to use the dashboard.

## Data Sources

    Eurostat API for GDP and Inflation data.

## Contributing
Fork the repo, make changes, and submit a pull request. Open an issue for major changes.

## License
MIT License (see LICENSE file if applicable).

## Acknowledgments

    João Fidalgo: Creator.
    Eurostat: Data provider.