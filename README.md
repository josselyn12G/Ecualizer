# Ecualizer

## Descripción del Proyecto

**Ecualizer** es una aplicación web orientada a la gestión de una plataforma musical digital inspirada en servicios como Spotify. El sistema permite administrar información relacionada con usuarios, artistas, canciones, álbumes, playlists, pagos, suscripciones, reproducciones, regalías, discográficas, contratos y reportes principales.

El proyecto se desarrolla como parte de la **Fase 7 del Proyecto Integrador**, cuyo objetivo es implementar una interfaz web conectada a una base de datos **MongoDB**, utilizando tecnologías web y una estructura organizada bajo el patrón arquitectónico **MVC: Modelo, Vista y Controlador**. El entregable debe incluir el código fuente de la aplicación, plantillas HTML, archivos CSS y JavaScript, conexión con MongoDB, manual de usuario, evidencias de funcionamiento y un video explicativo de una operación CRUD. :contentReference[oaicite:0]{index=0}

---

## Objetivo General

Desarrollar una aplicación web para el sistema **Ecualizer**, aplicando el patrón de arquitectura MVC, con el propósito de gestionar los principales procesos de una plataforma musical mediante una interfaz web conectada a una base de datos MongoDB.

---

## Objetivos Específicos

- Implementar una aplicación web utilizando Python y Flask.
- Conectar la aplicación con una base de datos MongoDB mediante PyMongo.
- Organizar el proyecto utilizando el patrón MVC.
- Crear vistas HTML para la interacción del usuario con el sistema.
- Implementar operaciones CRUD para al menos una entidad principal del sistema.
- Gestionar módulos relacionados con usuarios, catálogo musical, biblioteca, pagos, analítica e industria musical.
- Documentar la estructura, instalación, ejecución y funcionamiento del proyecto.
- Evidenciar el funcionamiento de la aplicación mediante capturas y un video explicativo.

---

## Tecnologías Utilizadas

| Tecnología | Descripción |
|---|---|
| Python | Lenguaje de programación principal utilizado para desarrollar el backend. |
| Flask | Framework web utilizado para construir la aplicación. |
| MongoDB | Base de datos NoSQL utilizada para almacenar la información del sistema. |
| PyMongo | Librería que permite conectar Python con MongoDB. |
| HTML5 | Lenguaje de marcado utilizado para estructurar las páginas web. |
| CSS3 | Tecnología utilizada para aplicar estilos a la interfaz. |
| JavaScript | Lenguaje utilizado para agregar interactividad en el frontend. |
| Jinja2 | Motor de plantillas utilizado por Flask para renderizar vistas HTML. |
| Git | Sistema de control de versiones del proyecto. |
| GitHub | Plataforma para alojar el repositorio del código fuente. |

---

## Arquitectura del Proyecto

El proyecto utiliza el patrón arquitectónico **MVC**, el cual permite separar la aplicación en capas para facilitar su organización, mantenimiento y escalabilidad.

MVC significa:

- **Modelo**
- **Vista**
- **Controlador**

---

## Modelo

La capa de modelo se encarga de representar las entidades del sistema y manejar la comunicación con la base de datos MongoDB.

En esta capa se implementan las operaciones relacionadas con inserción, consulta, actualización y eliminación de datos.

Ejemplos de archivos de modelo:

```text
app/models/cancion_model.py
app/models/usuario_model.py
app/models/playlist_model.py
app/models/pago_model.py
app/models/reproduccion_model.py
```

---

## Vista

La capa de vista contiene las páginas HTML que permiten al usuario interactuar con el sistema.

Estas vistas muestran formularios, tablas, reportes y páginas principales de navegación.

Ejemplos de archivos de vista:

```text
app/views/index.html
app/views/catalogo/listar_canciones.html
app/views/catalogo/crear_cancion.html
app/views/usuarios/crear.html
app/views/reportes/reporte_reproducciones.html
```

---

## Controlador

La capa de controlador contiene la lógica del sistema.

Su función principal es recibir las solicitudes del usuario, comunicarse con los modelos, procesar la información y devolver la vista correspondiente.

Ejemplos de archivos de controlador:

```text
app/controllers/catalogo_controller.py
app/controllers/usuario_controller.py
app/controllers/biblioteca_controller.py
app/controllers/pago_controller.py
app/controllers/reporte_controller.py
```

---

## Rutas

Las rutas definen las URL disponibles en la aplicación web.

Cada archivo de rutas permite organizar los accesos a los módulos del sistema.

