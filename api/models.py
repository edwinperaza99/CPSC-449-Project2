from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from enum import Enum

class AvailableClass(BaseModel):
    course_code: str
    course_name: str
    department: str
    instructor_first_name: str
    instructor_last_name: str
    current_enrollment: int
    max_enrollment: int
    waitlist: int
    section_number: int


class AvailableClassResponse(BaseModel):
    available_classes: List[AvailableClass]


class EnrollmentResponse(BaseModel):
    enrollment_status: str
    enrollment_date: Optional[datetime] = None

class EnrollmentRequest(BaseModel):
    section_number: int
    course_code: str
    student_id: int

class RegistrationStatus(str, Enum):
    ENROLLED = 'enrolled'
    WAITLISTED = 'waitlisted'
    NOT_ELIGIBLE = 'not_eligible'
    DROPPED = "dropped"
    ALREADY_ENROLLED = "already_enrolled"

class Registration(BaseModel):
    section_number: int #Section Number
    student_id: int
    enrollment_status: str
    course_code: str

class QueryStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"

class UserRole(str, Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    REGISTRAR = "registrar"
    NOT_FOUND = "not_found"

class DropCourseResponse(BaseModel):
    course_code: str
    section_number: int
    status: str
    
class AddClassRequest(BaseModel):
    course_code: str
    class_name: str
    department: str
    section_number: int
    instructor_id: int
    max_enrollment: int

class AddClassResponse(BaseModel):
    addClass_status: str

class DeleteSectionResponse(BaseModel):
    deleteSection_status: str

class DeleteSectionRequest(BaseModel):
    course_code: str
    section_number: int

class ChangeInstructorResponse(BaseModel):
    changeInstructor_status: str

class ChangeInstructorRequest(BaseModel):
    course_code: str
    section_number: int
    instructor_id: int

class FreezeEnrollmentResponse(BaseModel):
    freezeEnrollment_status: str

class FreezeEnrollmentRequest(BaseModel):
    course_code: str
    section_number: int

# instructor models 
class EnrollmentListResponse(BaseModel):
    student_cwid: int
    student_first_name: str
    student_last_name: str
    course_code: str
    section_number: int
    class_name: str
    status: str

class RecordsEnrollmentResponse(BaseModel):
    enrolled_students: List[EnrollmentListResponse]

class RecordsDroppedResponse(BaseModel):
    dropped_students: List[EnrollmentListResponse]

class RecordsWaitlistResponse(BaseModel):
    waitlisted_students: List[EnrollmentListResponse]

class WaitlistPositionReq(BaseModel):
    # section_number: int
    # course_code: str
    student_id: int

class WaitlistPositionList(BaseModel):
    section_number: int
    course_code: str
    waitlist_position: int

class WaitlistPositionRes(BaseModel):
    waitlist_positions: List[WaitlistPositionList]

class ViewWaitlistReq(BaseModel):
    section_number: int
    course_code: str

class WaitlistStudents(BaseModel):
    student_id: int
    student_name: str
    enrollment_date: datetime

class ViewWaitlistRes(BaseModel):
    waitlisted_students: List[WaitlistStudents]

class DropStudentRequest(BaseModel):
    instructor_id: int
    student_id: int
    section_number: int
    course_code: str

class DroppedResponse(BaseModel):
    drop_status: str
