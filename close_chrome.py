from os import system,name

def SetTitle(title_name:str):
    system("title {0}".format(title_name))

def clear():
    if name == 'posix':
        system('clear')
    elif name in ('ce', 'nt', 'dos'):
        system('cls')
    else:
        print("\n") * 120

SetTitle('One Man Builds Chrome Killer')
clear()
system('color 2 & taskkill /F /IM chrome.exe /T')
system('pause > nul')