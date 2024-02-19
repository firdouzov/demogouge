import telebot
from translator import *
import flag
import os
import PIL.Image
import google.generativeai as genai

try:
    bot=telebot.TeleBot('7073730848:AAESZdEMFEmUvUJrl7aNxIBKIOSFKca4d3s')
    genai.configure(api_key='AIzaSyAs5_WHo7NXArFquWU0Zpe1sOX7Bkzkp2A')

    safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
    ]
    modeltext = genai.GenerativeModel(model_name='gemini-pro',safety_settings=safety_settings)
    chattext = modeltext.start_chat(history=[])
    modelvision = genai.GenerativeModel(model_name='gemini-pro-vision',safety_settings=safety_settings)
    global a
    global lang
    lang='en'
    a=0
    @bot.message_handler(commands=['start'])
    def command_handler(message):
        bot.reply_to(message, f'Hello  @{message.chat.username} \U0001F44B, you can ask your questions :)\nI am a Gemini Pro and Gemini Vision Pro supported Large Language Model which can answer your questions with either text content or image content.\nFeel free to explore and use my features. If you have any questions or need assistance, you can use the /help command.')
    @bot.message_handler(commands=['help'])
    def command_handler(message):
        bot.reply_to(message, f"⚡How to use Demogouge Bot :\n\n1) You can send any text content and I will reply with the language I receive.\n2) You can send image and caption any specific task and I will reply with the language I receive also.\n3)You can send image without any caption and I will reply back with the description of image.\nIf the image has not any caption I will reply back with the last language you used. If any language is not recognized yet, by default I will reply with English. \n\nFor any suggestions or remarks, please contact '@firdouzov'")
        bot.send_media_group(
            chat_id=message.chat.id,
            media=[telebot.types.InputMediaPhoto(open('screenshot.jpg', 'rb')),
                   telebot.types.InputMediaPhoto(open('screenshot1.jpg', 'rb'))]
                   )
    @bot.message_handler(func=lambda message: True,content_types=['photo'])
    def echo_photo_text(message):
        try:
            global lang
            msg_id=bot.reply_to(message,translateazen('🤖 Gemini is generating content...\nPlease wait until this message is deleted')).message_id
            if message.caption is None:
                caption=message.caption
            else:
                if '?' in message.caption:
                    caption=message.caption.replace('?','')
                    caption,lang=translateazen(caption)
                else:
                    caption=message.caption
                    caption,lang=translateazen(caption)
            file_path = bot.get_file(message.photo[0].file_id).file_path
            file = bot.download_file(file_path)
            with open("output.jpg", "wb") as code:
                code.write(file)
            img = PIL.Image.open('output.jpg')
            response = (
                    modelvision.generate_content([caption, img])
                    if caption
                    else modelvision.generate_content(img)
                )
            if response.parts: # handle multiline resps
                for part in response.parts:
                    if message.caption is None:
                        translatedresponse=translateenaz(part.text,lang)
                        bot.delete_message(message.chat.id, msg_id)
                        bot.reply_to(message,f'{flag.flag(lang)} - {translatedresponse}')
                    else:
                        translatedresponse=translateenaz(part.text,lang)
                        bot.delete_message(message.chat.id, msg_id)
                        bot.reply_to(message,f'{flag.flag(lang)} - {translatedresponse}')
            elif response.text:
                if message.caption is None:
                    translatedresponse=translateenaz(part.text,lang)
                    bot.delete_message(message.chat.id, msg_id)
                    bot.reply_to(message,f'{flag.flag(lang)} - {translatedresponse}')
                else:
                    translatedresponse=translateenaz(response.text,lang)
                    bot.delete_message(message.chat.id, msg_id)
                    bot.reply_to(message,f'{flag.flag(lang)} - {translatedresponse}')
            os.remove('output.jpg')
        except:
            try:
                translatedresponse=translateenaz("There is some errors while generating content. Please try it again or contact '@firdouzov'",lang)
                bot.reply_to(message,f'{flag.flag(lang)} - {translatedresponse}')
            except:
                bot.reply_to(message,"There is some errors while generating content. Please try it again or contact '@firdouzov'")
    @bot.message_handler(func=lambda message: True,content_types=['text'])
    def echo_message(message):
        try:
            msg_id=bot.reply_to(message,'🤖 Gemini is generating content...\nPlease wait until this message is deleted').message_id
            global lang
            global a
            global chattext
            usrname=message.chat.username
            if usrname!=a:
                chattext = modeltext.start_chat(history=[])
            a=usrname
            translated,lang=translateazen(message.text)
            response=chattext.send_message(translated).text
            translatedresponse=translateenaz(response,lang)
            bot.delete_message(message.chat.id, msg_id)
            bot.reply_to(message,f'{flag.flag(lang)} - {translatedresponse}')
        except:
            try:
                translatedresponse=translateenaz("There is some errors while generating content. Please try it again or contact '@firdouzov'",lang)
                bot.reply_to(message,f'{flag.flag(lang)} - {translatedresponse}')
            except:
                bot.reply_to(message,"There is some errors while generating content. Please try it again or contact '@firdouzov'")
    '''@bot.message_handler(func=lambda message: True,content_types=['photo','text'])
    def echo_image(message):
        if message.content_type=='photo':
            if message.caption is None:
                caption=message.caption
            else:
                if '?' in message.caption:
                    caption=message.caption.replace('?','')
                else:
                    caption=message.caption
            file_path = bot.get_file(message.photo[0].file_id).file_path
            file = bot.download_file(file_path)
            with open("output.jpg", "wb") as code:
        	    code.write(file)
            img = PIL.Image.open('output.jpg')
            response=genaiimage(img,caption)
            translatedresposne=translateenaz(response)
            bot.reply_to(message,translatedresposne)'''
    bot.infinity_polling(timeout=30, long_polling_timeout = 20)
except ValueError:
    print("Sorry there are some contents in Azerbaijani Google blocks in order to uncertain reasons. Please use the English for like these cases or contact '@firdouzov'")