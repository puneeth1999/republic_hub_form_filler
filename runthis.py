from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import Select
import os
import requests
import xlrd
import re
import pandas as pd




'''____________ GOOGLE DRIVE IMAGE DOWNLOAD WITH ID __________________'''

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)




'''__________________ TURNING LINK INTO ID ____________________'''

def turn_into_id(link):
    string = link
    start_index = string.find('id=') + int(3)
    end_index = len(string)
    str_required = string[start_index:end_index]
    # print('file/image id',str_required)
    return str_required

def download_image_aadhaar(link):
    file_id = turn_into_id(link)
    destination = './aadhaar.png'
    download_file_from_google_drive(file_id, destination)

def download_image_pan(link):
    file_id = turn_into_id(link)
    destination = './pan.png'
    download_file_from_google_drive(file_id, destination)





'''______________________________PANDAS TO EXTRACT LISTS____________________________________'''

data = pd.read_excel(r'C:\Users\punee\PycharmProjects\formFillers\venv\data\retrial.xlsx', header = 0)
data = data.drop(['Timestamp', 'MAIN PORTAL Status', 'AGENT STATUS', 'mail'], axis =1)

data = data.dropna()
data = data.drop_duplicates(keep='last')




#Aadhaar and PAN cards
aadhaars = [x.strip('()').split(',') for x in data['Aadhar Upload']]

pans = [x.strip('()').split(',') for x in data['PAN Card Upload']]

aadhaar_links = []
pan_cards = []

for a in aadhaars:
    aadhaar_links.append(str(a[0]))

for p in pans:
    pan_cards.append(str(p[0]))


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
data['Date of birth'] = data['Date of birth'].dt.strftime('%d/%m/%Y')
dbs = [str(x).strip('()').split(',') for x in data['Date of birth']]
dobs = []
for nme in dbs:
    dobs.append(str(nme[0]))


#Phone Number
nmbrs = [str(x).strip('()').split(',') for x in data['Phone Number']]
numbers = []
for number in nmbrs:
    numbers.append((number[0][:10]))
print(numbers)

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






'''___________________________THE GREAT WALL OF THE FOR LOOP__________________________________'''

#TO FILL IN THE FORM
new_reg_counter = 1
driver = webdriver.Chrome()
for i in range(len(aadhaar_numbers)):

    # Opening up the page
    driver.get("https://republichub.net/customer/account/create/")
    sleep(3)
    # first name
    driver.find_element_by_xpath(
        '/html/body/div[2]/main/div[3]/div/form/fieldset[1]/div[1]/div/fieldset/div/div[2]/div/input').send_keys(
        first_names[i])
    # last name
    driver.find_element_by_xpath(
        '/html/body/div[2]/main/div[3]/div/form/fieldset[1]/div[1]/div/fieldset/div/div[3]/div/input').send_keys(last_names[i])
    # DOB
    driver.find_element_by_xpath(
        '/html/body/div[2]/main/div[3]/div/form/fieldset[1]/div[3]/div/input').send_keys(dobs[i])
    # Gender
    select = Select(driver.find_element_by_name('gender'))
    if (genders[i] == 'Male'):
        select.select_by_value('1')
    else:
        select.select_by_value('2')
    # E-mail
    driver.find_element_by_xpath(
        '/html/body/div[2]/main/div[3]/div/form/fieldset[3]/div[1]/div/input').send_keys(e_mails[i])
    # Password
    driver.find_element_by_xpath(
        '/html/body/div[2]/main/div[3]/div/form/fieldset[3]/div[2]/div/input').send_keys('king@123')
    # Confirm Password
    driver.find_element_by_xpath(
        '/html/body/div[2]/main/div[3]/div/form/fieldset[3]/div[3]/div/input').send_keys('king@123')
    # Reference Name
    driver.find_element_by_xpath(
        '/html/body/div[2]/main/div[3]/div/form/fieldset[3]/div[4]/div/input').send_keys('Choppanati Srinivasulu')
    # Reference Phone Number
    driver.find_element_by_xpath(
        '/html/body/div[2]/main/div[3]/div/form/fieldset[3]/div[5]/div/input').send_keys('9701132249')

    # Phone Number
    driver.find_element_by_xpath(
        '/html/body/div[2]/main/div[3]/div/form/fieldset[2]/div[1]/div/input').send_keys(numbers[i])
    # Street Address
    driver.find_element_by_xpath(
        '/html/body/div[2]/main/div[3]/div/form/fieldset[2]/div[2]/div/input').send_keys(
        addresses[i])
    # City
    driver.find_element_by_xpath(
        '/html/body/div[2]/main/div[3]/div/form/fieldset[2]/div[3]/div/input').send_keys(cities[i])
    sleep(3)
    # State
    sel = Select(driver.find_element_by_xpath('/html/body/div[2]/main/div[3]/div/form/fieldset[2]/div[4]/div/select'))
    sleep(4)
    sel.select_by_value('534')

    # Aadhaar
    driver.find_element_by_xpath(
        '/html/body/div[2]/main/div[3]/div/form/fieldset[3]/div[6]/div/input').send_keys(aadhaar_numbers[i])

    # PAN number
    driver.find_element_by_xpath(
        '/html/body/div[2]/main/div[3]/div/form/fieldset[3]/div[7]/div/input').send_keys(PAN_numbers[i])
    sleep(1)

    # Submit button
    driver.find_element_by_xpath(
        '/html/body/div[2]/main/div[3]/div/form/div[2]/div[1]/button').click()

    download_image_aadhaar(aadhaar_links[i])
    download_image_pan(pan_cards[i])


    try:
        # Choose File Aadhaar
        sleep(4)

        #print('Downloaded the aadhaar and pan of', first_names[i])
        try:
            driver.find_element_by_name(
                'application_form_attatchment').send_keys(r'C:\Users\punee\PycharmProjects\formFillers\venv\aadhaar.png')
        except:
            pass
        sleep(2)
        # Choose FIle PAN
        try:
            driver.find_element_by_name('agreement_copy_attatchment').send_keys(r'C:\Users\punee\PycharmProjects\formFillers\venv\pan.png')
        except:
            pass

        sleep(2)
        # Submit KYC
        driver.find_element_by_xpath(
            '/html/body/div[2]/main/div[3]/div[1]/form/div/div[3]/div/div/input').click()
        sleep(10)
        driver.find_element_by_xpath('/html/body/div[2]/header/div/div/div[2]/div[1]/ul/li[8]/a').click()
        new_reg_counter += 1
        print('Newly registered', first_names[i], last_names[i], 'The current count is', new_reg_counter)
        sleep(10)

    except:
        print('The user',first_names[i],last_names[i], 'was already registered. The count is', i+1)
        pass
        continue
    continue

print('____________________________JOB DONE__________________________________')




