from selenium import webdriver

import web_driver_tools

if __name__ == '__main__':
    driver = webdriver.Chrome()
    try:
        # 打开页面
        driver.get('http://www.zhihu.com')
        # 截屏
        screenshot_file = "d:/zhihu.png"
        element = driver.find_element_by_class_name("SignFlowHomepage-logo")
        driver_tools = web_driver_tools.WebDriverTools(driver)
        driver_tools.screenshot_on_element(element, screenshot_file)
    finally:
        driver.close()
    pass
