
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import zipfile


#########################
## CONFIGURACIÓN DE PÁGINA
#########################
st.set_page_config(
    page_title="Práctica Final",
    page_icon="👾​",
    layout="wide",  # "centered" o "wide"
    initial_sidebar_state="expanded"
)

#########################
## ESTILOS PERSONALIZADOS (OPCIONAL)
#########################
def kpi_card(title, value, bg_color="#FAD4C0"):
    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        ">
            <h4 style="margin: 0; color: #4A2C2A;">{title}</h4>
            <h1 style="margin: 10px 0 0 0; color: #4A2C2A;">{value}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

def kpi_card_months(title, value, bg_color="#9EDAF6"):
    """Versión más pequeña de kpi_card para múltiples tarjetas."""
    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            padding: 2px 10px;
            border-radius: 12px;
            text-align: left;
            box-shadow: 0 3px 8px rgba(0,0,0,0.08);
            margin-bottom:5px;
            width: 200px;
            display: inline-block;
            height: 50px;
        ">
            <h5 style="margin: 0; color: #4A2C2A;">{title}</h5>
            <h3 style="margin: 0px 0 0 0; color: #4A2C2A;">{value}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

def kpi_card_states(title, value, bg_color="#FFB98A"):
    """Versión más pequeña de kpi_card para múltiples tarjetas."""
    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            padding: 2px 10px;
            border-radius: 12px;
            text-align: left;
            box-shadow: 0 3px 8px rgba(0,0,0,0.08);
            margin-bottom:5px;
            margin-rigth:5px;
            width: 167px;
            display: inline-block;
            height: 80px;
        ">
            <h5 style="margin: 0; color: #000000; font-size: 18px">{title}</h5>
            <h3 style="margin: 0px 0 0 0; color: #000000;font-size: 18px">{value}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

def kpi_card_shop(title, value, bg_color="#1CB960"):
    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            padding: 10px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        ">
            <h4 style="margin: 0; color: #000000";>{title}</h4>
            <h1 style="margin: 10px 0 0 0; color: #000000;">{value}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

def kpi_card_product(title, value, bg_color="#FFFACD"):
    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            padding: 10px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            width: 1000px;
            height: 140px;
            margin-left:200px
        ">
            <h4 style="margin: 0; color: #000000;font-size: 20px">{title}</h4>
            <h1 style="margin: 10px 0 0 0; color: #000000;font-size: 28px">{value}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

def kpi_card_resumen(title, value, color_text, line_height = 1.1, bg_color="#FEF8B5"):
    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            height: 200px
        ">
            <h4 style="margin: 0; color:  #000000;font-size: 25px">{title}</h4>
            <h1 style="margin: 10px 0 0 0; color: {color_text};font-size: 35px; line-height: {line_height}">{value}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
#########################
## SIDEBAR (MENÚ LATERAL)
#########################
with st.sidebar:
    st.title("⚙️ Configuración")
    st.divider()

    # Selector de página/sección
    pagina = st.selectbox(
        "Selecciona una sección",
        ["🦞 HomePage", "📈 Visualización Global", "📋​ Análisis por tienda", "🌐​ Análisis por Estado", "📇​ Evolución Temporal"]
    )

    st.divider()

    # Filtros o controles adicionales
    st.subheader("Filtros")
    filtro_1 = st.checkbox("Activar filtro 1", value=True)
    filtro_2 = st.slider("Ajuste", 0, 100, 50)

    st.divider()
    st.caption("© 2025 - Cecilia Díaz Álvaro")

#########################
## CONTENIDO PRINCIPAL
#########################

