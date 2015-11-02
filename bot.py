#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import time
import telebot # Librería de la API del bot.
from telebot import types # Tipos para la API del bot.

from priv.__init__ import token as tk
bot = telebot.TeleBot(tk()) # Creamos el objeto de nuestro bot.

###############################################################################
#                            commands
###############################################################################

# start mensaje de bienvenida
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    comando = m.text[7:]
    if comando == 'reglas':
        command_reglas(m)
    else:
        bot.send_message(cid,"¡Hola! Soy Debatebot.\nUsa el comando /ayuda para que te muestre mis demás comandos.\n\nEspero ser de utilidad.")
########################################

# muestra los comandos visibles
@bot.message_handler(commands=['ayuda'])
def command_ayuda(m):
    bot.reply_to(m,"Guardo y doy información acerca de debates.\n/nuevo establezco el nuevo tema de debate.\n/actual muestro el tema actual de debate.\n/fin termino el debate actual.\n/reglas muestro las reglas actuales del grupo.")
########################################

# nuevo debat
@bot.message_handler(commands=['nuevo'])
def command_nuevo(m):
    pos = m.text.find(" ")
    cid = m.chat.id
    if pos == -1:
        bot.send_message(cid,m.from_user.first_name+", escribe:\n/nuevo nuevo_tema_de_debate")
    else:
        if get_matter(cid) == "":
            set_matter(cid, m.text[pos:])
            fuid = m.from_user.id
            set_matter_id(cid, fuid)
            bot.send_message(cid,"El tema actual se ha guardado con éxito, "+m.from_user.first_name+".")
        else:
            bot.send_message(cid,"Ya se está debatifino un tema, "+m.from_user.first_name+".\n/fin para terminarlo.\n/actual para obtenerlo.")
########################################

# debate actual
@bot.message_handler(commands=['actual'])
def command_actual(m):
    cid = m.chat.id
    actual = get_matter(cid)
    if actual != "":
        bot.send_message(cid,"\"* "+actual+" *\" es el tema actual.\n\n/fin para terminarlo.",parse_mode="Markdown")
    else:
        bot.send_message(cid,"No hay debate actualmente.\n/nuevo para comenzar uno.")
########################################

# terminar el debate
@bot.message_handler(commands=['fin'])
def command_fin(m):
    cid = m.chat.id
    if get_matter(cid) != "":
        uid = get_matter_id(cid)
        fuid = m.from_user.id
        if uid == fuid:
            set_matter(cid)
            set_matter_id(cid,uid)
            bot.send_message(cid,"Tema cerrado, "+m.from_user.first_name+".\n/nuevo para comenzar uno.")
        else:
            bot.send_message(cid,"No tiene permiso para terminar el debate, "+m.from_user.first_name+".")

    else:
        bot.send_message(cid, "No hay debate actualmente, "+m.from_user.first_name+".\n/nuevo para comenzar uno.")
########################################

REGLASID = ""

# reglas
@bot.message_handler(commands=['reglas'])
def command_to_reglas(m):
    cid = m.chat.id
    if cid < 0:
        REGLASID = str(cid)
        bot.send_message(cid,"Pulse [aquí](https://telegram.me/debate_bot?start=reglas)",parse_mode="Markdown")
    else:
        command_reglas(m)

def command_reglas(m):
    if REGLASID != "":
        reglas = get_reglas(REGLASID)
    else:
        cid = m.chat.id
        reglas = get_reglas(cid)
    if reglas != "":
        bot.reply_to(m,"Reglas de participación en este grupo:\n\n"+reglas)
    else:
        bot.reply_to(m,"No hay relgas definidas para este grupo.")
########################################

# definir las reglas
@bot.message_handler(commands=['definereglas'])
def command_definereglas(m):
    cid = m.chat.id
    text = m.text
    pos = text.find(" ")
    if pos != -1:
        txt = m.text[pos+1:]
        set_reglas(cid, txt)
    else:
        txt = ""
        set_reglas(cid, txt)
    
    
###############################################################################
#                               functions
###############################################################################

##### matter #####
def set_matter(chatid,txt=""):
    cid = str(chatid)
    with open("./matter/"+cid+".mat",'w') as f:
        f.write(txt)

def get_matter(chatid):
    cid = str(chatid)
    with open("./matter/"+cid+".mat",'a') as f:
        pass
    with open("./matter/"+cid+".mat",'r') as f:
        matter = f.read()
    return matter

##### reglas #####
def set_reglas(chatid, txt):
    cid = str(chatid)
    with open("./reglas/"+cid+".rul",'w') as f:
        f.write(txt)

def get_reglas(chatid):
    cid = str(chatid)
    with open("./reglas/"+cid+".rul",'a') as f:
        pass
    with open("./reglas/"+cid+".rul",'r') as f:
        reglas = f.read()
    return reglas

##### matter id #####
def set_matter_id(chatid,userid):
    cid = str(chatid)
    uid = str(userid)
    with open("./matter/"+cid+".matid",'w') as f:
        f.write(uid)

def get_matter_id(chatid):
    cid = str(chatid)
    with open("./matter/"+cid+".matid",'a') as f:
        pass
    with open("./matter/"+cid+".matid",'r') as f:
        uid = f.read()
    if uid == "":
        return -1
    else:
        return int(uid)

###############################################################################

bot.polling()