Ejemplos de archivos de rutas:

```text
app/routes/catalogo_routes.py
app/routes/usuario_routes.py
app/routes/biblioteca_routes.py
app/routes/pago_routes.py
app/routes/reporte_routes.py
```

---

## Estructura del Proyecto

```text
Ecualizer/
│
├── app/
│   ├── models/
│   │   ├── usuario_model.py
│   │   ├── persona_model.py
│   │   ├── administrador_model.py
│   │   ├── artista_model.py
│   │   ├── cancion_model.py
│   │   ├── album_model.py
│   │   ├── genero_model.py
│   │   ├── tipo_album_model.py
│   │   ├── playlist_model.py
│   │   ├── biblioteca_model.py
│   │   ├── like_model.py
│   │   ├── seguimiento_model.py
│   │   ├── pago_model.py
│   │   ├── suscripcion_model.py
│   │   ├── tipo_plan_model.py
│   │   ├── reproduccion_model.py
│   │   ├── regalia_model.py
│   │   ├── discografica_model.py
│   │   └── contrato_discografica_model.py
│   │
│   ├── views/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── usuarios/
│   │   │   ├── listar.html
│   │   │   ├── crear.html
│   │   │   ├── editar.html
│   │   │   └── detalle.html
│   │   ├── catalogo/
│   │   │   ├── listar_canciones.html
│   │   │   ├── crear_cancion.html
│   │   │   ├── editar_cancion.html
│   │   │   ├── listar_albumes.html
│   │   │   ├── crear_album.html
│   │   │   ├── listar_artistas.html
│   │   │   └── listar_generos.html
│   │   ├── biblioteca/
│   │   │   ├── listar_playlists.html
│   │   │   ├── crear_playlist.html
│   │   │   ├── editar_playlist.html
│   │   │   ├── favoritos.html
│   │   │   └── likes.html
│   │   ├── pagos/
│   │   │   ├── listar_pagos.html
│   │   │   ├── crear_pago.html
│   │   │   ├── suscripciones.html
│   │   │   └── planes.html
│   │   ├── analitica/
│   │   │   ├── reproducciones.html
│   │   │   ├── regalias.html
│   │   │   └── dashboard.html
│   │   ├── industria/
│   │   │   ├── discograficas.html
│   │   │   └── contratos.html
│   │   └── reportes/
│   │       ├── reporte_reproducciones.html
│   │       ├── reporte_canciones.html
│   │       ├── reporte_usuarios.html
│   │       └── reporte_pagos.html
│   │
│   ├── controllers/
│   │   ├── usuario_controller.py
│   │   ├── catalogo_controller.py
│   │   ├── biblioteca_controller.py
│   │   ├── pago_controller.py
│   │   ├── analitica_controller.py
│   │   ├── industria_controller.py
│   │   └── reporte_controller.py
│   │
│   ├── routes/
│   │   ├── usuario_routes.py
│   │   ├── catalogo_routes.py
│   │   ├── biblioteca_routes.py
│   │   ├── pago_routes.py
│   │   ├── analitica_routes.py
│   │   ├── industria_routes.py
│   │   └── reporte_routes.py
│   │
│   ├── database/
│   │   └── conexion_mongo.py
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── img/
│   │       └── logo.png
│   │
│   └── __init__.py
│
├── docs/
│   ├── manual_usuario/
│   │   └── manual_usuario.docx
│   ├── capturas_mongodb/
│   └── video/
│       └── enlace_video.txt
│
├── config.py
├── run.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Descripción de Carpetas Principales

| Carpeta o archivo | Descripción |
|---|---|
| app/ | Carpeta principal de la aplicación web. |
| app/models/ | Contiene los modelos encargados de interactuar con MongoDB. |
| app/views/ | Contiene las páginas HTML del sistema. |
| app/controllers/ | Contiene la lógica de negocio de cada módulo. |
| app/routes/ | Contiene la definición de rutas de la aplicación. |
| app/database/ | Contiene la configuración de conexión a MongoDB. |
| app/static/ | Contiene archivos CSS, JavaScript e imágenes. |
| docs/ | Contiene documentación, manual de usuario, capturas y enlace del video. |
| config.py | Archivo de configuración general del proyecto. |
| run.py | Archivo principal para ejecutar la aplicación Flask. |
| requirements.txt | Archivo que lista las dependencias necesarias. |
| README.md | Archivo de documentación principal del proyecto. |
| .gitignore | Archivo que define qué elementos no deben subirse al repositorio. |

---

## Módulos del Sistema

El sistema Ecualizer está dividido en los siguientes módulos principales:

---

## 1. Usuarios

Este módulo permite gestionar la información de los usuarios registrados en la plataforma.

### Funcionalidades

- Registrar nuevos usuarios.
- Consultar usuarios existentes.
- Editar información de usuarios.
- Eliminar usuarios.
- Gestionar perfiles asociados a personas, administradores y artistas.

### Archivos relacionados

```text
app/models/usuario_model.py
app/controllers/usuario_controller.py
app/routes/usuario_routes.py
app/views/usuarios/
```

---

## 2. Catálogo Musical

Este módulo permite administrar la información musical disponible dentro de la plataforma.

### Entidades principales

- Canciones.
- Álbumes.
- Artistas.
- Géneros musicales.
- Tipos de álbum.

### Funcionalidades

- Registrar canciones.
- Registrar álbumes.
- Consultar canciones disponibles.
- Consultar artistas.
- Consultar géneros musicales.
- Editar información musical.
- Eliminar registros del catálogo.

### Archivos relacionados

```text
app/models/cancion_model.py
app/models/album_model.py
app/models/artista_model.py
app/models/genero_model.py
app/controllers/catalogo_controller.py
app/routes/catalogo_routes.py
app/views/catalogo/
```

---

## 3. Biblioteca

Este módulo permite gestionar la biblioteca personal de los usuarios.

### Entidades principales

- Playlists.
- Canciones en playlists.
- Favoritos.
- Likes.
- Seguimiento de artistas.

### Funcionalidades

- Crear playlists.
- Consultar playlists.
- Editar playlists.
- Agregar canciones a una playlist.
- Gestionar canciones favoritas.
- Registrar likes.
- Seguir artistas.

### Archivos relacionados

```text
app/models/playlist_model.py
app/models/biblioteca_model.py
app/models/like_model.py
app/models/seguimiento_model.py
app/controllers/biblioteca_controller.py
app/routes/biblioteca_routes.py
app/views/biblioteca/
```

---

## 4. Pagos y Suscripciones

Este módulo permite gestionar los planes, pagos y suscripciones de los usuarios.

### Entidades principales

- Pagos.
- Suscripciones.
- Tipos de plan.

### Funcionalidades

- Registrar pagos.
- Consultar pagos realizados.
- Gestionar suscripciones activas.
- Consultar tipos de plan.
- Validar información de pagos y estados de suscripción.

### Archivos relacionados

```text
app/models/pago_model.py
app/models/suscripcion_model.py
app/models/tipo_plan_model.py
app/controllers/pago_controller.py
app/routes/pago_routes.py
app/views/pagos/
```

---

## 5. Analítica

Este módulo permite registrar y analizar la actividad de reproducción dentro de la plataforma.

### Entidades principales

- Reproducciones.
- Regalías.

### Funcionalidades

- Registrar reproducciones.
- Consultar reproducciones por canción.
- Consultar reproducciones por usuario.
- Generar reportes de actividad.
- Calcular o visualizar regalías.
- Analizar canciones más reproducidas.

### Archivos relacionados

```text
app/models/reproduccion_model.py
app/models/regalia_model.py
app/controllers/analitica_controller.py
app/routes/analitica_routes.py
app/views/analitica/
```

---

## 6. Industria Musical

Este módulo permite gestionar información relacionada con discográficas y contratos.

### Entidades principales

- Discográficas.
- Contratos discográficos.

### Funcionalidades

- Registrar discográficas.
- Consultar discográficas existentes.
- Consultar contratos.
- Gestionar contratos asociados a artistas.
- Relacionar artistas con entidades de la industria musical.

### Archivos relacionados

```text
app/models/discografica_model.py
app/models/contrato_discografica_model.py
app/controllers/industria_controller.py
app/routes/industria_routes.py
app/views/industria/
```

---

## 7. Reportes

Este módulo permite visualizar información relevante del sistema a través de consultas principales.

### Reportes sugeridos

- Reporte de canciones más reproducidas.
- Reporte de usuarios registrados.
- Reporte de pagos realizados.
- Reporte de reproducciones por canción.
- Reporte de regalías generadas.
- Reporte de playlists creadas.
- Reporte de suscripciones activas.

### Archivos relacionados

```text
app/controllers/reporte_controller.py
app/routes/reporte_routes.py
app/views/reportes/
```

---

## Instalación del Proyecto

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

### 2. Ingresar a la carpeta del proyecto

```bash
cd Ecualizer
```

### 3. Crear entorno virtual

```bash
python -m venv venv
```

### 4. Activar entorno virtual

En Windows:

```bash
venv\Scripts\activate
```

En macOS o Linux:

```bash
source venv/bin/activate
```

### 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Dependencias del Proyecto

El archivo `requirements.txt` debe incluir las siguientes dependencias:

```text
Flask
pymongo
python-dotenv
```

### Descripción de dependencias

| Dependencia | Descripción |
|---|---|
| Flask | Framework utilizado para crear la aplicación web. |
| pymongo | Librería utilizada para conectar Python con MongoDB. |
| python-dotenv | Permite manejar variables de entorno desde un archivo `.env`. |

---

## Configuración de Variables de Entorno

Se recomienda utilizar un archivo `.env` para almacenar la configuración de conexión a MongoDB.

Ejemplo de archivo `.env`:

```env
MONGO_URI=mongodb://localhost:27017/
MONGO_DB=Ecualizer
FLASK_ENV=development
FLASK_DEBUG=True
```

El archivo `.env` no debe subirse al repositorio, por lo tanto, debe agregarse al archivo `.gitignore`.

---

## Configuración de MongoDB

La conexión a MongoDB se gestiona desde el archivo:

```text
app/database/conexion_mongo.py
```

Ejemplo de configuración:

```python
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class ConexionMongo:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        self.mongo_db = os.getenv("MONGO_DB", "Ecualizer")
        self.cliente = MongoClient(self.mongo_uri)
        self.db = self.cliente[self.mongo_db]

    def obtener_base_datos(self):
        return self.db
