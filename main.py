from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from threading import Lock
from random import choice,randint
from colorama import init,Fore,Style
from time import sleep
from os import name,system
from sys import stdout
from concurrent.futures import ThreadPoolExecutor

class Main:
    def clear(self):
        if name == 'posix':
            system('clear')
        elif name in ('ce', 'nt', 'dos'):
            system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title_name:str):
        system("title {0}".format(title_name))

    def GetRandomUserAgent(self):
        useragents = self.ReadFile('useragents.txt','r')
        return choice(useragents)

    def PrintText(self,bracket_color:Fore,text_in_bracket_color:Fore,text_in_bracket,text):
        self.lock.acquire()
        stdout.flush()
        text = text.encode('ascii','replace').decode()
        stdout.write(Style.BRIGHT+bracket_color+'['+text_in_bracket_color+text_in_bracket+bracket_color+'] '+bracket_color+text+'\n')
        self.lock.release()

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('proxies.txt','r')
        return choice(proxies_file)

    def ReadFile(self,filename,method):
        with open(filename,method) as f:
            content = [line.strip('\n') for line in f]
            return content

    def Login(self,username,password,driver):
        try:
            logged_in = False

            driver.get('https://accounts.spotify.com/en/login/')
            element_present = EC.presence_of_element_located((By.ID, 'login-username'))
            WebDriverWait(driver, 20).until(element_present)
            username_elem = driver.find_element_by_id('login-username')
            username_elem.send_keys(username)
            password_elem = driver.find_element_by_id('login-password')
            password_elem.send_keys(password)
            login_button_elem = driver.find_element_by_id('login-button')
            login_button_elem.click()

            element_present = EC.url_matches('https://accounts.spotify.com/en/status')
            WebDriverWait(driver, 20).until(element_present)
            
            if driver.current_url == 'https://accounts.spotify.com/en/status':
                self.PrintText(Fore.CYAN,Fore.RED,'LOGIN',f'LOGGED IN WITH | {username}:{password}')
                logged_in = True
            else:
                self.PrintText(Fore.RED,Fore.CYAN,'LOGIN',f'FAILED TO LOGIN WITH | {username}:{password}')
                logged_in = False
        
            return logged_in
        except:
            driver.quit()
            self.Login(username,password)

    def Stream(self,username,password):
        
        try:
            options = Options()

            if self.headless == 1:
                options.add_argument('--headless')

            options.add_argument(f'--user-agent={self.GetRandomUserAgent()}')
            options.add_argument('no-sandbox')
            options.add_argument('--log-level=3')

            if self.use_proxy == 1:
                options.add_argument('--proxy-server=http://{0}'.format(self.GetRandomProxy()))

            #Removes navigator.webdriver flag
            options.add_experimental_option('excludeSwitches', ['enable-logging','enable-automation'])
            
            # For older ChromeDriver under version 79.0.3945.16
            options.add_experimental_option('useAutomationExtension', False)

            options.add_argument("window-size=1280,800")

            #For ChromeDriver version 79.0.3945.16 or over
            options.add_argument('--disable-blink-features=AutomationControlled')
            driver = webdriver.Chrome(options=options)

            if self.Login(username,password,driver) == True:
                driver.get(self.url)
                element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[2]/div[4]/main/div/div[2]/div/div/div[2]/section/div/div[4]/div[1]/div/div/div/div[2]/div[1]/div/div/div[1]'))
                WebDriverWait(driver, 20).until(element_present)
                index = 0
                for i in range(self.number_of_songs):
                    index += 1
                    playtime = randint(self.minplay,self.maxplay)
                    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,f'/html/body/div[4]/div/div[2]/div[4]/main/div/div[2]/div/div/div[2]/section/div/div[4]/div[1]/div/div/div/div[2]/div[{index}]/div/div/div[1]')))
                    driver.find_element_by_xpath(f'/html/body/div[4]/div/div[2]/div[4]/main/div/div[2]/div/div/div[2]/section/div/div[4]/div[1]/div/div/div/div[2]/div[{index}]/div/div/div[1]').click()
                    sleep(1)
                    WebDriverWait(driver,20).until(EC.text_to_be_present_in_element((By.XPATH,'/html/body/div[4]/div/div[2]/div[3]/footer/div[1]/div[2]/div/div[2]/div[1]'),'0:01'))
                    sleep(playtime)
                    self.PrintText(Fore.CYAN,Fore.RED,'STREAM',f'SONG {index} | STREAMED FOR {playtime}s | WITH {username}:{password}')
        except:
            driver.quit()
            self.Stream(username,password)
        finally:
            driver.quit()
            

    def __init__(self):
        init(convert=True)
        self.lock = Lock()
        self.clear()
        self.SetTitle('One Man Builds Spotify Streaming Tool Selenium')
        self.title = Style.BRIGHT+Fore.RED+"""
                                      ___________ _____ _____ _____________   __              
                                     /  ___| ___ \  _  |_   _|_   _|  ___\ \ / /              
                                     \ `--.| |_/ / | | | | |   | | | |_   \ V /               
                                      `--. \  __/| | | | | |   | | |  _|   \ /                
                                     /\__/ / |   \ \_/ / | |  _| |_| |     | |                
                                     \____/\_|    \___/  \_/  \___/\_|     \_/                
                                                                                    
                                                                                    
                               _____ ___________ _____  ___  ___  ________ _   _ _____ 
                              /  ___|_   _| ___ \  ___|/ _ \ |  \/  |_   _| \ | |  __ \\
                              \ `--.  | | | |_/ / |__ / /_\ \| .  . | | | |  \| | |  \/
                               `--. \ | | |    /|  __||  _  || |\/| | | | | . ` | | __ 
                              /\__/ / | | | |\ \| |___| | | || |  | |_| |_| |\  | |_\ \\
                              \____/  \_/ \_| \_\____/\_| |_/\_|  |_/\___/\_| \_/\____/
                                                         
                                                         
        """
        print(self.title)
        self.use_proxy = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Proxy ['+Fore.RED+'0'+Fore.CYAN+']Proxyless: '))
        self.headless = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] ['+Fore.RED+'1'+Fore.CYAN+']Headless ['+Fore.RED+'0'+Fore.CYAN+']Not Headless: '))
        self.minplay = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Minimum time to stream: '))
        self.maxplay = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Maximum time to stream: '))
        self.number_of_songs = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Songs on the playlist: '))
        self.browser_amount = int(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Browser amount: '))
        self.url = str(input(Style.BRIGHT+Fore.CYAN+'['+Fore.RED+'>'+Fore.CYAN+'] Stream url: '))
        print('')

    def Start(self):
        combos = self.ReadFile('combos.txt','r')
        with ThreadPoolExecutor(max_workers=self.browser_amount) as ex:
            for combo in combos:
                username = combo.split(':')[0]
                password = combo.split(':')[-1]

                ex.submit(self.Stream,username,password)

if __name__ == "__main__":
    main = Main()
    main.Start()