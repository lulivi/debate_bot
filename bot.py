# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import time
import telebot # Librería de la API del bot.
from telebot import types # Tipos para la API del bot.
import priv.token as tk
bot = telebot.TeleBot(tk.token()) # Creamos el objeto de nuestro bot.
import log.logger as log

# Funcion que recibe los mensajes
def recibe(messages): # Mensajes recibidos
    for m in messages: # Por cada dato 'm' en el dato 'messages'
        log.logger(m)
bot.set_update_listener(recibe) 

###############################################################################
#                            commands
###############################################################################

# start mensaje de bienvenida
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    comando = m.text[7:]
    if comando == 'rules':
        command_rules(m)
    else:
        bot.send_message(cid,"¡Hola! Soy Debatebot.\n\
        Usa el comando /help para que te muestre mis demás comandos.\n\n\
        Espero ser de utilidad.")
########################################

# muestra los comandos visibles         
@bot.message_handler(commands=['help'])
def command_help(m):
    bot.reply_to(m,"Guardo y doy información acerca de debates.\n\
    ~> Con el comando /new establezco el nuevo tema de debate.\n\
    ~> Con el comando /current muestro el tema actual de debate.\n\
    ~> Con el comando /end termino el debate actual.\n\
    ~> Con el comando /rules muestro las normas actuales del grupo.")
########################################

# nuevo debate
@bot.message_handler(commands=['new'])
def command_new(m):
    pos = m.text.find(" ")
    if pos == -1:
        bot.send_message(m.chat.id,m.from_user.first_name+", escribe:\n\
        ~> /new nuevo_tema_de_debate")
    else:
        if get_matter() == "":
            set_matter(m.text[5:])
            set_matter_id(m)
            bot.send_message(m.chat.id,"El tema actual se ha guardado \
            con éxito, "+m.from_user.first_name+".\n\
            ~> /end para terminarlo.\n\
            ~> /current para obtenerlo.")
        else:
            bot.send_message(m.chat.id,"Ya se está debatiendo un \
            tema, "+m.from_user.first_name+".\n\
            ~> /end para terminarlo.\n\
            ~> /current para obtenerlo.")
########################################

# debate actual
@bot.message_handler(commands=['current'])
def command_current(m):
    actual = get_matter()
    if actual != "":
        bot.send_message(m.chat.id,m.from_user.first_name+", el tema \
        actual es:\n\" "+actual+" \"\n\
        ~> /end para terminarlo.")
    else:
        bot.send_message(m.chat.id,"No hay debate \
        actualmente, "+m.from_user.first_name+".\n\
        ~> /new para comenzar uno.")
########################################

# terminar el debate
@bot.message_handler(commands=['end'])
def command_end(m):
    if get_matter() != "":
        uid = get_matter_id()
        if uid == m.from_user.id:
            set_matter()
            bot.send_message(m.chat.id,"Tema cerrado, \
            "+m.from_user.first_name+".\n~> /new para comenzar uno.")
        else:
            bot.send_message(m.chat.id,"No tiene permiso para terminar el \
            debate, "+m.from_user.first_name+".")
    else:
        bot.send_message(m.chat.id, "No hay debate \
        actualmente, "+m.from_user.first_name+".\n\
        ~> /new para comenzar uno.")
########################################

# reglas
@bot.message_handler(commands=['rules'])
def command_to_rules(m):
    if m.chat.id < 0:
        bot.reply_to(m,'https://telegram.me/debate_bot?start=rules')
    else:
        command_rules(m)

def command_rules(m):
    normas = get_normas()
    bot.reply_to(m,"Reglas de participación en este grupo:\n\n"+normas)

################################################################################
#                               functions
################################################################################

##### matter.txt #####
def set_matter(txt=""):
    with open('matter.txt','w') as f:
        f.write(txt)

def get_matter():
    with open('matter.txt','r') as f:
        matter = f.read()
    return matter

##### normas.txt #####
def get_normas():
    with open('rules.txt','r') as f:
        normas = f.read()
    return normas

##### currenttopicid.txt #####
def set_matter_id(m):
    with open('currenttopicid.txt','w') as f:
        f.write(str(m.from_user.id))

def get_matter_id():
    with open('currenttopicid.txt','r') as f:
        uid = f.read()
    return int(uid)

################################################################################

bot.polling(none_stop=True, block=False)
while True: 
    time.sleep(300)