```

---

## Ejecución del Proyecto

Para ejecutar la aplicación, usar el siguiente comando:

```bash
python run.py
```

Luego abrir en el navegador:

```text
http://127.0.0.1:5000/
```

---

## Archivo Principal de Ejecución

El archivo `run.py` será el punto de entrada de la aplicación.

Ejemplo sugerido:

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Archivo de Inicialización de la Aplicación

El archivo `app/__init__.py` permite crear y configurar la aplicación Flask.

Ejemplo sugerido:

```python
from flask import Flask

def create_app():
    app = Flask(
        __name__,
        template_folder="views",
        static_folder="static"
    )

    from app.routes.usuario_routes import usuario_bp
    from app.routes.catalogo_routes import catalogo_bp
    from app.routes.biblioteca_routes import biblioteca_bp
    from app.routes.pago_routes import pago_bp
    from app.routes.analitica_routes import analitica_bp
    from app.routes.industria_routes import industria_bp
    from app.routes.reporte_routes import reporte_bp

    app.register_blueprint(usuario_bp)
    app.register_blueprint(catalogo_bp)
    app.register_blueprint(biblioteca_bp)
    app.register_blueprint(pago_bp)
    app.register_blueprint(analitica_bp)
    app.register_blueprint(industria_bp)
    app.register_blueprint(reporte_bp)

    return app
