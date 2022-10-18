from beanie.odm.fields import PydanticObjectId
from fastapi import APIRouter, HTTPException

from app.dtos.jobapplication import (UpdateJobApplicationStatusReqDto,
                                     UpdateJobApplicationStatusResDto)
from app.models.jobapplication import JobApplication

router = APIRouter(prefix="/api/v1/job-applications", tags=["Job Application"])


@router.patch("/{job_application_id}", response_model=UpdateJobApplicationStatusResDto)
async def update_job_application_status(job_application_id: PydanticObjectId, req_dto: UpdateJobApplicationStatusReqDto):
    """Updates a job application's status"""
    jobapplication = await JobApplication.find_one({"_id": job_application_id}, fetch_links=True)
    if not jobapplication:
        raise HTTPException(status_code=404, detail="Job application not found")

    jobapplication.applicationStatus = req_dto.applicationStatus
    return await jobapplication.save()
