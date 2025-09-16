'''
aiosqlite replicates the standard sqlite3 module, 
but with async versions of all the standard connection and cursor methods, 
plus context managers for automatically closing connections and cursors
'''
import aiosqlite
import asyncio

async def async_fetch_users():
    #fetch all users
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users') as cursor:
            rows = await cursor.fetchall()
            print('All users: ')
            for row in rows:
                print(row)
            return rows

async def async_fetch_older_users():
    #fetch all users older than 40 yo
    async with aiosqlite.connect('users.db') as db:
        async with db.execute('SELECT * FROM users WHERE age > 40') as cursor:
            rows = await cursor.fetchall()
            print('All users older than 40 years old: ')
            for row in rows:
                print(row)
            return rows    

async def fetch_concurrently():
    #execute both queries concurrently
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())