```

---

## Operaciones CRUD

El proyecto debe demostrar al menos una operación CRUD completa desde la aplicación web y su reflejo en MongoDB.

CRUD significa:

| Operación | Significado | Descripción |
|---|---|---|
| Create | Crear | Registrar un nuevo documento en MongoDB. |
| Read | Leer | Consultar información almacenada. |
| Update | Actualizar | Modificar un documento existente. |
| Delete | Eliminar | Eliminar un documento de la base de datos. |

---

## CRUD Recomendado: Canciones

Se recomienda implementar el CRUD de canciones porque es una entidad central dentro del sistema Ecualizer.

### Operaciones del CRUD de Canciones

- Crear una canción desde un formulario HTML.
- Consultar las canciones registradas.
- Actualizar la información de una canción.
- Eliminar una canción.
- Verificar los cambios directamente en MongoDB.

### Campos sugeridos para canción

```text
nombreCancion
duracion
fechaLanzamiento
estadoCancion
calidadKbps
album
generos
artistaPrincipal
```

---

## Base de Datos MongoDB

Nombre sugerido de la base de datos:

```text
Ecualizer
```

---

## Colecciones Sugeridas

```text
usuarios
personas
administradores
artistas
canciones
albumes
generos
tipos_album
playlists
biblioteca
likes
seguimientos
pagos
suscripciones
planes
reproducciones
regalias
discograficas
contratos_discograficos
```

---

## Ejemplo de Documento: Canción

```json
{
  "nombreCancion": "Ejemplo de canción",
  "duracion": "00:03:45",
  "fechaLanzamiento": "2025-01-15",
  "estadoCancion": "activa",
  "calidadKbps": 320,
  "album": "Ejemplo de álbum",
  "generos": ["Pop", "Urbano"],
  "artistaPrincipal": "Artista de ejemplo"
}
```

---

## Ejemplo de Documento: Usuario

```json
{
  "nombre": "Usuario ejemplo",
  "correo": "usuario@ejemplo.com",
  "tipoUsuario": "oyente",
  "estado": "activo",
  "fechaRegistro": "2025-01-15"
}
```

---

## Ejemplo de Documento: Playlist

```json
{
  "nombrePlaylist": "Favoritas",
  "tipoVisibilidad": "privada",
  "tipoPlaylist": "personal",
  "usuario": "usuario@ejemplo.com",
  "canciones": [
    "Ejemplo de canción 1",
    "Ejemplo de canción 2"
  ]
}
```

---

## Flujo General de la Aplicación

```text
Usuario
   |
   v
