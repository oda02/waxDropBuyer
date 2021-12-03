import threading
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import undetected_chromedriver as uc
import queue
from MailParser import MailParser
from ScreenManager import CheckImage


class element_has_text(object):
  """An expectation for checking that an element has a particular css class.

  locator - used to find the element
  returns the WebElement once it has the particular css class
  """
  def __init__(self, xpath, driver):
    self.xpath = xpath
    self.driver = driver

  def __call__(self, driver):

    element = driver.find_element_by_xpath(self.xpath)   # Finding the referenced element
    if element.text == "":
        return False
    else:
        return element

class GamerBot:
    
    def __init__(self, options, acc_name, login, password, window, queue, email_psw):
        self.options = options
        self.driver = uc.Chrome(chrome_options=options)
        self.actions = ActionChains(self.driver)
        self.finder = CheckImage()
        self.mainWindowHandle = ''
        self.acc_name = acc_name
        self.password = password
        self.login = login
        self.window = window
        self.queue = queue
        self.stop = False
        self.parser = MailParser(login, email_psw)
        self.startgame()
    
    def startgame(self):

        #Login
        self.driver.get("https://neftyblocks.com/")
        # element = WebDriverWait(self.driver, 20).until(
        #     EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Accept All')]")))
        # element.click()
        # time.sleep(1)
        self.mainWindowHandle = self.driver.current_window_handle

        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Login')]")))  # пробелы для нефти
        element.click()
        time.sleep(1)
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'WAX Cloud Wallet')]")))
        element.click()


        flag = True
        while flag:
            try:
                windows = self.driver.window_handles
                for window in windows:
                    self.driver.switch_to.window(window)
                    element_err = self.driver.find_elements_by_xpath('//div[@id="cf-error-details"]')
                    element = self.driver.find_elements_by_xpath('//*[@name="userName"]')
                    if element:
                        flag = False
                        break
                    if element_err:
                        self.driver.switch_to.window(window)
                        self.driver.get("https://all-access.wax.io/cloud-wallet/login/")
                        time.sleep(2)
                        flag = False
                        break


                    time.sleep(0.5)

            except:
                pass

        flag = True
        while flag:
            try:
                windows = self.driver.window_handles
                for window in windows:
                    self.driver.switch_to.window(window)
                    element = self.driver.find_elements_by_xpath('//*[@name="userName"]')
                    if element:
                        element[0].click()
                        element[0].clear()
                        element[0].send_keys(self.login)
                        element2 = self.driver.find_elements_by_xpath('//*[@name="password"]')
                        element2[0].click()
                        element2[0].clear()
                        element2[0].send_keys(self.password)
                        # captcha.kok(self.driver, True, self.window, 'output_' + self.acc_name)
                        time.sleep(0.5)
                        element = self.driver.find_elements_by_xpath('//button[text()="Login"]')
                        element[0].click()
                        #
                        flag = False
                        break
                    time.sleep(0.5)
            except:
                pass
        flag = True
        time.sleep(5)
        if len(self.driver.window_handles) != 1:
            while flag:
                print('Я в цикле')
                try:
                    windows = self.driver.window_handles
                    for window in windows:
                        self.driver.switch_to.window(window)
                        element = self.driver.find_elements_by_xpath('//input[@name=\'code\']')
                        if element:
                            element[0].click()
                            element[0].clear()
                            element[0].send_keys(self.parser.get_email_code())
                            element[0].send_keys(u'\ue007')
                            time.sleep(0.5)
                            flag = False
                            self.driver.switch_to_window(self.mainWindowHandle)
                            break
                        element = self.driver.find_elements_by_xpath('//*[text()="Approve"]')
                        if element:
                            flag = False
                            self.driver.switch_to_window(self.mainWindowHandle)
                            break
                except Exception as err:
                    print(err)
        flag = True
        time.sleep(3)
        while flag:
            try:
                windows = self.driver.window_handles
                if len(windows) == 1:
                    flag = False
                    break
                for window in windows:
                    self.driver.switch_to.window(window)
                    element = self.driver.find_elements_by_xpath('//*[text()="Approve"]')
                    if element:
                        self.driver.switch_to.window(window)
                        element[0].click()
                        time.sleep(2)
                        flag = False
                        break
                    time.sleep(0.5)
            except:
                pass

        print('ll')
        self.driver.switch_to.window(self.mainWindowHandle)
        time.sleep(1)



        self.driver.switch_to.window(self.mainWindowHandle)


        # x = threading.Thread(target=self.captcha_thread)
        # x.start()
        self.main_cycle()



    def main_cycle(self):
        while not self.stop:
            try:
                self.window['output_' + self.acc_name].update('Press Go to start farming')
                self.window['go_' + self.acc_name].update(disabled=False)
                speed = self.queue.get()
                threading.Thread(target=self.kill_thread).start()
                self.window['go_' + self.acc_name].update(disabled=True)
                self.window['stop_' + self.acc_name].update(disabled=False)
                self.window['output_' + self.acc_name].update('Processing')
                with open('dropUrl.txt') as f:
                    url = f.read()
                self.driver.get(url)
                print('жду кнопку')
                element = WebDriverWait(self.driver, 99999).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//*[@class='v-card__actions']//div[@class='col-sm-4 col-6'][2]//button//span")))
                time = element.text
                kok = time.split()
                minutes = int(''.join(filter(str.isdigit, kok[0])))
                seconds = int(''.join(filter(str.isdigit, kok[1])))
                time = minutes * 60 + seconds
                self.window['output_' + self.acc_name].update(time)
                print('время: ', time)
                element = WebDriverWait(self.driver, time + 15).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//*[@class='v-card__actions']//div[@class='col-sm-4 col-6'][2]//button")))
                element.click()
                # captcha.kok(self.driver, False, self.window, 'output_' + self.acc_name)
            except:
                pass
        # while not self.stop:
        #     try:
        #         self.window['output_' + self.acc_name].update('Press Go to start farming')
        #         self.window['go_' + self.acc_name].update(disabled=False)
        #         speed = self.queue.get()
        #         threading.Thread(target=self.kill_thread).start()
        #         self.window['go_' + self.acc_name].update(disabled=True)
        #         self.window['stop_' + self.acc_name].update(disabled=False)
        #         self.window['output_' + self.acc_name].update('Processing')
        #         with open('dropUrl.txt') as f:
        #             url = f.read()
        #         self.driver.get(url)
        #         print('жду кнопку')
        #         element = WebDriverWait(self.driver, 99999).until(
        #             EC.presence_of_element_located(
        #                 (By.XPATH, "//span[@class='text-monospace']")))
        #         mytime = element.text
        #         kok = mytime.split()
        #         minutes = int(''.join(filter(str.isdigit, kok[0])))
        #         seconds = int(''.join(filter(str.isdigit, kok[1])))
        #         mytime = minutes * 60 + seconds
        #         self.window['output_' + self.acc_name].update(mytime)
        #         time.sleep(mytime - 44)
        #         key = captcha.getKey_atomichub(self.driver.current_url)
        #         element = WebDriverWait(self.driver, 300).until(
        #             EC.element_to_be_clickable(
        #                 (By.XPATH, "//button[@class='btn btn-primary btn-block']")))
        #         element.click()
        #         captcha.atomichub_pass(self.driver, key)
        #
        #         element = WebDriverWait(self.driver, 300).until(
        #             EC.element_to_be_clickable(
        #                 (By.XPATH, "//div[@class='mb-4']//button[@class='btn btn-primary btn-block']")))
        #
        #         element.click()
        #         captcha.kok(self.driver, False, self.window, 'output_' + self.acc_name)
        #     except:
        #         pass


    def kill_thread(self):
        while True:
            message = self.queue.get()
            print(message)
            if message == 'stop':
                self.stop = True
                print(self.stop)
                self.driver.quit();
                exit()

    
    def wait_for_find_button(self, button):
        while True:
            #print('ищу кнопку')
            # self.driver.save_screenshot(self.buttons[button])
            screenshot = self.driver.get_screenshot_as_png()
            cords = self.find_button(button, screenshot)
            if cords:
                return cords
            time.sleep(1)
    
    def click(self, cor1, cor2):
        # self.actions.move_by_offset(cor1, cor2).click().perform()
        # kekw = "document.elementFromPoint("+ str(cor1) +"," +  str(cor2) + ").click();"
        # self.driver.execute_script(kekw)
        self.actions.move_to_element_with_offset(self.driver.find_element_by_tag_name('html'), cor1,
                                                 cor2).click().perform()
        # self.actions.move_to_element(self.driver.find_element_by_tag_name('html')).move_by_offset(cor1, cor2).click().perform()
    
    def find_any_button(self):
        # self.driver.save_screenshot("screen.png")
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
        response = requests.post('https://wax.cryptolions.io/v1/chain/get_account',
                                 data='{{"account_name": "{0}"}}'.format(self.acc_name))
        response = response.json()
        cpu_used = round(response['cpu_limit']['used']/1000, 2)
        cpu_max = round(response['cpu_limit']['max']/1000, 2)
        percentage = round(cpu_used / cpu_max * 100)
        self.driver.execute_script('document.querySelector(".bar").style.width = "{}%";'.format(percentage))
        self.driver.execute_script('document.querySelector(".content").innerHTML = "{}%";'.format(percentage))
        self.driver.execute_script('document.querySelector(".perclabel").innerHTML = "CPU used - {} ms / {} ms";'.format(cpu_used,cpu_max))

        if response["cpu_limit"]["available"] >= 2200:
            return True
        else:
            return False


if __name__ == "__main__":
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--window-size=1600,900")
        # chromeProfile = 'D:\\Projects\\Python\\alienwords\\User Data1'
        # options.add_argument(f"--user-data-dir={chromeProfile}")
        # options.add_argument("--profile-directory=Profile 5")
    
    except:
        pass
    #print()
    bot = GamerBot(options, './chromedriver.exe')
    bot.startgame()
