# 🚀 Inicio Rápido - Mizuki Bot

## Levantar Bot + Base de Datos con Docker

### 1️⃣ Verificar configuración

```bash
# Asegúrate de que tu archivo .env tenga todas las variables necesarias
cat .env
```

Tu `.env` debe contener:
```env
# Discord
DISCORD_TOKEN=tu_token_aqui
DISCORD_PREFIX=!
DISCORD_ACTIVITY=Viendo Nodos
DISCORD_ADMIN_ID=tu_id_aqui

# Database
DB_USER=mizuki
DB_PASSWORD=tu_password_segura
DB_NAME=mizuki_bot
DB_PORT=5432
DB_HOST=localhost  # Se cambia automáticamente a 'postgres' en Docker
```

### 2️⃣ Construir e iniciar todo

```bash
# Construir las imágenes e iniciar servicios
docker compose up -d --build

# Ver logs en tiempo real
docker compose logs -f
```

### 3️⃣ Verificar que todo funciona

```bash
# Ver estado de los servicios
docker compose ps

# Deberías ver algo como:
# NAME                IMAGE               STATUS
# mizuki-bot         mizuki-bot          Up
# mizuki-postgres    postgres:16-alpine  Up (healthy)
```

### 4️⃣ Ver logs específicos

```bash
# Solo bot
docker compose logs -f mizuki-bot

# Solo base de datos
docker compose logs -f postgres

# Últimas 50 líneas
docker compose logs --tail=50
```

### 5️⃣ Conectarse a la base de datos (opcional)

```bash
# Entrar a PostgreSQL
docker exec -it mizuki-postgres psql -U mizuki -d mizuki_bot

# Ver tablas
\dt

# Ver datos de una tabla
SELECT * FROM guilds;

# Salir
\q
```

## 🔧 Comandos Útiles

### Gestión de servicios

```bash
# Detener todo
docker compose stop

# Iniciar todo
docker compose start

# Reiniciar todo
docker compose restart

# Reiniciar solo el bot (después de cambios en código)
docker compose restart mizuki-bot

# Ver recursos usados
docker stats
```

### Reconstruir después de cambios

```bash
# Si cambias el código del bot
docker compose up -d --build mizuki-bot

# Si cambias dependencias (pyproject.toml)
docker compose build --no-cache mizuki-bot
docker compose up -d mizuki-bot
```

### Limpiar y empezar de nuevo

```bash
# Detener y eliminar contenedores (datos persisten)
docker compose down

# Eliminar TODO incluyendo volúmenes (¡CUIDADO! Borra datos de la BD)
docker compose down -v

# Eliminar imágenes no usadas
docker system prune -a
```

## 🐛 Solución de Problemas

### El bot no se conecta a Discord
1. Verifica tu `DISCORD_TOKEN` en `.env`
2. Revisa los logs: `docker compose logs mizuki-bot`

### El bot no se conecta a la base de datos
1. Verifica que PostgreSQL esté healthy: `docker compose ps`
2. Revisa las credenciales en `.env`
3. Ver logs de la BD: `docker compose logs postgres`

### Puerto 5432 ya en uso
```bash
# Cambiar puerto en .env
DB_PORT=5433

# O detener PostgreSQL local
sudo systemctl stop postgresql
```

### El bot se reinicia constantemente
```bash
# Ver por qué crashea
docker compose logs --tail=100 mizuki-bot

# Verificar healthcheck de postgres
docker inspect mizuki-postgres | grep -A 10 Health
```

## 📦 Backup de Base de Datos

```bash
# Crear backup
docker exec mizuki-postgres pg_dump -U mizuki mizuki_bot > backup_$(date +%Y%m%d).sql

# Restaurar backup
cat backup_20240101.sql | docker exec -i mizuki-postgres psql -U mizuki -d mizuki_bot
```

## 🎯 Desarrollo Local (sin Docker)

Si prefieres desarrollar sin Docker:

```bash
# 1. Inicia solo la base de datos en Docker
docker compose up -d postgres

# 2. Cambia DB_HOST en .env
DB_HOST=localhost

# 3. Instala dependencias localmente
python -m venv .venv
source .venv/bin/activate
pip install -e .

# 4. Ejecuta el bot localmente
python main.py
```

## 📚 Más Información

- Ver [README.md](README.md) para documentación completa
- Ver [README_DATABASE.md](README_DATABASE.md) para detalles de la base de datos
- Ver logs: `docker compose logs -f`

---

¿Problemas? Revisa los logs con `docker compose logs -f`

