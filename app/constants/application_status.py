from enum import Enum


class ApplicationStatus(Enum):
    NEW = "new"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
