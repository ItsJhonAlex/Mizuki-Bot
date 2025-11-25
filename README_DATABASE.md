# 🗄️ Base de Datos - Mizuki Bot

## PostgreSQL con Docker

Esta guía te ayudará a entender y gestionar la base de datos PostgreSQL de Mizuki Bot.

> 💡 **Nota**: La base de datos se inicia automáticamente con `docker compose up`. No necesitas configuración adicional.

## 🚀 Inicio Rápido

### Opción 1: Todo Integrado (Recomendado)

```bash
# Esto inicia PostgreSQL + Bot automáticamente
docker compose up -d
```

### Opción 2: Solo Base de Datos

```bash
# Si solo quieres la base de datos (para desarrollo)
docker compose -f docker compose.db.yml up -d
```

## ⚙️ Configuración

Las variables de entorno están en el archivo `.env`:

```bash
# Copia el ejemplo si no lo has hecho
cp .env.example .env

# Edita las credenciales
nano .env
```

⚠️ **Importante**: Cambia `DB_PASSWORD` por una contraseña segura.

### 3. Conectarse a la base de datos

#### Desde tu máquina local:
```bash
# Usando psql
docker exec -it mizuki-postgres psql -U mizuki -d mizuki_bot

# O conectarse directamente si tienes psql instalado
psql -h localhost -p 5432 -U mizuki -d mizuki_bot
```

#### Desde Python (asyncpg):
```python
import asyncpg

async def connect():
    conn = await asyncpg.connect(
        host='localhost',
        port=5432,
        user='mizuki',
        password='tu_password',
        database='mizuki_bot'
    )
    return conn
```

## 🛠️ Comandos Útiles

### Gestión del contenedor

```bash
# Con el docker compose principal (Bot + DB)
docker compose stop postgres          # Detener solo PostgreSQL
docker compose start postgres         # Iniciar solo PostgreSQL
docker compose restart postgres       # Reiniciar solo PostgreSQL
docker compose logs -f postgres       # Ver logs en tiempo real

# Con el docker compose solo para DB (desarrollo)
docker compose -f docker compose.db.yml stop
docker compose -f docker compose.db.yml start
docker compose -f docker compose.db.yml restart
docker compose -f docker compose.db.yml down    # Los datos persisten
docker compose -f docker compose.db.yml down -v # ELIMINA TODO (incluidos datos)
```

### Backup y Restore

```bash
# Crear backup
docker exec mizuki-postgres pg_dump -U mizuki mizuki_bot > backup.sql

# Restaurar backup
cat backup.sql | docker exec -i mizuki-postgres psql -U mizuki -d mizuki_bot
```

### Ver logs

```bash
# Desde docker compose principal
docker compose logs -f postgres           # Tiempo real
docker compose logs --tail=100 postgres   # Últimas 100 líneas

# Desde docker compose solo DB
docker compose -f docker compose.db.yml logs -f
docker compose -f docker compose.db.yml logs --tail=100
```

## 📊 Información de Conexión

| Parámetro | Valor por Defecto | Variable |
|-----------|-------------------|----------|
| Host | localhost | `DB_HOST` |
| Puerto | 5432 | `DB_PORT` |
| Usuario | mizuki | `DB_USER` |
| Contraseña | - | `DB_PASSWORD` |
| Base de Datos | mizuki_bot | `DB_NAME` |

## 📦 Instalar Driver de Python

Para conectar tu bot con PostgreSQL, necesitas instalar un driver:

### asyncpg (Recomendado - Asíncrono)
```bash
pip install asyncpg

# o con uv
uv pip install asyncpg
```

### SQLAlchemy con asyncpg (Para ORM)
```bash
pip install sqlalchemy[asyncio] asyncpg

# o con uv
uv pip install sqlalchemy[asyncio] asyncpg
```

## 🔍 Verificar que funciona

```bash
# Entrar al contenedor
docker exec -it mizuki-postgres bash

# Conectar a PostgreSQL
psql -U mizuki -d mizuki_bot

# Ver tablas
\dt

# Salir
\q
exit
```

## 🔒 Seguridad

- ✅ Cambia siempre `DB_PASSWORD` en producción
- ✅ No subas el archivo `.env` a Git (ya está en `.gitignore`)
- ✅ Usa contraseñas fuertes (mínimo 16 caracteres)
- ✅ En producción, no expongas el puerto 5432 públicamente

## 🌐 Red Docker

La base de datos está en la red `mizuki_network`. Cuando quieras conectar el bot desde Docker:

```yaml
services:
  bot:
    # ... tu configuración del bot
    networks:
      - mizuki-network
    environment:
      DB_HOST: postgres  # Nombre del servicio de PostgreSQL
```

## ❓ Solución de Problemas

### El contenedor no inicia
```bash
# Ver logs de error
docker compose -f docker compose.db.yml logs postgres

# Verificar que el puerto 5432 no está en uso
sudo netstat -tlnp | grep 5432
```

### No puedo conectarme
```bash
# Verificar que el contenedor está corriendo
docker ps | grep mizuki-postgres

# Verificar el health check
docker inspect mizuki-postgres | grep Health -A 10
```

### Olvidé la contraseña
```bash
# Detener el contenedor
docker compose -f docker compose.db.yml down

# Editar .env con nueva contraseña
# Iniciar de nuevo
docker compose -f docker compose.db.yml up -d
```

## 📚 Recursos Adicionales

- [Documentación PostgreSQL](https://www.postgresql.org/docs/)
- [asyncpg Documentation](https://magicstack.github.io/asyncpg/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

