import streamlit as st
import pandas as pd
import copy
import numpy as np
import pydeck as pdk
import time

full_time = time.time()
print("Inicio Total")

st.set_page_config(layout="wide")

municipio = 'Todos'
categoria = 'Todas'
uf = 'Todas'



st.cache(allow_output_mutation=True)
def get_data():
    full_time = time.time()
    print("Inicio getdata()")
    data = pd.read_csv('dados/escolas.csv', sep=',',index_col=0)
    
    if categoria != 'Todas':
        data = data.query('`Categoria Administrativa`=="' + categoria + '"')
    if uf != 'Todas':
        data = data.query('`UF`=="' + uf + '"')
    if municipio != 'Todos':
        data = data.query('`Município`=="' + municipio + '"')
    

    print("Fim getdata() --- %s segundos ---" % (time.time() - start_time))
    return data

st.title("Dispersão das Escolas no Brasil")
st.subheader("Públicas, Privadas, Estados e Municípios")
st.write('Contato: humberto@humbertomoura.com.br')

st.sidebar.header("Exibição")
tab = st.sidebar.checkbox('Mostrar Tabela',value=True)
if tab:
    start_time = time.time()
    print("Inicio Tabela")
    
    st.subheader("Todos os Dados")
    dados = get_data()
    tabela = st.dataframe(dados[:5000])
   
    print("Fim Tabela --- %s segundos ---" % (time.time() - start_time))


ma = st.sidebar.checkbox('Mostrar Mapa Distribuição',value=True)
if ma:
    start_time = time.time()
    print("Inicio Mapa Simples")


    st.subheader("Distribuição Geográfica")
    mapa = st.map(get_data())
    print("Fim Mapa Simples --- %s segundos ---" % (time.time() - start_time))




#cols = "Restrição de Atendimento", "Escola", "Código INEP", "UF", "Município","Localização", "Localidade Diferenciada", "Categoria Administrativa", "Endereço", "Telefone","Dependência Administrativa","Categoria Escola Privada","Conveniada Poder Público","Regulamentação pelo Conselho de Educação","Porte da Escola","Etapas e Modalidade de Ensino Oferecidas","Outras Ofertas Educacionais","lat","lon"]

print("Inicio Categ Administrativa")
start_time = time.time()

st.sidebar.header("Escolas")
categoria = st.sidebar.radio("Categoria Administrativa",('Todas','Pública', 'Privada'))

if categoria=='Todas':  
    data = get_data()
    
else:
    if municipio != 'Todos':
        data = get_data().query('`Categoria Administrativa`=="' + categoria + ' AND Município=="' + municipio + '"')
    else:
        data = get_data().query('`Categoria Administrativa`=="' + categoria + '"')
    
if tab:
    tabela.write(data)
if ma:
    mapa.map(data)


print("Fim Cat. Administrativa --- %s segundos ---" % (time.time() - start_time))



start_time = time.time()
print("Início UF")
# a + get_data()['UF'].sort_values().unique().tolist(), index=0
uf = st.sidebar.selectbox('UF', ['Todas','AC','AL','AM','AP','BA','CE','DF','ES','GO','MA', 'MG','MS','MT','PA','PB','PE', 'PI','PR', 'RJ','RN','RO','RR','RS','SC','SE','SP','TO'])
if uf =='Todas':
    if tab:
        tabela.write(get_data()[:5000])
        
    if ma:
        mapa.map(get_data())
else:
    novo = get_data().query('UF=="' + uf + '"')
    if tab:
        tabela.write(novo[:5000])
    if ma:
        mapa.map(novo)
print("Fim UF --- %s segundos ---" % (time.time() - start_time))

start_time = time.time()
print("Início Município")
da = ['Todos']
municipio = st.sidebar.selectbox('Município', da + get_data()['Município'].sort_values().unique().tolist(), index=0)
if municipio=='Todos':
    if tab:
        tabela.write(get_data())       
    if ma:
        mapa.map(get_data())
else:
    novo = get_data().query('Município=="' + municipio + '"')
    if tab:
        tabela.write(novo[:5000])
    if ma:
        mapa.map(novo[:5000])
start_time = time.time()
print("Fim Município --- %s segundos ---" % (time.time() - start_time))

  
# cols = ["Restrição de Atendimento", "Escola", "Código INEP", "UF", "Município","Localização", "Localidade Diferenciada", "Categoria Administrativa", "Endereço", "Telefone","Dependência Administrativa","Categoria Escola Privada","Conveniada Poder Público","Regulamentação pelo Conselho de Educação","Porte da Escola","Etapas e Modalidade de Ensino Oferecidas","Outras Ofertas Educacionais","lat","lon"]
# cols = ["Porte da Escola","Etapas e Modalidade de Ensino Oferecidas"]


# lat = -30.0277
# lon = -51.2287

# start_time = time.time()
# print("Início Mapa Visão Geral")
# ma2 = st.sidebar.checkbox('Mostrar Visão Geral',value=True)
# if ma2:
#     st.subheader("Mapa Visão Geral")
#     mapa2 = st.pydeck_chart(
#         pdk.Deck(
#             map_style="mapbox://styles/mapbox/dark-v10",
#             initial_view_state=pdk.ViewState(
#             latitude=lat,
#             longitude=lon, 
#             zoom=9, 
#             pitch=50, 
#             bearing=-27.36,
#             pickable=True,
#             opacity=0.8,
#             stroked=True,
#             filled=True,
#             radius_scale=6,
#             radius_min_pixels=1,
#             radius_max_pixels=100,
#             line_width_min_pixels=1
#         ),
#         layers=[

#             pdk.Layer(
#                 "ScatterplotLayer",
#                 data=get_data().drop(axis=1, columns=cols),
#                 get_position="[lon, lat]",
#                 get_color="[200, 30, 0, 160]",
#                 get_radius=200,
#             ),
#         ],
#     )
# )

# print("Fim Mapa Visão Geral --- %s segundos ---" % (time.time() - start_time))
# print("Fim Total --- %s segundos ---" % (time.time() - full_time))


