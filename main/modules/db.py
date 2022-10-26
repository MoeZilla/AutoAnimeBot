import asyncio
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from config import MONGO_DB_URI

print("[INFO]: STARTING MONGO DB CLIENT")
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.autoanime

animedb = db.animes
uploadsdb = db.uploads
channeldb = db.channel
votedb = db.votes


async def get_animesdb():
    anime_list = []
    async for name in animedb.find():
        anime_list.append(name)
    return anime_list

async def is_uploaded(name):
    data = await get_uploads()
    anime = [i["name"] for i in data]
    return name in anime

async def save_animedb(name, data):
    data = await animedb.insert_one({"name": name, "data": data})
    return


async def del_anime(name):
    data = await animedb.delete_one({"name": name})
    return


async def get_uploads():
    anime_list = []
    async for name in uploadsdb.find():
        anime_list.append(name)
    return anime_list


async def save_uploads(name):
    data = await uploadsdb.insert_one({"name": name})
    return


# channel

async def get_channel(anilist):
    anilist = f"a{str(anilist)}"
    anime = await channeldb.find_one({"anilist": anilist})
    if anime is None:
        return 0, 0
    msg = anime["msg"].replace("a", "")
    return int(msg), anime['episodes']


async def save_channel(anilist, msg, episodes=None):
    if episodes is None:
        episodes = []
    anilist = f"a{str(anilist)}"
    msg = f"a{str(msg)}"
    data = await channeldb.update_one({"anilist": anilist,}, {"$set": {"msg": msg, "episodes": episodes}},upsert= True)
    return

# vote


async def is_voted(id, user):
    id = f"a{str(id)}"
    votes = await votedb.find_one({"id": id})
    if votes is None:
        return 0
    return 0 if user not in votes["users"] else 1


async def save_vote(id, user):
    id = f"a{str(id)}"
    data = await votedb.update_one({"id": id}, {"$addToSet": {"users": user}}, upsert=True)
    return
