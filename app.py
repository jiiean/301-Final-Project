# app.py
from flask import Flask, render_template
import pandas as pd
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def index():
    # --- 1. Load & preprocess CDC asthma data ---
    ast = pd.read_csv('tableL6.csv')
    ast = ast[ast['Sample Sizec'].astype(str).str.isdigit()]
    ast = ast.rename(columns={
        'Sample Sizec': 'sample_size',
        'Prevalence (Percent)': 'prevalence'
    })
    ast['sample_size'] = ast['sample_size'].astype(int)
    ast['prevalence'] = ast['prevalence'].astype(float)
    state_prev = (
        ast.groupby('State')
           .apply(lambda g: (g['prevalence']*g['sample_size']).sum()/g['sample_size'].sum())
           .reset_index(name='weighted_prevalence')
    )
    abbr = {
      'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA',
      'Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA',
      'Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS',
      'Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA',
      'Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT',
      'Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM',
      'New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK',
      'Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC',
      'South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT',
      'Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'
    }
    state_prev['state_code'] = state_prev['State'].map(abbr)
    state_prev.dropna(subset=['state_code'], inplace=True)

    # --- 2. Choropleth: Asthma Prevalence ---
    fig1 = px.choropleth(
        state_prev,
        locations='state_code',
        locationmode='USA-states',
        color='weighted_prevalence',
        color_continuous_scale='Reds',
        scope='usa',
        labels={'weighted_prevalence':'Asthma %'},
        title='📊 2021 Adult Asthma Prevalence by State'
    )

    # --- 3. Load & preprocess OpenAQ data ---
    aq = pd.read_csv('openaq.csv', sep=';')
    aq[['latitude','longitude']] = aq['Coordinates'].str.split(',', expand=True).astype(float)
    aq['timestamp'] = pd.to_datetime(aq['Last Updated'], errors='coerce')
    us_o3 = aq[
        (aq['Country Code']=='US') &
        (aq['Pollutant']=='O3') &
        (aq['Value']>0)
    ].copy()

    # --- 4. Scatter‐Geo: O₃ Sensor Readings ---
    fig2 = px.scatter_geo(
        us_o3,
        lat='latitude',
        lon='longitude',
        color='Value',
        size='Value',
        color_continuous_scale='Viridis',
        scope='usa',
        labels={'Value':'Ozone (µg/m³)'},
        hover_name='Location',
        hover_data={'City':True,'Value':':.1f'},
        title='🗺 2024 US Ozone Sensor Measurements'
    )

    # --- 5. Time Series: Monthly Avg O₃ Trend ---
    us_o3['month'] = us_o3['timestamp'].dt.to_period('M').dt.to_timestamp()
    monthly = (
        us_o3.groupby('month')['Value']
             .mean()
             .reset_index(name='avg_o3')
    )
    fig3 = px.line(
        monthly,
        x='month',
        y='avg_o3',
        markers=True,
        labels={'month':'Month','avg_o3':'Avg Ozone (µg/m³)'},
        title='📈 Monthly Avg. US Ozone Concentration (2024)'
    )
    last = monthly.iloc[-1]
    fig3.add_annotation(
        x=last['month'], y=last['avg_o3'],
        text=f"{last['avg_o3']:.1f}", showarrow=True, arrowhead=2
    )

    # Pass JSON to template
    return render_template(
        'index.html',
        fig1_json=fig1.to_json(),
        fig2_json=fig2.to_json(),
        fig3_json=fig3.to_json()
    )

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

