import pyautogui

import time

words = open("word.txt","r")
time.sleep(10)

for word in words:
    pyautogui.typewrite(words)
    pyautogui.press('enter')
    time.sleep(5)