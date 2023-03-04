import pyautogui
import pyperclip
import platform
import time
import os

PointsCopyInspectElement = { "X": 1430, "Y": 1238 }
PointsCloseInspectElement = { "X": 1795, "Y": 1197 }
pyautogui.PAUSE = .25

class AutoGui:
    def __init__(self):
        if (self.IsMacOs()):
            self.ctrlKey =  'command'
        else:
            self.ctrlKey = 'ctrl'

    def IsMacOs(self):
        return platform.system() == "Darwin"

    def OpenChrome(self):
        if (self.IsMacOs()):
            browserPath = '/Applications/Google\ Chrome.app'
            os.system(f"open {browserPath}")
        else: 
            pyautogui.press('winleft')
            pyautogui.write('chrome')
            pyautogui.press('enter')
        
        time.sleep(2)
        return

    def NavigateTo(self, link):
        self.OpenChrome()
        pyautogui.write(link)
        pyautogui.press('enter')
        time.sleep(2)
        return
    
    def ChangeStore(self, company, branchId):
        self.NavigateToPosition(company.PointChangeStore["X"], company.PointChangeStore["Y"])
        pyautogui.click()
        self.NavigateToPosition(company.PointFindOthers['X'], company.PointFindOthers['Y'])
        pyautogui.click()
        self.NavigateToPosition(company.PointLabel['X'], company.PointLabel['Y'])
        pyautogui.click()
        pyautogui.write(branchId)
        pyautogui.press('enter')
        self.NavigateToPosition(company.PointSelectStore['X'], company.PointSelectStore['Y'])
        pyautogui.click()
        return

    def NavigateToPosition(self, x, y):
        pyautogui.moveTo(x, y, .5)
        return
    
    def GetHtml(self):        
        pyautogui.press('f12')
        self.NavigateToPosition(PointsCopyInspectElement['X'], PointsCopyInspectElement['Y'])
        pyautogui.click()
        pyautogui.hotkey(self.ctrlKey, 'c')
        self.NavigateToPosition(PointsCloseInspectElement['X'], PointsCloseInspectElement['Y'])
        pyautogui.click()
        return str(pyperclip.paste())

    def GetMousePosition(self):
        while True:
            time.sleep(2)
            print(pyautogui.position())
        return
    
    def Close(self):
        pyautogui.hotkey(self.ctrlKey, 'w')