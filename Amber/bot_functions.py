from Amber.settings import *
from Amber.gpt_functions import *
import random
from matplotlib import pyplot as plt, ticker
from telebot import types

global mess, data

list_btns_1 = [types.InlineKeyboardButton(text=x, callback_data=x)
               if x not in data.keys()
               else types.InlineKeyboardButton(text=f'{x}: {data[x]}', callback_data=x)
               for x in questions.keys()] + [
                  types.InlineKeyboardButton(text='Начать общение с Эмбер', callback_data='Общение с Эмбер')]

list_btns_2 = [types.InlineKeyboardButton(text='Настройки Эмбер', callback_data='settings'),
               types.InlineKeyboardButton(text='Твои данные ', callback_data='info_user'),
               types.InlineKeyboardButton(text='Общаться с Эмбер', callback_data='Общение с Эмбер')]

list_btns_3 = [types.InlineKeyboardButton(text=x, callback_data=x)
               if x not in settings_amber.keys()
               else types.InlineKeyboardButton(text=f'{x}: {settings_amber[x]}', callback_data=x)
               for x in settings_amber_questions.keys()] \
              + [types.InlineKeyboardButton(text=answers['close_settings'], callback_data='close_settings')]


def markup_1(list_btns):
    return types.InlineKeyboardMarkup().add(*list_btns[0:2]) \
        .row(*list_btns[2:4]).row(*list_btns[4:6]).row(list_btns[-1])


def markup_2(list_btns):
    return types.InlineKeyboardMarkup().add(*list_btns[:-1]).row(list_btns[-1])


def markup_3(list_btns):
    return types.InlineKeyboardMarkup().add(*list_btns[0:5]) \
        .row(*list_btns[5:7]).row(*list_btns[7:9]).row(*list_btns[9:11]).row(list_btns[11])


lives = 3
count_mess = 0

mood = [0, 0, 0]
moods = [mood.copy()]

mod_18 = False
time_questions = True

mess_id_plt = None
msg_inf = None
sttngs = None
help_msg = None

id_edit, id_add = 0, 0
m1, m2 = 0, 0

creator = "Glazxchek"


