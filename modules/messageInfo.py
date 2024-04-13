#!/usr/bin/env python3 
# -*- coding:utf-8 _*-  
""" 
"""
from telegram import Update



class FileInfo:
    def __init__(self,file_name,file_size,file_id,file_unique_id):
        # Required
        self.file_name = file_name
        self.file_size = file_size
        self.file_unique_id = file_unique_id
        self.file_id = file_id




class MovieDownLoadTask:
    def __init__(self,movie_name,movie_link='') -> None:
        self.movie_name = movie_name
        self.movie_link = movie_link

    def __str__(self):
        return f"current task (movie_name:{self.movie_name}, movie_link:{self.movie_link})"



class MessageInfo:
    def __init__(
        self,
        update: Update
    ):
        # Required
        self.msgType = update.effective_chat.type
        self.user_id = str(update.effective_user.id)
        self.first_name = update.effective_user.first_name
        self.username = update.effective_user.username
        self.chat_id = update.message.message_id if update.message else int(update.callback_query.message.message_id)
        self.text = update.effective_message.text
        self.reply_to_message = None
        self.reply_from_user_name = None
        self.reply_from_text = None
        self.reply_from_msg_id = None
        if update.effective_message.reply_to_message:
            self.reply_to_message = update.effective_message.reply_to_message
            self.reply_from_user_name = self.reply_to_message.from_user.username
            self.reply_from_text = self.reply_to_message.text
            self.reply_from_msg_id = int(self.reply_to_message.message_id)
        
            



    def print(self):
        reply_info = f"""
        reply_from_user_name:{self.reply_from_user_name}
        reply_from_text:{self.reply_from_text}
        reply_from_msg_id:{self.reply_from_msg_id}
        """

        msg_info = f"""
        msgType:{self.msgType},
        user_id :{self.user_id},
        first_name :{self.first_name},
        username :{self.username},
        chat_id :{self.chat_id},
        "text" :{self.text}
        """
        if self.reply_to_message:
            msg_info = msg_info+reply_info


        return msg_info


