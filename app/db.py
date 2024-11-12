import asyncpg
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self._pool = None
        self._db_url = os.getenv("PG_LINK")

        logger.info("Создан экземпляр Database с URL:s %", self._db_url)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

    async def connect(self):
        """Подключаемся к базе данных и создаем пул соединений"""
        try:
            self._pool = await asyncpg.create_pool(dsn=self._db_url)
            logger.info("Подключение к базе данных установлено")
            await self.create_table()
        except Exception as e:
            logger.error("Ошибка подключения к базе данных: %s", e)
            raise

    async def disconnect(self):
        """Закрываем соединение с базой данных"""
        if self._pool:
            await self._pool.close()
            logger.info("Соединение с базой данных закрыто")

    async def execute(self, query: str, *args):
        """Выполняем запрос без возврата данных (например, INSERT, UPDATE)"""
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                result = await connection.execute(query, *args)
        return result

    async def fetch(self, query: str, *args):
        """Выполняем запрос с возвратом данных (например, SELECT)"""
        async with self._pool.acquire() as connection:
            result = await connection.fetch(query, *args)
        return result

    async def fetchrow(self, query: str, *args):
        """Выполняем запрос, возвращающий одну строку"""
        async with self._pool.acquire() as connection:
            result = await connection.fetchrow(query, *args)
        return result

    async def fetchval(self, query: str, *args):
        """Выполняем запрос, возвращающий одно значение"""
        async with self._pool.acquire() as connection:
            result = await connection.fetchval(query, *args)
        return result

    async def create_table(self):
        """Создаёт таблицу user_contacts, если её нет, и добавляет столбец company_id_by_contact, если он отсутствует."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS aask_users (
        chat_id SERIAL PRIMARY KEY,
        group_name VARCHAR(10) NOT NULL
         );
        """
        await self.execute(create_table_query)
        logger.info("Таблица aask_users создана или уже существует.")

    async def add_contact(self, chat_id: int, group_name: str):
        """Добавляет контакт в таблицу user_contacts с учетом company_id_by_contact"""
        insert_query = """
        INSERT INTO aask_users (chat_id, group_name)
        VALUES ($1, $2)
        ON CONFLICT (chat_id) DO UPDATE SET group_name = $2;
        """
        await self.execute(insert_query, chat_id, group_name)
        logger.info(
            f"Контакт с chat_id={chat_id}, из группы={group_name} добавлен в базу данных."
        )
    async def get_group_name_by_chat_id(self, chat_id: int):
        query = """
           SELECT get_group_name
           FROM aask_users
           WHERE chat_id = $1;
           """
        company_id = await self.fetchval(query, chat_id)
        if company_id is not None:
            logger.info(f"Найден company_id={company_id} для chat_id={chat_id}.")
        else:
            logger.info(f"Компания для chat_id={chat_id} не найдена.")
        return company_id