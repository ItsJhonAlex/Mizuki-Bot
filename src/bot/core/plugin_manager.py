import importlib
import pkgutil
import logging
import os
from typing import List, Dict, Any, Optional
from src.bot.plugins.base_plugin import BasePlugin

class PluginManager:
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("PluginManager")
        self.plugins: Dict[str, BasePlugin] = {}
        self.plugins_package = "src.bot.plugins"

    async def load_plugins(self) -> bool:
        self.logger.info("Loading plugins")

        try:
            plugins_package = importlib.import_module(self.plugins_package)

            for _, plugin_name, iskpg in pkgutil.iter_modules(plugins_package.__path__):
                if iskpg:
                    success = await self.load_plugin(plugin_name)
                    if not success:
                        self.logger.error(f"Failed to load plugin {plugin_name}")

            self.logger.info(f"{plugins_package.__name__} loaded")
            return True

        except Exception as e:
            self.logger.error(f"Failed to load plugin {plugins_package.__name__} : {e}")
            return False

    async def load_plugin(self, plugin_name: str) -> bool:
        try:
            module_path = f"{self.plugins_package}.{plugin_name}.plugin"
            module = importlib.import_module(module_path)

            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and
                    issubclass(attr, BasePlugin) and
                    attr != BasePlugin):
                    plugin_class = attr
                    break

            if not plugin_class:
                self.logger.error(f"Not found plugin {plugin_name}")
                return False

            plugin_instance = plugin_class(self.bot)
            await plugin_instance.setup()

            self.plugins[plugin_name] = plugin_instance

            metadata = plugin_instance.get_metadata()
            command_count = plugin_instance.get_command_count()

            self.logger.info(f"Plugin {metadata['name']} v{metadata['version']} loaded")
            self.logger.info(f"{command_count['prefix_commands']} prefix commands loaded,"
                         f"{command_count['slash_commands']} slash commands loaded")

            return True

        except Exception as e:
            self.logger.error(f"Failed to load plugin {plugin_name} : {e}")
            return False

    async def unload_plugin(self, plugin_name: str) -> bool:
        if plugin_name in self.plugins:
            try:
                await self.plugins[plugin_name].teardown()
                del self.plugins[plugin_name]
                self.logger.info(f"Plugin {plugin_name} unloaded")
                return True
            except Exception as e:
                self.logger.error(f"Failed to unload plugin {plugin_name} : {e}")
                return False
        return False

    async def reload_plugin(self, plugin_name: str) -> bool:
        if await self.unload_plugin(plugin_name):
            return await self.load_plugin(plugin_name)
        return False

    def get_plugin_info(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            metadata = plugin.get_metadata()
            command_count = plugin.get_command_count()

            return {
                **metadata,
                "commands": command_count,
                "loaded": True
            }
        return None

    def list_plugins(self) -> List[Dict[str, Any]]:
        plugins_info = []
        for plugin_name, plugin in self.plugins.items():
            plugins_info.append(self.get_plugin_info(plugin_name))
        return plugins_info
