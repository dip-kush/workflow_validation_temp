import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Crawler import initState
from logger import LoggerHandler
from FormExtractor import getFormFieldValue
from BeautifulSoup import BeautifulSoup

logger = LoggerHandler(__name__)


class Globals:
    '''
    Contains initialization of all the global variables
    '''

    def __init__(self):
        self.formFieldValues = {'id': {} , 'xpath': {}, 'name': {}}
        self.bannedUrls = []
        self.scopeUrls = []
        self.waitTime= 0
        self.baseAddress = ""        
        
    def getFormValues(self, formFile):
        self.formFieldValues = getFormFieldValue(formFile)
        
     
    def addBlackList(self, urls):
        print urls.split(',')
        self.bannedUrls = urls.split(',')
                
    def setGlobalWait(self, time):
        self.waitTime = time    
        
    def addScopeUrl(self, urls):
        self.scopeUrls = urls.split(",")
        
    def addBaseAddress(self, baseAddress):
        self.baseAddress = baseAddress

def doLogin(script,login_url ,driver):
    driver.get(login_url)
    f = open("login_script.html")
    bs = BeautifulSoup(f)
    l = bs.findAll("tr")
    print l
    for i in range(1, len(l)):
        type = l[i].findAll("td")[0].text
        target = l[i].findAll("td")[1].text
        value = l[i].findAll("td")[2].text
        
        if value == "" and type == "clickAndWait":
            element = driver.find_element_by_xpath(
            "(//input[@type='submit'])")
            element.click()            
        elif value != "":
            # print target, value
            target = str(target)
            index = str(target).find('=')
            type = target[0:index]
            fieldVal = target[index + 1:]
            if type == "id":
                print fieldVal
                element = driver.find_element_by_id(fieldVal)
                element.send_keys(value)
            elif type == "name":
                driver.find_element_by_name(fieldVal).send_keys(value)
            else:    
                driver.find_element_by_xpath(fieldVal).send_keys(value)
             

def main():
    '''
    crawls the demo website http://127.0.0.1:81/login/login.php
    with login credentials
    email = vinaysharma@gmail
    password = vinaykool
    '''
    login_url = None
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-l", "--login-script", action="store", dest="login_script", help="Path to python login script")
    parser.add_argument("-u", "--login-url", action="store", dest="login_url", help="Login Page Url")
    parser.add_argument("-f", "--form-script", action="store", dest="form_values_script", help="Path to Form Values Script")
    parser.add_argument("-b", "--base-address", action="store", dest="base_address", help="Base address")
    parser.add_argument("-s", "--start-url", action="store", dest="start_url", help="Starting Page Url")
    parser.add_argument("-bl", "--black-list", action="store", dest="black_list_urls", help="Black List Urls")
    parser.add_argument("-sc", "--scope", action="store", dest="scope_url", help="scope of the crawler")
    parser.add_argument('-t', action="store", dest="time", type=int)
    args = parser.parse_args()
    
    globalVariables = Globals()

    # globalVariables.bannedUrls.append("http://127.0.0.1:81/login/profile.html")

    #driver = webdriver.PhantomJS()
    
    driver = webdriver.Chrome()
    logger.info("Browser is Launched")
    #driver.get("http://127.0.0.1:81/login/login.php")
    if args.login_url:
        login_url = args.login_url
        
    if args.login_script:
        logger.info("Logging in Application")
        if not login_url:
            logger.error("No Login URL provided")
        else:
            doLogin(args.login_script, login_url ,driver)

    if args.form_values_script:
        globalVariables.getFormValues(args.form_values_script)
   
    if args.base_address:
        globalVariables.addBaseAddress(args.base_address)
        

    if args.start_url:
        driver.get(args.start_url)    
    
    if args.scope_url:
        globalVariables.addScopeUrl(args.scope_url)
    
    if args.black_list_urls:
        globalVariables.addBlackList(args.black_list_urls)

    if not args.start_url and not args.login_url:
        logger.error("No Start Url Provided not Login Url Provided")
        return 
    
    if args.time:
        globalVariables.setGlobalWait(args.time)
        
    # time.sleep(5)
    # print driver.page_source
    print driver.current_url, driver.title
    # move the controller to Initiate Crawler Activity
    logger.info("Initiating the Crawler")
    initState(
        driver.page_source,
        driver.current_url,
        driver.title,
        driver,
        globalVariables)

    #assert "Welcome, " in driver.page_source
    driver.close()


if __name__ == '__main__':
    main()
