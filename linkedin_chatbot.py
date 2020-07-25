import os, random,sys, time
from urllib.parse import urlparse
from selenium import webdriver
from bs4 import BeautifulSoup

browser = webdriver.Chrome('/home/prateek/Documents/chatbot/chromedriver')

browser.get('https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Ffeed%2F&fromSignIn=true&trk=cold_join_sign_in')
file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]

elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)

browser.refresh()



visitingProfileID = '/in/prateek-gupta-b4113b16b/'
fullLink = 'https://www.linkedin.com' + visitingProfileID
browser.get(fullLink)

visitedProfiles = []
profilesQueued = []


def getNewProfileIDs(soup, profilesQueued):
    profilesID=[]
    pav = soup.find('section',{'class': 'pv-browsemap-section pv-browsemap-section__wrapper'})
    all_links = pav.findAll('a',{'class':'pv-browsemap-section__member ember-view'})
    for link in all_links:
        userID = link.get('href')
        if((userID not in profilesQueued) and (userID not in visitedProfiles)):
            profilesID.append(userID)

    return profilesID




profilesQueued = getNewProfileIDs(BeautifulSoup(browser.page_source, "lxml"), profilesQueued)            

while profilesQueued:
    try:
        visitingProfileID = profilesQueued.pop()
        visitedProfiles.append(visitingProfileID)
        fullLink = 'https://www.linkedin.com' + visitingProfileID
        browser.get(fullLink)
        browser.find_element_by_class_name("pv-s-profile-actions ").click()
        browser.find_element_by_class_name("mr1").click()

        customMessage= "Hello, It's my pleasure to connect with you!!!"
        elementID = browser.find_element_by_id('custom-message')
        elementID.send_keys(customMessage)

        browser.find_element_by_class_name("ml1").click()

       #Add the ID to the visitedusersfile

        with open('visitedUsers.txt','a') as visitedUsersFile:
            visitedUsersFile.write(str(visitingProfileID) + '\n')

        visitedUsersFile.close()

       #Get new profiles ID
        soup = BeautifulSoup(browser.page_source)
        try:
            profilesQueued.extend(getNewProfileIDs(soup, profilesQueued))
        except:
             print('continue')

        #Pause
        time.sleep(random.uniform(5, 15))

        if(len(visitedProfiles)%50==0):
             print("Visited profiles: ", len(visitedProfiles))
        
        if(len(profilesQueued)> 100000):
            with open('profileQueued.txt','a') as visitedUsersFile:
                visitedUsersFile.write(str(visitingProfileID) + '\n')

            visitedUsersFile.close()    
            print('100000 Done!!!!!')
            break

    except:
        print("error")    
        

      
        
         