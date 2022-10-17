from typing import Union

from beanie.odm.fields import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from app.constants.application_status import ApplicationStatus

from app.dtos.jobapplication import (GetJobApplicationResDto,
                                     SubmitJobApplicationReqDto,
                                     SubmitJobApplicationResDto, UpdateJobApplicationStatusReqDto,
                                     UpdateJobApplicationStatusResDto)
from app.models.jobapplication import JobApplication
from app.models.joblisting import JobListing

router = APIRouter(prefix="/api/v1/job-listings/{job_listing_id}/job-applications", tags=["Job Listing's Application"])


@router.get("", response_model=list[GetJobApplicationResDto])
async def search_job_applications(job_listing_id: PydanticObjectId, applicationStatus: Union[str, None] = None):
    """Returns all job applications for a job listing with optional filtering by application status."""
    search_criteria: dict[str, Union[str, PydanticObjectId]] = {"jobListing._id": job_listing_id}
    if applicationStatus:
        search_criteria["applicationStatus"] = applicationStatus

    return await JobApplication.find(search_criteria, fetch_links=True).project(GetJobApplicationResDto).to_list()


@router.post("", response_model=SubmitJobApplicationResDto,
             status_code=status.HTTP_201_CREATED)
async def submit_job_application(job_listing_id: PydanticObjectId, req_dto: SubmitJobApplicationReqDto):
    """Submits a job application for a job listing"""
    jobListing = await JobListing.get(job_listing_id)
    if not jobListing:
        raise HTTPException(status_code=404, detail="Job listing not found")

    jobapplication = JobApplication(
        firstName=req_dto.firstName,
        lastName=req_dto.lastName,
        email=req_dto.email,
        startDate=req_dto.startDate,
        resumeLink=req_dto.resumeLink,
        personalStatement=req_dto.personalStatement,
        jobListing=jobListing  # type: ignore
    )
    return await jobapplication.save()


@router.patch("/{job_application_id}", response_model=UpdateJobApplicationStatusResDto)
async def update_job_application_status(job_application_id: PydanticObjectId, req_dto: UpdateJobApplicationStatusReqDto):
    """Updates a job application's status"""
    jobapplication = await JobApplication.find_one({"_id": job_application_id}, fetch_links=True)
    if not jobapplication:
        raise HTTPException(status_code=404, detail="Job application not found")

    jobapplication.applicationStatus = req_dto.applicationStatus
    return await jobapplication.save()