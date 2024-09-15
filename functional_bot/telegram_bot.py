import re
import os
import datetime
import logging

logging.disable(logging.CRITICAL)

if logging.getLogger().isEnabledFor(logging.CRITICAL):
    logging.basicConfig(filename=f'log-telegram-bot-{os.path.basename(__file__)}-{datetime.datetime.now()}.txt',
                        level=logging.INFO,
                        format=' %(asctime)s - %(levelname)s - %(message)s'
                        )

logger = logging.getLogger(__name__)

from dotenv import load_dotenv
from pathlib import Path

from telegram import Update, ForceReply, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler


class DotDict(dict):
    """Позволяет обращаться к элементам словаря через точку."""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class TelegramBot:
    def __init__(self):
        logger.info(f'Start {self.__init__.__name__}')
        dotenv_path = Path('.env')
        load_dotenv(dotenv_path=dotenv_path)

        self.tm_token__ = os.getenv('TM_TOKEN')
        logger.info('Get TM_TOKEN')
        self.chat_id = os.getenv('CHAT_ID')
        logger.info('Get CHAT_ID')

        self.commands = DotDict(
                {
                        'start'           : DotDict(
                                {
                                        'command'    : 'start',
                                        'button'     : '/start',
                                        'state_point': None,
                                        'callback'   : self.command_Start,
                                        }
                                ),
                        'cancel'          : DotDict(
                                {
                                        'command'    : 'cancel',
                                        'button'     : '/cancel',
                                        'state_point': None,
                                        'callback'   : self.command_Cancel,
                                        }
                                ),
                        'help'            : DotDict(
                                {
                                        'command'    : 'help',
                                        'button'     : '/help',
                                        'state_point': None,
                                        'callback'   : self.command_Help,
                                        }
                                ),
                        'echo'            : DotDict(
                                {
                                        'command'    : 'echo',
                                        'button'     : '/echo',
                                        'state_point': None,
                                        'callback'   : self.command_Echo,
                                        }
                                ),

                        ### 1. Поиск информации в тексте и её вывод.
                        'findEmails'      : DotDict(
                                {
                                        'command'    : 'find_email',
                                        'button'     : '/find_email',
                                        'state_point': 'find_email',
                                        'callback'   : self.command_FindEmails,
                                        }
                                ),
                        'findPhoneNumbers': DotDict(
                                {
                                        'command'    : 'find_phone_number',
                                        'button'     : '/find_phone_number',
                                        'state_point': 'find_phone_number',
                                        'callback'   : self.command_FindPhoneNumbers,
                                        }
                                ),

                        ### 2. Проверка сложности пароля регулярным выражением.
                        'verifyPassword'  : DotDict(
                                {
                                        'command'    : 'verify_password',
                                        'button'     : '/verify_password',
                                        'state_point': 'verify_password',
                                        'callback'   : self.command_VerifyPassword,
                                        }
                                ),
                        ### 3. Мониторинг Linux-системы.

                        ## 3.1. Сбор информации о системе.

                        # 3.1.1. О релизе.
                        'getRelease'      : DotDict(
                                {
                                        'command'    : 'get_release',
                                        'button'     : '/get_release',
                                        'state_point': 'get_release',
                                        'callback'   : self.command_GetRelease,
                                        }
                                ),

                        # 3.1.2. Об архитектуры процессора, имени хоста системы и версии ядра.
                        'getUname'        : DotDict(
                                {
                                        'command'    : 'get_uname',
                                        'button'     : '/get_uname',
                                        'state_point': 'get_uname',
                                        'callback'   : self.command_GetUname,
                                        }
                                ),

                        # 3.1.3. О времени работы.
                        'getUptime'       : DotDict(
                                {
                                        'command'    : 'get_uptime',
                                        'button'     : '/get_uptime',
                                        'state_point': 'get_uptime',
                                        'callback'   : self.command_GetUptime,
                                        }
                                ),

                        ## 3.2. Сбор информации о состоянии файловой системы.
                        'getDF'           : DotDict(
                                {
                                        'command'    : 'get_df',
                                        'button'     : '/get_df',
                                        'state_point': 'get_df',
                                        'callback'   : self.command_GetDF,
                                        }
                                ),

                        ## 3.3. Сбор информации о состоянии оперативной памяти.
                        'getFree'         : DotDict(
                                {
                                        'command'    : 'get_free',
                                        'button'     : '/get_free',
                                        'state_point': 'get_free',
                                        'callback'   : self.command_GetFree,
                                        }
                                ),

                        ## 3.4. Сбор информации о производительности системы.
                        'getMpstat'       : DotDict(
                                {
                                        'command'    : 'get_mpstat',
                                        'button'     : '/get_mpstat',
                                        'state_point': 'get_mpstat',
                                        'callback'   : self.command_GetMpstat,
                                        }
                                ),

                        ## 3.5. Сбор информации о работающих в данной системе пользователях.
                        'getW'            : DotDict(
                                {
                                        'command'    : 'get_w',
                                        'button'     : '/get_w',
                                        'state_point': 'get_w',
                                        'callback'   : self.command_GetW,
                                        }
                                ),

                        ## 3.6. Сбор логов.

                        # 3.6.1. Последние 10 входов в систему.
                        'getAuths'        : DotDict(
                                {
                                        'command'    : 'get_auths',
                                        'button'     : '/get_auths',
                                        'state_point': 'get_auths',
                                        'callback'   : self.command_GetAuths,
                                        }
                                ),
                        # 3.6.2. Последние 5 критических событий.
                        'getCritical'     : DotDict(
                                {
                                        'command'    : 'get_critical',
                                        'button'     : '/get_critical',
                                        'state_point': 'get_critical',
                                        'callback'   : self.command_GetCritical,
                                        }
                                ),

                        ## 3.7 Сбор информации о запущенных процессах.
                        'gepPS'           : DotDict(
                                {
                                        'command'    : 'get_ps',
                                        'button'     : '/get_ps',
                                        'state_point': 'get_ps',
                                        'callback'   : self.command_GetPS,
                                        }
                                ),

                        ## 3.8 Сбор информации об используемых портах.
                        'getSS'           : DotDict(
                                {
                                        'command'    : 'get_ss',
                                        'button'     : '/get_ss',
                                        'state_point': 'get_ss',
                                        'callback'   : self.command_GetSS,
                                        }
                                ),

                        ## 3.9 Сбор информации об установленных пакетах.
                        'getAptList'      : DotDict(
                                {
                                        'command'    : 'get_apt_list',
                                        'button'     : '/get_apt_list',
                                        'state_point': 'get_apt_list',
                                        'callback'   : self.command_GetAptList,
                                        }
                                ),
                        },
                )
        logger.info(f'Stop {self.__init__.__name__}')

    # Функция для создания кнопок основных запросов
    def keyboard_menu_main(self):
        logger.info(f'Start {self.keyboard_menu_main.__name__}')
        return ReplyKeyboardMarkup([
                [KeyboardButton(self.commands.start.button)],
                [KeyboardButton(self.commands.help.button)],
                [KeyboardButton(self.commands.findPhoneNumbers.button)],
                ], resize_keyboard=True
                )

    # Функция для создания кнопки отмены запроса
    def keyboard_menu_cancel(self):
        logger.info(f'Start {self.keyboard_menu_cancel.__name__}')
        return ReplyKeyboardMarkup([
                [KeyboardButton(self.commands.cancel.button)],
                ], resize_keyboard=True
                )

    def command_Start(self, update: Update = None, context=None):
        logger.info(f'Start {self.command_Start.__name__}')
        if update:
            user = update.effective_user
            update.message.reply_text(
                    f'Привет {user.full_name}!',
                    reply_markup=self.keyboard_menu_main()  # Отправляем клавиатуру с кнопками
                    )
        else:
            context.bot.send_message(
                    chat_id=self.chat_id,
                    text="Бот запущен!",
                    reply_markup=self.keyboard_menu_main()
                    )
        logger.info(f'Stop {self.command_Start.__name__}')

    def command_Help(self, update: Update, context):
        logger.info(f'Start {self.command_Help.__name__}')
        update.message.reply_text('Help!', reply_markup=self.keyboard_menu_main())
        logger.info(f'Stop {self.command_Help.__name__}')

    def command_Echo(self, update: Update, context):
        logger.info(f'Start {self.command_Echo.__name__}')
        update.message.reply_text(update.message.text, reply_markup=self.keyboard_menu_main())
        logger.info(f'Stop {self.command_Echo.__name__}')

    def command_Cancel(self, update: Update, context):
        logger.info(f'Start {self.command_Cancel.__name__}')
        update.message.reply_text('Запрос отменен.', reply_markup=self.keyboard_menu_main())
        logger.info(f'Stop {self.command_Cancel.__name__}')
        return ConversationHandler.END

    def command_FindEmails(self, update: Update, context):
        """
        Бот вывод список найденных email-адресов
        """
        logger.info(f'Start {self.command_FindEmails.__name__}')
        update.message.reply_text('Введите текст для поиска телефонных номеров: ',
                                  reply_markup=self.keyboard_menu_cancel()
                                  # Кнопка для отмены поиска
                                  )
        logger.info(f'Stop {self.command_FindEmails.__name__}')
        return self.commands.findEmails.state_point

    def findEmails(self, update: Update, context):
        logger.info(f'Start {self.findEmails.__name__}')
        user_input = update.message.text  # Получаем текст, содержащий (или нет) номера телефонов

        phoneNumRegex = re.compile(r'8 \(\d{3}\) \d{3}-\d{2}-\d{2}')  # формат 8 (000) 000-00-00

        phoneNumberList = phoneNumRegex.findall(user_input)  # Ищем номера телефонов

        if not phoneNumberList:  # Обрабатываем случай, когда номеров телефонов нет
            update.message.reply_text('Телефонные номера не найдены', reply_markup=self.keyboard_menu_cancel())
            return  # Завершаем выполнение функции

        phoneNumbers = ''  # Создаем строку, в которую будем записывать номера телефонов
        for i in range(len(phoneNumberList)):
            phoneNumbers += f'{i + 1}. {phoneNumberList[i]}\n'  # Записываем очередной номер

        update.message.reply_text(phoneNumbers)  # Отправляем сообщение пользователю
        logger.info(f'Stop {self.findEmails.__name__}')
        return ConversationHandler.END  # Завершаем работу обработчика диалога

    def command_FindPhoneNumbers(self, update: Update, context):
        """
        Бот вывод список найденных номеров телефона
        """
        logger.info(f'Start {self.command_FindPhoneNumbers.__name__}')
        update.message.reply_text('Введите текст для поиска телефонных номеров: ',
                                  reply_markup=self.keyboard_menu_cancel()
                                  # Кнопка для отмены поиска
                                  )
        logger.info(f'Stop {self.command_FindPhoneNumbers.__name__}')
        return self.commands.findPhoneNumbers.state_point

    def findPhoneNumbers(self, update: Update, context):
        logger.info(f'Start {self.findPhoneNumbers.__name__}')
        user_input = update.message.text  # Получаем текст, содержащий (или нет) номера телефонов

        phoneNumRegex = re.compile(r'8 \(\d{3}\) \d{3}-\d{2}-\d{2}')  # формат 8 (000) 000-00-00

        phoneNumberList = phoneNumRegex.findall(user_input)  # Ищем номера телефонов

        if not phoneNumberList:  # Обрабатываем случай, когда номеров телефонов нет
            update.message.reply_text('Телефонные номера не найдены', reply_markup=self.keyboard_menu_cancel())
            return  # Завершаем выполнение функции

        phoneNumbers = ''  # Создаем строку, в которую будем записывать номера телефонов
        for i in range(len(phoneNumberList)):
            phoneNumbers += f'{i + 1}. {phoneNumberList[i]}\n'  # Записываем очередной номер

        update.message.reply_text(phoneNumbers)  # Отправляем сообщение пользователю
        logger.info(f'Stop {self.findPhoneNumbers.__name__}')
        return ConversationHandler.END  # Завершаем работу обработчика диалога

    def command_VerifyPassword(self, update: Update, context):
        """
        Бот вывод
        """
        logger.info(f'Start {self.command_VerifyPassword.__name__}')
        update.message.reply_text('Введите текст для поиска телефонных номеров: ',
                                  reply_markup=self.keyboard_menu_cancel()
                                  # Кнопка для отмены поиска
                                  )
        logger.info(f'Stop {self.command_VerifyPassword.__name__}')
        return self.commands.findPhoneNumbers.state_point

    def verifyPassword(self, update: Update, context):
        logger.info(f'Start {self.verifyPassword.__name__}')
        user_input = update.message.text  # Получаем текст, содержащий (или нет) номера телефонов

        phoneNumRegex = re.compile(r'8 \(\d{3}\) \d{3}-\d{2}-\d{2}')  # формат 8 (000) 000-00-00

        phoneNumberList = phoneNumRegex.findall(user_input)  # Ищем номера телефонов

        if not phoneNumberList:  # Обрабатываем случай, когда номеров телефонов нет
            update.message.reply_text('Телефонные номера не найдены', reply_markup=self.keyboard_menu_cancel())
            return  # Завершаем выполнение функции

        phoneNumbers = ''  # Создаем строку, в которую будем записывать номера телефонов
        for i in range(len(phoneNumberList)):
            phoneNumbers += f'{i + 1}. {phoneNumberList[i]}\n'  # Записываем очередной номер

        update.message.reply_text(phoneNumbers)  # Отправляем сообщение пользователю
        logger.info(f'Stop {self.verifyPassword.__name__}')
        return ConversationHandler.END  # Завершаем работу обработчика диалога

    def main(self):
        logger.info(f'Start {self.main.__name__}')

        updater = Updater(self.tm_token__, use_context=True)

        # Получаем диспетчер для регистрации обработчиков
        dp = updater.dispatcher

        ## Регистрируем обработчики команд

        # Обработчик команды /start
        dp.add_handler(CommandHandler(self.commands.start.command, self.commands.start.callback))

        # Обработчик команды /help
        dp.add_handler(CommandHandler(self.commands.help.command, self.commands.help.callback))

        # Обработчик текстовых сообщений /echo
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.commands.echo.callback))

        # Обработчик команды /findEmails
        dp.add_handler(ConversationHandler(
                entry_points=[CommandHandler(self.commands.findEmails.state_point,
                                             self.commands.findEmails.callback
                                             )],
                states={
                        self.commands.findEmails.state_point: [
                                MessageHandler(Filters.text & ~Filters.command, self.findEmails)],
                        },
                fallbacks=[CommandHandler(self.commands.cancel.command, self.commands.cancel.callback)]
                )
                )

        # Обработчик команды /findPhoneNumbers
        dp.add_handler(ConversationHandler(
                entry_points=[CommandHandler(self.commands.findPhoneNumbers.state_point,
                                             self.commands.findPhoneNumbers.callback
                                             )],
                states={
                        self.commands.findPhoneNumbers.state_point: [
                                MessageHandler(Filters.text & ~Filters.command, self.findPhoneNumbers)],
                        },
                fallbacks=[CommandHandler(self.commands.cancel.command, self.commands.cancel.callback)]
                )
                )

        # Обработчик команды /verifyPassword
        dp.add_handler(ConversationHandler(
                entry_points=[CommandHandler(self.commands.verifyPassword.state_point,
                                             self.commands.verifyPassword.callback
                                             )],
                states={
                        self.commands.verifyPassword.state_point: [
                                MessageHandler(Filters.text & ~Filters.command, self.verifyPassword)],
                        },
                fallbacks=[CommandHandler(self.commands.cancel.command, self.commands.cancel.callback)]
                )
                )

        # Обработчик команды /get_release
        dp.add_handler(CommandHandler(self.commands.getRelease.command, self.commands.help.callback))

        # Обработчик команды /get_uname
        dp.add_handler(CommandHandler(self.commands.getUname.command, self.commands.help.callback))

        # Обработчик команды /get_uptime
        dp.add_handler(CommandHandler(self.commands.getUptime.command, self.commands.help.callback))

        # Обработчик команды /get_df
        dp.add_handler(CommandHandler(self.commands.getDF.command, self.commands.help.callback))

        # Обработчик команды /get_free
        dp.add_handler(CommandHandler(self.commands.getFree.command, self.commands.help.callback))

        # Обработчик команды /get_mpstat
        dp.add_handler(CommandHandler(self.commands.getMpstat.command, self.commands.help.callback))

        # Обработчик команды /get_w
        dp.add_handler(CommandHandler(self.commands.getW.command, self.commands.help.callback))

        # Обработчик команды /get_auths
        dp.add_handler(CommandHandler(self.commands.getAuths.command, self.commands.help.callback))

        # Обработчик команды /get_critical
        dp.add_handler(CommandHandler(self.commands.getCritical.command, self.commands.help.callback))

        # Обработчик команды /get_ps
        dp.add_handler(CommandHandler(self.commands.getPS.command, self.commands.help.callback))

        # Обработчик команды /get_SS
        dp.add_handler(CommandHandler(self.commands.getSS.command, self.commands.help.callback))

        # Обработчик команды /get_apt_list
        dp.add_handler(CommandHandler(self.commands.getAptList.command, self.commands.help.callback))

        # Запускаем бота
        updater.start_polling()

        # Отправляем кнопку /start автоматически при запуске бота
        self.command_Start(context=updater)

        # Останавливаем бота при нажатии Ctrl+C
        updater.idle()

        logger.info(f'Stop {self.main.__name__}')


if __name__ == '__main__':
    logger.info('Start Script')
    bot = TelegramBot()
    bot.main()
    logger.info('Stop Script')
