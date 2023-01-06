import time

import vk_api

from config import token


def clear_friends():
    vk = vk_api.VkApi(token=token)

    value: int = 0
    try:
        response: list = vk.method("friends.get", dict(order="random", count=100))["items"]

        for user_id in response:
            vk.method("friends.delete", dict(user_id=user_id))
            value += 1
            time.sleep(3)
        return
    except Exception as error:
        return


def clear_dog():
    vk = vk_api.VkApi(token=token)
    try:
        list_user, who_delete, vol = vk.method("friends.get", {"fields": "deactivated"}), [], 0
        count, items = list_user["count"], list_user["items"]
        for user in items:
            who_delete.append(user)
        if count == 5000:
            list_user = vk.method("friends.get", {"fields": "deactivated", "offset": 5000})["items"]
            for user in list_user:
                who_delete.append(user)
        count = 0
        for i in who_delete:
            if i.get("deactivated") != None:
                count += 1
        if count == 0:
            return

        try:
            for i in who_delete:
                if i.get("deactivated") != None:
                    vk.method("friends.delete", {"user_id": i["id"]})
                    vol += 1
                    time.sleep(3)
        except Exception as error:
            return
        else:
            return
    except Exception as error:
        return


def clear_uved(token):
    vkme = vk_api.VkApi(token=token)

    response = vkme.method("execute.getWallSubscriptions")
    count, items, vol = response["count"], response["items"], 0
    if count == 0:
        return
    else:

        mass = []
        try:
            for user in items:
                mass.append(user["id"])
            for akk_id in mass:
                vkme.method("wall.unsubscribe", {"owner_id": akk_id, "subscribe": 1})
                vol += 1
            return
        except Exception as error:
            return
