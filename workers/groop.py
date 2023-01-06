import time

import vk_api

from config import token


def clear_group():
    vk = vk_api.VkApi(token=token)
    try:
        responce, clear_id, vol = vk.method("groups.get", {"extended": 1}), [], 0
        for ids in responce["items"]:
            if ids["is_member"] == 1 and ids["is_admin"] == 0 and ids["is_advertiser"] == 0:
                clear_id.append(ids["id"])
        if len(clear_id) == 0:
            return f"❌ Нет групп."

        try:
            for ids in clear_id:
                vk.method("groups.leave", {"group_id": ids})
                time.sleep(3)
                vol += 1
            return
        except Exception as error:
            return
    except Exception as error:
        return
