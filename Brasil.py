import streamlit as st
import pandas as pd
import copy
import numpy as np
import pydeck as pdk

st.set_page_config(layout="wide")

municipio = 'Todos'
categoria = 'Todas'
uf = 'Todas'


# @st.cache(suppress_st_warning=True,allow_output_mutation=True)
def get_data():
    if uf == 'Todas':
        data = pd.read_csv('dados/escolas.csv', sep=';')
    
    data = data.drop(axis=1, columns=["Restrição de Atendimento","Localidade Diferenciada","Dependência Administrativa","Categoria Escola Privada","Conveniada Poder Público","Regulamentação pelo Conselho de Educação","Outras Ofertas Educacionais"])
    data.dropna(subset=['lat', 'lon'],inplace=True, axis=0, how = 'all')
    data.dropna(subset=['Escola'], inplace=True, axis=0, how='all')
    
    if uf != 'Todas':
        data = data.query('`UF`=="' + uf + '"')
    
    if municipio != 'Todos':
        data = data.query('`Município`=="' + municipio + '"')
    
    if categoria != 'Todas':
        data = data.query('`Categoria Administrativa`=="' + categoria + '"')

    return data

st.title("Dispersão das Escolas no Brasil")
st.subheader("Públicas, Privadas, Estados e Municípios")
st.write('Contato: humberto@humbertomoura.com.br')



st.subheader("Todos os Dados")
tabela = st.dataframe(get_data())



st.subheader("Distribuição Geográfica")
mapa = st.map(get_data())



#cols = "Restrição de Atendimento", "Escola", "Código INEP", "UF", "Município","Localização", "Localidade Diferenciada", "Categoria Administrativa", "Endereço", "Telefone","Dependência Administrativa","Categoria Escola Privada","Conveniada Poder Público","Regulamentação pelo Conselho de Educação","Porte da Escola","Etapas e Modalidade de Ensino Oferecidas","Outras Ofertas Educacionais","lat","lon"]

st.sidebar.header("Escolas")
cat = st.sidebar.radio("Categoria Administrativa",('Todas','Pública', 'Privada'))

categoria = cat
if categoria=='Todas':
    novo = get_data()
    if tab:
        tabela.write(novo)
    if ma:
        mapa.map(novo)
else:
    novo = get_data().query('`Categoria Administrativa`=="' + categoria + '"')
    novo = get_data().query('Município=="' + municipio + '"')
    if tab:
        tabela.write(novo)

    if ma:

        mapa.map(novo)
da = ['Todas']

uf = st.sidebar.selectbox('UF', da + get_data()['UF'].unique().tolist(), index=0)
if uf =='Todas':
    tabela.write(get_data())
    mapa.map(get_data())
else:
    novo = get_data().query('UF=="' + uf + '"')
    tabela.write(novo)
    mapa.map(novo)

da = ['Todos']
municipio = st.sidebar.selectbox('Município', da + get_data()['Município'].unique().tolist(), index=0)
if municipio=='Todos':
    tabela.write(get_data())
    mapa.map(get_data())
else:
    novo = get_data().query('Município=="' + municipio + '"')
    tabela.write(novo)
    mapa.map(novo)


  
# cols = ["Restrição de Atendimento", "Escola", "Código INEP", "UF", "Município","Localização", "Localidade Diferenciada", "Categoria Administrativa", "Endereço", "Telefone","Dependência Administrativa","Categoria Escola Privada","Conveniada Poder Público","Regulamentação pelo Conselho de Educação","Porte da Escola","Etapas e Modalidade de Ensino Oferecidas","Outras Ofertas Educacionais","lat","lon"]
#cols = ["Código INEP","Localização","Endereço", "Telefone","Porte da Escola","Etapas e Modalidade de Ensino Oferecidas"]


lat = -30.0277
lon = -51.2287
ma2 = st.sidebar.checkbox('Mostrar Visão Geral',value=True)
if ma2:
    st.subheader("Mapa Visão Geral")
    mapa2 = st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",
            initial_view_state=pdk.ViewState(
            latitude=lat,
            longitude=lon, 
            zoom=9, 
            pitch=50, 
            bearing=-27.36,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1
        ),
        layers=[

            pdk.Layer(
                "ScatterplotLayer",
                data=get_data().drop(axis=1, columns=cols),
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)




