from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randint
from concurrent.futures import ThreadPoolExecutor
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
        self.browser_amount = int(input('[QUESTION] How many browser would you like to run at the same time: '))
        self.number_of_songs = 0
        self.url = ""
        self.minplay = 0
        self.maxplay = 0
        self.minplay = int(input('[QUESTION] Enter the minimum amount of time (seconds) to stream: '))
        self.maxplay = int(input('[QUESTION] Enter the maximum amount of time (seconds) to stream: '))
        self.number_of_songs = int(input('[QUESTION] How many songs want to stream on the playlist: '))
        self.url = str(input('[QUESTION] Enter the stream url: '))
        print('')

    def ReadFile(self,filename,method):
        with open(filename,method) as f:
            content = [line.strip('\n') for line in f]
            return content

    def Login(self,username,password,driver:webdriver):
        logged_in = False
        driver.get('https://accounts.spotify.com/en/login/')
        username_elem = driver.find_element_by_id('login-username')
        username_elem.send_keys(username)
        password_elem = driver.find_element_by_id('login-password')
        password_elem.send_keys(password)
        login_button_elem = driver.find_element_by_id('login-button')
        login_button_elem.click()
        sleep(1)
        if driver.current_url == 'https://accounts.spotify.com/en/status':
            logged_in = True
        else:
            logged_in = False

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
            sleep(5)
            try:
                counter = 0
                for i in range(self.number_of_songs):
                    stream_time = randint(self.minplay,self.maxplay)
                    counter = counter+1
                    driver.execute_script("document.getElementsByClassName('_38168f0d5f20e658506cd3e6204c1f9a-scss')[{0}].click()".format(i))
                    #song_name = driver.execute_script("document.getElementsByClassName('_99bbcff33ae810da0bfc335662ae2c1d-scss _8a9c5cc886805907de5073b8ebc3acd8-scss')[{0}].getAttribute('aria-label')".format(i))
                    sleep(stream_time)
                    #print(song_name)
                    #driver.execute_script("document.getElementsByClassName('control-button spoticon-play-16 control-button--circled')[0].click()")
                    print('PLAYLIST [{0}] SONG [{1}] STREAMED WITH [{2}:{3}] FOR [{4} SECONDS]'.format(playlist_title,counter,username,password,stream_time))
                    with open('streamed.txt','a',encoding='utf8') as f:
                        f.write('PLAYLIST [{0}] SONG [{1}] STREAMED WITH [{2}:{3}] FOR [{4} SECONDS]\n'.format(playlist_title,counter,username,password,stream_time))
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