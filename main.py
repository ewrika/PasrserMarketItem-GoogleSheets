import time
from time import sleep
from info import *
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
import traceback


try:
    s='"'
    c='"'
    i=0
    j=1
    A = 2
    B = 2
    C = 2
    D = 2
    pages = 1
    #Инициализируем селениум
    firefox_binary = FirefoxBinary()
    driver = webdriver.Firefox(firefox_binary=firefox_binary)
    Options.binary_location = r"C:/location/to/Firefox/Binary/firefox.exe"

    urls="https://steamcommunity.com/market/"
    driver.get(url=urls)
    #Входим в стим под логином+паролем+гуард
    driver.find_element_by_class_name('global_action_link').click()
    sleep(2)

    driver.find_element_by_class_name('newlogindialog_TextInput_2eKVn').send_keys(username)
    sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[2]/input').send_keys(password)
    sleep(1)
    driver.find_element_by_class_name('newlogindialog_SubmitButton_2QgFE').click()
    #Вводим гуард
    code1=input("1st-code")
    driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/form/div/div[2]/div/input[1]').send_keys(code1)
    code2=input("2st-code")
    driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/form/div/div[2]/div/input[2]').send_keys(code2)
    code3=input("3st-code")
    driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/form/div/div[2]/div/input[3]').send_keys(code3)
    code4=input("4st-code")
    driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/form/div/div[2]/div/input[4]').send_keys(code4)
    code5=input("5st-code")
    driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/form/div/div[2]/div/input[5]').send_keys(code5)
    sleep(4)
    #pages - первая страница маркеты игры , а 1237 это общее количество +1
    while pages <1237 :
        url = f"https://steamcommunity.com/market/search?appid=304930#p{pages}_popular_desc"
        driver.get(url=url)
        pages +=1
        i=0
        j=1
        k=1
        #Обязательно делаем тайм слип в 6 секунд, тк через 60 айтомов гугл не дает записывать значение
        time.sleep(6)
        #общее количество которое тратится на страницу с тайм слипом = 15 секунд
        #15 секунд*1236 страниц = 18540 секунд/60 =309/60=5.15 часов на 12360 предметов
        while i <10:
            #Вроде бы i это количество изображений
            elem = driver.find_element_by_id(f'result_{i}_name')
            html = driver.execute_script("return arguments[0].innerHTML;", elem)
            #тут название получаем
            img = driver.find_element_by_id(f"result_{i}_image")
            src = img.get_attribute('src')
            #тут получаем цену
            elem2 = driver.find_element_by_xpath(f'/html/body/div[1]/div[7]/div[2]/div[1]/div[4]/div[2]/div[2]/div/div[1]/a[{j}]/div/div[1]/div[2]/span[1]/span[1]')
            html2 = driver.execute_script("return arguments[0].innerHTML;", elem2)
            #а тут количество
            elem3 = driver.find_element_by_xpath(f'/html/body/div[1]/div[7]/div[2]/div[1]/div[4]/div[2]/div[2]/div/div[1]/a[{k}]/div/div[1]/div[1]/span/span')
            html3 = driver.execute_script("return arguments[0].innerHTML;", elem3)

            # Файл, полученный в Google Developer Console
            CREDENTIALS_FILE = 'zalua-376207-e21a54e28d94.json'
            # ID Google Sheets документа (можно взять из его URL)
            spreadsheet_id = '1IjZapTadE1vt6LqOo_o9zgwBRudR1JlC7Q98IyFk5cU'

            # Авторизуемся и получаем service — экземпляр доступа к API
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                CREDENTIALS_FILE,
                ['https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive'])
            httpAuth = credentials.authorize(httplib2.Http())
            service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
            # Пример записи в файл
            values = service.spreadsheets().values().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    "valueInputOption": "USER_ENTERED",
                    "data": [
                        {"range": f"A{A}",
                         "majorDimension": "COLUMNS",
                         "values": [[f"=IMAGE({s}{src}{c})"]]},
                        {"range": f"B{B}",
                         "majorDimension": "COLUMNS",
                         "values": [[f"{html}"]]},
                        {"range": f"C{C}",
                         "majorDimension": "COLUMNS",
                         "values": [[f"{html2}"]]},
                        {"range": f"D{D}",
                         "majorDimension": "COLUMNS",
                         "values": [[f"{html3}"]]}

                    ]
                }
            ).execute()
            i+= 1
            j+= 1
            k+= 1
            A+= 1
            B+= 1
            C+= 1
            D+= 1
except Exception:
    traceback.print_exc()
    print('Ошибка, отдыхаем')
    print(pages)


