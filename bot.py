from json import load
import requests
import asyncio
import random
from aiohttp import ClientSession
with open('bot_config.json', 'r') as conf:
    conf = load(conf)
number_of_users = conf.get('number_of_users', 5)
max_posts_per_user = conf.get('max_posts_per_user', 5)
max_likes_per_user = conf.get('max_likes_per_user', 3)
api = conf.get('url', 'http://localhost:8000/api/')


async def execute(n):
    async with ClientSession() as session:
        # create user
        payload = {'username': n, 'password': n, 'email': f'{n}q@c.com'}
        await session.post(url=f'{api}users/create/', headers={'content-type': 'application/json'}, json=payload)

        # log in
        resp = await session.post(url=f'{api}users/get_token/', json={'username': n, 'password': n})
        token_data = await (resp.json())
        token = token_data['token']

        # create posts
        posts_to_create = random.randint(0, max_posts_per_user)
        for post_num in range(posts_to_create):
            await session.post(url=f'{api}posts/create/',
                               headers={'Authorization': f'Token {token}'},
                               json={'title': f"{n}'s post number {post_num}", 'text': 'some text'})

        # get created posts ids
        resp = await session.get(url=f'{api}posts/')
        posts_list = await resp.json()
        posts_id_pool = [_['id'] for _ in posts_list]

        # like posts
        number_posts_to_like = min(random.randint(0, max_likes_per_user), len(posts_id_pool))
        for pk in random.choices(posts_id_pool, k=number_posts_to_like):
            await session.get(url=f'{api}posts/post={pk}/like=1/', headers={'Authorization': f'Token {token}'})
        print(f'user {n} created {posts_to_create} posts and liked {number_posts_to_like} '
              f'times from pool of existing number of {len(posts_id_pool)}')
    return


async def main():
    await asyncio.gather(*map(execute, [_ for _ in range(number_of_users)]))

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f'executed in {elapsed:0.2f} seconds.')
