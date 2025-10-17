# api-p1d

<h1>Configuración de la api-p1d:</h1>

### 1. Clonar el repositorio

```bash
git clone https://github.com/abys72/api-p1d.git
cd api-p1d
```

### 2. Tener instalado en la maquina docker (Desktop/engine):

<h3>https://docs.docker.com/get-started/get-docker/<h3>

### 3. Crear el archivo .env usando la plantilla .env.sample y modificar variables

```bash 
cp .env.sample .env
```

### 4. Inciar contenedro.

Versiones antiguas:

```bash
docker-compose up -d
```

Ultimas versiones:

```bash
docker compose up -d
```

### 5. Ejecutar requests:

Ejemplo:

```bash
http://localhost:8083/api/v1/auth/access-token
```

### 6. Usuarios:
Por defecto la api generara un usuario y lo insertara en mongo.
Podemos usar el comando:
```bash
 docker logs api_p1d
```
Donde podremos ver el usuario y contrseña.

<h4>De igual manera por defecto es:<h4>
username: admin<br>
password: admin123