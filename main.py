import streamlit as st
import pandas as pd
import copy
import numpy as np
import pydeck as pdk
st.set_page_config(layout="wide")

municipio = 'Todos'
categoria = 'Todas'


def get_data():
    data = pd.read_csv('escolas.csv', sep=';')
    data.dropna(subset=['lat', 'lon'],inplace=True, axis=0, how = 'all')
    data.dropna(subset=['Escola'], inplace=True, axis=0, how='all')
    if municipio != 'Todos':
        data = data.query('`Município`=="' + municipio + '"')
    if categoria != 'Todas':
        data = data.query('`Categoria Administrativa`=="' + categoria + '"')

    return data

st.title("Escolas no RS")
st.write('Contato: humberto@humbertomoura.com.br')

st.sidebar.header("Exibição")
tab = st.sidebar.checkbox('Mostrar Tabela',value=True)
if tab:
    st.subheader("Todos os Dados")
    tabela = st.dataframe(get_data())


ma = st.sidebar.checkbox('Mostrar Mapa Distribuição',value=True)
if ma:
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
da = ['Todos']
municipio = st.sidebar.selectbox('Município', da + get_data()['Município'].unique().tolist(), index=0)
if municipio=='Todos':
    if tab:
        tabela.write(get_data())
    if ma:
        mapa.map(get_data())
else:
    #novo = novo[novo['Município'] == municipio]
    novo = get_data().query('Município=="' + municipio + '"')
    if tab:
        tabela.write(novo)

    if ma:
        mapa.map(novo)


#alunos = st.sidebar.slider('Quantidade de Professores', min_value=1,max_value=200,step=10)


#matriculas = st.sidebar.slider('Quantidade de Matrículas',1, 1000, (250, 750))

cols = ["Restrição de Atendimento", "Código INEP","Localização", "Localidade Diferenciada", "Endereço", "Telefone","Dependência Administrativa","Categoria Escola Privada","Conveniada Poder Público","Regulamentação pelo Conselho de Educação","Porte da Escola","Etapas e Modalidade de Ensino Oferecidas","Outras Ofertas Educacionais"]
# cols = ["Restrição de Atendimento", "Escola", "Código INEP", "UF", "Município","Localização", "Localidade Diferenciada", "Categoria Administrativa", "Endereço", "Telefone","Dependência Administrativa","Categoria Escola Privada","Conveniada Poder Público","Regulamentação pelo Conselho de Educação","Porte da Escola","Etapas e Modalidade de Ensino Oferecidas","Outras Ofertas Educacionais","lat","lon"]



#st.write(df)
lat = -30.0277
lon = -51.2287
ma2 = st.sidebar.checkbox('Mostrar Visão Geral',value=True)
if ma2:
    st.subheader("Mapa Visão Geral")
    mapa2 = st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",
            initial_view_state=pdk.ViewState(
            latitude=lat, longitude=lon, zoom=9, pitch=50, bearing=-27.36
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




