import pandas as pd
import requests
import telebot
import re

# Initialize the bot
BOT_TOKEN = '5823631337:AAH8qPNWbX8DMFaJAGyXsR2LUAkvuRKdMX0'

bot = telebot.TeleBot(BOT_TOKEN)

# Regular expression pattern to match email addresses
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
group_chat_id=-1001718466380

@bot.message_handler(func=lambda message: message.chat.id ==group_chat_id , content_types=['text'])
def handle_message(message):
    emails = re.findall(email_pattern, message.text)
    if emails:
        # Read the excel file into a DataFrame
        df = pd.read_excel("emails.xlsx", sheet_name="Sheet1")
        
        # Loop through the emails
        for email in emails:
            # Check if the email is already in the excel file
            if email not in df["Email"].tolist():
                # Add the email to the excel file
                new_row = pd.DataFrame({"Email": [email]})
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_excel('emails.xlsx', index=False)
                
@bot.message_handler(commands=['command1'])
def handle_emails_command(message):
  
    # Send the excel file to the chat
    with open("emails.xlsx", 'rb') as f:
                bot.send_document(chat_id=message.chat.id, document=f, reply_to_message_id=message.message_id)


bot.polling()


