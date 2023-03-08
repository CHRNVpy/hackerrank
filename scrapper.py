import json
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
import pyperclip
import chromedriver_binary
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Wait for an element to be present before proceeding
def wait_for_element_present(driver, locator, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )


# Wait for an element to be visible before proceeding
def wait_for_element_visible(driver, locator, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


result = {}

# getting all url links from google spreadsheet
def get_url_list(sheet_name: str, start_row: int):
    # set up credentials to access the Google Sheets API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('peppy-tiger-374003-fa5a704f0d24.json', scope)
    client = gspread.authorize(creds)

    # open the Google Spreadsheet
    sheet = client.open(sheet_name).sheet1

    # get all values in the sheet
    values = sheet.get_all_values()

    # iterate over values in the first column and exclude the header row
    for row in values[start_row:]:

        with open('links_from_spreadsheet.txt', 'a', newline='\n') as spreadsheet:
            spreadsheet.write(row[0] + '\n')


def get_data(source_url: str, login: str, password: str, counter: int):
    # getting data
    match = re.findall(r'\d+', source_url)
    if match:
        result['test_id'] = match[0]
        result['candidate_test_id'] = match[1]

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless') #can't use it, because code not copying to clipboard this way
    options.add_argument('user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0')
    options.add_argument(
        'cookies=fileDownload=true; hackerrankx_mixpanel_token=4a68ea1d-1c84-470c-a207-89ab9eba241b; session_referrer=https%3A%2F%2Fwww.google.com%2F; session_referring_domain=www.google.com; session_landing_url=https%3A%2F%2Fwww.hackerrank.com%2Fx%2Ftests%2F1510939%2Fcandidates%2F49219581%2Freport; _hrank_session=5b5a25e15aa86e07bb1bd25839613e9606f750b692af7a72d2ddffc50763fdf572ca660b9671a5f9c62910d0796f81f39777aaf36f46e76f92984800e8bc0cbb; _hp2_id.547804831=%7B%22userId%22%3A%223147998544213731%22%2C%22pageviewId%22%3A%221475261596001259%22%2C%22sessionId%22%3A%226533966268556496%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _ga=GA1.2.637147955.1677490464; _gid=GA1.2.1025315313.1677490464; web_browser_id=8851c39a690efff63c0cd85cd4d3dae1; ln_or=eyI0Nzc3MCI6ImQiLCI1ODIxMSI6ImQifQ%3D%3D; fs_uid=#Q02VK#5164114984751104:5234565886955520:::#f8a2de90#/1709026464; homepage_variant=about:srcdoc; _gcl_au=1.1.1895170442.1677490467; _an_uid=0; _gd_visitor=6841c7e0-674e-492e-87b7-1435877ed9a4; _gd_session=44a047bf-6f2f-4379-805d-adb085e86fe2; _uetsid=ee713760b68111ed8edf3dbdba387647; _uetvid=ee714670b68111ed951311d9ddc826f1; _ga=GA1.1.637147955.1677490464; _gid=GA1.1.1025315313.1677490464; show_cookie_banner=false; _wchtbl_uid=b24d9ebd-b563-4a9f-a1d2-9b68378fcf5e; _wchtbl_sid=36456d2a-18eb-4fcc-a67d-7581f2dd724f; _ga_BCP376TP8D=GS1.1.1677490570.1.1.1677490611.0.0.0; _ga_4G810X81GK=GS1.1.1677490570.1.1.1677490611.0.0.0; _ga_X2HP4BPSD7=GS1.1.1677490570.1.1.1677490611.0.0.0; _ga_ZDWKWB1ZWT=GS1.1.1677490571.1.1.1677490611.0.0.0; _ga_0QME21KCCM=GS1.1.1677490571.1.1.1677490611.0.0.0; _ga_R0S46VQSNQ=GS1.1.1677490571.1.1.1677490611.0.0.0; _ce.s=v~4f2cd5e0e660ccff545288839527133180690a93~vpv~0; cebs=1; _ce.clock_event=1; _mkto_trk=id:487-WAY-049&token:_mch-hackerrank.com-1677490581410-47174; hackerrank_mixpanel_token=269385c8-9a8a-4dee-828f-c6729638a2c2; hrc_l_i=T; _gd_svisitor=645b6068a00f00009179fc6335000000aa370e00; _ce.clock_data=85%2C90.156.228.9; cebsp_=2; mp_bcb75af88bccc92724ac5fd79271e1ff_mixpanel=%7B%22distinct_id%22%3A%20%221b66913d-d8c5-41ed-86f6-b56afb719602%22%2C%22%24device_id%22%3A%20%2218692393e661a5-08cead3596e7498-9762636-ff000-18692393e6736a%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%2C%22%24user_id%22%3A%20%221b66913d-d8c5-41ed-86f6-b56afb719602%22%7D; user_type=recruiter; _pk_id.5.fe0a=245dd33ddad61f6e.1677490616.; react_var=true__trm4; react_var2=true__trm4; metrics_user_identifier=101f1cc-a5f8b13ce50512f8f067f3906bd166e3eb8b4847; _hjSessionUser_2036154=eyJpZCI6IjU1NDc5MDA1LTdjNGYtNTc5My1hNThmLTQ2NGE2MjE5MzFhOCIsImNyZWF0ZWQiOjE2Nzc0OTA3Njk5NzgsImV4aXN0aW5nIjpmYWxzZX0=; _fbp=fb.1.1677491409399.1418790869; _biz_uid=90060d8aa08b4677982ad6f98ad5f9b4; _biz_nA=16; _biz_pendingA=%5B%5D; _biz_flagsA=%7B%22Version%22%3A1%2C%22Mkto%22%3A%221%22%2C%22ViewThrough%22%3A%221%22%2C%22XDomain%22%3A%221%22%7D; mp_bcb75af88bccc92724ac5fd79271e1ff_mixpanel=%7B%22distinct_id%22%3A%20%22269385c8-9a8a-4dee-828f-c6729638a2c2%22%2C%22%24device_id%22%3A%20%2218692393e661a5-08cead3596e7498-9762636-ff000-18692393e6736a%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%2C%22%24user_id%22%3A%20%22269385c8-9a8a-4dee-828f-c6729638a2c2%22%7D; access_token=49ee469a443e8cf4a900f380adb98f2d92903781a502aacd09ea4747e1a9cd70; session_id=kzdiulit-1677491610443; NPS_7398d1c9_last_seen=1677491616574; hacker_editor_theme=light; _hp2_ses_props.547804831=%7B%22r%22%3A%22https%3A%2F%2Fwww.hackerrank.com%2Fx%2Ftests%2Fall%2F1510939%2Fcandidates%2Fcompleted%2F49272112%2Freport%2Fdetailed%22%2C%22ts%22%3A1677495420797%2C%22d%22%3A%22www.hackerrank.com%22%2C%22h%22%3A%22%2Fwork%2Ftests%2F1510939%2Fcandidates%2Fcompleted%2F49272112%2Freport%2Fsummary%22%7D')
    driver = webdriver.Chrome(options=options)

    driver.get(url=source_url)
    driver.implicitly_wait(10)

    # enter login
    login = driver.find_element(By.ID, 'input-1').send_keys(login)
    next_button = driver.find_element(By.XPATH,
                                      '/html/body/div[4]/div/div/div/div/div[1]/div/div/div/div/form/button[1]').click()

    driver.implicitly_wait(10)

    # enter password
    password = driver.find_element(By.ID, 'input-2').send_keys(password)
    password_button = driver.find_element(By.XPATH,
                                          '/html/body/div[4]/div/div/div/div/div[1]/div/div/div/div/form/button/div/span').click()


    question_row = wait_for_element_visible(driver, (By.CLASS_NAME, "question-row"))
    question_number_list = []
    if question_row:

        # get question number, score
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        strings = soup.find_all('div', {'class': 'question-row'})
        for string in strings:
            string_match = re.search(r'^(\d+).*?(\d+/\d+)', string.text.strip(''))
            if match:
                problem_number = string_match.group(1)
                score = string_match.group(2)
                question_number_list.append(problem_number)
                question_number_list.append(score)

    score_1 = question_number_list[1]
    score_2 = question_number_list[3]

    question_number_1 = {'score': score_1}
    question_number_2 = {'score': score_2}

    # click to view code
    view_button = driver.find_element(By.XPATH,
                                      '/html/body/div[4]/div/div/div/div/div/div[2]/div[3]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div/div[3]/a/div/span').click()

    def get_code(question_number):
        code_page = wait_for_element_visible(driver, (By.CLASS_NAME, "c-fawirw"))

        if code_page:
            soup_code = BeautifulSoup(driver.page_source, 'html.parser')

            if soup_code.find('span', {'class': "c-fawirw"}).find('span').text == 'Not Attempted':
                question_number['candidate_code'] = 'No attempts'
                return question_number

            if soup_code.find('span', {'class': "c-fawirw"}).find('span').text == 'Partial' or 'Correct':
                # print(soup_code.find('span', {'class': "c-fawirw"}).find('span').text)
                code_lang = soup_code.find('span', {'data-automation': "ques-languge"}).text

                question_number['code_language'] = code_lang

                copy_code_button = driver.find_element(By.CSS_SELECTOR,
                                                       '.report-playback__copy-code > span:nth-child(1)'
                                                       ' > div:nth-child(1) > svg:nth-child(1)').click()

                question_number['candidate_code'] = pyperclip.paste()
                return question_number

            if soup_code.find('span', {'class': "c-fawirw"}).find('span').text == 'Incorrect':
                code_lang = soup_code.find('span', {'data-automation': "ques-languge"}).text

                question_number['code_language'] = code_lang

                next_copy_code_button = driver.find_element(By.CSS_SELECTOR,
                                                            '.report-playback__copy-code > span:nth-child(1)'
                                                            ' > div:nth-child(1) > svg:nth-child(1)').click()

                question_number['candidate_code'] = pyperclip.paste()
                return question_number

    result[f'question_{question_number_list[0]}'] = get_code(question_number_1)

    next_button = driver.find_element(By.CSS_SELECTOR, 'button.c-jakQqY:nth-child(2)').click()

    result[f'question_{question_number_list[2]}'] = get_code(question_number_2)

    print(f'Report #{counter} for candidate {match[1]} saved to JSON')

    return result


result_list = []
error_urls = []
my_list = []

# open the text file with error links
with open('error_urls.txt', 'r') as file:
    # read the contents of the file and split into lines
    contents = file.read()
    lines = contents.split('\n')
    for line in lines:
        my_list.append(line)


def main(login, password):
    # open the text file with spreadsheet links
    with open('links_from_spreadsheet.txt') as links:
        urls = [link.split('\n') for link in links.read().split(',')]
    counter = 1
    urls = urls[0][:-1]
    reports = []
    for url in urls:  # if errors occurs after scan, change urls to my_list, this will scan error_urls.txt(unscanned urls)
        try:
            res = get_data(url, login=login, password=password, counter=counter)
            reports.append(res)
            with open('one_reports.json', 'w') as report:
                json.dump(reports, report, indent=4)
                #report.write(',\n')
        except AttributeError:
            error_urls.append(url)
            print(f'Something happened')
            continue
        except IndexError:
            error_urls.append(url)
            print(f'Something happened')
            continue
        except TimeoutException:
            error_urls.append(url)
            print(f'Oops, the page is loading too slow or not loading at all')
            continue
        print(error_urls)
        counter += 1
        time.sleep(10)

    with open('error_urls.txt', 'w') as f:
        for url in error_urls:
            f.write(url + '\n')


if __name__ == '__main__':
    """ Firstly you need to run get_urls_list, and wait until links_from_spreadsheet.txt appears, 
    then comment the func with #
    Run main func """

    #get_url_list('Hackerrank Reports', 0) # int 0 is the row of spreadsheet to start

    # input lists has 2 options urls - list with links from spreadsheet, and my_list - error_links
    main(login='LOGIN', password='PASSWORD')

