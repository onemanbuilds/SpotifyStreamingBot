from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from random import randint
from concurrent.futures import ThreadPoolExecutor
from colorama import init,Fore
import os

class Main:
    def clear(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name in ('ce', 'nt', 'dos'):
            os.system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title_name:str):
        os.system("title {0}".format(title_name))

    def __init__(self):
        self.clear()
        self.SetTitle('One Man Builds Spotify Streaming Tool Selenium')
        init(convert=True)
        title = Fore.YELLOW+"""
                            
                    ____ ___  ____ ___ _ ____ _   _    ____ ___ ____ ____ ____ _  _ _ _  _ ____ 
                    [__  |__] |  |  |  | |___  \_/     [__   |  |__/ |___ |__| |\/| | |\ | | __ 
                    ___] |    |__|  |  | |      |      ___]  |  |  \ |___ |  | |  | | | \| |__] 
                                                                                                
        
        """
        print(title)
        self.browser_amount = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] How many browser would you like to run at the same time: '))
        self.number_of_songs = 0
        self.url = ""
        self.minplay = 0
        self.maxplay = 0
        self.minplay = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Enter the minimum amount of time (seconds) to stream: '))
        self.maxplay = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Enter the maximum amount of time (seconds) to stream: '))
        self.number_of_songs = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] How many songs want to stream on the playlist: '))
        self.waiting = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] How many seconds would you like to wait before streams: '))
        self.url = str(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Enter the stream url: '))
        print('')

    def ReadFile(self,filename,method):
        with open(filename,method) as f:
            content = [line.strip('\n') for line in f]
            return content

    def Login(self,username,password,driver:webdriver):
        logged_in = False
        driver.get('https://accounts.spotify.com/en/login/')
        try:
            element_present = EC.presence_of_element_located((By.ID, 'login-username'))
            WebDriverWait(driver, 5).until(element_present)
            username_elem = driver.find_element_by_id('login-username')
            username_elem.send_keys(username)
            password_elem = driver.find_element_by_id('login-password')
            password_elem.send_keys(password)
            login_button_elem = driver.find_element_by_id('login-button')
            login_button_elem.click()
            sleep(5)
            if driver.current_url == 'https://accounts.spotify.com/en/status':
                print(Fore.GREEN+'['+Fore.WHITE+'!'+Fore.GREEN+'] LOGGED IN WITH | {0}:{1}'.format(username,password))
                logged_in = True
            else:
                print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] FAILED TO LOGIN WITH | {0}:{1}'.format(username,password))
                logged_in = False
        except TimeoutException:
            print(Fore.RED+'['+Fore.WHITE+'-'+Fore.RED+'] Timed out waiting for page to load')

        return logged_in

    def Stream(self,combos):
        username = combos.split(':')[0].replace("['","")
        password = combos.split(':')[-1].replace("]'","")
        options = Options()
        options.add_argument('--headless')
        options.add_argument('no-sandbox')
        options.add_argument('--log-level=3')
        options.add_experimental_option('excludeSwitches', ['enable-logging','enable-automation'])
        driver = webdriver.Chrome(options=options)
        if self.Login(username,password,driver) == True:
            driver.get(self.url)
            playlist_title = driver.title
            sleep(self.waiting)
            try:
                counter = 0
                for i in range(self.number_of_songs):
                    stream_time = randint(self.minplay,self.maxplay)
                    counter = counter+1
                    driver.execute_script("document.getElementsByClassName('_38168f0d5f20e658506cd3e6204c1f9a-scss')[{0}].click()".format(i))
                    sleep(stream_time)
                    print(Fore.GREEN+'['+Fore.WHITE+'!'+Fore.GREEN+'] PLAYLIST {0} | SONG {1} | STREAMED WITH {2}:{3} | FOR {4} SECONDS'.format(playlist_title,counter,username,password,stream_time))
                    with open('streamed.txt','a',encoding='utf8') as f:
                        f.write('PLAYLIST {0} | SONG {1} | STREAMED WITH {2}:{3} | FOR {4} SECONDS\n'.format(playlist_title,counter,username,password,stream_time))
            except:
                pass
        driver.close()
        driver.quit()
            
    def Start(self):
        combos = self.ReadFile('combos.txt','r')
        with ThreadPoolExecutor(max_workers=self.browser_amount) as ex:
            for combo in combos:
                ex.submit(self.Stream,combo)
        
if __name__ == '__main__':
    main = Main()
    main.Start()