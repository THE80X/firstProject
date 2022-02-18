import vk_api

import os

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import main_token, group_token

vk_session = vk_api.VkApi(token = main_token)
longpoll = VkBotLongPoll(vk_session, group_token)
#longpoll = VkLongPoll(vk_session)
#цифирки отвечают за id группы


vk_admin_permission = {'593644570', '404872983', '678212445', '655707464 ', '457933399'}

def sender(id, text):
    vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        #if event.to_me:
            if event.from_chat:
                msg = event.object.message['text']
                msg_id = event.object.message['conversation_message_id']
                msg_id_sender = event.object.message['from_id']
                id = event.chat_id
                counter = msg.count('|')
                print("сообщение: " + msg)
                print("кол-во палок: " + str(counter))
                print("id сообщения: " + str(msg_id))
                print("id беседы: " + str(id))
                print("id собеседника: " + str(msg_id_sender))


                if id == 1:
                    if msg.count('|')>=2:
                        massive = msg.split('|')
                        person_name = massive[1]
                        if os.path.exists("персонажи/посты/" + person_name.lower() + ".rtf"):
                            f = open("персонажи/посты/" + person_name.lower() + ".rtf", 'r')
                            text_old = f.read()
                            f.close()
                            f = open("персонажи/посты/" + person_name.lower() + ".rtf", 'w')
                            print("Старое текст: " + text_old)
                            f.write(text_old + msg + '\n')
                            f.close()
                        else:
                            vk_session.get_api().messages.delete(message_ids=msg_id, delete_for_all=1)
                    else:
                        vk_session.get_api().messages.delete(message_ids=msg_id, delete_for_all=1)


                if id == 2:
                    if msg.count('|') == 4:
                        massive = msg.split("|")
                        if massive[0]== "!Имя ":
                            name_old = massive[1].lower()
                            name_new = massive[3].lower()
                            if os.path.exists("персонажи/посты/"+name_old+".rtf"):
                                f = open("персонажи/посты/"+name_old+".rtf")
                                Owner_line = f.readline()
                                Owner_data = Owner_line.split("|")
                                Owner = Owner_data[1]
                                print("Владелец: " + Owner)
                                f.close()
                                if (int(Owner) == int(msg_id_sender)):
                                    f_old = os.path.join("D:\\Pythonchick\\firstProject\\персонажи\\посты", name_old+".rtf")
                                    f_new = os.path.join("D:\\Pythonchick\\firstProject\\персонажи\\посты", name_new+".rtf")
                                    os.rename(f_old,f_new)
                                    sender(id, "Имя персонажа было успешно изменено")
                                else:
                                    sender(id, "У вас нет такого персонажа")
                            else:
                                sender(id, "Нет такого персонажа")
                                print("Старое имя: "+name_old)