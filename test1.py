import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('./chromedriver.exe')
    pytest.driver.implicitly_wait(10)
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    #<{}

    yield

    pytest.driver.quit()


def test_show_my_pets():
    #{{
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys('iva.gla7@gmail.com')
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys('мирумир')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    #}}
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    
    pytest.driver.find_element(By.XPATH,'//a[contains(@href,"/my_pets")]').click()
    assert pytest.driver.title == 'PetFriends: My Pets'

    a = pytest.driver.find_element(By.XPATH, "//div[@class='.col-sm-4 left']").text
    n = int(list(filter(lambda x: "Питомцев" in x, a.split('\n')))[0].strip().split(':')[1].strip())
    table = pytest.driver.find_element(By.XPATH, '//*[@id="all_my_pets"]/table')
    rows = table.find_elements(By.TAG_NAME, 'tr')
    assert len(rows) == n+1  # 1 строка - заголовок

#def test_show_my_pets2():

    images = list(pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody//th/img'))
    urls = list(map(lambda elem: elem.get_attribute("src"), images))
    nonemptyurls = list(filter(lambda x: x, urls))
    assert len(nonemptyurls) >= len(urls)/2

    data = list(pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td'))
    data = list(map(lambda x: x.text, data))
    #data1 = list(map(lambda elem: elem.get_attribute("td"), data))
    nonemptydata = list(filter(lambda x: x, data))
    assert nonemptydata == data
    
    data = list(pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]'))
    data = list(map(lambda x: x.text, data))
    #assert data == 1
    names = {}
    for d in data:
        names[d] = 1
    assert len(names) == len(data)
    #assert data == names

    name = list(pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]'))
    name = list(map(lambda x: x.text, name))
    breed = list(pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]'))
    breed = list(map(lambda x: x.text, breed))
    age = list(pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]'))
    age = list(map(lambda x: x.text, age))

    data = list(zip(name, breed, age))
    data = list(map(str, data))
    pets = {}
    for d in data:
        pets[d] = 1
    assert len(pets) == len(data)
    assert data == pets
