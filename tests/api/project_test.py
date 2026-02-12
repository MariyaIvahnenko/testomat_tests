import pytest

from src.api.client import TestomatClient
from tests.fixtures.api import (
    api_credentials,
    api_client,
    unauthenticated_client
)


class TestAuthentication:

    def test_login_with_valid_token(self, api_credentials):
        client = TestomatClient()
        client.email = api_credentials["email"]
        client.password = api_credentials["password"]
        client.base_url = api_credentials["base_url"]

        result = client.login()

        assert result is True
        assert client.jwt_token is not None
        assert isinstance(client.jwt_token, str)
        assert len(client.jwt_token) > 0
        assert len(client.jwt_token) > 50

    def test_jwt_token_is_cached(self, unauthenticated_client):
        client = unauthenticated_client

        first_login = client.login()
        first_token = client.jwt_token

        assert first_login is True
        assert first_token is not None

        projects1 = client.get_projects()
        token_after_first_call = client.jwt_token
        assert token_after_first_call == first_token

        projects2 = client.get_projects()
        token_after_second_call = client.jwt_token
        assert token_after_second_call == first_token

        assert projects1 == projects2


class TestGetProjects:

    def test_get_projects_returns_response(self, api_client):
        response = api_client.get_projects()

        assert response is not None
        assert isinstance(response, dict)
        assert len(response) > 0

    def test_get_projects_returns_list_of_projects(self, api_client):
        response = api_client.get_projects()

        assert 'data' in response

        data = response['data']
        assert isinstance(data, list)
        assert data is not None

    def test_project_has_required_attributes(self, api_client):
        response = api_client.get_projects()
        projects = response['data']

        if len(projects) == 0:
            pytest.skip("No projects found in account (valid state)")

        for project in projects:
            assert 'id' in project
            assert project['id'] is not None
            assert isinstance(project['id'], str)

            assert 'type' in project
            assert project['type'] is not None

            assert 'attributes' in project
            assert isinstance(project['attributes'], dict)

    def test_projects_response_is_iterable(self, api_client):
        response = api_client.get_projects()
        projects = response['data']

        projects_count = len(projects)
        assert isinstance(projects_count, int)
        assert projects_count >= 0

        iteration_count = 0
        for project in projects:
            assert isinstance(project, dict)
            assert 'id' in project or 'attributes' in project
            iteration_count += 1

        assert iteration_count == projects_count

        project_ids = [p.get('id') for p in projects]
        assert len(project_ids) == projects_count

        enumerated_projects = list(enumerate(projects))
        assert len(enumerated_projects) == projects_count

        if projects_count > 0:
            first_project = projects[0]
            assert isinstance(first_project, dict)

            sliced = projects[:1]
            assert isinstance(sliced, list)
            assert len(sliced) <= projects_count
