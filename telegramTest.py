import telegram
from telegram.ext import Updater, MessageHandler, Filters

token = "5297680956:AAGsASU0zdgLJmczunkMVvByaZ4OyrT6DFg"  # @UpbitPricing_bot 채팅방 토큰
chat_id = "5503560786"  # 내 텔레그램 id

telegram_bot = telegram.Bot(token=token)

# update_data = telegram_bot.getUpdates() # 그 동안 온 메시지 있나? 다 프린트해 봐.
# for data in update_data:
#    print(data.message)

#telegram_bot.sendMessage(chat_id=chat_id, text="우왕좌왕") #'우왕좌왕'이라고 메시지 보내 봐.

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()


def handler(update, context):
    user_text = update.message.text
    if user_text == '1':
        telegram_bot.sendMessage(chat_id=chat_id, text='1이 입력되었디.')
    elif user_text == '2':
        telegram_bot.sendMessage(chat_id=chat_id, text='2가 입력되었디.')


echo_handler = MessageHandler(Filters.text, handler)
dispatcher.add_handler(echo_handler)