def main(bot):
    def system_text(message, text, reply_markup=None):
        return bot.send_message(message.chat.id, f'<i>{text}</i>', parse_mode='HTML', reply_markup=reply_markup)

    def heading_text(message, text, reply_markup=None):
        return bot.send_message(message.chat.id, f'<b>{text}</b>', parse_mode='HTML', reply_markup=reply_markup)

    @bot.message_handler(commands=['start'])
    def start(message):
        global mood, moods, mess, lives, help_msg
        global markup_1, msg_inf, list_btns_1, list_btns_3

        mess[0] = {"role": "system", "content": '\n'.join(content)}
        list_btns_1[0].text = f'Имя: {message.from_user.first_name}'

        if message.from_user.username == creator:
            lives = 99999999

        if lives <= 0:
            bot.send_message(
                chat_id=message.chat.id,
                text=answers['ban'],
            )
        elif time_questions:
            help_msg = help(message)
            msg_inf = heading_text(message, text='Выбери действие:', reply_markup=markup_2(list_btns_2))
        else:
            begin_dialogue(message)

    @bot.message_handler(commands=['help'])
    def help(message):
        img_1 = types.InputMediaPhoto(open('Amber/data/help/1.jpg', 'rb'))
        img_2 = types.InputMediaPhoto(open('Amber/data/help/2.jpg', 'rb'))
        img_2.parse_mode = 'HTML'
        img_2.caption = open('Amber/data/help/help.txt', encoding='utf-8').read()
        if message.from_user.username == creator:
            img_2.caption += '\n\n/connect_module_18\n /disconnect_module_18'
        return bot.send_media_group(message.chat.id, media=[img_1, img_2])

    @bot.message_handler(commands=['settings'])
    def settings(message):
        global time_questions, list_btns_3, sttngs
        time_questions = True
        list_btns_3[-1].callback_data = 'close_settings'
        sttngs = heading_text(message,
                              answers['settings'],
                              reply_markup=markup_3(list_btns_3))

    def begin_dialogue(message):
        global m1, m2
        global time_questions
        global msg_inf, mess, mood

        mood, moods = [0, 0, 0], [mood.copy()]
        mess = [mess[0]]
        time_questions = False
        lives_text = ['попыток', 'попытка', 'попытки', 'попытки']

        if msg_inf:
            bot.delete_message(msg_inf.chat.id, msg_inf.message_id)
            msg_inf = None

        msg = system_text(message, text='Диалог начат!')
        if lives == 3:
            system_text(message, text=f'У вас есть {lives} {lives_text[lives]} впечатлить Эмбер')
        else:
            system_text(message, text=f'У вас есть {lives} попыток впечатлить Эмбер')

        bot.pin_chat_message(msg.chat.id, msg.id)

        m1 = msg.message_id
        m2 = message.chat.id

        mess.append({
            "role": "system",
            "content": f'Эмбер знает перечисленную ниже информацию о собеседнике:'
                       f'\n {[f"{i} - {data[i]}" for i in list(data.keys())]}'
                       f'Эмбер полность соответствовует всем параметрам ниже:'
                       + ''.join([f"{i} - {settings_amber_questions[i]}" for i in settings_amber_questions.keys()])
        })

    @bot.message_handler(commands=['info_user'])
    def info_user(message):
        global time_questions
        global msg_inf
        global list_btns

        if not time_questions:
            list_btns_1[-1].text = 'Продолжить общение с Эмбер'
            list_btns_1[-1].callback_data = 'Продолжить общение с Эмбер'

            time_questions = True
            msg_inf = bot.send_message(
                chat_id=message.chat.id,
                text=f'<b>Информация о тебе:</b>',
                reply_markup=types.InlineKeyboardMarkup().add(*list_btns_1[0:-1]).row(list_btns_1[-1]),
                parse_mode='HTML'
            )

    @bot.message_handler(commands=['edit'])
    def edit(message):
        global id_edit
        ms = bot.send_message(message.chat.id, 'Отправьте новый log')
        id_edit = ms.message_id

    @bot.message_handler(commands=['add'])
    def add(message):
        global id_add
        ms = bot.send_message(message.chat.id, 'Отправьте новый пункт')
        id_add = ms.message_id

    @bot.message_handler(commands=['plt'])
    def plt_command(message, rm=True, text=None):
        global mess_id_plt
        if len(moods) > 1:
            fig, ax = plt.subplots()

            ax.set_ylim([-10, 10])

            fig.set_figwidth(8)
            fig.set_figheight(8)

            ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
            ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

            plt.plot([i[0] for i in moods], label='Влюбленность', linewidth=3, alpha=0.6,
                     color=status_color_plt['Влюбленность'])
            plt.plot([i[1] for i in moods], label='Настроение', linewidth=3, alpha=0.6,
                     color=status_color_plt['Настроение'])
            plt.plot([i[2] for i in moods], label='Возбужденность', linewidth=3, alpha=0.6,
                     color=status_color_plt['Возбужденность'])

            plt.legend(loc='lower left')
            plt.title(answers['plt'])
            plt.savefig('Amber/data/charts/all.png')

            btns = [types.InlineKeyboardButton(text=i, callback_data=i) for i in
                    ['Влюбленность', 'Настроение', 'Возбужденность']]
            markup_2 = types.InlineKeyboardMarkup().add(*btns)

            if rm:
                mess_id_plt = bot.send_photo(
                    message.chat.id,
                    photo=open('Amber/data/charts/all.png', 'rb'),
                    reply_markup=markup_2,
                    caption=text,
                )
            else:
                bot.send_photo(
                    message.chat.id,
                    photo=open('Amber/data/charts/all.png', 'rb'),
                    reply_markup=markup_2,
                    caption=text,
                )
        else:
            system_text(message, answers['plt_no_data'])

    @bot.message_handler(commands=['del_memory'])
    def erase_memory(message):
        global mess
        system_text(message, answers['erase_memory'])
        mess = [mess[0]]

    @bot.message_handler(commands=['del_memory_msg'])
    def erase_memory_message(message):
        global mess
        system_text(message, answers['erase_memory_message'])
        del mess[-3:-1]

    @bot.message_handler(commands=['connect_module_18'])
    def module_18(message):
        global dialogue_len, mod_18
        if mod_18:
            system_text(message, answers['module_18_yes_connect'])
        elif 'Возраст' in data.keys():
            if data['Возраст'].isnumeric() and int(data['Возраст']) >= 18:
                mod_18 = True
                mess[0]['content'] += '\n'.join(
                    open('Amber/data/tasks/module_18.txt', 'r', encoding="utf-8").readlines())
                system_text(message, answers['module_18_yes_connect'])
            else:
                system_text(message, answers['module_18_access'])
        else:
            list_btns_4 = [types.InlineKeyboardButton(text='Да', callback_data='yes_module_18'),
                           types.InlineKeyboardButton(text='Нет', callback_data='no_module_18'), ]

            bot.send_message(message.chat.id,
                             '<b>Вам есть 18 лет?</b> \nДанная функция содержит интимный характер.',
                             reply_markup=types.InlineKeyboardMarkup().add(*list_btns_4),
                             parse_mode='HTML')

    @bot.message_handler(commands=['disconnect_module_18'])
    def no_module_18(message):
        if mod_18:
            mess[0]['content'] = content
            system_text(message, answers['module_18_disconnect'])
        else:
            system_text(message, answers['module_18_not_connect'])

    @bot.callback_query_handler(func=lambda message: True)
    def answer(call):
        global question, time_questions, questions_limit, \
            dialogue_len, list_btns_1, markup_1, mod_18, msg_inf, sttngs

        if call.data == 'start':
            start(call.message)
        if call.data == 'settings':
            bot.edit_message_text(answers['settings'], msg_inf.chat.id, msg_inf.message_id)
            list_btns_3[-1].callback_data = 'close_settings_start'
            bot.edit_message_reply_markup(msg_inf.chat.id, msg_inf.message_id, reply_markup=markup_3(list_btns_3))
        if call.data == 'close_settings_start':
            bot.edit_message_text('Выбери действие', msg_inf.chat.id, msg_inf.message_id)
            bot.edit_message_reply_markup(msg_inf.chat.id, msg_inf.message_id, reply_markup=markup_2(list_btns_2))
        if call.data == 'info_user':
            bot.edit_message_text(answers['info_user'], msg_inf.chat.id, msg_inf.message_id)
            list_btns_1[-1].callback_data, list_btns_1[-1].text = 'close_settings_start', 'Закрыть заполнение данных'
            bot.edit_message_reply_markup(msg_inf.chat.id, msg_inf.message_id, reply_markup=markup_1(list_btns_1))
        elif time_questions:

            if call.data in questions.keys():
                question = [bot.send_message(chat_id=call.message.chat.id, text=questions[call.data]), call.data]

            elif call.data in settings_amber_questions.keys():
                question = [
                    bot.send_message(chat_id=call.message.chat.id, text=settings_amber_questions[call.data]), call.data
                ]
            elif call.data == 'close_settings':
                time_questions = False
                bot.delete_message(sttngs.chat.id, sttngs.message_id)
                if settings_amber_copy != settings_amber:
                    system_text(call.message, answers['setting_save'])

            elif call.data == 'Общение с Эмбер':
                begin_dialogue(call.message)

            elif call.data == 'Продолжить общение с Эмбер':
                bot.delete_message(msg_inf.chat.id, msg_inf.message_id)
                system_text(call.message, answers['dialogue_last'])

        elif call.data in list(status.keys()) + ['все']:
            markup_plt = types.InlineKeyboardMarkup().add(
                *[types.InlineKeyboardButton(text=i, callback_data=i) for i in
                  [i for i in (*list(status.keys()), 'все') if i != call.data]])
            fig_1, ax_1 = plt.subplots()
            ax_1.set_ylim([-10, 10])

            fig_1.set_figwidth(8)
            fig_1.set_figheight(8)

            ax_1.xaxis.set_major_locator(ticker.MultipleLocator(1))
            ax_1.yaxis.set_major_locator(ticker.MultipleLocator(1))
            eng = {'Влюбленность': 'love', 'Настроение': 'sense', 'Возбужденность': 'excite', 'все': 'all'}
            if call.data != 'все':
                plt.plot([i[list(status.keys()).index(call.data)] for i in moods],
                         label=call.data, linewidth=3, alpha=0.6, color=status_color_plt[call.data])
                plt.legend(loc='lower left')
                plt.title(answers['plt'])
            else:
                plt.plot([i[0] for i in moods], label='Влюбленность', linewidth=3, alpha=0.6,
                         color=status_color_plt['Влюбленность'])
                plt.plot([i[1] for i in moods], label='Настроение', linewidth=3, alpha=0.6,
                         color=status_color_plt['Настроение'])
                plt.plot([i[2] for i in moods], label='Возбужденность', linewidth=3, alpha=0.6,
                         color=status_color_plt['Возбужденность'])
                plt.legend(loc='lower left')
                plt.title(f'График {call.data} Эмбер')
            plt.savefig(f'Amber/data/charts/{eng[call.data]}.png')
            bot.edit_message_media(chat_id=mess_id_plt.chat.id,
                                   message_id=mess_id_plt.message_id,
                                   media=types.InputMediaPhoto(open(f'Amber/data/charts/{eng[call.data]}.png', 'rb')),
                                   reply_markup=markup_plt)
            plt.close('all')

        if 'module_18' in call.data:
            if call.data == 'yes_module_18':
                mod_18 = True
                mess[0]['content'] += ' '.join(
                    open('Amber/data/tasks/module_18.txt', 'r', encoding="utf-8").readlines())
                bot.delete_message(call.message.chat.id, call.message.message_id, 5)
                system_text(call.message, answers['module_18_connect'])
            elif call.data == 'no_module_18':
                system_text(call.message, answers['module_18_access'])

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        global data, old_list_btns_3, list_btns_1, list_btns_3, question, questions_limit, time_questions, mess
        global mood, moods, id_edit, id_add, count_mess, lives, mess_id_plt, sttngs

        if time_questions and question:
            if question[1] in settings_amber_questions.keys():
                settings_amber[question[1]] = message.text
                old_list_btns_3 = [i.text for i in list_btns_3.copy()]
                for j in list_btns_3:
                    if j.text.split(':')[0] in settings_amber.keys():
                        j.text = f'{j.callback_data}: {settings_amber[j.callback_data]}'
                if old_list_btns_3 != [i.text for i in list_btns_3]:
                    if sttngs == None:
                        bot.edit_message_reply_markup(msg_inf.chat.id, msg_inf.message_id,
                                                      reply_markup=markup_3(list_btns_3))
                    else:
                        bot.edit_message_reply_markup(sttngs.chat.id, sttngs.message_id,
                                                      reply_markup=markup_3(list_btns_3))
            else:
                data[question[1]] = message.text
                if 'Возраст' in data.keys() and int(data['Возраст']) < 18 and mod_18:
                    no_module_18(message)
                old_list_btns = [i.text for i in list_btns_1.copy()]
                for i in list_btns_1:
                    if i.text in data.keys():
                        i.text = f'{i.callback_data}: {data[i.callback_data]}'

                if old_list_btns != [i.text for i in list_btns_1]:
                    bot.edit_message_reply_markup(msg_inf.chat.id, msg_inf.message_id,
                                                  reply_markup=markup_1(list_btns_1))
        elif not time_questions:
            bot.send_chat_action(chat_id=message.chat.id, action='typing')
            if id_edit + 1 == message.message_id:
                mess[0]['content'] = message.text
                system_text(message, answers['edit'])
                return None

            if id_add + 1 == message.message_id:
                mess[0]['content'] += "\n" + message.text
                system_text(message, answers['add'])
                return None

            count_mess += 1
            mess = update(mess, 'user', message.text)
            model_response = get_response(
                messages=mess,
                temperature=float(settings_amber['temperature']),
                max_tokens=int(settings_amber['max_tokens']),
                top_p=int(settings_amber['top_p']),
                frequency_penalty=int(settings_amber['frequency_penalty']),
                presence_penalty=int(settings_amber['presence_penalty']),
            )
            mess = update(mess, 'assistant', model_response)

            if mess_id_plt:
                bot.delete_message(mess_id_plt.chat.id, mess_id_plt.message_id)
                mess_id_plt = None
            if "BAN" in model_response \
                    or "Бан" in model_response \
                    or "бан" in model_response:
                lives -= 1
                system_text(message, answers['ban'])
                heading_text(message, answers['plt_ban'])
                plt_command(message, rm=False)
                bot.edit_message_text(chat_id=m2, message_id=m1, text=answers['ban_title'])
                markup = types.InlineKeyboardMarkup()
                btn = types.InlineKeyboardButton(text="Давай", callback_data='start')
                markup.add(btn)
                bot.send_message(message.chat.id, reply_markup=markup, text=answers['after_ban'])

            elif "IGNOR" in model_response:
                print("IGNOR")

            elif "PHOTO" in model_response and photos:
                photo = photos[random.randint(0, len(photos) - 1)]
                bot.send_photo(message.chat.id,
                               photo=open(photo, 'rb'),
                               caption=model_response.replace('"PHOTO"', '').split('|')[-1])
                del photo

            else:
                bot.send_message(message.chat.id, model_response.split('|')[-1])

                if model_response.count('|') == 4:
                    for x in range(len(status)):
                        try:
                            mood[x] = int(model_response.split('|')[x + 1])
                        except:
                            pass

                moods.append(mood.copy())

                txt_emj = f'💎{num_tokens_from_messages(mess)} 💬{count_mess} ⭐' \
                          f'{lives if message.from_user.username != creator else "∞"} |' + ''.join(
                    [f' {list(status.values())[x][mood[x] + 9]}' f'{mood[x]} ' for x in range(len(status))])
                txt_inf = f'Жизни: {lives}\nСообщений: {count_mess}\n' + ''.join([f'{list(status.keys())[x]}: '
                                                                                  f'{mood[x]}\n' for x in
                                                                                  range(len(status))]) \
                          + f'Токены: {num_tokens_from_messages(mess)}'

                bot.edit_message_text(chat_id=m2, message_id=m1, text=txt_emj)
                bot.edit_message_text(chat_id=m2, message_id=m1 + 1, text=txt_inf)

                while num_tokens_from_messages(mess) > (4000 - int(settings_amber['max_tokens'])):
                    del mess[1]

    bot.polling()
