import streamlit as st
import pandas as pd
import plotly.express as px


# Junta datos de establecimietos y ubiego
dfEstab = pd.read_csv("TB_CENTRO_VACUNACION.csv", delimiter=";")
#dfEstab = dfEstab.drop(["id_eess"])
dfUbi = pd.read_csv("TB_UBIGEOS.csv", delimiter=";")
# Elimina columnas que sobran
dfUbi = dfUbi.drop(["ubigeo_reniec","ubigeo_inei","departamento_inei","provincia_inei","region",
            "macroregion_inei","macroregion_minsa","iso_3166_2","fips","superficie","Frontera",
            "latitud","longitud"], axis=1)
# Junta dataframes
dfCentros = pd.merge(dfEstab, dfUbi, on="id_ubigeo")
dfCentros = dfCentros.drop(["id_centro_vacunacion","id_ubigeo","id_eess"], axis=1)

# Elimina filas que tiene Latitud o Longitud en cero
dfCentros.drop(dfCentros[(dfCentros["latitud"]==0) & (dfCentros["longitud"]==0)].index, inplace=True )

#st.title("Centros de Vacunación")

# URL de la imagen de fondo
fondo_url = "https://raw.githubusercontent.com/JUANJO2023/PCD/refs/heads/main/Fondo.png"


# Título centrado y con color personalizado
st.markdown(
    "<h1 style='color: #023e8a; text-align: center;'>Centros de Vacunación</h1>",
    unsafe_allow_html=True
)

