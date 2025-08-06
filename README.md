# Blog FullStack con Vue, FastAPI y MongoDB

Este es un blog minimalista y moderno desarrollado como proyecto fullstack. Permite crear, leer y eliminar publicaciones (con imágenes opcionales), autenticarse como usuario y alternar entre modo claro y oscuro. Todo está dockerizado para facilitar su despliegue.

---

## Tecnologías utilizadas
- **Frontend:**
    - [Vue 3](https://vuejs.org/)
    - [Pinia](https://pinia.vuejs.org/)
    - [Tailwind CSS](https://tailwindcss.com/)
    - [Vue Quill Editor](https://vueup.github.io/vue-quill)

- **Backend:**
    - [FastAPI](https://fastapi.tiangolo.com/)
    - [Pymongo](https://pymongo.readthedocs.io/)

- **Base de datos:**
    - [MongoDB](https://www.mongodb.com/)
    - [Mongo Express](https://hub.docker.com/_/mongo-express)

---

## Características

- Registro e inicio de sesión de usuarios
- CRUD de posts (crear, listar, eliminar)
- Subida de imágenes para las entradas
- Editor de texto enriquecido (Quill)
- Vista lateral de posts recientes
- Modo claro y modo oscuro persistente
- Contenedores Docker para facilitar la instalación

---

## Requisitos previos

- Docker Desktop instalado en tu máquina (Windows, macOS o Linux)

---

## Instalación y ejecución

1. Clona el repositorio:

    ```bash
    git clone https://github.com/tu-usuario/nombre-del-repo.git
    cd nombre-del-repo
    docker compose up --build
    ```

2. Esto iniciará cuatro contenedores:
    - frontend: Vue (http://localhost:3000)

    - backend: FastAPI (http://localhost:8000/docs)

    - mongodb: servicio de base de datos (http://localhost:27017)
    - mongo-express: administrador de base de datos (http://localhost:8081)

3. **¿Cómo usarlo?**
    - Abre la app en http://localhost:3000

    - Regístrate como nuevo usuario

    - Inicia sesión

    - Crea un nuevo post desde el botón [Nuevo Post](http://localhost:3000/new-post)

    - Sube una imagen si deseas (opcional)

    - El post aparecerá en la lista, y también en la barra lateral

    - Solo puedes eliminar tus propios posts