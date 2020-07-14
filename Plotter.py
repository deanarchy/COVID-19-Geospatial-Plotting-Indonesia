import plotly.express as px
from plotly.offline import iplot,plot
import json
with open('Geospatial Files/indonesia-prov.geojson') as json_file:
    data = json.load(json_file)
import pandas as pd
import requests
resp = requests.get('https://api.kawalcorona.com/indonesia/provinsi')
print('Connecting to : https://api.kawalcorona.com/...')
if resp.status_code != 200:
    raise APIError(f'GET /provinsi/ {resp.status_code}')

covid = resp.json()
df = pd.DataFrame.from_dict({(i) : covid[i]['attributes'] for i in range(0,34)},
                            orient='index')
df['Provinsi'] = [i.upper() for i in df['Provinsi']]
df.rename(inplace = True,
         columns = {'Kasus_Posi':'Positif',
                    'Kasus_Semb':'Sembuh',
                    'Kasus_Meni':'Meninggal',
                    'Kode_Provi':'ID Provinsi'})
fig = px.choropleth_mapbox(df, geojson=data,locations='Provinsi',
                    featureidkey='properties.Provinsi',
                    center={"lat": -0.789275, "lon": 113.921326},
                    mapbox_style='open-street-map',
                    color='Positif',zoom=5,opacity=0.4,
                    title='Peta Persebaran COVID-19 Indonesia',
                    color_continuous_scale='algae',
                    hover_name='ID Provinsi',
                    hover_data=['Positif','Sembuh','Meninggal'])
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
plot(fig)
