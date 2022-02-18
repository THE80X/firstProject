import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from datetime import datetime


token = "cab597883f5eca90fb6db66e377e3b5e6c0fba88b4fb55d741631f3ac77a5b7df72cef13489dcb3b2e001"
vk_session = vk_api.VkApi(token=token)
longpoll=VkBotLongPoll(vk_session, '186698662')


def DebugP (text):
    logFile.write( str(datetime.strftime(datetime.now(), "%H:%M:%S")) + ' ' + text+'\n')

def addUser(Vk_Id):
    L_file = open('UsersInfo/User№' + str(Vk_Id) + '.txt', "w")
    L_file.write('-1\n')
    L_file.close()

def changeUserPairs(Vk_Id, New_Pair, New_ChatId = '-1'):
    L_file = open('UsersInfo/User№' + str(Vk_Id) + '.txt', "w")
    L_file.write(str(New_Pair) + '\n')
    L_file.write(str(New_ChatId) + '\n')
    L_file.close()

def getPair(Vk_Id):
    L_file = open('UsersInfo/User№' + str(Vk_Id) + '.txt', "r")
    out = int(str(L_file.readline()).replace('\n', ''))
    L_file.close()
    return (out)

def refreshInfoFile():
    L_file = open('Info.txt', 'w')
    L_file.write(str(UserInSearch) + '\n')
    L_file.close()

def getUserInSearch():
    L_file = open('Info.txt', 'r')
    out = int(str(L_file.readline()).replace('\n', ''))
    L_file.close()
    return (out)

def ChatLodgMassageAdd(Vk_Id, L_message, L_userChatId = 1):
    L_userfile = open('UsersInfo/User№' + str(Vk_Id) + '.txt', "r")
    L_chatId = str(((L_userfile.readlines())[L_userChatId]).replace('\n', ''))
    L_userfile.close()
    if L_chatId != '-1':
        L_file = open('ChatsData/' + L_chatId + '.txt', 'a')
        L_file.write(str(datetime.strftime(datetime.now(), "%Y!%m!%d_%H:%M:%S")) + '_' + str(Vk_Id) + ':' + L_message + '\n')
        L_file.close()

def getNewChatId():
    try:
        L_file = open('chatLogId.txt', 'r')
    except:
        open('chatLogId.txt', 'w').close()
        L_file = open('chatLogId.txt', 'r')
    L_Id = int('0' + L_file.read()) + 1
    L_file.close()
    L_file = open('chatLogId.txt', 'w')
    L_file.write(str(L_Id))
    L_file.close()
    return (str(datetime.strftime(datetime.now(), "%Y!%m!%d_%H!%M!%S_")) + str(L_Id))

try:
    UserInSearch = getUserInSearch()
except:
    UserInSearch = -1

