from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# a Python package that can install the up-to-date chromedriver
from webdriver_manager.chrome import ChromeDriverManager

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
n = 3
# driver = webdriver.Chrome(executable_path='./chromedriver')
# The above is not working for 1. executable_path has been deprecated selenium python, have to use an instance of the Service() class;
# 2. chromedriver in the path has been outdated.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# The webpage of CODiS is rendered dynamically with AJAX. Found this real link by monitoring AJAX response with DevTools.
url = "https://e-service.cwb.gov.tw/HistoryDataQuery/QueryDataController.do?command=viewMain&_=1649428773019"


driver.get(url)
# Links for CSV download and moving to next month data will be hidden if the windows is not maximize
driver.maximize_window()

# Select County
selectCounty = Select(driver.find_element(By.ID, 'stationCounty'))
selectCounty.select_by_visible_text(County)

wait = WebDriverWait(driver, 10) # Define max waiting time

# Select Station
sub_menu = wait.until(EC.element_to_be_clickable((By.ID, 'station')))
selectStation = Select(sub_menu)
selectStation.select_by_visible_text(Station)

# Select Dataclass and DataType
selectDataClass = Select(driver.find_element(By.ID, 'dataclass'))
selectDataClass.select_by_visible_text(DataClass)
selectDataType = Select(driver.find_element(By.ID, 'datatype'))
selectDataType.select_by_visible_text(DataType)

# Select Date
element_date = driver.find_element(By.ID, 'datepicker')
element_date.send_keys(Date)

# Click submission button
element_submitBTN = driver.find_element(By.ID, 'doquery')
element_submitBTN.click()

# Switch to the newly popped-out window
wait.until(EC.number_of_windows_to_be(2)) # window_handles[1] is the second window
driver.switch_to.window(driver.window_handles[1])

# Loop through download and next month buttons
for i in range(n):
    element_downloadBTN = wait.until(EC.element_to_be_clickable((By.ID, 'downloadCSV')))
    element_downloadBTN.click()

    element_nextBTN = wait.until(EC.element_to_be_clickable((By.ID, 'nexItem')))
    element_nextBTN.click()

# Close the window
driver.quit()
