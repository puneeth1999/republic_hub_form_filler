from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
import os
import requests
import xlrd
import re
import pandas as pd

'''__________________________________________DATA______________________________________________________'''
data = pd.read_excel(r'C:\Users\punee\PycharmProjects\formFillers\venv\data\retrial.xlsx', header = 0)
data = data.drop(['Timestamp', 'MAIN PORTAL Status', 'AGENT STATUS', 'mail'], axis =1)

data = data.dropna()
data = data.drop_duplicates(keep='last')



'''_________________________________________PANDAS______________________________________________________'''
#First Names
fnames = [x.strip('()').split(',') for x in data['First Name']]
first_names = []
for name in fnames:
    first_names.append(str(name[0]))

#Last Names
lnames = [x.strip('()').split(',') for x in data['Last Name']]
last_names = []
for nme in lnames:
    last_names.append(str(nme[0]))


#Genders
gdrs = [x.strip('()').split(',') for x in data['Gender']]
genders = []
for g in gdrs:
    genders.append(str(g[0]))

#DOBs
data['Date of birth'] = data['Date of birth'].dt.strftime('%Y-%m-%d')
dbs = [str(x).strip('()').split(',') for x in data['Date of birth']]
dobs = []
for nme in dbs:
    dobs.append(str(nme[0]))


#Phone Number
nmbrs = [str(x).strip('()').split(',') for x in data['Phone Number']]
numbers = []
for number in nmbrs:
    numbers.append(number[0])

#Street Address
adds = [x.strip('()').split(',') for x in data['Address']]
addresses = []
for a in adds:
    addresses.append(a[0])

#City
cit = [x.strip('()').split(',') for x in data['City']]
cities = []
for c in cit:
    cities.append(c[0])


#Pincode
pins = [str(x).strip('()').split(',') for x in data['Pincode']]
pincodes = []
for p in pins:
    pincodes.append(p[0])


#Email
mails = [x.strip('()').split(',') for x in data['Email Address']]
e_mails = []
for mail in mails:
    e_mails.append(mail[0])

#aadhaar number
adnum = [str(x).strip('()').split(',') for x in data['Adhar Number']]
aadhaar_numbers = []
for a in adnum:
    aadhaar_numbers.append(a[0])

#PAN number
pns = [str(x).strip('()').split(',') for x in data['PAN number']]
PAN_numbers = []
for p in pns:
    PAN_numbers.append(p[0])


'''____________________________________________THE GREAT FOR LOOP____________________________________________________'''
driver = webdriver.Chrome()
# Opening up the page
driver.get("http://dist.republichub.org/doCommonAction.action?param=regAgent")
sleep(2)

# Username
driver.find_element_by_name('loginId').send_keys('YOUR USERNAME HERE')

# Password
driver.find_element_by_name('password').send_keys('YOUR PASSWORD HERE')
sleep(2)

# Submit button
driver.find_element_by_xpath('/html/body/div/div[1]/form/input[4]').click()
for i in range(len(PAN_numbers)):


    # # Opening up the page
    # driver.get("http://dist.republichub.org/doCommonAction.action?param=regAgent")
    # sleep(2)
    #


    # Add agents
    sleep(3)
    driver.get("http://dist.republichub.org/doCommonAction.action?param=regAgent")
    sleep(2)

    # First name
    driver.find_element_by_name('firstname').send_keys(first_names[i])

    # Last name
    driver.find_element_by_name('lastname').send_keys(last_names[i])

    # Gender
    if(str(genders[i]) == 'Male'):
        driver.find_element_by_xpath(
            '/html/body/div[1]/div/div/section/div/form/div[4]/div/select/option[2]').click()  # For male
    else:
        driver.find_element_by_xpath(
            '/html/body/div[1]/div/div/section/div/form/div[4]/div/select/option[3]').click()  # For female


    # Date of birth
    driver.find_element_by_xpath('/html/body/div[1]/div/div/section/div/form/div[3]/div/div/input').send_keys(
        dobs[i])

    # Company/Firm type
    driver.find_element_by_xpath('/html/body/div[1]/div/div/section/div/form/div[5]/div/select/option[3]').click()

    # Company name
    driver.find_element_by_xpath('/html/body/div[1]/div/div/section/div/form/div[6]/div/input').send_keys('CSC MEESEVA')

    # E-mail id
    driver.find_element_by_xpath('/html/body/div[1]/div/div/section/div/form/div[7]/div/input').send_keys(
        e_mails[i])

    # Mobile number
    driver.find_element_by_xpath('/html/body/div[1]/div/div/section/div/form/div[8]/div/input').send_keys(numbers[i])

    # Address
    driver.find_element_by_xpath('/html/body/div[1]/div/div/section/div/form/div[9]/div/input').send_keys(addresses[i])

    # State
    driver.find_element_by_xpath('/html/body/div[1]/div/div/section/div/form/div[12]/div/select/option[3]').click()

    # District
    sleep(3)
    driver.find_element_by_xpath('/html/body/div[1]/div/div/section/div/form/div[13]/div/select/option[3]').click()

    # City
    driver.find_element_by_xpath('/html/body/div[1]/div/div/section/div/form/div[14]/div/input').send_keys(cities[i])

    # Pin code
    driver.find_element_by_xpath('/html/body/div[1]/div/div/section/div/form/div[15]/div/input').send_keys(pincodes[i])

    # PAN
    driver.find_element_by_xpath('/html/body/div[1]/div/div/section/div/form/div[17]/div/input').send_keys(PAN_numbers[i])

    # Submit
    driver.find_element_by_xpath('/html/body/div[1]/div/div/section/div/form/div[18]/div/input').click()


    #Print statement
    print('We took care of', first_names[i], last_names[i], 'the count is', (i+1))


print('____________________________JOB DONE__________________________________')
#System.exit(0)