while True:

    for event in longpoll.listen():

        with open('Logs/' + str(datetime.strftime(datetime.now(), "%Y!%m!%d")) + '.txt', 'a') as logFile:

            if event.type == VkBotEventType.MESSAGE_NEW:

                if event.from_user and not event.from_group:
                    L_Message = event.obj['text']
                    L_message = event.obj['text'].lower()
                    L_canTalk = bool(0)
                    L_userId = event.obj['peer_id']
                    # Проверка отправлено ли сообщение боту запись сообщения, создание переменной отвечающей за взаимодействие с пользователем

                    if L_message == '!help' or L_message == '!помощь':
                        vk_session.method('messages.send', {'user_id': L_userId, 'message': "!find или !поиск - подбирает случайного собеседника.\n"
                                                                                            "!trade или !товар - вызовает оператора для приобретения какого-либо товара, услуги.\n"
                                                                                            "!stop или !стоп - останвливает диалог, поиск собеседника или вызов оператора",
                                                            'random_id': 0})
                    else:
                        try:
                            L_Pair = getPair(L_userId)
                            # Проверка наличия пользователя в системе запись пары в переменную
                        except:
                            addUser(L_userId)
                            L_Pair = -1
                            DebugP('Пользователю №' + str(L_userId) + ' добавлен в базу данных')
                            # Добавляет бользователя в базу данных
                        if L_Pair >= 0:
                            # Проверка пользователя на наличие пары для диалога
                            if L_message != '!stop' and L_message != '!стоп':
                                # Проверка на запрос остановки диалога
                                try:

                                    if L_Message != '':
                                        vk_session.method('messages.send', {'user_id': L_Pair, 'message': L_Message, 'random_id': 0})
                                        ChatLodgMassageAdd(L_userId, L_Message)

                                except:

                                    vk_session.method('messages.send', {'user_id': L_userId, 'message': "Возникла непредвиденная ошибка, сообщение не было переданно, "
                                                                                                        "просьба сообщить админисрации группы.", 'random_id': 0})
                                    DebugP('Сообщение небыло передано пользователю №' + str(L_Pair) + ' неизвестная ошибка')

                                #try:
                                #    print(str(event.obj['attachments']))
                                #except:
                                #    print(',fu')

                            else:
                                DebugP('Пользователь №' + str(L_userId) + ' и пользователь№' + str(L_Pair) + ' были рассоеденены')
                                changeUserPairs(L_Pair, -1)
                                vk_session.method('messages.send', {'user_id': L_Pair,
                                                                    'message': "Ваш собеседник завершил диалог. Для поиска нового собеседника напишите !find или !поиск", 'random_id': 0})
                                L_Pair = -1
                                changeUserPairs(L_userId, -1)
                                vk_session.method('messages.send', {'user_id': L_userId, 'message': "Вы завершили диалог. Для поиска нового собеседника напишите !find или !поиск", 'random_id': 0})
                                L_canTalk = bool(1)
                                # Проверяет наличие пользователя в базе данных и наличие у него пары, если условия соблюдены отправляет сообщение партнеру так же разединяет пользователей

                        if L_Pair == -1:
                            if L_message == "!find" or L_message == "!поиск":

                                # Модуль подбора собеседника
                                if UserInSearch != -1:
                                    L_newChatId = getNewChatId()
                                    changeUserPairs(L_userId, UserInSearch, L_newChatId)
                                    changeUserPairs(UserInSearch, L_userId, L_newChatId)
                                    L_Pair = UserInSearch
                                    vk_session.method('messages.send', {'user_id': L_userId, 'message': "Собеседник найден!", 'random_id': 0})
                                    vk_session.method('messages.send', {'user_id': L_Pair, 'message': "Собеседник найден!", 'random_id': 0})
                                    DebugP('Пользователю №' + str(L_userId) + ' подобран в пару пользователь №' + str(L_Pair) + ', данные о сообщениях в файле:' + L_newChatId)
                                    UserInSearch = -1
                                    refreshInfoFile()
                                else:
                                    UserInSearch = L_userId
                                    refreshInfoFile()
                                    changeUserPairs(L_userId, -2)
                                    L_Pair = -2
                                    vk_session.method('messages.send', {'user_id': L_userId, 'message': "Подбираем собеседника!", 'random_id': 0})
                                    DebugP('Пользователь №' + str(L_userId) + ' в активном поиске!')

                            elif L_message == '!trade' or L_message == '!товар' or str(event.obj['attachments']).find('market') != -1:
                                vk_session.method('messages.send', {'user_id': 457933399, 'message': "Ванек, новый клиент!", 'random_id': 0})
                                vk_session.method('messages.send', {'user_id': L_userId, 'message': "Ожидайте ответа оператора. Если вы хотите отменить запрос напишите !stop или !стоп",
                                                                    'random_id': 0})
                                vk_session.method('messages.markAsImportantConversation', {'peer_id': L_userId, 'important': 1, 'group_id': 186698662})
                                changeUserPairs(L_userId, -3, getNewChatId())
                                L_Pair = -3
                                DebugP('Пользователь№' + str(L_userId) + ' ожидает ответа администратора.')

                            elif not L_canTalk:
                                vk_session.method('messages.send', {'user_id': L_userId, 'message': "Неизвесный запрос, для получения полного спика команд напишите !help или !помощь",
                                                                    'random_id': 0})
                        # Модуль подбора собеседника

                        elif L_Pair == -2:
                            if L_message == '!stop' or L_message == '!стоп':
                                L_Pair = -1
                                changeUserPairs(L_userId, -1)
                                UserInSearch = -1
                                refreshInfoFile()
                                vk_session.method('messages.send', {'user_id': L_userId, 'message': "Поиск собеседника остановлен, что бы начать поиск напишите !поиск или !find", 'random_id': 0})
                            else:
                                vk_session.method('messages.send', {'user_id': L_userId,
                                                                    'message': "Вы находитесть с состоянии поиска собеседника, если хотите прекраить поиск напишите !stop или !стоп.", 'random_id': 0})

                        elif L_Pair == -3:
                            if L_message == '!stop' or L_message == '!стоп':
                                L_Pair = -1
                                changeUserPairs(L_userId, -1)
                                vk_session.method('messages.markAsImportantConversation', {'peer_id': L_userId, 'important': 0, 'group_id': 186698662})
                                vk_session.method('messages.send', {'user_id': L_userId, 'message': "Запрос отменен.", 'random_id': 0})
                            else:
                                #vk_session.method('messages.send', {'user_id': 457933399, 'message': "Ванек, клиент написал!", 'random_id': 0})
                                ChatLodgMassageAdd(L_userId, L_Message)

            elif event.type == VkBotEventType.MESSAGE_REPLY:
                try:
                    L_userId = event.obj['peer_id']
                    if getPair(L_userId) == -3:
                        L_Message = event.obj['text']
                        L_message = event.obj['text'].lower()
                        try:
                            if L_message != '!stop' and L_message != '!стоп':
                                ChatLodgMassageAdd(L_userId, 'Admin_' + L_Message)
                            else:
                                if getPair(L_userId) == -3:
                                    changeUserPairs(L_userId, -1)
                                    vk_session.method('messages.markAsImportantConversation', {'peer_id': L_userId, 'important': 0, 'group_id': 186698662})
                                    vk_session.method('messages.send', {'user_id': L_userId, 'message': "Администратор отключил вас от беседы.", 'random_id': 0})
                                else:
                                    vk_session.method('messages.send', {'user_id': L_userId, 'message': "Админ - ты дебил.", 'random_id': 0})
                        except:
                            DebugP('Какая-то хуета с отправкой сообщений')
                except:
                    print(event.obj['peer_id'])
