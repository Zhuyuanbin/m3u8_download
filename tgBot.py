#!/usr/bin/env python3 
# -*- coding:utf-8 _*-  

from conf import config
from modules.logger import logPrint,cclog
from modules.messageInfo import MessageInfo,MovieDownLoadTask
import modules.task as task
from telegram import Update, Chat, ChatMember, ParseMode, ChatMemberUpdated,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    ChatMemberHandler,
    MessageHandler, 
    Filters,
    CallbackQueryHandler, 
)




def send_msg(update:Update, text:str):
    return update.effective_message.reply_text(text)

def show_message_info(update):
    msg = MessageInfo(update)
    cclog.info(msg.print())
    return msg

def download_handler(update: Update, context: CallbackContext):
    msg = show_message_info(update)
    if msg.user_id != config.admin_user:
        send_msg(update,"您没有权限")
        return       
    cmds = msg.text.split(' ')
    if len(cmds)<2:
        send_msg(update,"参数错误")
        return
    index = msg.text.find(' ')
    movie_params = msg.text[index:]
    print(movie_params)
    movie_params = movie_params.strip()
    params = movie_params.split(',')
    if len(params)==2:
        movie_task = MovieDownLoadTask(params[0],params[1])
    else:
        movie_task = MovieDownLoadTask(movie_params)
    task.AddMovieDownloadTask(movie_task)
    send_msg(update,f"添加{movie_task} 任务成功")

                 
                    
def main() -> None:

    task.task_thread1.daemon = True
    task.task_thread1.start()

    updater = Updater(config.bot_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher


    dispatcher.add_handler(CommandHandler("download", download_handler))

    """
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text, show_chats))
    dispatcher.add_handler(MessageHandler(Filters.video, video_chats))
    dispatcher.add_handler(MessageHandler(Filters.voice, voice_chats))
    dispatcher.add_handler(MessageHandler(Filters.photo, pic_chats))
    dispatcher.add_handler(MessageHandler(Filters.document, document_chats))
    dispatcher.add_handler(MessageHandler(Filters.audio,audio_chats))
    """

    
    # Start the Bot
    # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
    # To reset this, simply pass `allowed_updates=[]`
    updater.start_polling(poll_interval=1.5,allowed_updates=Update.ALL_TYPES)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()



if __name__ == "__main__":
    main()