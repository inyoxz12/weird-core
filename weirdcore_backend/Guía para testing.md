# Guía de pruebas con `curl` (Windows CMD)

Este documento muestra ejemplos de peticiones `curl` para probar el backend desde **Windows (CMD o PowerShell)**.

Se asume que el servidor está corriendo en:

```text
http://127.0.0.1:8000
```

Si utilizas otra IP o puerto, solo debes modificar las URL.

Para los ejemplos se usará el siguiente **usuario de prueba**:

- `username`: `testuser`
- `email`: `testuser@example.com`
- `password`: `ClaveSegura123`
- `display_name`: `Test User`
- `favorite_color`: `#00d184`

---

## 1. Registro de usuario

```bat
curl -X POST "http://127.0.0.1:8000/api/auth/register/" ^
  -H "Content-Type: application/json" ^
  -d "{""username"":""testuser"",""email"":""testuser@example.com"",""password"":""ClaveSegura123"",""display_name"":""Test User"",""favorite_color"":""#00d184""}"
```

Si el usuario ya está registrado, recibirás un error 400 indicando que el nombre de usuario o correo ya existe. En ese caso, simplemente continúa con el paso de inicio de sesión.

---

## 2. Inicio de sesión (obtención de tokens JWT)

```bat
curl -X POST "http://127.0.0.1:8000/api/auth/login/" ^
  -H "Content-Type: application/json" ^
  -d "{""username"":""testuser"",""password"":""ClaveSegura123""}"
```

La respuesta tendrá este formato (resumen):

```json
{
  "refresh": "REFRESH_TOKEN_AQUI",
  "access": "ACCESS_TOKEN_AQUI",
  "user": { ... }
}
```

Guarda ambos tokens en variables de entorno de Windows para facilitar las pruebas:

```bat
set ACCESS=ACCESS_TOKEN_AQUI
set REFRESH=REFRESH_TOKEN_AQUI
```

(Recuerda reemplazar `ACCESS_TOKEN_AQUI` y `REFRESH_TOKEN_AQUI` por los valores reales devueltos por la API.)

Todas las peticiones autenticadas utilizarán el encabezado:

```http
Authorization: Bearer %ACCESS%
```

---

## 3. Endpoints de usuario

### 3.1 Ver perfil propio `/api/auth/me/`

```bat
curl "http://127.0.0.1:8000/api/auth/me/" ^
  -H "Authorization: Bearer %ACCESS%"
```

### 3.2 Modificar parcialmente el perfil (por ejemplo, mensaje de estado)

```bat
curl -X PATCH "http://127.0.0.1:8000/api/auth/me/" ^
  -H "Authorization: Bearer %ACCESS%" ^
  -H "Content-Type: application/json" ^
  -d "{""status_message"":""Probando el backend WEIRdCore""}"
```

### 3.3 Listar usuarios

```bat
curl "http://127.0.0.1:8000/api/auth/users/" ^
  -H "Authorization: Bearer %ACCESS%"
```

### 3.4 Buscar usuarios por nombre de usuario (query `search`)

```bat
curl "http://127.0.0.1:8000/api/auth/users/?search=test" ^
  -H "Authorization: Bearer %ACCESS%"
```

### 3.5 Enviar solicitud de amistad

Supongamos que el usuario con id `2` es el destinatario.

```bat
curl -X POST "http://127.0.0.1:8000/api/auth/friend-requests/" ^
  -H "Authorization: Bearer %ACCESS%" ^
  -H "Content-Type: application/json" ^
  -d "{""to_user_id"":2}"
```

### 3.6 Listar solicitudes de amistad (enviadas y recibidas)

```bat
curl "http://127.0.0.1:8000/api/auth/friend-requests/" ^
  -H "Authorization: Bearer %ACCESS%"
```

### 3.7 Aceptar o rechazar una solicitud de amistad

Si la solicitud tiene id `5`:

```bat
:: Aceptar
curl -X POST "http://127.0.0.1:8000/api/auth/friend-requests/5/accept/" ^
  -H "Authorization: Bearer %ACCESS%"

:: Rechazar
curl -X POST "http://127.0.0.1:8000/api/auth/friend-requests/5/reject/" ^
  -H "Authorization: Bearer %ACCESS%"
```

---

## 4. Posts (similar a un muro de Facebook)

### 4.1 Crear un post de texto

```bat
curl -X POST "http://127.0.0.1:8000/api/posts/" ^
  -H "Authorization: Bearer %ACCESS%" ^
  -H "Content-Type: application/json" ^
  -d "{""content"":""Este es mi primer post de prueba""}"
```

### 4.2 Consultar el feed (tus posts + amigos)

```bat
curl "http://127.0.0.1:8000/api/posts/" ^
  -H "Authorization: Bearer %ACCESS%"
```

