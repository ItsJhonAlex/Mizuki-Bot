# 🌙 Mizuki Bot

> Tu perfecto asistente lunar para Discord. Con su elegancia celestial y tecnología avanzada, te ayuda a gestionar tu servidor con la suave luz de la luna.

[![Python Version](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.6.4-blue.svg)](https://github.com/Rapptz/discord.py)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ Características

- 🔌 **Sistema de Plugins Modular**: Arquitectura extensible basada en plugins
- ⚡ **Comandos Slash y Prefix**: Soporte para ambos tipos de comandos
- 📝 **Logging Robusto**: Sistema de logs con rotación automática
- 🔄 **Carga en Caliente**: Carga/descarga dinámica de plugins
- 🐳 **Docker Ready**: Deployment fácil con Docker
- 🛡️ **Seguro**: Comandos administrativos protegidos

## 📦 Estructura del Proyecto

```
Mizuki-Bot/
├── src/
│   ├── bot/
│   │   ├── core/          # Núcleo del bot
│   │   │   ├── bot.py
│   │   │   └── plugin_manager.py
│   │   ├── plugins/       # Sistema de plugins
│   │   │   ├── base_plugin.py
│   │   │   └── admin/
│   │   ├── utils/         # Utilidades
│   │   │   └── logger.py
│   │   ├── config/        # Configuración
│   │   └── models/        # Modelos de datos
│   ├── scripts/           # Scripts de utilidad
│   │   └── create_plugin.py
│   └── tests/             # Tests
├── main.py                # Punto de entrada
├── pyproject.toml         # Configuración del proyecto
├── Dockerfile             # Contenedor Docker
└── docker compose.yml     # Orchestración Docker
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.14 o superior
- pip o uv (gestor de paquetes)
- Discord Bot Token ([Cómo obtenerlo](https://discord.com/developers/applications))

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/ItsJhonAlex/Mizuki-Bot.git
cd Mizuki-Bot
```

2. **Crear un entorno virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -e .
# o con uv
uv pip install -e .
```

4. **Configurar variables de entorno**

Crea un archivo `.env` en la raíz del proyecto:

```env
DISCORD_TOKEN=tu_token_de_discord_aqui
DISCORD_PREFIX=!
DISCORD_ACTIVITY=the moon 🌙
```

5. **Ejecutar el bot**
```bash
python main.py
```

### Instalación con Docker

> 🐳 El Docker Compose incluye PostgreSQL + Bot automáticamente

1. **Configurar variables de entorno**

Crea un archivo `.env` desde el ejemplo:

```bash
cp .env.example .env
nano .env  # Edita y configura tus credenciales
```

**⚠️ Importante**: Configura al menos:
- `DISCORD_TOKEN` - Tu token de Discord
- `DB_PASSWORD` - Contraseña segura para PostgreSQL
- `DISCORD_ADMIN_ID` - Tu ID de Discord

2. **Iniciar todo (Base de datos + Bot)**
```bash
# Construir e iniciar en segundo plano
docker compose up -d

# Ver logs en tiempo real
docker compose logs -f

# Ver solo logs del bot
docker compose logs -f mizuki-bot

# Ver solo logs de la base de datos
docker compose logs -f postgres
```

3. **Comandos útiles**
```bash
# Detener todo
docker compose stop

# Reiniciar solo el bot
docker compose restart mizuki-bot

# Ver estado de los servicios
docker compose ps

# Detener y eliminar contenedores (los datos persisten)
docker compose down

# Reconstruir después de cambios en el código
docker compose up -d --build
```

## 🔌 Sistema de Plugins

### Plugins Incluidos

#### 🏓 Ping Plugin
- **Comandos**: `/ping`, `!ping`
- **Descripción**: Verifica la latencia del bot (WebSocket y API)
- **Permisos**: Todos
- **Características**:
  - Muestra latencia WebSocket y API
  - Colores según rendimiento (verde/naranja/rojo)
  - Funciona con slash y prefix commands

#### 🔧 Admin Plugin
- **Comando**: `/plugins`
- **Descripción**: Lista todos los plugins cargados
- **Permisos**: Administrador

### Crear un Nuevo Plugin

Usa el script de creación de plugins:

```bash
python src/scripts/create_plugin.py nombre_del_plugin --author "Tu Nombre" --description "Descripción del plugin"
```

Esto creará la estructura básica en `src/bot/plugins/nombre_del_plugin/`.

### Estructura de un Plugin

```python
from discord import app_commands
from discord.ext import commands
from src.bot.plugins.base_plugin import BasePlugin

class MiPlugin(BasePlugin):
    PLUGIN_NAME = "Mi Plugin"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Descripción de mi plugin"
    PLUGIN_AUTHOR = "Tu Nombre"

    async def setup(self):
        # Registrar comandos prefix
        @commands.command(name="hola")
        async def hola(ctx: commands.Context):
            await ctx.send("¡Hola mundo!")
        
        self.register_prefix_command(hola)

        # Registrar comandos slash
        @app_commands.command(name="hola", description="Saluda")
        async def hola_slash(interaction: discord.Interaction):
            await interaction.response.send_message("¡Hola mundo!")
        
        self.register_slash_command(hola_slash)
```

## 📝 Variables de Entorno

### Discord
| Variable | Descripción | Ejemplo | Requerido |
|----------|-------------|---------|-----------|
| `DISCORD_TOKEN` | Token del bot de Discord | `MTIzNDU2Nzg5MDEyMzQ1Njc4OQ...` | ✅ |
| `DISCORD_PREFIX` | Prefijo para comandos de texto | `!` | ✅ |
| `DISCORD_ACTIVITY` | Estado/actividad del bot | `the moon 🌙` | ❌ |
| `DISCORD_ADMIN_ID` | ID del administrador del bot | `123456789012345678` | ✅ |

### Base de Datos (PostgreSQL)
| Variable | Descripción | Ejemplo | Requerido |
|----------|-------------|---------|-----------|
| `DB_HOST` | Host de la base de datos | `postgres` (Docker) / `localhost` (local) | ✅ |
| `DB_PORT` | Puerto de PostgreSQL | `5432` | ✅ |
| `DB_USER` | Usuario de PostgreSQL | `mizuki` | ✅ |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `tu_password_segura` | ✅ |
| `DB_NAME` | Nombre de la base de datos | `mizuki_bot` | ✅ |

> 💡 **Nota**: En Docker, `DB_HOST` se configura automáticamente a `postgres`. Para desarrollo local, usa `localhost`.

## 🛠️ Desarrollo

### Ejecutar Tests

```bash
pytest
```

### Formato de Código

```bash
black src/
```

### Linting

```bash
ruff check src/
```

## 📚 Comandos Disponibles

### Comandos Slash

| Comando | Descripción | Permisos |
|---------|-------------|----------|
| `/ping` | Verifica la latencia del bot | Todos |
| `/plugins` | Lista todos los plugins cargados | Administrador |

### Comandos Prefix

Configurable mediante `DISCORD_PREFIX` (por defecto: `!`)

| Comando | Descripción | Permisos |
|---------|-------------|----------|
| `!ping` | Verifica la latencia del bot | Todos |

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👤 Autor

**ItsJhonAlex**
- Email: itsjhonalex@gmail.com
- GitHub: [@ItsJhonAlex](https://github.com/ItsJhonAlex)

## 🌟 Agradecimientos

- [discord.py](https://github.com/Rapptz/discord.py) - Biblioteca principal
- La comunidad de Discord por su apoyo

---

<div align="center">
  <sub>Hecho con 🌙 por ItsJhonAlex</sub>
</div>
