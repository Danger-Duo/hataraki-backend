from beanie.odm.fields import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from app.dtos.jobapplication import (GetJobApplicationResDto,
                                     SubmitJobApplicationReqDto,
                                     SubmitJobApplicationResDto)
from app.models.jobapplication import JobApplication
from app.models.joblisting import JobListing

router = APIRouter(prefix="/api/v1/job-listings/{job_listing_id}/job-applications", tags=["Job Application"])


@router.get("", response_model=list[GetJobApplicationResDto])
async def search_job_applications(job_listing_id: PydanticObjectId):
    """Returns all job applications for a job listing"""
    # TODO: add filter criteria
    search_criteria = {}
    if job_listing_id:
        search_criteria["jobListing._id"] = job_listing_id
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
