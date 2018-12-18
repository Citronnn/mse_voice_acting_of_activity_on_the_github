import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from sys import platform as _platform

#Проверка кнопки About (открыть,закрыть,открыть,закрыть)
def test_about(driver):
    about_but = driver.find_element_by_id('aboutbutton')
    about_but.click()
    #time.sleep(1)
    about_span = driver.find_element_by_tag_name('span')
    about_span.click()
    #time.sleep(1)
    about_but = driver.find_element_by_id('aboutbutton')
    about_span = driver.find_element_by_tag_name('span')

#Проверка кнопки смены цвета (проверка цветов, смена темы, проверка цветов, смена темы)
def test_theme_colors(driver):
    color_but = driver.find_element_by_id('changecolors')
    header = driver.find_element_by_id('VA')
    body = driver.find_element_by_tag_name('body')
    bar = driver.find_element_by_id('bar')
    displaydiv = driver.find_element_by_id('displaydiv')
    eventfield = driver.find_element_by_id('eventfield')
    filt_1 = driver.find_element_by_id('filt_1')
    assert 'w3-black' in color_but.get_attribute('class')
    assert 'color: rgb(0, 0, 0)' in header.get_attribute('style')
    assert 'background-color: white' in body.get_attribute('style')
    assert 'color: rgb(0, 0, 0)' in bar.get_attribute('style')
    assert 'background-color: rgb(232, 232, 231)' in displaydiv.get_attribute('style')
    assert 'color: rgb(0, 0, 0)' in eventfield.get_attribute('style')
    assert 'black' in filt_1.get_attribute('class')
    for i in range(10):
        if i != 1:
            assert 'w3-white' in driver.find_element_by_id('filt_' + str(i)).get_attribute('class')
    #time.sleep(1)
    color_but.click()
    #time.sleep(1)
    assert 'w3-white' in color_but.get_attribute('class')
    assert 'color: rgb(255, 255, 255)' in header.get_attribute('style')
    assert 'background-color: rgb(41, 41, 41)' in body.get_attribute('style')
    assert 'color: rgb(255, 255, 255)' in bar.get_attribute('style')
    assert 'background-color: rgb(54, 53, 53)' in displaydiv.get_attribute('style')
    assert 'color: rgb(255, 255, 255)' in eventfield.get_attribute('style')
    assert 'w3-white' in filt_1.get_attribute('class')
    for i in range(10):
        if i != 1:
            assert 'black' in driver.find_element_by_id('filt_' + str(i)).get_attribute('class')
    color_but.click()
    assert 'w3-black' in color_but.get_attribute('class')

#Проверка слайдера звука (Прокрутить до конца, прокрутить до начала)
def test_volume_slidebar(driver):
    volinp = driver.find_element_by_id('volinp')
    assert volinp.get_attribute('value') == '20'
    move = ActionChains(driver)
    #time.sleep(2)
    move.click_and_hold(volinp).move_by_offset(300, 0).perform()
    #time.sleep(2)
    assert volinp.get_attribute('value') == '100'
    move.click_and_hold(volinp).move_by_offset(-300, 0).perform()
    #time.sleep(2)
    assert volinp.get_attribute('value') == '0'

#Проверка реакции нажатия на фильтры (поочереди каждый включается, выключается)
def test_click_filters(driver):
    for i in range(10):
        filt = driver.find_element_by_id('filt_' + str(i))
        filt.click()
       # time.sleep(0.5)
        assert 'black' in filt.get_attribute('class')
        filt.click()
        #time.sleep(0.5)
        assert 'w3-white' in filt.get_attribute('class')

#Вспомогательная функция, чтобы события успели появится для проверки их ссылок
def create_events(driver):
    driver.find_element_by_id('filt_0').click()
    time.sleep(2)
    driver.find_element_by_id('filt_0').click()

#Проверка работы перехода по нажатию на фигуру (проверка флага нового окна,
#проверка соответсвия новой страницы названию репозитория, выбранного события
def test_refs_displayfig(driver,current_url):
    create_events(driver)
    new_ref = driver.find_element_by_css_selector('#displaydiv > a')
    assert new_ref.get_attribute('target') == '_blank'
    text = driver.find_element_by_id('text_figure').text
    driver.get(new_ref.get_attribute("href"))
    #time.sleep(1)
    assert driver.find_element_by_link_text(text)
    driver.get(current_url)
    #time.sleep(1)

#Проверка работы перехода по нажатию на ссылку в текстовом поле (проверка флага нового окна,
#проверка соответсвия новой страницы названию репозитория, выбранного события
def test_refs_eventfield(driver, current_url):
    create_events(driver)
    new_ref = driver.find_element_by_css_selector('#one_event > a')
    assert new_ref.get_attribute('target') == '_blank'
    text = new_ref.text.split('/')[-1][1:]
    driver.get(new_ref.get_attribute("href"))
    #time.sleep(1)
    assert driver.find_element_by_link_text(text)
    driver.get(current_url)
    #time.sleep(1)

if __name__ == '__main__':
    if _platform == "linux" or _platform == "linux2":
        driver = webdriver.Chrome('./chromedriverlin')
    elif _platform == "win32" or _platform == "win64":
        driver = webdriver.Chrome('./chromedriver.exe')
    elif _platform == "darwin":
        driver = webdriver.Chrome('./chromedrivermac')
    driver.get('http://127.0.0.1')
    driver.set_window_size(1200, 780)
    current_url = driver.current_url
    test_about(driver)
    test_theme_colors(driver)
    test_volume_slidebar(driver)
    test_click_filters(driver)
    test_refs_displayfig(driver,current_url)
    test_refs_eventfield(driver,current_url)
    driver.quit()