import queue
import threading

import PySimpleGUI as sg
import undetected_chromedriver as uc
from selenium import webdriver
import time

import dropBuyer

class bot:

    def __init__(self, options, path):
        self.options = options
        self.driver = uc.Chrome(chrome_options=options)

        self.mainWindowHandle = ''
        self.acc_name = None
        x = threading.Thread(target=self.main_kok)
        x.start()

    def main_kok(self):
        while True:
            print(self.driver.window_handles)
            time.sleep(2)



accounts = {}
f = open('./accs.txt')
for line in f:
    if line:
        line = line.split()
        accounts.update({line[2]:[line[0], line[1], queue.Queue(),  line[3]]})

print(accounts)
layout = []
for account in accounts:
    layout_line = [sg.Text(account), sg.Button('Run',key='run_' + account), sg.Button('Go',key='go_' + account, disabled=True),
                   sg.Text(size=(40,1), key='output_'+account,visible=True), sg.Button('Stop',key='stop_' + account, disabled=True)]
    print('output_'+account)
    layout.append(layout_line)
layout.append([sg.Button('RunAll')])
layout.append([sg.Button('GoAll')])
# Create the window
window = sg.Window('Window Title', layout)


def start_bot(account):
    try:

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--window-size=1600,900")
        # chromeProfile = 'D:\\Projects\\Python\\alienwords\\User Data1'
        # options.add_argument(f"--user-data-dir={chromeProfile}")
        # options.add_argument("--profile-directory=Profile 1")
        threading.Thread(target=dropBuyer.GamerBot,
                         args=(options, account, accounts[account][0], accounts[account][1], window, accounts[account][2], accounts[account][3])).start()
        #window['run_' + account].update(disabled=True)

    except:
        pass


while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    print(event)
    if event == 'RunAll':
        for account in accounts:
            start_bot(account)

    if event == 'GoAll':
        for account in accounts:
            accounts[account][2].put('go')


    if 'run_' in event:
        acc = event.split('_')[1]
        start_bot(acc)

    if 'go_' in event:
        acc = event.split('_')[1]
        accounts[acc][2].put('go')
    if 'stop_' in event:
        acc = event.split('_')[1]
        accounts[acc][2].put('stop')
        window[event].update(disabled=True)
        window['run_' + acc].update(disabled=False)



# Finish up by removing from the screen
window.close()


