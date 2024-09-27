import sender_stand_request
import data


def get_user_body(name):
    current_body = data.user_body.copy()
    current_body['firstName'] = name
    return current_body

def positive_assert(name):
    user_body = get_user_body(name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()['authToken'] != ''
    users_table_response = sender_stand_request.get_users_table()
    str_user = (user_body['firstName'] + ',' + user_body['phone'] + ','
                + user_body['address'] + ',,,' + user_response.json()['authToken'])
    assert users_table_response.text.count(str_user) == 1
def negative_assert(name):
    user_body = get_user_body(name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()['code'] == 400
    assert user_response.json()['message'] == ('Имя пользователя введено некорректно. '
                                                'Имя может содержать только русские '
                                         'или латинские буквы, длина должна быть не менее 2 и не более 15 символов')
def negative_assert_no_first_name(user_body):
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()['code'] == 400
    assert user_response.json()['message'] == 'Не все необходимые параметры были переданы'


# 1. Имя из двух букв
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert('Аа')
# 2. Имя из 15 букв
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert('Ааааааааааааааа')
# 3. Имя из 1 буквы
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert('А')
# 4. Имя из 16 букв
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert('Аааааааааааааааа')
# 5. Имя на английском
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert('QWErty')
# 6. Имя на русском
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert('Витя')
# 7. Имя с пробелами
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert('Человек и КО')
# 8. Имя со спецсимволами
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert("№%@")
# 9. Имя с цифрами
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert('12345')
# 10. Параметр не передан в запросе
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop('firstName')
    negative_assert_no_first_name(user_body)
# 11. Пустое значение параметра
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body('')
    negative_assert_no_first_name(user_body)
# 12 Передан другой тип параметра 'Имя' - число
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400