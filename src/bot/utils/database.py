"""
Database connection utilities for Mizuki Bot
Uses asyncpg for PostgreSQL async connections
"""

import asyncpg
import logging
import os
from typing import Optional


logger = logging.getLogger("mizuki.database")


class Database:
    """Database connection manager for PostgreSQL"""
    
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "5432"))
        self.user = os.getenv("DB_USER", "mizuki")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "mizuki_bot")
    
    async def connect(self) -> bool:
        """
        Establishes connection to the database
        
        Returns:
            bool: True if connection was successful, False otherwise
        """
        try:
            logger.info(f"Connecting to PostgreSQL at {self.host}:{self.port}/{self.database}")
            
            self.pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                min_size=5,
                max_size=20,
                command_timeout=60
            )
            
            # Verify connection
            async with self.pool.acquire() as conn:
                version = await conn.fetchval("SELECT version()")
                logger.info(f"Successfully connected to PostgreSQL")
                logger.debug(f"Version: {version}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error connecting to database: {e}")
            return False
    
    async def close(self):
        """Closes the database connection"""
        if self.pool:
            logger.info("Closing database connection")
            await self.pool.close()
            self.pool = None
    
    async def execute(self, query: str, *args):
        """
        Executes a query without returning results (INSERT, UPDATE, DELETE)
        
        Args:
            query: SQL query
            *args: Query parameters
        """
        if not self.pool:
            raise RuntimeError("Database pool is not initialized")
        
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)
    
    async def fetch(self, query: str, *args):
        """
        Executes a query and returns all results
        
        Args:
            query: SQL query
            *args: Query parameters
            
        Returns:
            List of records
        """
        if not self.pool:
            raise RuntimeError("Database pool is not initialized")
        
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)
    
    async def fetchrow(self, query: str, *args):
        """
        Executes a query and returns the first result
        
        Args:
            query: SQL query
            *args: Query parameters
            
        Returns:
            A record or None
        """
        if not self.pool:
            raise RuntimeError("Database pool is not initialized")
        
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)
    
    async def fetchval(self, query: str, *args):
        """
        Executes a query and returns a single value
        
        Args:
            query: SQL query
            *args: Query parameters
            
        Returns:
            A value or None
        """
        if not self.pool:
            raise RuntimeError("Database pool is not initialized")
        
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)
    
    async def init_tables(self):
        """Initializes the necessary database tables"""
        try:
            logger.info("Initializing database tables...")
            
            # Example: Server configuration table
            await self.execute("""
                CREATE TABLE IF NOT EXISTS guilds (
                    guild_id BIGINT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    prefix VARCHAR(10) DEFAULT '!',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Example: Users table
            await self.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username VARCHAR(32) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            logger.info("✅ Tables initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing tables: {e}")
            raise


# Global database instance
db = Database()

