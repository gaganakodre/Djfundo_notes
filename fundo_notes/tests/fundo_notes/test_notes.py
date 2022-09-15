import json

import pytest
from django.urls import reverse

pytest_mark = pytest.mark.django_db

URL = reverse('note:notes_operation')
ERROR_URL = "note"


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='gagana', first_name="gaga", last_name="na",
                                                 email='gagana@gmail.com',
                                                 password='gagana', is_verified=True)


@pytest.fixture
def user_details(user):
    return {
        "user": user.id,
        "title": "note1",
        "description": "sad1111hgfva"

    }


@pytest.fixture
def user_details_error(user):
    return {
        "user": "id",
        "tite": "note1",
        "description": "sadhgfva"
    }


@pytest.fixture
def user_data_for_delete(client, user, user_details, token_validation):
    token = token_validation
    response = client.post(URL, user_details, content_type="application/json", HTTP_TOKEN=token)
    result = json.loads(response.content)
    note_id = result.get("data").get("id")
    return {"id": note_id}


@pytest.fixture
def user_data_for_delete_error(client, user, user_details, token_validation):
    token = token_validation
    response = client.post(URL, user_details, content_type="application/json", HTTP_TOKEN=token)
    result = json.loads(response.content)
    note_id = result.get("data").get("id")
    return {"i": 'note_id'}


@pytest.fixture
def user_data_for_put(client, user, user_details, token_validation):
    user_id = user.id
    token = token_validation
    response = client.post(URL, user_details, content_type="application/json", HTTP_TOKEN=token)
    result = json.loads(response.content)
    note_id = result.get("data").get("id")
    return {
        "id": note_id,
        "user": user_id,
        "title": "note1",
        "description": "sad1111hgfva"
    }


@pytest.fixture
def user_data_for_put_error(client, user, user_details, token_validation):
    user_id = user.id
    token = token_validation
    response = client.post(URL, user_details, content_type="application/json", HTTP_TOKEN=token)
    result = json.loads(response.content)
    note_id = result.get("data").get("id")
    return {
        "i": note_id,
        "user": "userid",
        "title": "note1",
        "description": "sad1111hgfva"
    }


@pytest.fixture
def token_validation(client, django_user_model, db):
    """
    Function to get the token
    """
    user = django_user_model.objects.create_user(username='gagana1', first_name="gaga", last_name="na",
                                                 email='gagana1@gmail.com',
                                                 password='gagana', is_verified=True)
    url = reverse('user:user_login')
    data = {'email': 'gagana1@gmail.com', 'password': 'gagana'}
    response = client.post(url, data)
    token = response.data['data']['token']
    return token


class TestNotesApiView:

    @pytest.mark.django_db
    def test_get_notes_successfully(self, client, django_user_model, db, token_validation):
        data = {'user': 1}
        token = token_validation
        response = client.get(URL, data, content_type="application/json", HTTP_TOKEN=token)
        print(response)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_notes_unsuccessfully(self, client, django_user_model, db, token_validation):
        data = {'user': 1}
        token = token_validation
        response = client.get(ERROR_URL, data, content_type="application/json", HTTP_TOKEN=token)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_post_notes_successfully(self, client, user, user_details, token_validation):
        token = token_validation
        response = client.post(URL, user_details, content_type="application/json", HTTP_TOKEN=token)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_post_notes_unsuccessfully(self, client, user, user_details_error, token_validation):
        token = token_validation
        response = client.post(URL, user_details_error, content_type="application/json", HTTP_TOKEN=token)
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_post_notes_unsuccessfully_with_bad_request(self, client, user, user_details_error, token_validation):
        token = token_validation
        response = client.post(ERROR_URL, user_details_error, content_type="application/json", HTTP_TOKEN=token)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_delete_notes_successfully(self, client, user_data_for_delete, token_validation):
        token = token_validation
        response = client.delete(URL, user_data_for_delete, content_type="application/json", HTTP_TOKEN=token)
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_delete_notes_unsuccessfully(self, client, user_data_for_delete_error, token_validation):
        token = token_validation
        response = client.delete(URL, user_data_for_delete_error, content_type="application/json", HTTP_TOKEN=token)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_delete_notes_unsuccessfully_with_bad_request(self, client, user_data_for_delete_error, token_validation):
        token = token_validation
        response = client.delete(ERROR_URL, user_data_for_delete_error, content_type="application/json",
                                 HTTP_TOKEN=token)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_put_notes_successfully(self, client, user, user_details, user_data_for_put, token_validation):
        token = token_validation
        response = client.put(URL, user_data_for_put, content_type="application/json", HTTP_TOKEN=token)
        assert response.status_code == 202

    @pytest.mark.django_db
    def test_put_notes_unsuccessfully(self, client, user, user_details, user_data_for_put_error, token_validation):
        token = token_validation
        response = client.put(URL, user_data_for_put_error, content_type="application/json", HTTP_TOKEN=token)
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_put_notes_unsuccessfully_with_bad_request(self, client, user, user_details, user_data_for_put_error,
                                                       token_validation):
        token = token_validation
        response = client.put(ERROR_URL, user_data_for_put_error, content_type="application/json", HTTP_TOKEN=token)
        assert response.status_code == 404
