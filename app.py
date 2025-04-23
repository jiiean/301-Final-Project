# app.py
from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go
import requests

app = Flask(__name__)

def make_figure():
    # Simulated data
    data = pd.DataFrame({
        'county_name': [
            'Baltimore City', 'Montgomery County', "Prince George's County",
            'Howard County', 'Anne Arundel County', 'Allegany County',
            'Harford County', 'Charles County', 'Frederick County',
            'Wicomico County'
        ],
        'fips': ['24510','24031','24033','24027','24003','24001','24025','24017','24021','24045'],
        'ozone_level': [35,28,31,22,29,20,24,27,25,30],
        'asthma_rate': [11.2,7.9,10.5,6.8,8.3,13.0,9.1,10.0,7.5,12.1]
    })

    # Load counties geojson
    geojson_url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    geojson = requests.get(geojson_url).json()

    fig = go.Figure()

    # Asthma choropleth
    fig.add_choropleth(
        geojson=geojson,
        locations=data.fips,
        z=data.asthma_rate,
        colorscale="Reds",
        zmin=5, zmax=15,
        colorbar_title="Asthma %",
        visible=True,
        hovertext=data.county_name + '<br>O₃: ' + data.ozone_level.astype(str) + ' ppb',
        hoverinfo='text'
    )

    # Ozone choropleth
    fig.add_choropleth(
        geojson=geojson,
        locations=data.fips,
        z=data.ozone_level,
        colorscale="Blues",
        zmin=20, zmax=40,
        colorbar_title="Ozone (ppb)",
        visible=False,
        hovertext=data.county_name + '<br>Asthma: ' + data.asthma_rate.astype(str) + '%',
        hoverinfo='text'
    )

    # Toggle buttons
    fig.update_layout(
        updatemenus=[{
            "type": "buttons", "direction": "right",
            "x": 0.5, "y": 1.15, "xanchor": "center", "yanchor": "top",
            "buttons": [
                {
                    "label": "🌬️ Asthma",
                    "method": "update",
                    "args":[{"visible":[True,False]}, {"title":"Asthma Rates in Maryland Counties"}]
                },
                {
                    "label": "☁️ Ozone",
                    "method": "update",
                    "args":[{"visible":[False,True]}, {"title":"Ozone Levels in Maryland Counties"}]
                }
            ]
        }],
        title_text="Environmental & Health Indicators in Maryland Counties",
        geo_scope="usa"
    )

    # return HTML div
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

@app.route("/")
def index():
    plot_div = make_figure()
    return render_template("index.html", plot_div=plot_div)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
