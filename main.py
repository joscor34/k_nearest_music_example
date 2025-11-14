"""
Sistema de Recomendación Musical usando K-Nearest Neighbors
Visualización 3D Interactiva WEB para Enseñanza

Este programa simula un sistema de recomendación musical tipo Spotify usando KNN.
Las canciones se representan en un espacio 3D según sus características:
- Eje X: Energía (0-100)
- Eje Y: Bailable (0-100)  
- Eje Z: Valencia/Positividad (0-100)
"""

import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, callback
import plotly.express as px
from typing import Dict, List, Tuple
import dash_bootstrap_components as dbc
import dash_daq as daq

class SistemaRecomendacionMusical:
    def __init__(self):
        """Inicializa el sistema con un dataset de canciones ficticias"""
        np.random.seed(42)
        
        # Géneros musicales
        self.generos = ['Pop', 'Rock', 'EDM', 'Jazz', 'Reggaeton', 'Indie', 'Hip Hop', 'Clásica']
        self.colores_generos = {
            'Pop': '#FF1493',
            'Rock': '#FF4500', 
            'EDM': '#00FFFF',
            'Jazz': '#FFD700',
            'Reggaeton': '#FF69B4',
            'Indie': '#9370DB',
            'Hip Hop': '#32CD32',
            'Clásica': '#87CEEB'
        }
        
        # Generar canciones de ejemplo
        self.canciones = self._generar_canciones(100)
        
        # Estado actual
        self.k_actual = 5
        self.punto_consulta = None
        self.vecinos_cercanos = []
        
    def _generar_canciones(self, n_canciones):
        """Genera un dataset de canciones con características según el género"""
        canciones = []
        
        # Características típicas por género (energía, bailabilidad, valencia)
        caracteristicas_genero = {
            'Pop': ([60, 80], [70, 90], [60, 85]),
            'Rock': ([70, 95], [40, 70], [40, 70]),
            'EDM': ([80, 100], [75, 95], [60, 90]),
            'Jazz': ([20, 50], [30, 60], [40, 70]),
            'Reggaeton': ([70, 90], [80, 100], [65, 85]),
            'Indie': ([40, 70], [40, 70], [45, 75]),
            'Hip Hop': ([60, 85], [70, 90], [40, 70]),
            'Clásica': ([20, 40], [10, 30], [50, 80])
        }
        
        for i in range(n_canciones):
            genero = np.random.choice(self.generos)
            rangos = caracteristicas_genero[genero]
            
            cancion = {
                'id': i,
                'nombre': f'{genero} Song {i % 20 + 1}',
                'genero': genero,
                'energia': np.random.uniform(rangos[0][0], rangos[0][1]),
                'bailabilidad': np.random.uniform(rangos[1][0], rangos[1][1]),
                'valencia': np.random.uniform(rangos[2][0], rangos[2][1])
            }
            canciones.append(cancion)
            
        return canciones
    
    def calcular_distancia(self, cancion1, cancion2):
        """Calcula la distancia euclidiana entre dos canciones"""
        caracteristicas1 = np.array([cancion1['energia'], 
                                     cancion1['bailabilidad'], 
                                     cancion1['valencia']])
        caracteristicas2 = np.array([cancion2['energia'], 
                                     cancion2['bailabilidad'], 
                                     cancion2['valencia']])
        return np.linalg.norm(caracteristicas1 - caracteristicas2)
    
    def encontrar_k_vecinos(self, punto_consulta, k):
        """Encuentra los K vecinos más cercanos a un punto de consulta"""
        distancias = []
        
        for cancion in self.canciones:
            dist = self.calcular_distancia(punto_consulta, cancion)
            distancias.append((cancion, dist))
        
        # Ordenar por distancia y tomar los K más cercanos
        distancias.sort(key=lambda x: x[1])
        return distancias[:k]
    
    def recomendar(self, punto_consulta, k):
        """Genera recomendaciones basadas en KNN"""
        vecinos = self.encontrar_k_vecinos(punto_consulta, k)
        
        # Contar géneros entre los vecinos
        conteo_generos = {}
        for cancion, _ in vecinos:
            genero = cancion['genero']
            conteo_generos[genero] = conteo_generos.get(genero, 0) + 1
        
        # Género más común
        genero_recomendado = max(conteo_generos.items(), key=lambda x: x[1])[0]
        
        return vecinos, genero_recomendado, conteo_generos


