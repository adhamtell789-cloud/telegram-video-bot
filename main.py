import asyncio
import aiohttp
import random
import string

letters = string.ascii_lowercase + string.digits

def generate_username():
    return ''.join(random.choice(letters) for _ in range(4))

async def check(session, username):
    url = f"https://www.instagram.com/{username}/"
    try:
        async with session.get(url) as r:
            if r.status == 404:
                print("AVAILABLE:", username)
    except:
        pass

async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = []
            for _ in range(200):  # عدد الفحوصات في نفس الوقت
                tasks.append(check(session, generate_username()))
            await asyncio.gather(*tasks)

asyncio.run(main())
