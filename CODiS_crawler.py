from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# County = '臺北市 (TaipeiCity)'
# Station = '臺北 (TAIPEI)'
#
# County = '臺中市 (TaichungCity)'
# Station = '臺中 (TAICHUNG)'

County = '高雄市 (KaohsiungCity)'
Station = '高雄 (KAOHSIUNG)'

DataClass = '資料查詢 (Data Inquiry)'
DataType = '月報表 (monthly data)'
Date = '2018-01'
n = 54
driver = webdriver.Chrome(executable_path='./chromedriver')
# The webpage of CODiS is rendered dynamically with AJAX. Found this real link by monitoring AJAX response with DevTools.
url = "https://e-service.cwb.gov.tw/HistoryDataQuery/QueryDataController.do?command=viewMain&_=1649428773019"


driver.get(url)
# Links for CSV download and moving to next month data will be hidden if the windows is not maximize
driver.maximize_window()

selectCounty = Select(driver.find_element(By.ID, 'stationCounty'))
selectCounty.select_by_visible_text(County)

wait = WebDriverWait(driver, 10)
sub_menu = wait.until(EC.element_to_be_clickable((By.ID, 'station')))
selectStation = Select(sub_menu)
selectStation.select_by_visible_text(Station)

selectDataClass = Select(driver.find_element(By.ID, 'dataclass'))
selectDataClass.select_by_visible_text(DataClass)
selectDataType = Select(driver.find_element(By.ID, 'datatype'))
selectDataType.select_by_visible_text(DataType)

element_date = driver.find_element(By.ID, 'datepicker')
element_date.send_keys(Date)
element_submitBTN = driver.find_element(By.ID, 'doquery')
element_submitBTN.click()

wait.until(EC.number_of_windows_to_be(2))
# window_handles[1] is a second window
driver.switch_to.window(driver.window_handles[1])

for i in range(n):
    element_downloadBTN = wait.until(EC.element_to_be_clickable((By.ID, 'downloadCSV')))
    element_downloadBTN.click()

    element_nextBTN = wait.until(EC.element_to_be_clickable((By.ID, 'nexItem')))
    element_nextBTN.click()

element_downloadBTN = wait.until(EC.element_to_be_clickable((By.ID, 'downloadCSV')))
element_downloadBTN.click()

driver.quit()