class AplicacionWebKNN:
    def __init__(self, sistema):
        """Inicializa la aplicación web interactiva"""
        self.sistema = sistema
        self.app = Dash(__name__, 
                       external_stylesheets=[dbc.themes.CYBORG, dbc.icons.FONT_AWESOME],
                       suppress_callback_exceptions=True)
        
        # Generar punto inicial
        self.sistema.punto_consulta = {
            'energia': 50.0,
            'bailabilidad': 50.0,
            'valencia': 50.0
        }
        self.sistema.k_actual = 5
        
        self.configurar_layout()
        self.configurar_callbacks()
        
    def configurar_layout(self):
        """Configura el diseño de la aplicación web con diseño profesional"""
        
        # Estilos personalizados
        CUSTOM_CSS = """
        .main-container {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
            min-height: 100vh;
            font-family: 'Helvetica Neue', Arial, sans-serif;
        }
        .control-card {
            background: linear-gradient(145deg, #1e1e1e 0%, #2d2d2d 100%);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(29, 185, 84, 0.2);
            transition: all 0.3s ease;
        }
        .control-card:hover {
            box-shadow: 0 12px 48px rgba(29, 185, 84, 0.3);
            border-color: rgba(29, 185, 84, 0.4);
        }
        .graph-container {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .info-card {
            background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
            border-radius: 15px;
            border: 1px solid rgba(29, 185, 84, 0.3);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        .slider-container {
            padding: 15px 0;
        }
        .btn-spotify {
            background: linear-gradient(135deg, #1DB954 0%, #1ed760 100%);
            border: none;
            box-shadow: 0 4px 15px rgba(29, 185, 84, 0.4);
            transition: all 0.3s ease;
        }
        .btn-spotify:hover {
            background: linear-gradient(135deg, #1ed760 0%, #1DB954 100%);
            box-shadow: 0 6px 25px rgba(29, 185, 84, 0.6);
            transform: translateY(-2px);
        }
        .metric-card {
            background: rgba(29, 185, 84, 0.1);
            border-left: 4px solid #1DB954;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }
        """
        
        self.app.layout = dbc.Container([
            # CSS personalizado inyectado
            html.Link(
                rel='stylesheet',
                href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
            ),
            
            # Navbar
            dbc.Navbar(
                dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.I(className="fas fa-music fa-2x", 
                                      style={'color': '#1DB954', 'marginRight': '15px'}),
                                html.Span("K-Nearest Neighbors", 
                                         style={'fontSize': '28px', 'fontWeight': 'bold', 
                                               'color': 'white'}),
                            ], style={'display': 'flex', 'alignItems': 'center'})
                        ], width="auto"),
                        dbc.Col([
                            html.Div([
                                html.I(className="fas fa-graduation-cap", 
                                      style={'marginRight': '8px', 'color': '#1DB954'}),
                                html.Span("Sistema de Recomendación Musical", 
                                         style={'color': '#b3b3b3'})
                            ], style={'textAlign': 'right'})
                        ])
                    ], align="center", className="w-100", justify="between")
                ], fluid=True),
                color="dark",
                dark=True,
                className="mb-3",
                style={'boxShadow': '0 4px 20px rgba(0,0,0,0.5)'}
            ),
            
            # Contenido principal
            dbc.Row([
                # Panel de controles izquierdo
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.I(className="fas fa-sliders-h", style={'marginRight': '10px'}),
                            html.Span("Panel de Control", style={'fontSize': '18px', 'fontWeight': 'bold'})
                        ], style={'background': 'linear-gradient(135deg, #1DB954 0%, #17a34a 100%)', 
                                 'color': 'white', 'border': 'none'}),
                        
                        dbc.CardBody([
                            # Control K con indicador digital
                            html.Div([
                                dbc.Label([
                                    html.I(className="fas fa-users", style={'marginRight': '8px'}),
                                    "Número de Vecinos (K)"
                                ], style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#1DB954'}),
                                
                                dbc.Row([
                                    dbc.Col([
                                        daq.LEDDisplay(
                                            id='k-display',
                                            value=5,
                                            color="#1DB954",
                                            backgroundColor="#1e1e1e",
                                            size=50,
                                            style={'margin': '10px auto'}
                                        )
                                    ], width=12, className="text-center"),
                                ]),
                                
                                dcc.Slider(
                                    id='k-slider',
                                    min=1,
                                    max=30,
                                    step=1,
                                    value=5,
                                    marks={i: {'label': str(i), 'style': {'color': '#1DB954', 'fontWeight': 'bold'}} 
                                          for i in [1, 5, 10, 15, 20, 25, 30]},
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    className="mb-3"
                                ),
                            ], className="slider-container"),
                            
                            html.Hr(style={'borderColor': 'rgba(29, 185, 84, 0.3)', 'margin': '25px 0'}),
                            
                            # Título para características
                            html.Div([
                                html.I(className="fas fa-music", style={'marginRight': '8px', 'color': '#1DB954'}),
                                html.Span("Características Musicales", 
                                         style={'fontSize': '16px', 'fontWeight': 'bold', 'color': 'white'})
                            ], className="mb-3"),
                            
                            # Energía con gauge
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.I(className="fas fa-bolt", 
                                              style={'color': '#FF6B6B', 'fontSize': '20px'}),
                                        dbc.Label(" Energía", style={'color': 'white', 'fontWeight': 'bold', 
                                                                    'marginLeft': '8px'})
                                    ], width=6),
                                    dbc.Col([
                                        dbc.Badge(id='energia-badge', color="danger", className="float-end",
                                                 style={'fontSize': '14px'})
                                    ], width=6)
                                ], className="mb-2"),
                                dcc.Slider(
                                    id='energia-slider',
                                    min=0,
                                    max=100,
                                    step=1,
                                    value=50,
                                    marks={i: {'label': str(i), 'style': {'color': '#FF6B6B'}} 
                                          for i in [0, 50, 100]},
                                    tooltip={"placement": "bottom", "always_visible": True}
                                ),
                            ], className="slider-container"),
                            
                            # Bailabilidad con gauge
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.I(className="fas fa-walking", 
                                              style={'color': '#4ECDC4', 'fontSize': '20px'}),
                                        dbc.Label(" Bailabilidad", style={'color': 'white', 'fontWeight': 'bold',
                                                                         'marginLeft': '8px'})
                                    ], width=6),
                                    dbc.Col([
                                        dbc.Badge(id='bailabilidad-badge', color="info", className="float-end",
                                                 style={'fontSize': '14px'})
                                    ], width=6)
                                ], className="mb-2"),
                                dcc.Slider(
                                    id='bailabilidad-slider',
                                    min=0,
                                    max=100,
                                    step=1,
                                    value=50,
                                    marks={i: {'label': str(i), 'style': {'color': '#4ECDC4'}} 
                                          for i in [0, 50, 100]},
                                    tooltip={"placement": "bottom", "always_visible": True}
                                ),
                            ], className="slider-container"),
                            
                            # Valencia con gauge
                            html.Div([
                                dbc.Row([
                                    dbc.Col([
                                        html.I(className="fas fa-smile", 
                                              style={'color': '#FFE66D', 'fontSize': '20px'}),
                                        dbc.Label(" Valencia", style={'color': 'white', 'fontWeight': 'bold',
                                                                     'marginLeft': '8px'})
                                    ], width=6),
                                    dbc.Col([
                                        dbc.Badge(id='valencia-badge', color="warning", className="float-end",
                                                 style={'fontSize': '14px'})
                                    ], width=6)
                                ], className="mb-2"),
                                dcc.Slider(
                                    id='valencia-slider',
                                    min=0,
                                    max=100,
                                    step=1,
                                    value=50,
                                    marks={i: {'label': str(i), 'style': {'color': '#FFE66D'}} 
                                          for i in [0, 50, 100]},
                                    tooltip={"placement": "bottom", "always_visible": True}
                                ),
                            ], className="slider-container"),
                            
                            html.Hr(style={'borderColor': 'rgba(29, 185, 84, 0.3)', 'margin': '25px 0'}),
                            
                            # Botones de acción
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button([
                                        html.I(className="fas fa-random", style={'marginRight': '10px'}),
                                        "Generar Aleatorio"
                                    ], id='random-button', n_clicks=0, className="btn-spotify w-100 mb-3",
                                    size="lg", style={'borderRadius': '25px', 'fontWeight': 'bold'})
                                ], width=12),
                                dbc.Col([
                                    dbc.Button([
                                        html.I(className="fas fa-redo", style={'marginRight': '10px'}),
                                        "Reiniciar"
                                    ], id='reset-button', n_clicks=0, color="secondary", 
                                    className="w-100", size="lg", style={'borderRadius': '25px'})
                                ], width=12),
                            ]),
                        ], className="control-card", style={'padding': '30px'})
                    ], className="control-card", style={'border': 'none', 'boxShadow': 'none'})
                ], md=4, lg=3),
                
                # Gráfico 3D principal
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Loading(
                                id="loading-graph",
                                type="default",
                                color="#1DB954",
                                children=[
                                    dcc.Graph(
                                        id='grafico-3d',
                                        style={'height': '75vh'},
                                        config={
                                            'displayModeBar': True, 
                                            'displaylogo': False,
                                            'modeBarButtonsToRemove': ['pan3d', 'select3d', 'lasso3d']
                                        }
                                    )
                                ]
                            )
                        ], style={'padding': '10px'})
                    ], className="graph-container", style={'border': 'none'})
                ], md=8, lg=6),
                
                # Panel de información derecho
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.I(className="fas fa-info-circle", style={'marginRight': '10px'}),
                            html.Span("Análisis y Recomendación", 
                                     style={'fontSize': '18px', 'fontWeight': 'bold'})
                        ], style={'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
                                 'color': 'white', 'border': 'none'}),
                        
                        dbc.CardBody([
                            html.Div(id='info-panel')
                        ], className="info-card", style={'maxHeight': '75vh', 'overflowY': 'auto',
                                                        'padding': '20px'})
                    ], className="control-card", style={'border': 'none', 'boxShadow': 'none'})
                ], md=12, lg=3),
            ], className="g-3"),
            
            # Store para valores aleatorios
            dcc.Store(id='random-values'),
            
        ], fluid=True, className="main-container", style={'padding': '20px'})
    
    def crear_grafico_3d(self, k, energia, bailabilidad, valencia):
        """Crea el gráfico 3D con Plotly"""
        # Actualizar punto de consulta
        self.sistema.punto_consulta = {
            'energia': energia,
            'bailabilidad': bailabilidad,
            'valencia': valencia
        }
        self.sistema.k_actual = k
        
        # Crear figura
        fig = go.Figure()
        
        # Agrupar canciones por género
        for genero in self.sistema.generos:
            canciones_genero = [c for c in self.sistema.canciones if c['genero'] == genero]
            if canciones_genero:
                energias = [c['energia'] for c in canciones_genero]
                bailabilidades = [c['bailabilidad'] for c in canciones_genero]
                valencias = [c['valencia'] for c in canciones_genero]
                nombres = [c['nombre'] for c in canciones_genero]
                
                fig.add_trace(go.Scatter3d(
                    x=energias,
                    y=bailabilidades,
                    z=valencias,
                    mode='markers',
                    name=genero,
                    marker=dict(
                        size=8,
                        color=self.sistema.colores_generos[genero],
                        opacity=0.7,
                        line=dict(color='white', width=0.5)
                    ),
                    text=nombres,
                    hovertemplate='<b>%{text}</b><br>' +
                                 'Energía: %{x:.1f}<br>' +
                                 'Bailabilidad: %{y:.1f}<br>' +
                                 'Valencia: %{z:.1f}<br>' +
                                 f'<b>{genero}</b><extra></extra>'
                ))
        
        # Encontrar vecinos
        vecinos, genero_rec, conteo = self.sistema.recomendar(
            self.sistema.punto_consulta, k)
        
        # Agregar líneas a vecinos
        for cancion, distancia in vecinos:
            fig.add_trace(go.Scatter3d(
                x=[energia, cancion['energia']],
                y=[bailabilidad, cancion['bailabilidad']],
                z=[valencia, cancion['valencia']],
                mode='lines',
                line=dict(color='yellow', width=2, dash='dot'),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Resaltar vecinos
        for cancion, distancia in vecinos:
            fig.add_trace(go.Scatter3d(
                x=[cancion['energia']],
                y=[cancion['bailabilidad']],
                z=[cancion['valencia']],
                mode='markers',
                name='Vecino cercano',
                marker=dict(
                    size=12,
                    color=self.sistema.colores_generos[cancion['genero']],
                    line=dict(color='yellow', width=3)
                ),
                text=cancion['nombre'],
                showlegend=False,
                hovertemplate=f'<b>VECINO: {cancion["nombre"]}</b><br>' +
                             f'Distancia: {distancia:.2f}<br>' +
                             'Energía: %{x:.1f}<br>' +
                             'Bailabilidad: %{y:.1f}<br>' +
                             'Valencia: %{z:.1f}<extra></extra>'
            ))
        
        # Agregar punto de consulta (estrella)
        fig.add_trace(go.Scatter3d(
            x=[energia],
            y=[bailabilidad],
            z=[valencia],
            mode='markers',
            name='⭐ Tu Música',
            marker=dict(
                size=20,
                color='yellow',
                symbol='diamond',
                line=dict(color='white', width=3)
            ),
            hovertemplate='<b>⭐ TU PREFERENCIA</b><br>' +
                         'Energía: %{x:.1f}<br>' +
                         'Bailabilidad: %{y:.1f}<br>' +
                         'Valencia: %{z:.1f}<extra></extra>'
        ))
        
        # Agregar esfera de alcance
        if vecinos:
            max_dist = vecinos[-1][1]
            u = np.linspace(0, 2 * np.pi, 30)
            v = np.linspace(0, np.pi, 20)
            x = max_dist * np.outer(np.cos(u), np.sin(v)) + energia
            y = max_dist * np.outer(np.sin(u), np.sin(v)) + bailabilidad
            z = max_dist * np.outer(np.ones(np.size(u)), np.cos(v)) + valencia
            
            fig.add_trace(go.Surface(
                x=x, y=y, z=z,
                opacity=0.15,
                colorscale=[[0, 'yellow'], [1, 'yellow']],
                showscale=False,
                name='Radio de búsqueda',
                hoverinfo='skip'
            ))
        
        # Configurar layout con diseño premium
        fig.update_layout(
            scene=dict(
                xaxis=dict(
                    title=dict(text='⚡ Energía', font=dict(size=14, color='#FF6B6B', family='Arial Black')),
                    range=[0, 100], 
                    backgroundcolor="rgba(10, 14, 39, 0.8)",
                    gridcolor="rgba(29, 185, 84, 0.2)", 
                    showbackground=True,
                    gridwidth=2
                ),
                yaxis=dict(
                    title=dict(text='💃 Bailabilidad', font=dict(size=14, color='#4ECDC4', family='Arial Black')),
                    range=[0, 100], 
                    backgroundcolor="rgba(10, 14, 39, 0.8)",
                    gridcolor="rgba(29, 185, 84, 0.2)", 
                    showbackground=True,
                    gridwidth=2
                ),
                zaxis=dict(
                    title=dict(text='😊 Valencia', font=dict(size=14, color='#FFE66D', family='Arial Black')),
                    range=[0, 100], 
                    backgroundcolor="rgba(10, 14, 39, 0.8)",
                    gridcolor="rgba(29, 185, 84, 0.2)", 
                    showbackground=True,
                    gridwidth=2
                ),
                bgcolor="rgba(10, 14, 39, 0.5)",
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.3),
                    center=dict(x=0, y=0, z=0)
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', family='Helvetica Neue'),
            margin=dict(l=0, r=0, t=60, b=0),
            title=dict(
                text=f'<b>K = {k} vecinos</b> | Recomendación: <b style="color:{self.sistema.colores_generos[genero_rec]}">{genero_rec}</b>',
                x=0.5,
                xanchor='center',
                font=dict(size=18, color='white', family='Arial Black'),
                pad=dict(t=10)
            ),
            legend=dict(
                bgcolor='rgba(30, 30, 30, 0.9)',
                bordercolor='#1DB954',
                borderwidth=2,
                font=dict(size=11, family='Helvetica Neue'),
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                itemsizing='constant'
            ),
            hovermode='closest',
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.8)",
                font_size=13,
                font_family="Helvetica Neue",
                bordercolor='#1DB954'
            )
        )
        
        return fig, vecinos, genero_rec, conteo
    
    def crear_panel_info(self, vecinos, genero_rec, conteo, k):
        """Crea el panel de información con diseño moderno"""
        if not vecinos:
            return dbc.Alert([
                html.I(className="fas fa-info-circle fa-2x mb-3"),
                html.H5("Ajusta los controles"),
                html.P("Usa los sliders para configurar tus preferencias musicales")
            ], color="info", className="text-center")
        
        # Género recomendado - Card destacado
        genero_card = dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.I(className="fas fa-trophy fa-3x mb-3", 
                          style={'color': self.sistema.colores_generos[genero_rec]}),
                    html.H3("Género Recomendado", 
                           style={'color': '#b3b3b3', 'fontSize': '14px', 'textTransform': 'uppercase',
                                 'letterSpacing': '2px', 'marginBottom': '10px'}),
                    html.H2(genero_rec, 
                           style={'color': self.sistema.colores_generos[genero_rec], 
                                 'fontWeight': 'bold', 'fontSize': '32px', 'marginBottom': '10px'}),
                    dbc.Badge(f"Basado en {k} vecinos", 
                             color="success", className="mt-2", 
                             style={'fontSize': '12px'})
                ], className="text-center")
            ], style={'background': 'linear-gradient(135deg, rgba(29, 185, 84, 0.1) 0%, rgba(29, 185, 84, 0.05) 100%)',
                     'borderRadius': '15px', 'padding': '20px'})
        ], className="mb-4", style={'border': f'2px solid {self.sistema.colores_generos[genero_rec]}',
                                    'boxShadow': f'0 4px 20px {self.sistema.colores_generos[genero_rec]}40'})
        
        # Distribución de géneros - Con progress bars modernos
        distribucion_cards = []
        for genero, cantidad in sorted(conteo.items(), key=lambda x: x[1], reverse=True):
            porcentaje = (cantidad / k) * 100
            distribucion_cards.append(
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.Span(genero, 
                                             style={'fontWeight': 'bold', 'fontSize': '14px',
                                                   'color': self.sistema.colores_generos[genero]}),
                                    html.Br(),
                                    html.Small(f"{cantidad} canciones", 
                                              style={'color': '#888', 'fontSize': '11px'})
                                ])
                            ], width=5),
                            dbc.Col([
                                dbc.Progress(
                                    value=porcentaje,
                                    color="success",
                                    style={'height': '25px', 'backgroundColor': 'rgba(255,255,255,0.1)'},
                                    className="mb-0"
                                ),
                            ], width=5),
                            dbc.Col([
                                html.Div(f"{porcentaje:.0f}%", 
                                        style={'fontWeight': 'bold', 'fontSize': '16px',
                                              'color': self.sistema.colores_generos[genero]})
                            ], width=2, className="text-end")
                        ], align="center")
                    ], style={'padding': '10px'})
                ], className="mb-2", 
                style={'background': f'linear-gradient(90deg, {self.sistema.colores_generos[genero]}15 0%, transparent 100%)',
                      'border': 'none', 'borderLeft': f'3px solid {self.sistema.colores_generos[genero]}'})
            )
        
        distribucion_section = html.Div([
            html.H5([
                html.I(className="fas fa-chart-pie", style={'marginRight': '10px', 'color': '#1DB954'}),
                "Distribución de Géneros"
            ], style={'color': 'white', 'marginBottom': '15px', 'fontWeight': 'bold'}),
            html.Div(distribucion_cards)
        ], className="mb-4")
        
        # Top vecinos - Lista con cards
        vecinos_cards = []
        for i, (cancion, distancia) in enumerate(vecinos[:5]):
            vecinos_cards.append(
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.I(className="fas fa-music", 
                                          style={'color': self.sistema.colores_generos[cancion['genero']],
                                                'marginRight': '10px', 'fontSize': '20px'}),
                                    html.Span(f"#{i+1}", 
                                             style={'fontSize': '20px', 'fontWeight': 'bold',
                                                   'color': '#666', 'marginRight': '10px'})
                                ], style={'display': 'inline-flex', 'alignItems': 'center'})
                            ], width=2),
                            dbc.Col([
                                html.Div([
                                    html.Div(cancion['nombre'], 
                                            style={'fontWeight': 'bold', 'color': 'white',
                                                  'fontSize': '14px'}),
                                    html.Small(cancion['genero'], 
                                              style={'color': self.sistema.colores_generos[cancion['genero']],
                                                    'fontSize': '11px'})
                                ])
                            ], width=7),
                            dbc.Col([
                                dbc.Badge([
                                    html.I(className="fas fa-ruler", 
                                          style={'marginRight': '5px', 'fontSize': '10px'}),
                                    f"{distancia:.1f}"
                                ], color="dark", style={'fontSize': '12px'})
                            ], width=3, className="text-end")
                        ], align="center")
                    ], style={'padding': '12px'})
                ], className="mb-2 vecino-card", 
                style={'background': 'rgba(255,255,255,0.05)', 'border': 'none',
                      'borderLeft': f'4px solid {self.sistema.colores_generos[cancion["genero"]]}',
                      'transition': 'all 0.3s ease'})
            )
        
        vecinos_section = html.Div([
            html.H5([
                html.I(className="fas fa-star", style={'marginRight': '10px', 'color': '#FFD700'}),
                f"Top {min(5, len(vecinos))} Vecinos Cercanos"
            ], style={'color': 'white', 'marginBottom': '15px', 'fontWeight': 'bold'}),
            html.Div(vecinos_cards)
        ], className="mb-4")
        
        # Información del algoritmo - Accordion
        algoritmo_info = dbc.Accordion([
            dbc.AccordionItem([
                html.P([
                    html.I(className="fas fa-star", style={'color': '#FFD700', 'marginRight': '8px'}),
                    "El punto amarillo (estrella) representa tus preferencias musicales en el espacio 3D"
                ], style={'marginBottom': '10px', 'color': '#ccc'}),
                html.P([
                    html.I(className="fas fa-search", style={'color': '#4ECDC4', 'marginRight': '8px'}),
                    "El algoritmo calcula la distancia euclidiana a todas las canciones"
                ], style={'marginBottom': '10px', 'color': '#ccc'}),
                html.P([
                    html.I(className="fas fa-circle", style={'color': '#FFE66D', 'marginRight': '8px'}),
                    "La esfera amarilla muestra el radio hasta el K-ésimo vecino más cercano"
                ], style={'marginBottom': '10px', 'color': '#ccc'}),
                html.P([
                    html.I(className="fas fa-link", style={'color': '#FF6B6B', 'marginRight': '8px'}),
                    "Las líneas conectan tu punto con los K vecinos seleccionados"
                ], style={'marginBottom': '10px', 'color': '#ccc'}),
                html.P([
                    html.I(className="fas fa-trophy", style={'color': '#1DB954', 'marginRight': '8px'}),
                    "El género más frecuente entre los vecinos es la recomendación final"
                ], style={'marginBottom': '0', 'color': '#ccc'})
            ], title="💡 ¿Cómo funciona el algoritmo?", item_id="item-1")
        ], start_collapsed=False, flush=True, 
        style={'background': 'transparent'})
        
        # Ensamblar todo
        return html.Div([
            genero_card,
            distribucion_section,
            vecinos_section,
            algoritmo_info
        ])
    
    def configurar_callbacks(self):
        """Configura los callbacks de la aplicación"""
        @self.app.callback(
            [Output('grafico-3d', 'figure'),
             Output('info-panel', 'children'),
             Output('k-display', 'value')],
            [Input('k-slider', 'value'),
             Input('energia-slider', 'value'),
             Input('bailabilidad-slider', 'value'),
             Input('valencia-slider', 'value'),
             Input('random-values', 'data')]
        )
        def actualizar_visualizacion(k, energia, bailabilidad, valencia, random_data):
            # Si hay valores aleatorios, usarlos
            if random_data:
                energia = random_data['energia']
                bailabilidad = random_data['bailabilidad']
                valencia = random_data['valencia']
            
            fig, vecinos, genero_rec, conteo = self.crear_grafico_3d(
                k, energia, bailabilidad, valencia)
            panel = self.crear_panel_info(vecinos, genero_rec, conteo, k)
            
            return fig, panel, k
        
        @self.app.callback(
            [Output('energia-badge', 'children'),
             Output('bailabilidad-badge', 'children'),
             Output('valencia-badge', 'children')],
            [Input('energia-slider', 'value'),
             Input('bailabilidad-slider', 'value'),
             Input('valencia-slider', 'value')]
        )
        def actualizar_badges(energia, bailabilidad, valencia):
            return f"{energia:.0f}%", f"{bailabilidad:.0f}%", f"{valencia:.0f}%"
        
        @self.app.callback(
            [Output('random-values', 'data'),
             Output('energia-slider', 'value'),
             Output('bailabilidad-slider', 'value'),
             Output('valencia-slider', 'value')],
            [Input('random-button', 'n_clicks'),
             Input('reset-button', 'n_clicks')],
            prevent_initial_call=True
        )
        def generar_aleatorio_o_reset(random_clicks, reset_clicks):
            from dash import callback_context
            
            if not callback_context.triggered:
                return None, 50, 50, 50
            
            button_id = callback_context.triggered[0]['prop_id'].split('.')[0]
            
            if button_id == 'reset-button':
                return None, 50, 50, 50
            else:  # random-button
                energia = float(np.random.uniform(10, 90))
                bailabilidad = float(np.random.uniform(10, 90))
                valencia = float(np.random.uniform(10, 90))
                
                return (
                    {'energia': energia, 'bailabilidad': bailabilidad, 'valencia': valencia},
                    energia,
                    bailabilidad,
                    valencia
                )
    
    def ejecutar(self, debug=True, port=8050):
        """Ejecuta la aplicación web"""
        print("\n" + "="*70)
        print("  🎵 SISTEMA DE RECOMENDACIÓN MUSICAL - K-NEAREST NEIGHBORS")
        print("="*70)
        print(f"\n✓ {len(self.sistema.canciones)} canciones cargadas")
        print(f"✓ {len(self.sistema.generos)} géneros disponibles")
        print(f"\n🌐 Servidor web iniciado en: http://localhost:{port}")
        print("\n🎮 CONTROLES INTERACTIVOS:")
        print("  • Usa los sliders para ajustar K y las características")
        print("  • Click en 'Nueva Consulta Aleatoria' para generar nuevos gustos")
        print("  • Arrastra el gráfico 3D para rotar la vista")
        print("  • Haz zoom con scroll o pinch")
        print("  • Pasa el cursor sobre puntos para ver detalles")
        print("\n" + "="*70 + "\n")
        
        self.app.run(debug=debug, port=port)


def main():
    """Función principal"""
    # Crear sistema de recomendación
    sistema = SistemaRecomendacionMusical()
    
    # Crear y ejecutar aplicación web
    app_web = AplicacionWebKNN(sistema)
    app_web.ejecutar(debug=True, port=8050)


if __name__ == "__main__":
    main()
