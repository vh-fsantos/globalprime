import pyautogui
import pyperclip
import platform
import time
import os

PointsCopyInspectElement = { "X": 1138, "Y": 126 }
PointsCloseInspectElement = { "X": 1342, "Y": 83 }

pyautogui.PAUSE = 2

class AutoGui:
    def __init__(self):
        self.LastBranchId = ""
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
        time.sleep(1)
        pyautogui.write(link)
        pyautogui.press('enter')
        time.sleep(2)
        return
    
    def ChangeStore(self, key, company, branchId):
        lowes = key == "lowes"
        menards = key == "menards"

        self.NavigateToPosition(company.PointChangeStore["X"], company.PointChangeStore["Y"])
        if not menards:
            pyautogui.click()

        if not lowes and not menards:
            pointFindOthers = company.PointFindOthers['Y']
            if self.LastBranchId in company.IdsIncreaseY:
                pointFindOthers += 25
            self.NavigateToPosition(company.PointFindOthers['X'], pointFindOthers)
            pyautogui.click()

        self.NavigateToPosition(company.PointLabel['X'], company.PointLabel['Y'])
        pyautogui.click()

        if lowes: 
            pyautogui.hotkey(self.ctrlKey, 'a')
            pyautogui.hotkey(self.ctrlKey, 'c')
            labelText = str(pyperclip.paste())

        pyautogui.write(branchId)
        pyautogui.press('enter')
        pointSelectStore = company.PointSelectStore['Y']
        if menards and self.LastBranchId in company.IdsIncreaseY:
            pointSelectStore += 15

        self.NavigateToPosition(company.PointSelectStore['X'], pointSelectStore)
        pyautogui.click()
        if lowes and labelText == branchId:
            pyautogui.press('esc')

        if not menards:    
            self.LastBranchId = "#" + branchId
        else:
            self.LastBranchId = branchId    

        time.sleep(1)
        return

    def NavigateToPosition(self, x, y):
        pyautogui.moveTo(x, y, 1)
        return
    
    def GetHtml(self):
        time.sleep(1)
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
    
    def ShowElapsedTime(self, totalElapsed):
        pyautogui.alert(text=f'The execution was succeeded in {totalElapsed}s', title='Execution Finished', button='OK')
