# 🎵 Sistema de Recomendación Musical con K-Nearest Neighbors

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Dash](https://img.shields.io/badge/Dash-2.0+-green.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Una aplicación web interactiva en 3D que visualiza el algoritmo **K-Nearest Neighbors (KNN)** aplicado a un sistema de recomendación musical.

## ✨ Características

### 🎨 Interfaz Premium
- **Diseño moderno** inspirado en Spotify con tema oscuro
- **Visualización 3D interactiva** con Plotly
- **Panel de control completo** con sliders y controles en tiempo real
- **Indicadores LED** para visualización de valores
- **Animaciones suaves** y efectos hover
- **Responsive design** que se adapta a cualquier pantalla

### 🎯 Funcionalidades KNN
- **Ajuste dinámico de K** (1-30 vecinos)
- **Control de características musicales**:
  - ⚡ Energía (0-100)
  - 💃 Bailabilidad (0-100)
  - 😊 Valencia/Positividad (0-100)
- **Generación aleatoria** de puntos de consulta
- **Visualización de vecinos** cercanos en 3D
- **Esfera de alcance** que muestra el radio de búsqueda
- **Recomendación automática** basada en géneros

### 📊 Visualización Educativa
- **100 canciones** distribuidas en 8 géneros musicales
- **Códigos de color** por género
- **Líneas de conexión** entre punto de consulta y vecinos
- **Tooltips informativos** con detalles de cada canción
- **Panel de análisis** con métricas y estadísticas
- **Explicación interactiva** del algoritmo

## 🎬 Demo Visual

### Panel Principal
La aplicación muestra:
- **Gráfico 3D rotable** con todas las canciones coloreadas por género
- **Punto de consulta** (estrella amarilla) representando tus gustos
- **K vecinos cercanos** resaltados con bordes amarillos
- **Esfera semitransparente** mostrando el radio de búsqueda

### Panel de Control
- Slider para ajustar K con display LED
- Sliders para cada característica musical con badges de valor
- Botón para generar consultas aleatorias
- Botón de reinicio

### Panel de Información
- Card destacado con el género recomendado
- Gráfico de distribución de géneros entre vecinos
- Lista de top 5 vecinos más cercanos
- Explicación desplegable del algoritmo

## 🚀 Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el repositorio**
```bash
git clone <tu-repositorio>
cd k_nearest
```

2. **Crear un entorno virtual** (recomendado)
```bash
python -m venv .venv
source .venv/bin/activate  # En macOS/Linux
# o
.venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias**
```bash
pip install numpy plotly dash dash-bootstrap-components dash-daq
```

### Instalación Rápida
```bash
# Todo en un comando
python -m venv .venv && source .venv/bin/activate && pip install numpy plotly dash dash-bootstrap-components dash-daq
```

## 💻 Uso

### Iniciar la Aplicación

```bash
python main.py
```

La aplicación se iniciará en `http://localhost:8050`

### Controles Interactivos

#### 🎚️ Slider de K
- Ajusta el número de vecinos cercanos (1-30)
- Observa cómo cambia la recomendación en tiempo real
- El display LED muestra el valor actual

#### 🎸 Características Musicales
- **Energía**: Nivel de intensidad y actividad
- **Bailabilidad**: Qué tan apto es para bailar
- **Valencia**: Positividad musical (feliz vs triste)
- Cada slider muestra el valor actual en un badge

#### 🎲 Botones de Acción
- **Generar Aleatorio**: Crea un nuevo punto de consulta aleatorio
- **Reiniciar**: Vuelve a valores por defecto (50, 50, 50, K=5)

#### 🖱️ Interacción con el Gráfico 3D
- **Arrastrar**: Rotar la visualización
- **Scroll**: Hacer zoom in/out
- **Hover**: Ver detalles de cada canción
- **Click en leyenda**: Ocultar/mostrar géneros

## 🧠 Cómo Funciona

### El Algoritmo K-Nearest Neighbors

1. **Representación en 3D**: Cada canción es un punto en el espacio 3D donde:
   - Eje X = Energía
   - Eje Y = Bailabilidad
   - Eje Z = Valencia

2. **Cálculo de Distancia**: Se usa la distancia euclidiana:
   ```
   d = √[(x₁-x₂)² + (y₁-y₂)² + (z₁-z₂)²]
   ```

3. **Búsqueda de Vecinos**: 
   - Se calculan distancias a todas las canciones
   - Se seleccionan las K canciones más cercanas

4. **Clasificación/Recomendación**:
   - Se cuentan los géneros entre los K vecinos
   - El género más frecuente es la recomendación

### Géneros Musicales

| Género | Color | Características Típicas |
|--------|-------|------------------------|
| 🎵 Pop | Rosa (#FF1493) | Alta energía, muy bailable, positivo |
| 🎸 Rock | Naranja (#FF4500) | Muy alta energía, medianamente bailable |
| 🎧 EDM | Cyan (#00FFFF) | Máxima energía y bailabilidad |
| 🎺 Jazz | Dorado (#FFD700) | Baja energía, relajado |
| 💃 Reggaeton | Rosa claro (#FF69B4) | Alta energía, muy bailable |
| 🎹 Indie | Púrpura (#9370DB) | Energía y bailabilidad media |
| 🎤 Hip Hop | Verde (#32CD32) | Alta energía y bailabilidad |
| 🎻 Clásica | Azul claro (#87CEEB) | Muy baja energía, poco bailable |

## 🛠️ Tecnologías

### Core
- **Python 3.8+**: Lenguaje principal
- **NumPy**: Cálculos matemáticos y álgebra lineal
- **Plotly**: Visualización 3D interactiva

### Framework Web
- **Dash**: Framework web de Python
- **Dash Bootstrap Components**: Componentes UI modernos
- **Dash DAQ**: Componentes de instrumentación (LED Display)

### Estilos y Diseño
- **Bootstrap Cyborg Theme**: Tema oscuro profesional
- **Font Awesome 6**: Iconos vectoriales
- **CSS3**: Gradientes, animaciones y efectos

## 🎓 Casos de Uso Educativos

1. **Experimentación Práctica**
   - Ajusta K y observa cómo cambia la recomendación
   - Prueba diferentes combinaciones de características
   - Compara resultados con diferentes géneros

2. **Comprensión Visual**
   - Ve cómo se agrupan canciones similares
   - Entiende el concepto de "espacio de características"
   - Observa el efecto del parámetro K

3. **Proyecto Base**
   - Úsalo como punto de partida para proyectos
   - Modifica géneros o características
   - Agrega más dimensiones o funcionalidades

## 🎨 Personalización

### Agregar Nuevos Géneros

```python
# En la clase SistemaRecomendacionMusical.__init__()
self.generos = ['Pop', 'Rock', 'EDM', 'Jazz', 'TuGenero']
self.colores_generos['TuGenero'] = '#TuColor'

# En _generar_canciones()
caracteristicas_genero = {
    'TuGenero': ([energia_min, energia_max], 
                 [bailabilidad_min, bailabilidad_max], 
                 [valencia_min, valencia_max])
}
```

### Modificar Número de Canciones

```python
# En main()
sistema = SistemaRecomendacionMusical()
# Modifica en _generar_canciones(n_canciones)
self.canciones = self._generar_canciones(200)  # Por defecto: 100
```

### Cambiar Puerto del Servidor

```python
# En main()
app_web.ejecutar(debug=True, port=8080)  # Por defecto: 8050
```

### Personalizar Características

Modifica las características musicales por otras:
- Tempo (BPM)
- Acousticness
- Instrumentalness
- Speechiness

## 👨‍💻 Autor

Creado con ❤️ para fines educativos

## 🔗 Links Útiles

- [Documentación de Dash](https://dash.plotly.com/)
- [Plotly Python](https://plotly.com/python/)
- [K-Nearest Neighbors en Scikit-Learn](https://scikit-learn.org/stable/modules/neighbors.html)
- [Spotify API](https://developer.spotify.com/documentation/web-api/)

---

**¡Happy Learning! 🎓🎵**