### 4.3 Ver solo los posts del usuario autenticado

```bat
curl "http://127.0.0.1:8000/api/posts/my_posts/" ^
  -H "Authorization: Bearer %ACCESS%"
```

### 4.4 Comentar un post

Si el post tiene id `10`:

```bat
curl -X POST "http://127.0.0.1:8000/api/posts/10/comments/" ^
  -H "Authorization: Bearer %ACCESS%" ^
  -H "Content-Type: application/json" ^
  -d "{""content"":""Excelente publicación""}"
```

### 4.5 Reaccionar a un post

Tipos de reacción permitidos: `like`, `love`, `wow`, `sad`, `angry`.

```bat
curl -X POST "http://127.0.0.1:8000/api/posts/10/reactions/" ^
  -H "Authorization: Bearer %ACCESS%" ^
  -H "Content-Type: application/json" ^
  -d "{""type"":""love""}"
```

> Nota: si se envía la misma reacción nuevamente, se elimina (comportamiento de "toggle").

---

## 5. Chat (salas y mensajes)

### 5.1 Obtener o crear un chat privado con otro usuario

```bat
curl -X POST "http://127.0.0.1:8000/api/chat/rooms/private_room/" ^
  -H "Authorization: Bearer %ACCESS%" ^
  -H "Content-Type: application/json" ^
  -d "{""other_user_id"":2}"
```

La respuesta incluirá el `id` de la sala, por ejemplo `{"id": 3, ...}`.

### 5.2 Listar salas de chat del usuario

```bat
curl "http://127.0.0.1:8000/api/chat/rooms/" ^
  -H "Authorization: Bearer %ACCESS%"
```

### 5.3 Enviar un mensaje de texto a una sala

Suponiendo que la sala tiene id `3`:

```bat
curl -X POST "http://127.0.0.1:8000/api/chat/rooms/3/messages/" ^
  -H "Authorization: Bearer %ACCESS%" ^
  -H "Content-Type: application/json" ^
  -d "{""message_type"":""text"",""content"":""Hola, este es un mensaje de prueba""}"
```

### 5.4 Enviar un "zumbido" (buzz)

```bat
curl -X POST "http://127.0.0.1:8000/api/chat/rooms/3/messages/" ^
  -H "Authorization: Bearer %ACCESS%" ^
  -H "Content-Type: application/json" ^
  -d "{""message_type"":""buzz"",""content"":""Zumbido"",""extra_data"":{""intensity"":3}}"
```

El frontend puede interpretar este tipo de mensaje para hacer vibraciones, animaciones u otros efectos.

### 5.5 Listar mensajes de una sala

```bat
curl "http://127.0.0.1:8000/api/chat/rooms/3/messages/" ^
  -H "Authorization: Bearer %ACCESS%"
```

> Para mensajes de tipo `image`, `audio` o `drawing`, el frontend puede almacenar los archivos en un servicio de almacenamiento (o en el propio backend) y enviar en `extra_data` la URL o metadatos necesarios.

---

## 6. Pregunta del día y tablero de historias

### 6.1 Obtener la pregunta activa

```bat
curl "http://127.0.0.1:8000/api/community/questions/active/" ^
  -H "Authorization: Bearer %ACCESS%"
```

Supongamos que la pregunta activa tiene id `1`.

### 6.2 Responder la pregunta del día

```bat
curl -X POST "http://127.0.0.1:8000/api/community/questions/1/answers/" ^
  -H "Authorization: Bearer %ACCESS%" ^
  -H "Content-Type: application/json" ^
  -d "{""content"":""Esta es mi respuesta de prueba a la pregunta del día""}"
```

### 6.3 Crear una historia en el tablero

```bat
curl -X POST "http://127.0.0.1:8000/api/community/stories/" ^
  -H "Authorization: Bearer %ACCESS%" ^
  -H "Content-Type: application/json" ^
  -d "{""title"":""Mi primera historia"",""content"":""Contenido de ejemplo para el tablero de historias""}"
```

---

## 7. Refrescar el token de acceso

Cuando el token de acceso caduque, puedes solicitar uno nuevo usando el token de refresco:

```bat
curl -X POST "http://127.0.0.1:8000/api/auth/token/refresh/" ^
  -H "Content-Type: application/json" ^
  -d "{""refresh"":""%REFRESH%""}"
```

La respuesta incluirá un nuevo `access`. Puedes actualizar la variable de entorno:

```bat
set ACCESS=NUEVO_ACCESS_TOKEN
```

Con estos ejemplos deberías poder probar cómodamente todo el flujo principal del backend (usuarios, amigos, posts, chat y comunidad) directamente desde la consola de Windows utilizando `curl`.

