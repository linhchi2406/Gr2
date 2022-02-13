from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time

phone = "linhchi24060508@gmail.com"
password = "linhchi24060508@@"
service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get('https://www.facebook.com')
# time.sleep(3)
# driver.find_element_by_css_selector("input[name='email']").send_keys(phone)
# driver.find_element_by_css_selector("input[name='pass']").send_keys(password)
# driver.find_element_by_css_selector("button[type='submit']").click()
# time.sleep(10)
# time.sleep(5)
# search = driver.find_element_by_css_selector("input[type='search']")
# search.send_keys("Quang Trần")
# search.send_keys(Keys.ENTER)
def post_fb(driver):
    for x in range(1, 5):
        time.sleep(4)
        driver.find_element_by_xpath("//div[@class='m9osqain a5q79mjw gy2v8mqq jm1wdb64 k4urcfbm qv66sw1b']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//div[@data-contents='true']").send_keys("Test 2"+ str(x))
        driver.find_element_by_xpath("//div[@aria-label='Đăng']").click()
        time.sleep(1)
def like(driver):
    driver.find_element_by_xpath('//div[@aria-label="Thích"]').click();
    time.sleep(1)
def login(driver):
    time.sleep(2)
    driver.find_element_by_css_selector("input[name='email']").send_keys(phone)
    driver.find_element_by_css_selector("input[name='pass']").send_keys(password)
    driver.find_element_by_css_selector("button[type='submit']").click()
    time.sleep(3)
def search(driver, content):
    time.sleep(5)
    search = driver.find_element_by_css_selector("input[type='search']")
    search.send_keys(content)
    search.send_keys(Keys.ENTER)
    time.sleep(3)
    driver.find_element_by_xpath("//div[@class='tvfksri0 taijpn5t j83agx80 ll8tlv6m']").click()
    time.sleep(5)
    driver.find_element_by_xpath('//div[@class="oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 mg4g778l pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr du4w35lb n00je7tq arfg74bv qs9ysxi8 k77z8yql pq6dq46d btwxx1t3 abiwlrkh p8dawk7l lzcic4wl gokke00a"]').click();

if __name__ == "__main__":
    login(driver)
    time.sleep(10)
    for x in range(1, 10):
        like(driver)
        time.sleep(2)
    # post_fb(driver)
    driver.quit
    