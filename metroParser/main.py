# Данный проект реализует парсер сайта магазина Метро.

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import json


# Открытие файла metro.json для записи собранных данных
json_data = []
with open('metro.json', 'w', encoding='windows-1251') as file:
    file.write(json.dumps(json_data, indent=2, ensure_ascii=False))

# запуск браузера и переход по ссылке на сайт Метро
driver = webdriver.Chrome()
driver.get("https://online.metro-cc.ru/")

time.sleep(5)
# Нажатие на кнопку "Каталог"
driver.find_element(By.XPATH, "//button[@data-qa='header-catalog-button']").click()
time.sleep(2)

# Нажатие на кнопку категории "Сладости, чипсы, снеки"
driver.find_element(By.XPATH, "//span[contains(text(),'Сладости, чипсы, снеки')]").click()
time.sleep(5)

# Нажатие на кнопку категории "Шоколад и батончики"
driver.find_element(By.XPATH, "//a/span[contains(text(), 'Шоколад и батончики')]").click()
time.sleep(5)

# Выставляем фильтр, чтобы товар был в наличии
driver.find_elements(By.XPATH, "//span[@class='catalog-checkbox__text is-clickable']")[0].click()
time.sleep(5)

# Выставляем фильтр, чтобы товар был доступен к заказу
driver.find_elements(By.XPATH, "//span[@class='catalog-checkbox__text is-clickable']")[1].click()
time.sleep(5)

i = 0  # Счетчик товаров на одной странице
global_count = 0  # Общий счетчик всех товаров, пройденных парсером

# Цикл "пока есть товары на странице"
while driver.find_elements(By.CLASS_NAME, "simple-button__text"):
    # Нажатие на товар
    driver.find_elements(By.XPATH, "//a[@data-qa='product-card-photo-link']")[i].click()
    time.sleep(2)
    id = driver.find_element(By.XPATH, "//p[@itemprop='productID']").text[9:]
    link = driver.current_url
    name = driver.find_element(By.XPATH, "//meta[@itemprop='name']").get_attribute("content")
    if driver.find_elements(By.XPATH, "//span[@class='product-price__sum-rubles']"):
        regular_price = driver.find_elements(By.XPATH, "//span[@class='product-price__sum-rubles']")[1].text
    else:
        regular_price = driver.find_element(By.XPATH, "//span[@class='product-price__sum-rubles']").text
    promo_price = driver.find_element(By.XPATH, "//meta[@itemprop='price']").get_attribute("content")
    brand = driver.find_elements(By.XPATH, "//li/a[@class='product-attributes__list-item-link reset-link active-blue-text']")[3].text
    print("Count: ", i)
    print("id: ", id)
    print("link: ", link)
    print("name: ", name)
    print("regular price: ", regular_price)
    print("promo price: ", promo_price)
    print("brand: ", brand)

    # Помещение извлеченной о товаре информации в словарь
    json_data = {
        "id": id,
        "name": name,
        "link": link,
        "regular price": regular_price,
        "promo price": promo_price,
        "brand": brand
    }
    data = json.load(open("metro.json"))
    data.append(json_data)
    with open("metro.json", "w") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    # Возвращение на предыдущую посещенную страницу
    driver.back()
    time.sleep(5)
    i += 1

    # Если все товары страницы пройдены, перейти на следующую страницу с товарами
    if i % 30 == 0:
        time.sleep(5)
        driver.find_element(By.XPATH, "//span[contains(text(), 'Показать ещё')]").click()
        time.sleep(5)
        global_count += i
        i = 0
print("Count of products in category 'Шоколад и батончики': ", global_count)
