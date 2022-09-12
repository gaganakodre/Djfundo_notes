import pytest
from django.urls import reverse

pytest_mark = pytest.mark.django_db
REGISTER_URL = reverse('user:user_register')
LOGIN_URL = reverse('user:user_login')


@pytest.fixture
def user_data():
    return {'username': 'gagana',
            'first_name': 'gaga', 'last_name': 'na',
            'email': 'gagana@gmail.com',
            'password': 'gagana'}


@pytest.fixture
def user_data_error():
    return {'usernam': 'gagana',
            'first_name': 'gaga', 'last_name': 'na',
            'email': 'gagana@gmail.com',
            'password': 'gagana'}


@pytest.fixture
def user(django_user_model, db, user_data):
    return django_user_model.objects.create_user(**user_data)


@pytest.fixture
def user_login_data():
    return {'email': 'gagana@gmail.com', 'password': 'gagana'}


@pytest.fixture
def user_login_data_error():
    return {'email': 'gagana@gmail.com', 'user': 'gagana'}


class TestUserLoginAndRegister:
    @pytest.mark.django_db
    def test_user_registration_successfully(self, client, django_user_model, user_data):
        response = client.post(REGISTER_URL, user_data, content_type="application/json")
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_registration_unsuccessfully(self, client, django_user_model, user_data_error):
        response = client.post(REGISTER_URL, user_data, content_type="application/json")
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_user_login_successfully(self, client, user, user_login_data):
        response = client.post(LOGIN_URL, user_login_data, content_type="application/json")
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_user_login_unsuccessfully(self, client, user, user_login_data_error):
        response = client.post(LOGIN_URL, user_login_data_error, content_type="application/json")
        assert response.status_code == 403