Vista HTML
   |
   v
Ruta Flask
   |
   v
Controlador
   |
   v
Modelo
   |
   v
MongoDB
```

---

## Documentación del Proyecto

La documentación del proyecto se encuentra en la carpeta:

```text
docs/
```

---

## Manual de Usuario

El manual de usuario se encuentra en:

```text
docs/manual_usuario/manual_usuario.docx
```

Este documento debe incluir:

- Descripción general del sistema.
- Objetivo de la aplicación.
- Funcionalidades principales.
- Capturas de la aplicación web.
- Capturas de MongoDB.
- Explicación de una operación CRUD.
- Resultados obtenidos.
- Conclusiones del uso del sistema.

---

## Capturas de MongoDB

Las capturas de MongoDB deben guardarse en:

```text
docs/capturas_mongodb/
```

Se recomienda incluir capturas de:

- Base de datos creada.
- Colecciones principales.
- Inserción de documentos.
- Consulta de documentos.
- Actualización de documentos.
- Eliminación de documentos.

---

## Video Explicativo

El enlace del video explicativo debe guardarse en:

```text
docs/video/enlace_video.txt
```

El video debe demostrar:

- Presentación breve del proyecto.
- Explicación de la estructura MVC.
- Demostración de una operación CRUD desde la aplicación web.
- Verificación del cambio en MongoDB.
- Participación de los integrantes del grupo.
- Duración aproximada de 3 a 4 minutos.

---

## Repositorio de Código

El proyecto debe estar disponible en un repositorio de código, por ejemplo GitHub.

```text
URL_DEL_REPOSITORIO
```

El repositorio debe contener:

- Código fuente del proyecto.
- Archivo README.md.
- Archivo requirements.txt.
- Estructura de carpetas organizada.
- Documentación requerida.
- Evidencias necesarias para la entrega.

---

## Archivo .gitignore Sugerido

```gitignore
venv/
__pycache__/
*.pyc
.env
.DS_Store
.vscode/
.idea/
```

---

## Estado del Proyecto

```text
En desarrollo
```

---

## Autores

Proyecto desarrollado por:

```text
Adrián Freire
Josselyn Guevara
Anthonny Llanos
```

---

## Conclusiones

- La implementación de Ecualizer permite aplicar conocimientos de desarrollo web, bases de datos NoSQL y arquitectura MVC.
- Flask facilita la creación de rutas, controladores y vistas dentro de una aplicación web.
- MongoDB permite almacenar información de manera flexible mediante documentos.
- El uso del patrón MVC mejora la organización del código y facilita el mantenimiento del proyecto.
- La aplicación web permite interactuar con la base de datos mediante formularios, consultas y reportes.
- La documentación del proyecto es fundamental para explicar la instalación, ejecución y funcionamiento del sistema.

---

## Lecciones Aprendidas

- Se comprendió la importancia de organizar un proyecto web mediante una arquitectura MVC.
- Se aplicó la conexión entre Python y MongoDB usando PyMongo.
- Se reforzó el uso de Flask para crear rutas y controlar solicitudes del usuario.
- Se aprendió a estructurar vistas HTML utilizando Jinja2.
- Se identificó la importancia de separar responsabilidades entre modelos, vistas y controladores.
- Se evidenció la necesidad de documentar correctamente el proyecto para facilitar su revisión y presentación.
- Se comprendió la importancia de evidenciar el funcionamiento del sistema mediante capturas y video explicativo.

---

## Licencia

Este proyecto fue desarrollado con fines académicos como parte del Proyecto Integrador.
