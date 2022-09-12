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
                                                 password='gagana')


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
        "title": "note1",
        "description": "sad1111hgfva"
    }

@pytest.fixture
def user_data_for_delete(client, user, user_details):
    response = client.post(URL, user_details, content_type="application/json")
    result = json.loads(response.content)
    note_id = result.get("data").get("id")
    # print(result)
    return {"id": note_id}
@pytest.fixture
def user_data_for_delete_error(client, user, user_details):
    response = client.post(URL, user_details, content_type="application/json")
    result = json.loads(response.content)
    note_id = result.get("data").get("id")
    # print(result)
    return {"id": "note_id"}


@pytest.fixture
def user_data_for_put(client, user, user_details):
    user_id = user.id
    response = client.post(URL, user_details, content_type="application/json")
    result = json.loads(response.content)
    note_id = result.get("data").get("id")
    return {
        "id": note_id,
        "user": user_id,
        "title": "note1",
        "description": "sad1111hgfva"
    }
@pytest.fixture
def user_data_for_put_error(client, user, user_details):
    user_id = user.id
    response = client.post(URL, user_details, content_type="application/json")
    result = json.loads(response.content)
    note_id = result.get("data").get("id")
    return {
        "id": note_id,
        "user": "user_id",
        "title": "note1",
        "description": "sad1111hgfva"
    }


class TestBookApiView:

    @pytest.mark.django_db
    def test_get_notes_successfully(self, client, django_user_model, db):
        data = {'user': 1}
        response = client.get(URL, data, content_type="application/json")
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_notes_unsuccessfully(self, client, django_user_model, db):
        data = {'user': 1}
        response = client.get(ERROR_URL, data, content_type="application/json")
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_post_notes_successfully(self, client, user, user_details):
        response = client.post(URL, user_details, content_type="application/json")
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_post_notes_unsuccessfully(self, client, user, user_details_error):
        response = client.post(URL, user_details_error, content_type="application/json")
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_post_notes_unsuccessfully_with_bad_request(self, client, user, user_details_error):
        response = client.post(ERROR_URL, user_details_error, content_type="application/json")
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_delete_notes_successfully(self, client, user, user_details, user_data_for_delete):
        response = client.delete(URL, user_data_for_delete, content_type="application/json")
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_delete_notes_unsuccessfully(self, client, user, user_details, user_data_for_delete_error):
        response = client.delete(URL, user_data_for_delete_error, content_type="application/json")
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_delete_notes_unsuccessfully_with_bad_request(self, client, user, user_details, user_data_for_delete_error):
        response = client.delete(ERROR_URL, user_data_for_delete_error, content_type="application/json")
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_put_notes_successfully(self, client, user, user_details, user_data_for_put):
        response = client.put(URL, user_data_for_put, content_type="application/json")
        assert response.status_code == 202

    @pytest.mark.django_db
    def test_put_notes_unsuccessfully(self, client, user, user_details, user_data_for_put_error):
        response = client.put(URL, user_data_for_put_error, content_type="application/json")
        assert response.status_code == 406

    @pytest.mark.django_db
    def test_put_notes_unsuccessfully_with_bad_request(self, client, user, user_details, user_data_for_put_error):
        response = client.put(ERROR_URL, user_data_for_put_error, content_type="application/json")
        assert response.status_code == 404
