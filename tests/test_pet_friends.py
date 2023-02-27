import pytest


from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email= valid_email, password= valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Dog', animal_type='собака', age='2', pet_photo='images/ddog.jpg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'добавлен {result}')

def test_add_pet_with_valid_data_without_photo(name='Собачка_без_фото', animal_type='Собака', age='2'):
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'добавлен {result}')

def test_add_pet_with_a_lot_of_age_in_variable_age(name='Каспер', animal_type='Собака', pet_photo='images/dog.jpg'):
    age = '234'
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)

    age = float(result['age'])
    assert status == 200
    assert (age > 20 or age < 0), 'Добавлен питомец с невозможным возрастом, меньше 0 или старше 20 лет.'
    print(f'\n Сайт позволяет добавлять питомеца с невозможным возрастом, меньше 0 или старше 20 лет. {age}')

def test_add_pet_with_valid_data_empty_field():
    name = ''
    animal_type = ''
    age = ''
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(api_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name
    print('ok')
    print(f'Сайт позволяет добавлять "пустых" питомецев {result}')

def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Кубик", "Собака", "5", "images/doog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке было, {num} питомцев')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке , {num} питомцев')


def test_successful_delete_invalid_key_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    print()
    print(auth_key)
    auth_key = {'key': 'kjdcbkwe28313ba9e44ac74jhbds7238hdshb3f57a5c91'}
    print(auth_key)

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Кубик", "Cобака", "5", "images/doog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке было, {num} питомцев')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    assert status == 403
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке , {num} питомцев')

def test_successful_update_self_pet_info(name='Макс', animal_type='Собака', age=6):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
        print('ok')
        print(result)
    else:
        raise Exception("There is no my pets")


def test_successful_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Dog", "собака", "2", "images/ddog.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке было, {num} питомцев')

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()
    num = len(my_pets['pets'])
    print('ok')
    print(f'в списке , {num} питомцев')

def test_get_api_key_with_correct_mail_and_wrong_password(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неправильным паролем')

def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result
    print('ok')
    print(f'Статус {status} для теста с неправильным email')


