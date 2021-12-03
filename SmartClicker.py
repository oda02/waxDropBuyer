import os
import sys
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import captcha
import requests


from ScreenManager import CheckImage

class GamerBot:

    def __init__(self, options, path):
        self.options = options
        self.driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        self.actions = ActionChains(self.driver)
        self.finder = CheckImage()
        self.buttons = {'mine1.png':'main.png', 'login.png': 'screen.png', 'mining hub button.png':'return menu.png', 'mine2.png':'mining hub.png', 'claim.png':'claim menu.png'}
        self.mainbuttons = ['mine1.png', 'mining hub button.png', 'mine2.png', 'claim.png', 'Close.png', 'Close2.png', 'claim_big.png', 'login.png']
        self.mainWindowHandle = ''
        self.acc_name = None

    def startgame(self):
        self.driver.get("https://play.alienworlds.io/")
        cords = self.wait_for_find_button('login.png')
        print(cords)
        self.click(cords[0], cords[1])
        self.mainWindowHandle = self.driver.current_window_handle
        time.sleep(10)
        with open('auth.txt') as f:
            login = f.readline()
            login = login.replace('\n','')
            password = f.readline()
            password = password.replace('\n', '')
            self.acc_name = f.readline()

        flag = True
        while flag:
            windows = self.driver.window_handles
        #
            for window in windows:
                self.driver.switch_to.window(window)
                element = self.driver.find_elements_by_xpath('//*[@name="userName"]')
                if element:
        #
                    element[0].click()
                    element[0].clear()
                    element[0].send_keys(login)
                    element2 = self.driver.find_elements_by_xpath('//*[@name="password"]')
                    element2[0].click()
                    element2[0].clear()
                    element2[0].send_keys(password)
                    captcha.kok(self.driver, True)
                    time.sleep(4)
                    element = self.driver.find_elements_by_xpath('//button[text()="Login"]')
                    element[0].click()
        #
                    flag = False
                    break
        self.driver.switch_to.window(self.mainWindowHandle)
        input()
        time.sleep(10)
        x = threading.Thread(target=self.captcha_thread)
        x.start()
        self.main_cycle()

    def main_cycle(self):
        # main
        while True:
            if self.get_cpu():
                try:
                    cords = self.find_any_button()
                    print(cords)
                    if cords:
                        try:
                            self.click(cords[0], cords[1])
                        except:
                            pass
                except:
                    pass
            else:
                print('Кажется кончилось цпу')
                time.sleep(5)
            time.sleep(5)

    def captcha_thread(self):
        while True:
            windows = self.driver.window_handles
            print(windows)
            if len(windows) > 1:
                try:
                    captcha.kok(self.driver, False)
                except:
                    self.driver.close()
                time.sleep(2)
                self.driver.switch_to.window(self.mainWindowHandle)
                time.sleep(7)
            time.sleep(4)

    def wait_for_find_button(self, button):
        while True:
            print('ищу кнопку')
            #self.driver.save_screenshot(self.buttons[button])
            screenshot = self.driver.get_screenshot_as_png()
            cords = self.find_button(button, screenshot)
            if cords:
                return cords
            time.sleep(1)

    def click(self, cor1, cor2):
        #self.actions.move_by_offset(cor1, cor2).click().perform()
        #kekw = "document.elementFromPoint("+ str(cor1) +"," +  str(cor2) + ").click();"
        #self.driver.execute_script(kekw)
        self.actions.move_to_element_with_offset(self.driver.find_element_by_tag_name('html'), cor1, cor2).click().perform()
        #self.actions.move_to_element(self.driver.find_element_by_tag_name('html')).move_by_offset(cor1, cor2).click().perform()


    def find_any_button(self):
        #self.driver.save_screenshot("screen.png")
        screenshot = self.driver.get_screenshot_as_png()
        for key in self.mainbuttons:
            cords = self.find_button(key, screenshot)
            if cords:
                return cords
        return ()


    def find_button(self, button, screenshot):
        self.finder.upload_image(screenshot)
        return self.finder.find_image(button)
    
    def get_cpu(self):
        response = requests.post('https://wax.greymass.com/v1/chain/get_account',
                                 data='{{"account_name": "{0}"}}'.format(self.acc_name))
        response = response.json()
        if response["cpu_limit"]["available"] >=1000:
            return True
        else:
            return False
        
        
if __name__ == "__main__":
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--window-size=1600,900")
#        chromeProfile = userdata
 #       options.add_argument(f"--user-data-dir={chromeProfile}")
        #options.add_argument("--profile-directory=Profile 1")

    except:
        pass
    print()
    bot = GamerBot(options, './chromedriver.exe')
    bot.startgame()
