import asyncpg


class DBClient:

    def __init__(self, dsn):
        self.dsn = dsn

    async def fetch_order(self, order_id):
        conn = await asyncpg.connect(self.dsn)
        row = await conn.fetchrow(
            "SELECT * FROM orders WHERE id=$1",
            order_id,
        )
        await conn.close()
        return row
