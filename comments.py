# необходимо установить selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from time import sleep
import socket

# опции брузера
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")

#выбираем и настраиваем браузер
driver = webdriver.Chrome(options=options)

#проверяем соединение
def internet_connection():
    try:
        socket.create_connection(("www.youtube.com", 80), timeout=3)
        return True
    except:
        pass
    return False

# проверка существования
def check_exists(XPATH_ELEMENT):
    try:
        driver.find_element(By.XPATH, XPATH_ELEMENT)
    except NoSuchElementException:
        return False
    return True

# получение комментариев
def get_comments():
    SCROLL_PAUSE_TIME = 2
    comments = []
    number = 0

    link = input('Отправьте ссылку на видео YouTube \n')

    while number <= 0:
        try:
            number = int(input('Введите число комментариев для обработки \n'))
        except Exception as e:
            print(e)
            continue
    try:
        if not internet_connection():
            raise Exception("Exception: No internet connection!")

        # поиск видео
        driver.get(link)
        sleep(5)

        # листаем до комментов
        body = driver.find_element(By.XPATH, '/html')
        body.send_keys(Keys.PAGE_DOWN)
        sleep(.1)
        body.send_keys(Keys.PAGE_DOWN)
        sleep(SCROLL_PAUSE_TIME * 3)

        # получаем комменты
        for i in range(1, number+1):
            sleep(.1)
            if check_exists(f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{i}]/ytd-comment-renderer/div[3]/div[2]/div[2]/ytd-expander/div/yt-formatted-string'):
                comment = driver.find_element(By.XPATH, f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{i}]/ytd-comment-renderer/div[3]/div[2]/div[2]/ytd-expander/div/yt-formatted-string').text
                comments.append(comment)
            else:
                body.send_keys(Keys.PAGE_DOWN)
                if check_exists(f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{i}]/ytd-comment-renderer/div[3]/div[2]/div[2]/ytd-expander/div/yt-formatted-string'):
                    comment = driver.find_element(By.XPATH, f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{i}]/ytd-comment-renderer/div[3]/div[2]/div[2]/ytd-expander/div/yt-formatted-string').text
                    comments.append(comment)
                else:
                    continue
        return comments
    except KeyboardInterrupt:
        print("\nStopping! Bye.")
    except Exception as e:
        print(e)
    finally:
        # закрываем страницу
        if driver:
            driver.close()
