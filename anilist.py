mport aiohttp
import re
import asyncio

query = """
query($query: String){
    User(name: $query){
        favourites{
            anime {
                nodes{
                    siteUrl
                    title {
                        romaji
                    }
                }
            }
        }
    }
}
"""




async def main():
    async with aiohttp.ClientSession() as ses:
        async with ses.post(
            'https://graphql.anilist.co',
            json={
                'query': query,
                'variables': {"query": 'rcage'}
            }
        ) as resp:
            r = (
                await resp.json()
            )['data']['User']['favourites']['anime']['nodes']
        await ses.close()
    new = '<!-- anilist_start-->\n'
    for x in r:
        new += f" - [{x['title']['romaji']}]({x['siteUrl']})\n"
    new += "<!-- anilist_end-->"
    with open("README.md", "r", encoding="utf8") as x:
        text = re.compile(
            "<!-- anilist_start-->.*<!-- anilist_end-->",
            re.DOTALL
        ).sub(new, x.read())
    with open("README.md", "w", encoding="utf8") as x:
        x.write(text)


if __name__ == "__main__":
    asyncio.run(main())
