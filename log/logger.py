# -*- coding: utf-8 -*-
import sys
sys.setdefaultencoding("utf-8")
import time

########################################

# time funciton
def actualtime():
    return "["+(time.strftime("%d/%m/%Y"))+"-"+(time.strftime("%H:%M"))+"]"
########################################

# log function
def logger(m):
    uid = str(m.from_user.id)
    ufn = m.from_user.first_name
    if m.chat.id > 0:
        f = open("./log/privatelog.txt", "r+")
        log = actualtime()+"["+uid+"]["+ufn+"]: "
    else:
        f = open("./log/grouplog.txt", "r+")
        gid = str(m.chat.id)
        log = actualtime()+"["+gid+"]["+uid+"]["+ufn+"]: "
    f.seek(0,2)
    
    if hasattr(m, 'text'):
        f.write(log+m.text+"\n")
    ####################
    elif hasattr(m, 'audio'):
        fid = m.audio.file_id
        fd = str(m.audio.duration)
        f.write(log+"audio ("+fid+") ["+fd+"sec]\n")
    ####################
    elif hasattr(m, 'document'):
        fid = m.document.file_id
        fn = m.document.file_name
        f.write(log+"document ("+fid+") \""+fn+"\"\n")
    ####################
    elif hasattr(m, 'photo'):
        if hasattr(m, 'caption'):
            pc = m.caption
            f.write(log+"photo: \""+pc+"\"\n")
        else:
            f.write(log+"photo\n")
    ####################
    elif hasattr(m, 'sticker'):
        fid = m.sticker.file_id
        fw = str(m.sticker.width)
        fh = str(m.sticker.height)
        f.write(log+"sticker ("+fid+") ["+fw+"x"+fh+"px]\n")
    ####################
    elif hasattr(m, 'video'):
        fid = m.video.file_id
        fw = str(m.video.width)
        fh = str(m.video.height)
        fd = str(m.video.duration)
        if hasattr(m, 'caption'):
            vc = m.caption
            f.write(log+"video ("+fid+") \""+vc+"\" - ["+fw+"x"+fh+"px]["+fd+"sec]\n")          
        else:
            f.write(log+"video ("+fid+") - ["+fw+"x"+fh+"px]["+fd+"sec]\n")
    ####################
    elif hasattr(m, 'voice'):
        fid = m.voice.file_id
        fd = str(m.voice.duration)
        f.write(log+"voice ("+fid+") - ["+fd+"sec]\n")
    ####################
    elif hasattr(m, 'contact'):
        pn = m.contact.phone_number
        fn = m.contact.first_name
        f.write(log+"contact ("+pn+") "+fn+"\n")
    ####################
    elif hasattr(m, 'location'):
        llong = str(m.location.longitude)
        llat = str(m.location.latitude)
        f.write(log+"location ["+llong+"]["+llat+"]\n")
    ####################
    elif hasattr(m, 'new_chat_participant'):
        uname = m.from_user.username
        newuname = m.new_chat_participant.username
        f.write(log+"@"+uname+" added @"+newuname+"\n")
    ####################
    elif hasattr(m, 'left_chat_participant'):
        uname = m.left_chat_participant.username
        f.write(log+"@"+uname+" left the group\n")
    ####################
    elif hasattr(m, 'new_chat_title'):
        nct = m.new_chat_title
        f.write(log+"The new group tittle is: "+nct+"\n")
    ####################
    elif hasattr(m, 'new_chat_photo'):
        uname = m.from_user.username
        f.write(log+"@"+uname+" has changed chat's photo\n")
    ####################
    elif m.delete_chat_photo:
        uname = m.from_user.username
        f.write(log+"@"+uname+" has deleted chat's photo.\n")
    ####################
    elif m.group_chat_created:
        uname = m.from_user.username
        gtitle = m.chat.title
        f.write(log+"@"+uname+" has created \""+gtitle+"\n\n")
    ####################
    else:
        f.write(log+"other stuff\n")
    ####################
    f.close()