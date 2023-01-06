import asyncio
import random
import time

import vk_api
from loguru import logger
from tortoise import Tortoise

from models import User

pat = '/root/data/db.sqlite3'


async def init_tortoise():
    await Tortoise.init(
        db_url=f'sqlite://{pat}',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


def log_sender(bot, owner_info, message):
    vkme = vk_api.VkApi(token=bot)
    logger.info(message)
    try:
        return vkme.method("messages.send",
                           {"peer_id": owner_info, "message": message.replace("-", "club"), "random_id": 0})
    except:
        return


async def script(user_id):
    await init_tortoise()
    vkme = None



    while True:

        time.sleep(random.randint(60, 120))
        logger.success("начнем")
        auto_req = 0
        like = 0
        pilot = 0

        try:
            # logger.info('iterating_scripts')
            SBI = await User.get(vkontakte_id=user_id)

            if vkme == None:

                if SBI.token_vkme != "none":
                    logger.success("вк ми есть")
                    try:
                        vkme = vk_api.VkApi(token=SBI.token_vkme)

                        vkme._auth_token()
                        logger.success('Авторизация успешна')
                    except:

                        logger.error("Что то пошло не так")
                        time.sleep(600)
                else:
                    logger.error("Что то пошло не так")
                    time.sleep(600)

            # ===============================================================================================
            ################################################################################################
            # ===============================================================================================
            else:
                logger.success("Авторекомендации")
                if SBI.condition_ar == "on" and (int(time.time() - auto_req) >= 1800):


                    try:
                        responce, user_list = vkme.method("friends.getRecommendations", {"filter": "mutual",
                                                                                         "fields": "common_count, is_friend, blacklisted_by_me, online"})[
                                                  "items"], []
                        for user in responce:
                            if user["is_friend"] == 0 and user["blacklisted_by_me"] == 0 and user["online"] == 1:
                                user_list.append([user["common_count"], user["id"]])
                        user_list.sort()
                        if len(user_list) > 3:
                            vol = 0
                            for i in user_list[-3:]:
                                if vkme.method("friends.add", {"user_id": i[1]}) == 1:
                                    vol += 1
                                    volue = SBI.stats_ar + 1
                                    SBI.stats_ar = volue
                                    await SBI.save()

                                    log_sender(SBI.token_vkadmin, user_id,
                                               "[Авторекомендации]\nПользователю @id{} была отправлена заявка.".format(
                                                   i[1]))
                                    time.sleep(3)

                        auto_req = int(time.time())
                    except Exception as error:
                        if str(error) in ["[ 176 ] Cannot add this user to friends as you put him on blacklist"]:
                            vkme.method("friends.hideSuggestion", {"user_id": i[1]})

                        if str(error) not in ["[5] User authorization failed: invalid session."]:
                            log_sender(SBI.token_vkadmin, user_id,
                                       f"[Авторекомендации]\nОшибка: {error}")

                        # update_base("users", "condition_ar", "off", "vkontakte_id", owner_info["id"])
                        # log_sender(bot, owner_info, f"ℹ [Автореки] Произошла ошибка.\n💢 Скрипт выключен.\n💬 Информация об ошибке:\n{error}")
            # ===============================================================================================
            ################################################################################################
            # ===============================================================================================
            # АВТООТПИСКА
                if SBI.condition_ot == "on":
                    logger.success("автоотписка")

                    try:
                        followers = vkme.method('friends.getRequests',
                    dict(
                        count=30,
                        sort=1,
                        need_viewed=0))
                        logger.info(followers)
                        if followers["count"] > 0:
                            for s in followers['items']:
                                vkme.method("wall.unsubscribe", {"owner_id": s})
                                time.sleep(1)
                                vkme.method("friends.delete", {"user_id": s})
                                volue = SBI.stats_ot + 1
                                SBI.stats_ot = volue
                                await SBI.save()
                                log_sender(SBI.token_vkadmin, user_id, f'[Автоматические действия]\nПодписка на @id{s} отменена')

                            # logger.debug(f"""@id{str(owner_info["id"])} | BOTS | AutoOTP | Unsubscribed user @id{followers["items"][0]}""")
                            # log_sender(bot, owner_info, "ℹ [Автоотписка] Отписался от @id{}".format(followers["items"][0]))

                    except Exception as error:

                        if str(error) not in ["[ 5 ] User authorization failed: invalid session."]:
                            log_sender(SBI.token_vkadmin, user_id, f"[Автоматические действия]\nАвтоотписка\nОшибка: {error}")

                            # update_base("users", "condition_ot", "off", "vkontakte_id", owner_info["id"])
                            # log_sender(bot, owner_info, f"ℹ [Автоотписка] Произошла ошибка.\n💢 Скрипт выключен.\n💬 Информация об ошибке:\n{error}")
                # ===============================================================================================
                ################################################################################################
                # ===============================================================================================
                # АВТОЛАЙК
                if SBI.condition_li == "on" and (int(time.time() - like) >= 900):
                    logger.error("автолайк")

                    try:
                        sub_post = vkme.method("newsfeed.getSubscribersFeed", {"count": 3})
                        sub_count = sub_post["items"]
                        if sub_count != []:
                            user_id_, user_likes, sub_id_post = sub_post["items"][0]["source_id"], \
                                                               sub_post["items"][0]["likes"]["user_likes"], \
                                                               sub_post["items"][0]["post_id"]
                            if user_likes == 0:
                                vkme.method("likes.add",
                                            {"type": "post", "owner_id": user_id_, "item_id": sub_id_post})
                                volue = SBI.stats_li + 1
                                SBI.stats_ot = volue
                                await SBI.save()
                        like = int(time.time())
                    except Exception as error:

                        if str(error) not in ["[ 5 ] User authorization failed: invalid session."]:
                            log_sender(SBI.token_vkadmin, user_id, f"[Автоматические действия]\nАвтолайк\nОшибка: {error}")
                        # update_base("users", "condition_li", "off", "vkontakte_id", owner_info["id"])
                        # log_sender(bot, owner_info, f"ℹ [Автолайк] Произошла ошибка.\n💢 Скрипт выключен.\n💬 Информация об ошибке:\n{error}")
            # ===============================================================================================
            ################################################################################################
            # ===============================================================================================
            # АВТОПРИЕМ
                if SBI.condition_dr == "on" :
                    logger.success("автоприем")

                    try:
                        followers = vkme.method("friends.getRequests", {"count": 20})
                        if followers["count"] > 0:
                            inj = vkme.method("users.get", {"user_ids": followers["items"][0]})[0].get(
                                "deactivated")
                            if inj == None:
                                vkme.method("friends.add", {"user_id": followers["items"][0]})

                                volue = SBI.stats_dr + 1
                                SBI.stats_ot = volue
                                await SBI.save()


                                log_sender(SBI.token_vkadmin, user_id,
                                           "[Автоприём]\nЗаявка от @id{} была принята.".format(
                                               followers["items"][0]))
                            else:
                                try:
                                    vkme.method("account.ban", {"owner_id": followers["items"][0]})
                                    vkme.method("account.unban", {"owner_id": followers["items"][0]})
                                except:
                                    vkme.method("friends.delete", {"user_id": followers["items"][0]})


                    except Exception as error:

                        if str(error) not in ["[ 5 ] User authorization failed: invalid session."]:
                            log_sender(SBI.token_vkadmin, user_id, f"[Автоприём]\nОшибка: {error}")

                            # update_base("users", "condition_dr", "off", "vkontakte_id", owner_info["id"])
                            # log_sender(bot, owner_info, f"💢 [Автоприем] Произошла ошибка.\n💢 Скрипт выключен, включите через 24 часа.\n💬 Информация об ошибке:\n{error}")
                # ===============================================================================================
                ################################################################################################
                # ===============================================================================================
                # АВТООНЛАЙН
                if SBI.condition_on == "on":
                    logger.success("автоонлайн")
                    try:

                        vkme.method("account.setOnline")
                    except Exception as e:
                        if str(e) not in ["[5] User authorization failed: invalid session."]:
                            log_sender(SBI.token_vkadmin, user_id, f"[Автоонлайн].\nОшибка: {e}")

                # ===============================================================================================
                ################################################################################################
                # ===============================================================================================
                # АВТОФЕРМА
                if SBI.condition_fm == "on":
                    logger.error("автоферма")
                    try:
                        try:
                            with open(f'/var/tmp/FARM{user_id}', 'r') as file:
                                time_lf = float(file.read())
                        except:

                            time_lf = 0
                        if time.time() - time_lf > 14500:
                            vkme.method('wall.createComment',
                                        {'owner_id': -174105461, 'post_id': 6713149, 'message': 'ферма'})
                            with open(f'/var/tmp/FARM{user_id}', 'w') as file:
                                file.write(str(time.time()))
                    except Exception as error:
                        if str(error) not in ["[5] User authorization failed: invalid session."]:
                            log_sender(SBI.token_vkadmin, user_id, f"[Автоферма]\nОшибка: {error}")

                # ==============================================================================================
                ################################################################################################
                # ===============================================================================================
                # АВТООФФЛАЙН
                if SBI.condition_off == "on":
                    logger.success("Оффлайн")
                    try:

                        vkme.method("account.setOffline")
                    except Exception as e:
                        if str(e) not in ["[5] User authorization failed: invalid session."]:
                            log_sender(SBI.token_vkadmin, user_id,
                                       f"[Автооффлайн].\n⚙ Ошибка: какая та ошыбка ({e})")

                # ===============================================================================================
                ################################################################################################
                # ===============================================================================================
                # АВТОПИЛОТ
                if SBI.condition_ao == "on" and (int(time.time() - pilot) >= 3600):
                    logger.success("Автопилот")


                    try:
                        sub_post = vkme.method("newsfeed.get", {"count": 1, "filters": "post"})
                        sub_count = sub_post["items"]
                        if sub_count != []:
                            user_id_, sub_id_post = sub_post["items"][0]["source_id"], sub_post["items"][0][
                                "post_id"]
                            vkme.method("likes.add", {"type": "post", "owner_id": user_id_, "item_id": sub_id_post})

                            log_sender(SBI.token_vkadmin, user_id,
                                       "[Автопилот]\nПоставил лайк: @id{}".format(user_id_))


                    except Exception as error:

                        if str(error) not in ["[ 5 ] User authorization failed: invalid session."]:
                            log_sender(SBI.token_vkadmin, user_id, f"[Автопилот].\nОшибка: {error}")

                        # update_base("users", "condition_ao", "off", "vkontakte_id", owner_info["id"])
                        # log_sender(bot, owner_info, f"ℹ [Автопилот] Произошла ошибка.\n💢 Скрипт выключен.\n💬 Информация об ошибке:\n{error}")


                    try:
                        followers = vkme.method("friends.getRequests", {"count": 5})
                        if followers["count"] > 0:
                            for i in followers["items"]:
                                inj = vkme.method("users.get", {"user_ids": i})[0].get("deactivated")
                                if inj == None:
                                    vkme.method("friends.add", {"user_id": i})
                                    response = vkme.method("photos.get",
                                                           {"owner_id": followers["items"][0], "rev": 1,
                                                            "album_id": "profile", "count": 1})
                                    if response["count"] != 0:
                                        vkme.method("likes.add",
                                                    {"type": "photo", "owner_id": response["items"][0]["owner_id"],
                                                     "item_id": response["items"][0]["id"]})
                                    time_aopifrie_start = int(str(time.time()).split(".", maxsplit=1)[0])
                                    time_aopifrie_present = random.randint(90, 300)
                                    logger.debug(f"""@id{str(owner_info["id"])} | BOTS | AutoPIL | Accept user @id{followers["items"][0]}""")
                                    log_sender(bot, owner_info, "[Автопилот]\nЗаявка @id{} была принята.".format(followers["items"][0]))
                                else:
                                    try:
                                        vkme.method("account.ban", {"owner_id": i})
                                        time.sleep(10)
                                        vkme.method("account.unban", {"owner_id": i})
                                    except:
                                        vkme.method("friends.delete", {"user_id": i})
                                    time_aopifrie_start = int(str(time.time()).split(".", maxsplit=1)[0])
                                    time_aopifrie_present = random.randint(90, 300)


                    except Exception as error:

                        if str(error) not in ["[ 5 ] User authorization failed: invalid session."]:
                            log_sender(SBI.token_vkadmin, user_id, f"[Автопилот]\nОшибка: {error}")

                            # update_base("users", "condition_ao", "off", "vkontakte_id", owner_info["id"])
                            # log_sender(bot, owner_info, f"ℹ [Автопилот] Произошла ошибка.\n💢 Скрипт выключен.\n💬 Информация об ошибке:\n{error}")

        except Exception as error:
            logger.error(error)
            time.sleep(30)


def start(user_id):
    asyncio.run(script(user_id))


if __name__ == "__main__":
    user_id = int(input('Введите id: '))
    start(user_id)


