from httpx import AsyncClient
from typing import Generator
from beanie import WriteRules
from beanie.odm.fields import PydanticObjectId

import pytest
from app.constants.application_status import ApplicationStatus

from app.models.job_application import JobApplication
from app.models.job_listing import JobListing
from app.models.user import User
from app.utils.auth import get_password_hash

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
async def setup_test_job_application():
    user = User(**user_1)
    user.password = get_password_hash(user.password)
    new_job_listing_1 = JobListing(**job_listing_1, createdBy=user)  # type: ignore
    new_job_application_1 = JobApplication(**job_application_1, jobListing=new_job_listing_1)  # type: ignore
    try:
        await new_job_application_1.save(link_rule=WriteRules.WRITE)
        yield
    finally:
        await JobApplication.delete_all()
        await JobListing.delete_all()
        await User.delete_all()


async def test_update_job_application_status(setup_test_job_application: Generator, client: AsyncClient):
    ja_1_obj_id = PydanticObjectId(job_application_1['id'])
    job_application = await JobApplication.get(ja_1_obj_id)
    assert job_application is not None
    assert job_application.applicationStatus == ApplicationStatus.NEW
    response = await client.patch(f"/api/v1/job-applications/{ja_1_obj_id}", json={"applicationStatus": ApplicationStatus.INTERVIEW_SCHEDULED.value})
    assert response.status_code == 200
    assert response.json().get('applicationStatus') == ApplicationStatus.INTERVIEW_SCHEDULED.value
    job_application = await JobApplication.get(ja_1_obj_id)
    assert job_application is not None
    assert job_application.applicationStatus == ApplicationStatus.INTERVIEW_SCHEDULED