# CSS personalizado
st.markdown(
    f"""
    <style>
    /* Barra superior transparente */
    header[data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0);
        box-shadow: none;
    }}

    /* Contenedor del expander */
    .streamlit-expanderHeader {{
        background-color: #0077b6 !important;
        color: black !important;
        font-weight: bold;
        border-radius: 8px;
        padding: 5px 10px;
    }}

    /* Contenido del expander */
    .streamlit-expanderContent {{
        background-color: rgba(255, 255, 255, 0.7);
        padding: 10px;
        border-radius: 8px;
        color: black;
    }}

    details[open] > summary {{
        box-shadow: none !important;
    }}

    /* Fondo completo de la app */
    .stApp {{
        background: url("{fondo_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}

    .block-container {{
        background-color: rgba(255, 255, 255, 0.4);
        padding: 2rem;
        border-radius: 1rem;
    }}

    section[data-testid="stSidebar"] {{
        background-color: #1d3557;
        color: black;
    }}

    section[data-testid="stSidebar"] .css-1d391kg {{
        color: black;
    }}

    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {{
        color: #ffffff;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

menu = ["Todos","Ubicación","Personalizado (Distritos)","Centro de Vacunación"]

#Ubicación de logotipo
Logo_url='https://raw.githubusercontent.com/JUANJO2023/PCD/refs/heads/main/Logo.png'
st.sidebar.image(Logo_url)
choice = st.sidebar.selectbox("Menu",menu)
color = st.sidebar.color_picker("Color", value="#9E1FA2")

config = {'scrollZoom': True}

if choice=="Todos":
    # Ordena dataframe
    dfCentros.sort_values(["departamento","provincia","distrito","nombre"],inplace=True)

    with st.expander("Ver datos"):
        dfCentros.reset_index(inplace=True, drop=True)
        st.dataframe(dfCentros)

    fig = px.scatter_mapbox(dfCentros, lat="latitud", lon="longitud", hover_name="nombre", hover_data=["departamento","provincia","distrito"],
        color_discrete_sequence=[color], zoom=4, height=700)
    # Ordena dataframe
    dfCentros.sort_values(["departamento","provincia","distrito","nombre"],inplace=True)

    with st.expander("Ver datos"):
        dfCentros.reset_index(inplace=True, drop=True)
        st.dataframe(dfCentros)

    fig = px.scatter_mapbox(dfCentros, lat="latitud", lon="longitud", hover_name="nombre", hover_data=["departamento","provincia","distrito"],
                             color_discrete_sequence=[color], zoom=4, height=700, text='nombre')
    fig.update_layout(mapbox_style="open-street-map",
        paper_bgcolor="#e6f2ff",
        plot_bgcolor="#e6f2ff"        
        )
    st.plotly_chart(fig, config=config)

elif choice=="Ubicación":
    #pass
    # Ordena dataframe
    dfCentros.sort_values(["departamento","provincia","distrito","nombre"],inplace=True)

    dep_list = dfCentros["departamento"].unique().tolist()
    selected_dep = st.sidebar.selectbox("Departamento", dep_list,index=dep_list.index("LIMA"))

    df_tmp = dfCentros[(dfCentros["departamento"]==selected_dep)]
    prov_list = df_tmp["provincia"].unique().tolist()
    selected_prov = st.sidebar.selectbox("Provincia", prov_list, index=prov_list.index("LIMA"))    

    df_tmp = dfCentros[(dfCentros["departamento"]==selected_dep) & (dfCentros["provincia"]==selected_prov) ]
    dist_list = df_tmp["distrito"].unique().tolist()
    selected_dist = st.sidebar.selectbox("Distrito", dist_list, index=dist_list.index("LIMA"))

    with st.expander("Ver datos"):
        df = dfCentros[(dfCentros["departamento"]==selected_dep) & (dfCentros["provincia"]==selected_prov) & (dfCentros["distrito"]==selected_dist) ]
        df.reset_index(inplace=True, drop=True)
        st.dataframe(df)

    fig = px.scatter_mapbox(df, lat="latitud", lon="longitud", hover_name="nombre", hover_data=["departamento","provincia","distrito"],
                             color_discrete_sequence=[color], zoom=14, height=700)
    fig.update_traces(marker=dict(size=10,color=color,opacity=0.9))
    fig.update_layout(mapbox_style="open-street-map",
        paper_bgcolor="#e6f2ff",
        plot_bgcolor="#e6f2ff"        
        )
    st.plotly_chart(fig, config=config)

elif choice=="Personalizado (Distritos)":
    # Ordena dataframe
    dfCentros.sort_values(["distrito","nombre"],inplace=True)

    seldist_list = dfCentros["distrito"].unique().tolist()
    selected_dist = st.multiselect("Distritos",seldist_list, default=["LIMA"])
    with st.expander("Ver datos"):
        gdf = dfCentros[dfCentros["distrito"].isin(selected_dist)]
        gdf.reset_index(inplace=True, drop=True)
        st.dataframe(gdf)

    fig = px.scatter_mapbox(gdf, lat="latitud", lon="longitud", hover_name="nombre", hover_data=["departamento","provincia","distrito"],
                             color_discrete_sequence=[color], zoom=14, height=700)
    fig.update_traces(marker=dict(size=10,color=color,opacity=0.9))
    fig.update_layout(mapbox_style="open-street-map",
        paper_bgcolor="#e6f2ff",
        plot_bgcolor="#e6f2ff"        
        )
    st.plotly_chart(fig, config=config)

elif choice=="Centro de Vacunación":
    # Ordena dataframe
    dfCentros.sort_values(["nombre"],inplace=True)

    nom_list = dfCentros["nombre"].unique().tolist()
    selected_nombre = st.multiselect("Centro de Vacunación",nom_list, default=["CENTRO DE SALUD UNIDAD VECINAL Nº 3"])
    with st.expander("Ver datos"):
        gdf = dfCentros[dfCentros["nombre"].isin(selected_nombre)]
        gdf.reset_index(inplace=True, drop=True)
        st.dataframe(gdf)

    fig = px.scatter_mapbox(gdf, lat="latitud", lon="longitud", hover_name="nombre", hover_data=["departamento","provincia","distrito"],
                             color_discrete_sequence=[color], zoom=14, height=700)
    fig.update_traces(marker=dict(size=10,color=color,opacity=0.9))
    fig.update_layout(mapbox_style="open-street-map",
        paper_bgcolor="#e6f2ff",
        plot_bgcolor="#e6f2ff"        
        )
    st.plotly_chart(fig, config=config)

else:
    st.subheader("About")



