import pytest
import requests
from pprint import pprint

BASE_URL = 'https://restful-booker.herokuapp.com/booking'
AUTH_URL = 'https://restful-booker.herokuapp.com/auth'
STATUS_OK = 200


@pytest.fixture(scope='function')
def booking_id():
    payload = {
        "firstname": "Bob",
        "lastname": "Jimmisson",
        "totalprice": 659,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-10-20",
            "checkout": "2023-10-27"
        },
        "additionalneeds": "Seaside"}
    response = requests.post(BASE_URL, json=payload)
    booking_id = response.json()['bookingid']
    # в фикстурах принято использовать yield вместо return
    yield booking_id


@pytest.fixture(scope='module')
def token():
    payload = {
    "username" : "admin",
    "password" : "password123"}
    response = requests.post(AUTH_URL, json=payload)
    response_data = response.json()
    token = response_data['token']
    assert response.status_code == STATUS_OK
    yield token


def test_get_all_bookings():
    response = requests.get(BASE_URL)
    assert response.status_code == STATUS_OK
    assert 'Connection' in response.headers, 'There is no such key'
    # print(f'\n{len(response.json())}')
    # assert len(response.json()) == 2400, 'Wrong number'


def test_get_booking_with_id(booking_id):
    response = requests.get(f'{BASE_URL}/{booking_id}')
    response_data = response.json()
    # print(response_data)
    assert response.status_code == STATUS_OK
    expected_keys = ['firstname', 'lastname', 'totalprice', 'depositpaid', 'bookingdates']
    assert response_data['firstname'] == 'Bob'
    for key in expected_keys:
        assert key in response_data.keys()


def test_create_booking():
    payload = {
    "firstname": "Jimmy",
    "lastname": "Bobson",
    "totalprice": 777,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2023-10-20",
        "checkout": "2023-10-27"
    },
    "additionalneeds": "Seaside"}
    response = requests.post(BASE_URL, json=payload)
    # print(response.json())
    assert response.status_code == STATUS_OK
    id = response.json()['bookingid']
    get_response = requests.get(f'{BASE_URL}/{id}]')
    assert get_response.json()['firstname'] == 'Jimmy'


def test_create_booking_with_fixture(booking_id):
    response = requests.get(f'{BASE_URL}/{booking_id}')
    assert response.json()['firstname'] == 'Bob'


def test_update_booking(booking_id, token):
    header = {'Cookie': f'token={token}'}
    payload = {
        "firstname": "Iggy",
        "lastname": "Hendrix",
        "totalprice": 666,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-10-20",
            "checkout": "2023-10-27"
        },
        "additionalneeds": "Seaside"}
    response = requests.put(f'{BASE_URL}/{booking_id}', headers=header, json=payload)
    assert response.status_code == STATUS_OK


def test_partial_update_booking(booking_id, token):
    header = {'Cookie': f'token={token}'}
    payload = {
        "firstname": "Ozzy",
        "lastname": "Malmsten"}
    response = requests.patch(f'{BASE_URL}/{booking_id}', headers=header, json=payload)
    assert response.status_code == 200


def test_delete_new_booking(booking_id, token):
    header = {'Cookie': f'token = {token}'}
    response = requests.delete(f'{BASE_URL}/{booking_id}', headers=header)
    assert response.status_code == 201
    get_response = requests.get(f'{BASE_URL}/{booking_id}')
    assert get_response.status_code == 404