# Título principal con estilo tipo Coca-Cola
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');

    .logo-text {
        font-family: 'Pacifico', cursive;
        font-size: 60px;
        color: #FF0000;  /* rojo atractivo */
        text-align: center;
    }

    .subtitle-text {
        font-family: 'Arial', sans-serif;
        font-size: 20px;
        color: #333333;
        text-align: center;
    }
    </style>

    <div class="logo-text">🦞 Empresa de Alimentación El Bogavante</div>
    <div class="subtitle-text">Estudio Anual</div>
    """,
    unsafe_allow_html=True
)

st.divider()
# -------------------------------
# CARGA DE DATOS
# -------------------------------
#@st.cache_data
def load_data():
    zip_path1 = "parte_1.zip"      # tu archivo zip
    csv_inside_zip1 = "parte_1.csv"  # ruta dentro del zip
    with zipfile.ZipFile(zip_path1, 'r') as zip_ref:
    # Abrir el CSV dentro del zip como archivo
        with zip_ref.open(csv_inside_zip1) as csv_file1:
            df1 = pd.read_csv(csv_file1)
    zip_path2 = "parte_2.zip"      # tu archivo zip
    csv_inside_zip2 = "parte_2.csv"  # ruta dentro del zip
    with zipfile.ZipFile(zip_path2, 'r') as zip_ref:
    # Abrir el CSV dentro del zip como archivo
        with zip_ref.open(csv_inside_zip2) as csv_file2:
            df2 = pd.read_csv(csv_file2)

    #df1 = pd.read_csv("parte_1.zip/parte_1/parte_1.csv")
    #df2 = pd.read_csv("parte_2.zip/parte_2/parte_2.csv")

    df = pd.concat([df1, df2], ignore_index=True)

    # Convertir fecha
    df["date"] = pd.to_datetime(df["date"])

    return df

df = load_data()

#########################
## PÁGINA: INICIO
#########################
if pagina == "🦞 HomePage":
    st.markdown("""
        <h1 style="
            text-align: center;
            color:blue ;
            font-size: 60px;
            font-weight: bold;
        ">
        RESUMEN ANUAL VENTAS 
        </h1>
        """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1.5, 2, 1])  

    
    with col2:
        st.image("pngtree-red-lobster-boiled-sketching-craw-vector-png-image_17551474.png", width=400)

    st.markdown("""
        <h1 style="
            text-align: center;
            color:blue ;
            font-size: 60px;
            font-weight: bold;
        ">
        EJERCICIO 2025 
        </h1>
        """, unsafe_allow_html=True)


elif pagina == "📈 Visualización Global":

    col1, col2, col3 = st.columns([1, 2, 1])  
    with col2:
        st.markdown(
            """
            <h1 style="
                color: #E69118;           /* rojo anaranjado */
                font-family: 'Times New Roman', serif; /* letra elegante */
                font-weight: bold;
                text-align: center;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                margin-bottom: 20px;
                font-size: 45px;
            ">
                SITUACIÓN VENTAS
            </h1>
            """,
            unsafe_allow_html=True
        )
    st.divider()
    st.markdown(" ")
    st.markdown(" ")

    st.markdown(
    """
    <h2 style="
        color: #C21807;        /* burdeos */
        font-family: 'Arial', sans-serif;  /* puedes cambiar por 'Georgia', 'Verdana', etc. */
        font-weight: bold;      /* negrita */
        text-align: left;       /* izquierda, center, right */
        margin-bottom: 10px;
        font-size: 30px;
    ">
        📊 Conteo general
    </h2>
    """,
    unsafe_allow_html=True
    )

    st.markdown(" ")

    col1, col2= st.columns(2)

    with col1:
        kpi_card(
            "Nº tiendas",
            df["store_nbr"].nunique()
        )

    with col2:
        kpi_card(
            "Nº productos",
            df["family"].nunique()
        )

    st.markdown(" ")
    st.subheader("Estados")
    states = sorted(df["state"].unique())

    num_cols = 8
    rows = [states[i:i+num_cols] for i in range(0, len(states), num_cols)]
    for row in rows:
        cols = st.columns(len(row))
        for i, state in enumerate(row):
            with cols[i]:
                kpi_card_states(state, "")  

    st.divider()


    st.subheader("Meses")
    df["month_name"] = df["date"].dt.month_name()
    months = (
        df[["month", "month_name"]]
        .drop_duplicates()
        .sort_values("month")["month_name"]
    )
    for month in months:
        kpi_card_months(month, "")


    st.divider()

    st.markdown(
    """
    <h2 style="
        color: #C21807;        /* burdeos */
        font-family: 'Arial', sans-serif;  /* puedes cambiar por 'Georgia', 'Verdana', etc. */
        font-weight: bold;      /* negrita */
        text-align: left;       /* izquierda, center, right */
        margin-bottom: 10px;
        font-size: 30px;
    ">
        🎯​Ranking y Distribución
    </h2>
    """,
    unsafe_allow_html=True
    )

    st.markdown(" ")

    colA, colB = st.columns(2)


    with colA:

        top_families = (
            df.groupby("family")["sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        ).reset_index()


        fig = px.bar(
            top_families,
            x='family',
            y='sales',
            text='sales',  
            color_discrete_sequence=["#F88379"] 
        )

       
        fig.update_traces(
            texttemplate='%{y:,}',
            textposition='outside',  
            textfont_size=16
        )

        # Layout del gráfico
        fig.update_layout(
            title={
                'text': "Top 10 Productos más vendidos",
                'x':0.5,  # centrar título
                'xanchor': 'center',
                'font': {'size':16, 'color':"#000000", 'family':'Arial'}
            },
            xaxis_title="Producto",
            yaxis_title="Ventas",
            xaxis_tickangle=-45,
            yaxis=dict(tickformat=','),
            margin=dict(t=80, b=100),
            height=525    
        )

       
        st.plotly_chart(fig, use_container_width=True)


        promo_df = df[df["onpromotion"] == True]

        top_tiendas_promo = (
            promo_df.groupby("store_nbr")["sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        # Crear columna para etiquetas de eje X
        top_tiendas_promo['store_label'] = top_tiendas_promo['store_nbr'].apply(lambda x: f"T. {x}")

        # Gráfico vertical interactivo
        fig2 = px.bar(
            top_tiendas_promo,
            x='store_label', 
            y='sales',       
            text='sales',     
            color_discrete_sequence=['#9B59B6']  
        )

        fig2.update_traces(
            texttemplate='%{y:,}',
            textposition='outside',
            textfont_size=14
        )

        fig2.update_layout(
            title={
                'text': "Top 10 Tiendas con ventas en promoción",
                'x':0.5,
                'xanchor': 'center',
                'font': {'size':16, 'color':"#000000", 'family':'Arial'}
            },
            xaxis_title="Tienda",
            yaxis_title="Ventas",
            xaxis_tickangle=-45,  
            yaxis=dict(tickformat=','),
            margin=dict(t=80, b=150, l=80),  
            height=525 
        )

        st.plotly_chart(fig2, use_container_width=True)

    with colB:
        
        ventas_tienda = (
            df.groupby("store_nbr")["sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        
        ventas_tienda['store_label'] = ventas_tienda['store_nbr'].apply(lambda x: f"T. {x}")

       
        fig = px.bar(
            ventas_tienda,
            y='store_label', 
            x='sales',
            text='sales',     
            orientation='h',
            color_discrete_sequence=["#1CB960"]
        )

        
        fig.update_traces(
            texttemplate='%{x:,}',  
            textposition='outside',
            textfont_size=14
        )

       
        fig.update_layout(
            title={
                'text': "Ventas por Tienda",
                'x':0.5,
                'xanchor': 'center',
                'font': {'size':16, 'color':"#000000", 'family':'Arial'}
            },
            xaxis_title="Ventas",
            yaxis_title="Tienda",
            yaxis=dict(autorange="reversed"),  
            margin=dict(t=80, b=50, l=100),    
            height=1000
        )

        st.plotly_chart(fig, use_container_width=True)


    st.divider()
    st.markdown(
    """
    <h2 style="
        color: #C21807;        /* burdeos */
        font-family: 'Arial', sans-serif;  /* puedes cambiar por 'Georgia', 'Verdana', etc. */
        font-weight: bold;      /* negrita */
        text-align: left;       /* izquierda, center, right */
        margin-bottom: 10px;
        font-size: 30px;
    ">
        ​📉​Estacionalidad de las ventas
    </h2>
    """,
    unsafe_allow_html=True
    )

    st.markdown(" ")

    coll,colr = st.columns(2)

    with colr:

        week_sales = (
            df.groupby("week")["sales"]
            .mean()
            .reset_index()
        )

        fig = px.line(
            week_sales,
            x="week",
            y="sales",
            markers=True,
            color_discrete_sequence=["#C0392B"]  
        )

        fig.update_traces(
            marker=dict(size=6),
            line=dict(width=3)
        )

        fig.update_layout(
            title={
                'text': "Ventas medias semanales",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size':16, 'family':'Arial'}
            },
            xaxis=dict(
            title="Semana del año",
            tickmode='array',
            tickvals=list(week_sales["week"]),
            ticktext=[f"S.{int(w)}" for w in week_sales["week"]],
            range=[week_sales["week"].min(), week_sales["week"].max()],
            showgrid=True,
            tickfont=dict(size=9)
            ),
            yaxis=dict(
                title="Ventas medias",
                range=[0, None],              
                tickformat=',',
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(0,0,0,0.1)'
            ),
            margin=dict(t=80, b=60),
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    with coll:

        orden_dias = [
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"
        ]

        weekday_sales = (
            df.groupby("day_of_week")["sales"]
            .mean()
            .reindex(orden_dias)
            .reset_index()
        )

       
        fig = px.bar(
            weekday_sales,
            x="day_of_week",
            y="sales",
            text="sales",
            color_discrete_sequence=["#F4A6C1"] 
        )

       
        fig.update_traces(
            texttemplate='%{y:,.0f}',  
            textposition='outside',
            textfont_size=14
        )

       
        fig.update_layout(
            title={
                'text': "Ventas medias por día de la semana",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size':16, 'color':"#000000", 'family':'Arial'}
            },
            xaxis_title="Día de la semana",
            yaxis_title="Ventas medias",
            yaxis=dict(tickformat=','),
            margin=dict(t=80, b=80),
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    orden_meses = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
    ]

    month_sales = (
        df.groupby("month_name")["sales"]
        .mean()
        .reindex(orden_meses)
        .reset_index()
    )

    fig = px.line(
        month_sales,
        x="month_name",
        y="sales",
        markers=True,                
        color_discrete_sequence=["#2471A3"]  
    )

    fig.update_traces(
        marker=dict(size=8),
        line=dict(width=3)
    )

    fig.update_layout(
        title={
            'text': "Ventas medias por mes",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size':16, 'family':'Arial'}
        },
        xaxis_title="Mes",
        yaxis_title="Ventas medias",
        xaxis=dict(
            showgrid=True
        ),
        yaxis=dict(
            range=[0, None],
            tickformat=',',
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        margin=dict(t=80, b=80, l=175, r=175),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

elif pagina == "📋​ Análisis por tienda":

    # Título centrado
    col1, col2, col3 = st.columns([1.1, 2, 1])
    with col2:
        st.markdown(
            """
            <h1 style="
                color: #E69118;           /* rojo anaranjado */
                font-family: 'Times New Roman', serif; /* letra elegante */
                font-weight: bold;
                text-align: center;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                margin-bottom: 20px;
                font-size: 45px;
            ">
                INFORMACIÓN TIENDAS
            </h1>
            """,
            unsafe_allow_html=True
        )
    st.divider()
    st.markdown(" ")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown(
        """
        <h2 style="
            color: #C21807;        /* burdeos */
            font-family: 'Arial', sans-serif;  /* puedes cambiar por 'Georgia', 'Verdana', etc. */
            font-weight: bold;      /* negrita */
            text-align: left;       /* izquierda, center, right */
            margin-bottom: 10px;
            margin-left:90px;
            font-size: 40px;
        ">
            ​🏬 ​​Tienda
        </h2>
        """,
        unsafe_allow_html=True
        )

    
    
    with col2:
        store = st.selectbox(
            "",
            sorted(df["store_nbr"].unique())  
        )
    st.markdown(" ")
    st.markdown(" ")

    df_store = df[df["store_nbr"] == store]

    sales_year = df_store.groupby("year")["sales"].sum().reset_index()

    
    fig = px.bar(
        sales_year,
        x="year",
        y="sales",
        text="sales",  
        color_discrete_sequence=["#FFA65B"] 
    )

    
    fig.update_traces(
        texttemplate='%{y:,.0f}',  
        textposition='outside',
        textfont_size=14
    )

    
    fig.update_layout(
        title={
            'text': '<b>Ventas por año</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size':20, 'family':'Arial', 'color':'#000000'}
        },
        xaxis_title="Año",
        yaxis_title="Ventas",
        yaxis=dict(tickformat=',', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
        xaxis_tickangle=-45,
        margin=dict(t=80, b=100),
        height=700
    )

    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(" ")
    st.markdown(" ")

    cola, colb = st.columns(2)

    with cola:
        total_ventas = int(df_store["sales"].sum())
        kpi_card_shop(
            "Productos vendidos",
            f"{total_ventas:,}" 
        )

    with colb:
        promo_products = df_store[df_store["onpromotion"] > 0].shape[0]
        kpi_card_shop(
            "Productos en promoción",
            f"{promo_products:,}"
        )




elif pagina == "🌐​ Análisis por Estado":
        
    col1, col2, col3 = st.columns([1.1, 2, 1])
    with col2:
        st.markdown(
            """
            <h1 style="
                color: #E69118;           /* rojo anaranjado */
                font-family: 'Times New Roman', serif; /* letra elegante */
                font-weight: bold;
                text-align: center;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                margin-bottom: 20px;
                font-size: 45px;
            ">
                INFORMACIÓN ESTADOS
            </h1>
            """,
            unsafe_allow_html=True
        )
    st.divider()
    st.markdown(" ")

    col1,col2 = st.columns(2)
    with col1:
        st.markdown(
        """
        <h2 style="
            color: #C21807;        /* burdeos */
            font-family: 'Arial', sans-serif;  /* puedes cambiar por 'Georgia', 'Verdana', etc. */
            font-weight: bold;      /* negrita */
            text-align: left;       /* izquierda, center, right */
            margin-bottom: 10px;
            margin-left:80px;
            font-size: 40px;
        ">
            ​​🗾 ​​Estado
        </h2>
        """,
        unsafe_allow_html=True
        )

   
    
    with col2:
        state = st.selectbox(
            "",
            sorted(df["state"].unique())  
        )
    st.markdown(" ")
    st.markdown(" ")

   
    state_coords = {
        "Azuay": (-2.9006, -79.0045),
        "Bolivar": (-1.6006, -79.0001),
        "Chimborazo": (-1.5506, -78.9500),
        "Cotopaxi": (-0.9336, -78.6167),
        "El Oro": (-3.3667, -79.9667),
        "Esmeraldas": (0.8333, -79.6833),
        "Guayas": (-2.1667, -79.9000),
        "Imbabura": (0.3333, -78.1167),
        "Loja": (-4.0000, -79.2000),
        "Los Rios": (-1.7833, -79.7500),
        "Manabi": (-0.9500, -80.6667),
        "Pastaza": (-1.7500, -77.6167),
        "Pichincha": (-0.1500, -78.5000),
        "Santa Elena": (-2.2000, -80.8333),
        "Santo Domingo de los Tsachilas": (0.2500, -79.1667),
        "Tungurahua": (-1.2500, -78.5000)
    }

    df_map = pd.DataFrame([{
        "state": state,
        "lat": state_coords[state][0],
        "lon": state_coords[state][1]
    }])

    
    fig_map = px.scatter_mapbox(
        df_map,
        lat="lat",
        lon="lon",
        hover_name="state",
        size=[30],  
        color_discrete_sequence=["#C0392B"],  
    )

    
    fig_map.update_layout(
        mapbox=dict(
            style="open-street-map",  
            center={"lat": -1.7, "lon": -80.5}, 
            zoom=5.7,
        ),
        margin=dict(t=0, b=0, l=10, r=0),
        height=500,
        showlegend=False
    )

    
    fig_map.add_scattermapbox(
        lat=[state_coords[state][0]],
        lon=[state_coords[state][1]],
        mode="text",
        text=[state],
        textposition="top center",
        textfont=dict(size=16, color="#C0392B", family="Arial Black")
    )

    
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown(" ")
    st.markdown(" ")


    df_state = df[df["state"]==state]

    col3, col4 = st.columns(2)

    with col4:
    
        transactions = df_state.groupby("year")["transactions"].sum().reset_index()

        
        fig = px.line(
            transactions,
            x="year",
            y="transactions",
            markers=True,  
            color_discrete_sequence=["#FF8FD6"]  
        )

        
        fig.update_traces(
            texttemplate='<b>%{y:.}</b>',
            textposition='top center',
            textfont=dict(size=14, family='Arial', color='#000000'),
            line=dict(width=3)
        )

        
        fig.update_layout(
            title={
                'text': f"<b>Transacciones por año </b>",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size':16, 'family':'Arial', 'color':'#000000'}
            },
            xaxis_title="Año",
            yaxis_title="Número de transacciones",
            yaxis=dict(tickformat=',', showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
            xaxis=dict(dtick=1,showgrid=True),  
            margin=dict(t=80, b=100, l=60, r=40),
            height=550
        )

        
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        ventas_tienda_estado = (
            df_state.groupby("store_nbr")["sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        
        ventas_tienda_estado["store_label"] = ventas_tienda_estado["store_nbr"].apply(
            lambda x: f"Tienda {x}"
        )

        
        fig = px.bar(
            ventas_tienda_estado,
            y="store_label",
            x="sales",
            orientation="h",
            text="sales",
            color_discrete_sequence=["#50C878"] 
        )

        
        fig.update_traces(
            texttemplate="<b>%{x:.}</b>",
            textposition="outside",
            textfont=dict(size=14)
        )

       
        fig.update_layout(
            title={
                "text": f"<b>Ranking tiendas con más ventas</b>",
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 15, "family": "Arial"}
            },
            xaxis_title="Ventas",
            yaxis_title="",
            yaxis=dict(autorange="reversed"),  
            xaxis=dict(tickformat=",", showgrid=True, gridcolor="rgba(0,0,0,0.1)"),
            margin=dict(t=80, b=50, l=0, r=40),
            height=520
        )

        
        st.plotly_chart(fig, use_container_width=True)

    
    producto_top_estado = (
        df_state.groupby("family")["sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .iloc[0]
    )

    producto_nombre = producto_top_estado["family"]
    producto_ventas = int(producto_top_estado["sales"])

    st.markdown(" ")

    kpi_card_product(
    "Producto más vendido",
    value=f"{producto_nombre} ({producto_ventas:,} ventas)"
    )

elif pagina == "📇​ Evolución Temporal":

    
    col1, col2, col3 = st.columns([1.1, 2, 1])
    with col2:
        st.markdown(
            """
            <h1 style="
                color: #E69118;           /* rojo anaranjado */
                font-family: 'Times New Roman', serif; /* letra elegante */
                font-weight: bold;
                text-align: center;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                margin-bottom: 20px;
                font-size: 45px;
            ">
                EVOLUCIÓN 
            </h1>
            """,
            unsafe_allow_html=True
        )
    st.divider()
    st.markdown(" ")
    st.markdown(" ")


    
    ventas_year = df.groupby("year")["sales"].sum().sort_index()

   
    crecimiento_pct = (
        (ventas_year.iloc[-1] - ventas_year.iloc[-2]) / ventas_year.iloc[-2] * 100
    )

    
    pct_promo = df[df["onpromotion"] > 0]["sales"].sum() / df["sales"].sum() * 100

    
    crecimiento_estado = (
        df.groupby(["state", "year"])["sales"].sum()
        .reset_index()
        .pivot(index="state", columns="year", values="sales")
        .dropna()
    )

    crecimiento_estado["crecimiento"] = (
        crecimiento_estado.iloc[:, -1] - crecimiento_estado.iloc[:, -2]
    ) / crecimiento_estado.iloc[:, -2] * 100


    
    estado_top = crecimiento_estado["crecimiento"].idxmax()
    estado_peor = crecimiento_estado["crecimiento"].idxmin()

    col1, col2, col3, col4 = st.columns(4)

    if crecimiento_pct < 0:
        crecimiento_text = f"⬇ {crecimiento_pct:.1f} %"
        color_text_crecimiento= "#DC1929"
    else:
        crecimiento_text = f"⬆ {crecimiento_pct:.1f} %"
        color_text_crecimiento = "#05A129"

    if pct_promo >= 50:
        color_text =   "#05A129"
    else:
        color_text = "#DC1929"

    with col1:
        kpi_card_resumen("Crecimiento anual ventas", 
            crecimiento_text,
            color_text_crecimiento,
        )

  

    with col2:
        kpi_card_resumen(
            "Ventas en promoción     ",
            f"  {  pct_promo:.1f} %",
            color_text,
            line_height=2.7
        )

    with col3:
        kpi_card_resumen(
            "Estado con mayor crecimiento",
            estado_top,
            color_text="#05A129"
        )

    with col4:
        kpi_card_resumen(
            "Estado con peor evolución",
            estado_peor,
            color_text="#DC1929"
        )

    st.markdown(" ")
    st.markdown(" ")
    st.divider()

    st.markdown(
    """
    <h2 style="
        color: #C21807;        /* burdeos */
        font-family: 'Arial', sans-serif;  /* puedes cambiar por 'Georgia', 'Verdana', etc. */
        font-weight: bold;      /* negrita */
        text-align: left;       /* izquierda, center, right */
        margin-bottom: 10px;
        font-size: 30px;
    ">
        ⚖️​ Impacto Promociones por Estado
    </h2>
    """,
    unsafe_allow_html=True
    )

    st.markdown(" ")

    promo_state = (
        df.groupby("state")
        .agg(
            ventas=("sales", "sum"),
            promo=("onpromotion", lambda x: (x > 0).mean() * 100),
            transacciones=("transactions", "sum")
        )
        .reset_index()
    )

    
    colores = [
    "#FFA65B", 
    "#6CA0DC", 
    "#C0392B", 
    "#7A3EBF",  
    "#4FB286", 
    "#E6A75A",  
    "#5DA8B6",  
    "#D77FA1"  
]
    fig = px.scatter(
        promo_state,
        x="promo",
        y="ventas",
        size="transacciones",
        size_max=40,  
        color="ventas",  
        color_discrete_sequence=colores,  
        hover_data={
            "state": True,
            "ventas": ":,.0f",  
            "promo": ":.1f",
            "transacciones": ":,.0f"
        },
        labels={
            "promo": "% productos en promoción",
            "ventas": "Ventas totales",
            "transacciones": "Transacciones"
        }
    )
    fig.update_traces(
        marker=dict(
            line=dict(color="black", width=1.5) 
        )
    )


    
    fig.update_layout(
        height=550,
        title={
            "text": "<b>Promociones y ventas</b>",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size":18}
        },
        xaxis=dict(showgrid=True, title="% productos en promoción"),
        yaxis=dict(showgrid=True, title="Ventas totales", tickformat=","),
        coloraxis_colorbar=dict(title="Ventas"),
        template="plotly_white"
    )

    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(" ")
    st.markdown(" ")
    st.divider()

    
    st.markdown(
    """
    <h2 style="
        color: #C21807;        /* burdeos */
        font-family: 'Arial', sans-serif;  /* puedes cambiar por 'Georgia', 'Verdana', etc. */
        font-weight: bold;      /* negrita */
        text-align: left;       /* izquierda, center, right */
        margin-bottom: 10px;
        font-size: 30px;
    ">
        🏭​ Eficiencia ventas por tipo de tienda
    </h2>
    """,
    unsafe_allow_html=True
    )

    st.markdown(" ")

    eficiencia = (
        df.groupby("store_type")
        .agg(
            ventas_totales=("sales", "sum"),
            tiendas=("store_nbr", "nunique")
        )
        .reset_index()
    )

    eficiencia["ventas_por_tienda"] = eficiencia["ventas_totales"] / eficiencia["tiendas"]

    fig = px.bar(
        eficiencia,
        x="store_type",
        y="ventas_por_tienda",
        text="ventas_por_tienda",
        color_discrete_sequence=["#FF9288"]
    )

    fig.update_traces(
        texttemplate="<b>%{y:,.0f}</b>",
        textposition="outside"
    )

    fig.update_layout(
        height=450,
        yaxis=dict(tickformat=","),
        title={
            "text":"<b>Ventas medias por tienda</b>",
            "x": 0.5
        },
        yaxis_title = "Ventas",
        xaxis_title = "Tipo tienda"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(" ")
    st.markdown(" ")
    st.divider()

    st.markdown(
    """
    <h2 style="
        color: #C21807;        /* burdeos */
        font-family: 'Arial', sans-serif;  /* puedes cambiar por 'Georgia', 'Verdana', etc. */
        font-weight: bold;      /* negrita */
        text-align: left;       /* izquierda, center, right */
        margin-bottom: 10px;
        font-size: 30px;
    ">
        🗓️​​ Impacto Festivos
    </h2>
    """,
    unsafe_allow_html=True
    )

    st.markdown(" ")

    festivos = df.copy()
    festivos["es_festivo"] = festivos["holiday_type"].notna()

    ventas_festivos = (
        festivos.groupby("es_festivo")["sales"]
        .mean()
        .reset_index()
    )

    ventas_festivos["es_festivo"] = ventas_festivos["es_festivo"].map({
        True: "Festivos",
        False: "No festivos"
    })

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            ventas_festivos,
            x="es_festivo",
            y="sales",
            text="sales", # clave
            color_discrete_sequence =["#C77DFF"]
        )

        fig.update_traces(
            texttemplate="<b>%{y:,.0f}</b>",
            textposition="outside"
        )

        fig.update_layout(
            height=450,
            title={
                "text":"<b>Ventas medias días festivos y laborables</b>",
                "x": 0.3
            },
            yaxis=dict(tickformat=","),
            yaxis_title = "Ventas",
            xaxis_title = "Tipo de día"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
   
        df_holiday = df[df["holiday_type"].notnull()]

        
        ventas_por_dia_festivo = (
            df_holiday.groupby("day_of_week")["sales"]
            .mean()
            .reindex(["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
            .reset_index()
        )

        
        fig = px.bar(
            ventas_por_dia_festivo,
            x="day_of_week",
            y="sales",
            text="sales",
            color="sales",
            color_continuous_scale="Tealgrn",
            labels={"day_of_week":"Día de la semana", "sales":"Ventas medias"}
        )

        fig.update_traces(
            texttemplate="%{y:,.0f}",
            textposition="outside"
        )

        fig.update_layout(
            title={
                "text": "<b>Ventas medias en festivos según el día de la semana</b>",
                "x": 0.2
            },
            yaxis=dict(tickformat=","),
            xaxis_tickangle=-45,
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

    
    ventas_dia_festivo = (
        df.groupby(["day_of_week", "holiday_type"])
        .agg(ventas=("sales", "sum"))
        .reset_index()
    )
    orden_dias = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
    ]

    
    fig = px.bar(
        ventas_dia_festivo,
        x="day_of_week",
        y="ventas",
        color="holiday_type",
        barmode="group",
        text="ventas",
        labels={"ventas": "Ventas totales", "day_of_week": "Día de la semana", "holiday_type": "Tipo de festivo"},
        color_discrete_sequence=["#2E8B57","#66CDAA","#A3C586","#4CAF50", "#8FBC8F", "#CFE8D2"],
        category_orders={ "day_of_week": orden_dias}
        )  
    

    
    fig.update_traces(
        texttemplate="%{y:,.0f}".replace(",", " "), 
        textposition="outside"
    )

    fig.update_layout(
        title={
            "text": "<b>Ventas según día de la semana y tipo de festivo</b>",
            "x": 0.4
        },
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)', tickformat=','),
        xaxis=dict(showgrid=False)
    )

   
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(" ")
    st.markdown(" ")
    st.divider()
    
    st.markdown("""
    <div style="
        background-color: white;
        color: black;
        padding:25px;
        border: 8px solid #D32F2F;
        border-radius:6px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.10);
        margin-left: 10%; 
        margin-right: 10%;
    ">
    <h3 style="text-align:center; color: #C21807; margin-bottom: 20px; font-size: 40px">​💰 Conclusión Ventas</h3>
    <ul>
    <li style= "margin-left: 300px">Descenso general de las ventas durante el período analizado.</li>
    <li style= "margin-left: 300px">Alta dependencia de promociones (más del 50% del volumen vendido).</li>
    <li style= "margin-left: 300px">Manabí lidera el crecimiento y desarrollo comercial.</li>
    <li style= "margin-left: 300px">Mejor rendimiento en tiendas tipo A; bajo desempeño en tipo C.</li>
    <li style= "margin-left: 300px;  margin-bottom: 20px">Mayor volumen de ventas en días festivos, especialmente festivos añadidos (Additional).</li>
    <p style= "margin-left: 100px"><b>Implicación:</b> reforzar estrategias promocionales y priorizar inversión en tiendas tipo A y regiones de alto rendimiento.</p>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("© 2025 - Cecilia Díaz Álvaro")





