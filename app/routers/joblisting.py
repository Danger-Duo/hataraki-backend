from typing import Union

from fastapi import APIRouter, Depends

from app.dtos.joblisting import (CreateJobListingReqDto,
                                 CreateJobListingResDto, GetJobListingResDto)
from app.models.joblisting import JobListing
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/job-listings", tags=["Job Listing"])


@router.get("/", response_model=list[GetJobListingResDto])
async def search_job_listings(title: Union[str, None] = None, company: Union[str, None] = None, location: Union[str, None] = None, employmentType: Union[str, None] = None):
    """Returns all joblistings with optional search query"""
    search_criteria = {}
    if title:
        search_criteria["title"] = title
    if company:
        search_criteria["createdBy.company"] = company
    if location:
        search_criteria["location"] = location
    if employmentType:
        search_criteria["employmentType"] = employmentType
    return await JobListing.find(search_criteria, fetch_links=True).project(GetJobListingResDto).to_list()


@router.post("/", response_model=CreateJobListingResDto)
async def create_job_listing(req_dto: CreateJobListingReqDto, user: User = Depends(get_current_user)):
    """Creates a joblisting"""
    joblisting = JobListing(
        title=req_dto.title,
        description=req_dto.description,
        location=req_dto.location,
        startDate=req_dto.startDate,
        employmentType=req_dto.employmentType,
        createdBy=user,  # type: ignore
    )
    return await joblisting.save()
