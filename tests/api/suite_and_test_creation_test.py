import pytest
from faker import Faker

from src.api.controllers import SuiteController, TestController
from src.api.models import Project

fake = Faker()


@pytest.mark.smoke
@pytest.mark.api
def test_create_suite(
    project: Project,
    suite_controller: SuiteController,
    test_controller: TestController,
):
    suite_name = fake.sentence()
    suite_response = suite_controller.create(project_id=project.id, title=suite_name, description=fake.paragraph())

    actual_test_suite = suite_controller.get_by_id(project.id, suite_response.id)

    assert suite_response.id == actual_test_suite.id
    assert suite_response.attributes.title == actual_test_suite.attributes.title
    assert actual_test_suite.attributes.title == suite_name


@pytest.mark.regression
@pytest.mark.api
def test_create_suite_and_case(
    project: Project,
    suite_controller: SuiteController,
    test_controller: TestController,
):
    suite_name = fake.sentence()
    suite = suite_controller.create(project_id=project.id, title=suite_name, description="")

    test_ui_title = fake.sentence()
    test_ui = test_controller.create(
        project_id=project.id,
        suite_id=suite.id,
        title=test_ui_title,
    )

    test_case_title = fake.sentence()
    test_case_description = fake.paragraph()
    test_case = test_controller.create(
        project_id=project.id,
        suite_id=suite.id,
        title=test_case_title,
        description=test_case_description,
    )

    assert test_case.id is not None
    assert test_case.title == test_case_title
    assert test_case.type == "test"

    test_controller.delete(project.id, test_case.id)
    test_controller.delete(project.id, test_ui.id)
    suite_controller.delete(project.id, suite.id)


@pytest.mark.regression
@pytest.mark.api
def test_update_suite(
    project: Project,
    suite_controller: SuiteController,
):
    original_name = fake.sentence()
    original_description = fake.paragraph()

    suite = suite_controller.create(project_id=project.id, title=original_name, description=original_description)
    updated_name = fake.sentence()
    updated_description = fake.paragraph()

    updated_suite = suite_controller.update(
        project_id=project.id, suite_id=suite.id, title=updated_name, description=updated_description
    )

    assert updated_suite.id == suite.id
    assert updated_suite.attributes.title == updated_name
    assert updated_suite.attributes.description == updated_description

    retrieved_suite = suite_controller.get_by_id(project.id, suite.id)
    assert retrieved_suite.attributes.title == updated_name
    assert retrieved_suite.attributes.description == updated_description

    suite_controller.delete(project.id, suite.id)
