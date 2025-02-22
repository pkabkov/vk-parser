import os
import vk_api
from dotenv import load_dotenv
import pandas as pd
import csv
from pprint import pprint
from typing import List, Union, Dict, Any
import datetime

# Авторизация VK Api
load_dotenv()
session = vk_api.VkApi(token=os.getenv("TOKEN"))
vk = session.get_api()


# Выгрузка данных в таблицу
def data_upload(file_name: str, data: List[str]):
    ...


# Получение информации постов по айди группы или короткому имени
def get_posts(group: Union[int, str]) -> Dict[str, Any]:
    if type(group) is str:
        response = vk.wall.get(domain=group)
    else:
        response = vk.wall.get(owner_id=group)
    return {
        x["id"]: {
            "group_id": x["owner_id"],
            "text": x["text"],
            "likes": x["likes"]["count"],
            "views": x["views"]["count"]
        } for x in response["items"]
    }


# Получение информации по комментариям
def get_comments(posts: Dict[str, Any]) -> List[Dict[str, Any]]:
    comments = []
    for key, value in posts.items():
        response = vk.wall.getComments(owner_id=value["group_id"], post_id=key, need_likes=1, count=100)["items"]
        response = {key: list(
            filter(
                lambda verifiable: verifiable["text"].strip() != "",
                map(
                    lambda comment: {
                        "author_id": comment["from_id"],
                        "text": comment["text"],
                        "likes": comment.get("likes", {}).get("count", 0)
                    }, response
                ))
        )}
        comments.append(response)
    return comments


if __name__ == "__main__":
    pprint(get_comments(get_posts("foot.trans.news")))
