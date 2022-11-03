import pytest
from beanie import WriteRules
from httpx import AsyncClient

from app.constants.application_status import ApplicationStatus
from app.models.job_application import JobApplication
from app.models.job_listing import JobListing
from app.models.user import User

user_1 = {
    "id": "634cd28b6f3c8f9a18cf3d45",
    "email": "test@example.com",
    "company": "test-company",
    "password": "test",
    "roles": ["user"],
}

job_listing_1 = {
    "id": "634cd28b6f3c8f9a18cf3d46",
    "title": "test-title",
    "description": "test-description",
    "location": "test-location",
    "startDate": "2021-09-01T00:00:00",
    "employmentType": "test-employmentType",
    "createdAt": "2021-09-01T00:00:00",
    "updatedAt": "2021-09-01T00:00:00"
}

job_application_1 = {
    "id": "634cd28b6f3c8f9a18cf3d47",
    "firstName": "John",
    "lastName": "Doe",
    "email": "johndoe@example.com",
    "startDate": "2021-09-01T00:00:00",
    "resumeLink": "https://example.com/resume.pdf",
    "personalStatement": "I am a highly motivated individual with a passion for software development. I am a quick learner and I am always looking to improve my skills. I am a team player and I am always willing to help others. I am a hard worker and I am always looking to take on new challenges.",
    "applicationStatus": ApplicationStatus.NEW.value,
    "createdAt": "2021-09-02T13:00:23",
    "updatedAt": "2021-09-02T13:00:23"
}


@pytest.fixture(scope='module')
async def setup_test_job_listing_application():
    new_user_1 = User(**user_1)
    new_job_listing_1 = JobListing(**job_listing_1, createdBy=new_user_1)  # type: ignore
    new_job_application_1 = JobApplication(**job_application_1, jobListing=new_job_listing_1)  # type: ignore
    try:
        await new_job_application_1.save(link_rule=WriteRules.WRITE)
        yield
    finally:
        await JobApplication.delete_all()
        await JobListing.delete_all()
        await User.delete_all()


async def test_search_job_applications(setup_test_job_listing_application, client: AsyncClient):
    response = await client.get(f"/api/v1/job-listings/{job_listing_1.get('id')}/job-applications")
    assert response.status_code == 200
    res_json = response.json()
    assert len(res_json) == 1
    assert res_json[0].get("firstName") == job_application_1.get("firstName")
    assert res_json[0].get("lastName") == job_application_1.get("lastName")
    assert res_json[0].get("email") == job_application_1.get("email")
    assert res_json[0].get("startDate") == job_application_1.get("startDate")
    assert res_json[0].get("resumeLink") == job_application_1.get("resumeLink")
    assert res_json[0].get("personalStatement") == job_application_1.get("personalStatement")


async def test_submit_job_application(setup_test_job_listing_application, client: AsyncClient):
    new_job_application_2 = {
        "firstName": "Jane",
        "lastName": "Dean",
        "email": "jane@example.com",
        "startDate": "2021-09-01T00:00:00",
        "resumeLink": "https://example.com/resume.pdf",
        "personalStatement": "I am a highly motivated individual with a passion for marketing. I am a quick learner and I am always looking to improve my skills. I am a team player and I am always willing to help others. I am a hard worker and I am always looking to take on new challenges."
    }
    response = await client.post(f"/api/v1/job-listings/{job_listing_1.get('id')}/job-applications", json=new_job_application_2)
    assert response.status_code == 201
    res_json = response.json()
    assert res_json.get("firstName") == new_job_application_2.get("firstName")
    assert res_json.get("lastName") == new_job_application_2.get("lastName")
    assert res_json.get("email") == new_job_application_2.get("email")
    assert res_json.get("startDate") == new_job_application_2.get("startDate")
    assert res_json.get("resumeLink") == new_job_application_2.get("resumeLink")
    assert res_json.get("personalStatement") == new_job_application_2.get("personalStatement")
