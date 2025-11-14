#!/usr/bin/env python3
"""
Main entry point for Mizuki Bot.
"""

import asyncio
import os
import logging
import sys

from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.bot.core.bot import Bot
from src.bot.utils.logger import setup_logger

async def main():
    setup_logger()
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting Mizuki Bot...")
        bot = Bot()
        await bot.start()

    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt).")
    except Exception as e:
        logger.exception(f"A critical error occurred: {e}")
        sys.exit(1)
if __name__ == "__main__":
    asyncio.run(main())