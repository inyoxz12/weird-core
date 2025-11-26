# WEIRdCore Social Backend (Django + DRF)

Backend de red social estilo "vieja escuela" para usarse con un frontend en React
(y más adelante app móvil). Incluye:

- Registro y login con JWT (seguro, listo para SPA)
- Perfil de usuario (avatar, color favorito, estado, amigos)
- Sistema de amigos con solicitudes
- Posts tipo Facebook con comentarios y reacciones
- Módulo de comunidad:
  - Pregunta del día
  - Tablero de historias (stories / posts largos)
- Sistema de chat:
  - Chats privados (1 a 1)
  - Rooms de grupo
  - Random chat (match con desconocidos)
  - Soporte para tipos de mensaje: texto, emoji, zumbidos, imágenes, audio, dibujos (a nivel de modelo)

## Requisitos

- Python 3.11.4
- Pip
- (Opcional pero recomendado) entorno virtual `venv`

## Instalación rápida en Windows

```bash
cd weirdcore_backend

# 1) Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate

# 2) Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 3) Crear archivo .env (opcional pero recomendado)
copy .env.example .env
# Edita .env y cambia el SECRET_KEY por uno largo y aleatorio

# 4) Crear migraciones y base de datos
python manage.py makemigrations
python manage.py migrate

# 5) Crear superusuario para entrar al admin
python manage.py createsuperuser

# 6) Levantar servidor de desarrollo
python manage.py runserver
```

El backend quedará escuchando en `http://127.0.0.1:8000/`.

## Endpoints principales

- Autenticación / usuarios (`/api/auth/`):
  - `POST /api/auth/register/` → registro
  - `POST /api/auth/login/` → login (JWT)
  - `POST /api/auth/token/refresh/` → refrescar token
  - `GET/PUT /api/auth/me/` → ver / editar perfil propio
  - `GET /api/auth/users/` → listar usuarios
  - `GET /api/auth/users/?search=texto` → buscar usuarios por username
  - `GET /api/auth/friend-requests/` → ver solicitudes (enviadas y recibidas)
  - `POST /api/auth/friend-requests/` → crear solicitud (`{ "to_user_id": X }`)
  - `POST /api/auth/friend-requests/{id}/accept/` → aceptar
  - `POST /api/auth/friend-requests/{id}/reject/` → rechazar

- Posts (`/api/posts/`):
  - `GET /api/posts/` → feed (tus posts + amigos)
  - `POST /api/posts/` → crear post
  - `GET /api/posts/my_posts/` → solo tus posts
  - `POST /api/posts/{post_id}/comments/` → comentar
  - `POST /api/posts/{post_id}/reactions/` → reaccionar / cambiar reacción / quitar reacción

- Comunidad (`/api/community/`):
  - `GET /api/community/questions/active/` → pregunta del día
  - `POST /api/community/questions/{id}/answers/` → responder
  - `GET/POST /api/community/stories/` → listar / crear historias

- Chat (`/api/chat/`):
  - `GET /api/chat/rooms/` → rooms del usuario
  - `POST /api/chat/rooms/` → crear room de grupo (envía `name`, `room_type="group"`, `participants=[ids]`)
  - `POST /api/chat/rooms/private_room/` → obtener/crear chat privado (`{ "other_user_id": X }`)
  - `POST /api/chat/rooms/random_room/` → entrar a random chat (pairing simple)
  - `GET/POST /api/chat/rooms/{room_id}/messages/` → listar / enviar mensajes

Los tipos de mensaje en chat son: `text`, `emoji`, `buzz`, `image`, `audio`, `drawing`, `system`.
El frontend puede decidir cómo renderizar cada uno y qué datos poner en `extra_data`.

## Seguridad básica

- Passwords siempre se guardan hashados usando los validadores de Django.
- Autenticación vía JWT (access + refresh) usando `djangorestframework-simplejwt`.
- CSRF y protecciones estándar de Django activadas para vistas no-API.
- CORS abierto solo en modo DEBUG; para producción ajusta `CORS_ALLOWED_ORIGINS`
  y `DJANGO_DEBUG=False`.

**Importante:** esto es una base sólida pero NO reemplaza una auditoría de seguridad profesional
para producción. Antes de abrirlo a muchos usuarios reales, revisa:

- Configuración de HTTPS en tu servidor (Nginx/Caddy/etc).
- Uso de base de datos robusta (PostgreSQL) en lugar de SQLite.
- Config de `ALLOWED_HOSTS`, CORS y cookies seguras.
