"""Main module to run server and serve endpoints for clients."""

from datetime import datetime
import sqlite3
import contextlib
import logging

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from loguru import logger
from typing import Optional
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from .database_query import *
from .models import *
from .utils import *

DATABASE_URL = "./api/var/enrollments.db"

class Settings(BaseSettings, env_file=".env", extra="ignore"):
    database: str
    logging_config: str

def get_logger():
    return logging.getLogger(__name__)

def get_db(logger: logging.Logger = Depends(get_logger)):
    with contextlib.closing(sqlite3.connect(DATABASE_URL, check_same_thread = False)) as db:
        db.row_factory = sqlite3.Row
        db.isolation_level = None
        db.set_trace_callback(logger.debug)
        yield db

settings = Settings()
app = FastAPI()

logging.config.fileConfig(settings.logging_config, disable_existing_loggers = False)

@app.on_event("shutdown")
async def shutdown(db_connection = Depends(get_db)):
    db_connection.close()

@app.get(path='/db_liveness', operation_id='check_db_health')
async def check_db_health(db_connection = Depends(get_db)):
    try:
        db_connection.cursor()
        return JSONResponse(content= {'status': 'ok'}, status_code = status.HTTP_200_OK)
    except Exception as ex:
        return JSONResponse(content= {'status': 'not connected'}, status_code = status.HTTP_503_SERVICE_UNAVAILABLE)


##########   STUDENTS ENDPOINTS     ######################
@app.get(path="/classes", operation_id="available_classes", response_model = AvailableClassResponse)
async def available_classes(department_name: str, db_connection = Depends(get_db)):
    """API to fetch list of available classes for a given department name.

    Args:
        department_name (str): Department name

    Returns:
        AvailableClassResponse: AvailableClassResponse model
    """
    result = get_available_classes(db_connection=db_connection, department_name=department_name)
    logger.info('Succesffuly exexuted available')
    return AvailableClassResponse(available_classes = result)

@app.post(path ="/enrollment", operation_id="course_enrollment", response_model= EnrollmentResponse)
async def course_enrollment(enrollment_request: EnrollmentRequest, db_connection = Depends(get_db)):
    """Allow enrollment of a course under given section for a student

    Args:
        enrollment_request (EnrollmentRequest): EnrollmentRequest model

    Raises:
        HTTPException: Raise HTTP exception when role is not authrorized
        HTTPException: Raise HTTP exception when query fail to execute in database

    Returns:
        EnrollmentResponse: EnrollmentResponse model
    """

    role = check_user_role(db_connection, enrollment_request.student_id)
    if role == UserRole.NOT_FOUND or role != UserRole.STUDENT:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'Enrollment not authorized for role:{role}')
    check_if_already_enrolled = check_status_query(db_connection, enrollment_request)
    if check_if_already_enrolled :
        return check_if_already_enrolled
    eligibility_status = check_enrollment_eligibility(db_connection, enrollment_request.section_number, enrollment_request.course_code)
    if eligibility_status == RegistrationStatus.NOT_ELIGIBLE:
        return EnrollmentResponse(enrollment_status = 'not eligible')
    active = check_if_active(db_connection, enrollment_request)
    if active == False:
        logger.info('Class is no longer active')
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'Class is no longer active')
    
    try:
        registration = Registration(student_id = enrollment_request.student_id, enrollment_status = eligibility_status, 
                                    section_number = enrollment_request.section_number, course_code = enrollment_request.course_code) 
        insert_status = complete_registration(db_connection,registration)
        if insert_status == QueryStatus.SUCCESS:
            return EnrollmentResponse(enrollment_date = datetime.utcnow(), enrollment_status = eligibility_status)

    except DBException as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= err.error_detail)


@app.put(path = "/dropcourse", operation_id= "update_registration_status",response_model= DropCourseResponse)
async def update_registration_status(enrollment_request:EnrollmentRequest, db_connection = Depends(get_db)):
    """API for students to drop a course

    Args:
        enrollment_request (EnrollmentRequest): Enrollment request

    Raises:
        HTTPException: Raise Exception if database fail to execute query

    Returns:
        DropCourseResponse : drop course response
    """
    try:
        registration = Registration(section_number= enrollment_request.section_number,
                                    student_id=enrollment_request.student_id,
                                    course_code=enrollment_request.course_code,
                                    enrollment_status='enrolled')
        result = update_student_registration_status(db_connection,registration)
        
        if result == RegistrationStatus.DROPPED:
            return DropCourseResponse(course_code=enrollment_request.course_code,
                                                   section_number=enrollment_request.section_number,
                                                   status='already dropped')
                                                  
        return DropCourseResponse(course_code=enrollment_request.course_code,
                                                   section_number=enrollment_request.section_number,
                                                   status='drop successfull')
    except DBException as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=err.error_detail)

##########   REGISTRAR ENDPOINTS     ######################
@app.post(path="/classes", operation_id="add_class", response_model=AddClassResponse)
async def add_class(addClass_request: AddClassRequest, db_connection = Depends(get_db)):
    classExists = check_class_exists(db_connection, addClass_request.course_code)
    if classExists:
        try:
            response = addSection(db_connection, addClass_request.section_number, addClass_request.course_code, addClass_request.instructor_id, addClass_request.max_enrollment)
            if response == QueryStatus.SUCCESS:
                return AddClassResponse(addClass_status = 'Successfully added new section')
            else:
                return AddClassResponse(addClass_status = 'Failed to add Section')
        
        except DBException as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= err.error_detail)
    else:
        try:
            addClassResponse = addClass(db_connection, addClass_request.course_code, addClass_request.class_name, addClass_request.department)
            if addClassResponse == QueryStatus.SUCCESS:
                addSectionResponse = addSection(db_connection, addClass_request.section_number, addClass_request.course_code, addClass_request.instructor_id, addClass_request.max_enrollment)
                if addSectionResponse == QueryStatus.SUCCESS:
                    return AddClassResponse(addClass_status = 'Successfully added Class & Section')
                else:
                    return AddClassResponse(addClass_status = 'Failed to add Class & Section')
        
        except DBException as err:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= err.error_detail)

@app.delete(path="/sections", operation_id="delete_section", response_model=DeleteSectionResponse)  
async def delete_section(deleteSection_Request: DeleteSectionRequest, db_connection = Depends(get_db)):
    sectionExists = check_section_exists(db_connection, deleteSection_Request.course_code, deleteSection_Request.section_number)
    if not sectionExists:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'This section does not exist')
    response = deleteSection(db_connection, deleteSection_Request.course_code, deleteSection_Request.section_number)
    if response == QueryStatus.SUCCESS:
        return DeleteSectionResponse(deleteSection_status = 'Successfully deleted section ' + str(deleteSection_Request.section_number) + ' of course ' + deleteSection_Request.course_code)
    else:
        return DeleteSectionResponse(deleteSection_status = 'Failed to delete section')
    
@app.post(path="/changeSectionInstructor", operation_id="change_section_instructor", response_model=ChangeInstructorResponse)
async def change_section_instructor(changeInstructor_Request: ChangeInstructorRequest, db_connection = Depends(get_db)):
    sectionExists = check_section_exists(db_connection, changeInstructor_Request.course_code, changeInstructor_Request.section_number)
    if sectionExists == 0:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'This section does not exist')
    response = changeSectionInstructor(db_connection, changeInstructor_Request.course_code, changeInstructor_Request.section_number, changeInstructor_Request.instructor_id)
    if response == QueryStatus.SUCCESS:
        return ChangeInstructorResponse(changeInstructor_status = 'Successfully changed instructor of section ' + str(changeInstructor_Request.section_number))
    else:
        return ChangeInstructorResponse(changeInstructor_status = 'Failed to change instructor')
    
@app.post(path="/freezeEnrollment", operation_id='freeze_enrollment', response_model=FreezeEnrollmentResponse)
async def freeze_enrollment(freezeEnrollment_Request: FreezeEnrollmentRequest, db_connection = Depends(get_db)):
    sectionExists = check_section_exists(db_connection, freezeEnrollment_Request.course_code, freezeEnrollment_Request.section_number)
    if sectionExists == 0:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'This section does not exist')
    response = freezeEnrollment(db_connection, freezeEnrollment_Request.course_code, freezeEnrollment_Request.section_number)
    if response == QueryStatus.SUCCESS:
        return FreezeEnrollmentResponse(freezeEnrollment_status = 'Successfully freezed enrollment for section ' + str(freezeEnrollment_Request.section_number))
    else:
        return FreezeEnrollmentResponse(freezeEnrollment_status = 'Failed to freeze enrollment')

##########   REGISTRAR ENDPOINTS ENDS    ######################    

                                             
##########   WAITLIST ENDPOINTS     ######################
# student viewing their position in the waitlist
@app.get(path="/waitlist_position", operation_id="waitlist_position", response_model = WaitlistPositionRes)
async def waitlist_position(student_id: int, db_connection = Depends(get_db)):
    """API to fetch the current position of a student in a waitlist.
    Args:
        student_id: int
    Returns:
        WaitlistPositionRes: WaitlistPositionRes model
    """
    result = get_waitlist_status(db_connection=db_connection, 
                                 student_id=student_id)
    logger.info('Succesffuly executed the query')
    return WaitlistPositionRes(waitlist_positions = result)

# instructors viewing the current waitlist for a course and section
@app.get(path="/view_waitlist", operation_id="view_waitlist", response_model = ViewWaitlistRes)
async def view_waitlist(course_code: str, section_number: int, db_connection = Depends(get_db)):
    """API to fetch the students in a waitlist.
    Args:
        section_number: int
        course_code: str
    Returns:
        ViewWaitlistRes: ViewWaitlistRes model
    """
    result = get_waitlist(db_connection=db_connection, 
                                 course_code=course_code, 
                                 section_number=section_number)
    logger.info('Succesffuly executed the query')
    return ViewWaitlistRes(waitlisted_students = result)

##########   WAITLIST ENDPOINTS ENDS    ######################    


##########   INSTRUCTOR ENDPOINTS     ######################
@app.get(path="/classEnrollment", operation_id="list_enrollment", response_model=RecordsEnrollmentResponse)
async def list_enrollment(instructor_id: int, section_number: Optional[int] = None, course_code: Optional[str] = None, db_connection = Depends(get_db)):
    """API to fetch list of enrolled students for a given instructor.

    Args:
        instructor_id (int): Instructor id
        section_number (Optional[int]): Section number (optional)
        course_code (Optional[str]): Course code (optional)

    Returns:
        RecordsEnrollmentResponse: RecordsEnrollmentResponse model
    """
    role = check_is_instructor(db_connection, instructor_id)
    if role == UserRole.NOT_FOUND or role != UserRole.INSTRUCTOR:
        logger.info('List Class Enrollment not authorized for role')
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'List Class Enrollment not authorized for role: {role}')
    result = get_enrolled_students(db_connection, instructor_id, course_code, section_number)
    logger.info('Successfully executed list_enrollment')
    return RecordsEnrollmentResponse(enrolled_students = result)


@app.get(path="/classWaitlist", operation_id="list_waitlist", response_model=RecordsWaitlistResponse)
async def list_waitlist(instructor_id: int, section_number: Optional[int] = None, course_code: Optional[str] = None, db_connection = Depends(get_db)):
    """API to fetch list of enrolled students for a given instructor.

    Args:
        instructor_id (int): Instructor id
        section_number (Optional[int]): Section number (optional)
        course_code (Optional[str]): Course code (optional)

    Returns:
        RecordsWaitlistResponse: RecordsWaitlistResponse model
    """
    role = check_is_instructor(db_connection, instructor_id)
    if role == UserRole.NOT_FOUND or role != UserRole.INSTRUCTOR:
        logger.info('List Class Waitlist not authorized for role')
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'List Class Waitlist not authorized for role: {role}')
    result = get_waitlisted_students(db_connection, instructor_id, course_code, section_number)
    logger.info('Successfully executed list_waitlist')
    return RecordsWaitlistResponse(waitlisted_students = result)

@app.get(path="/classDropped", operation_id="list_dropped", response_model=RecordsDroppedResponse)
async def list_dropped(instructor_id: int, section_number: Optional[int] = None, course_code: Optional[str] = None, db_connection = Depends(get_db)):
    """API to fetch list of dropped students for a given section.

    Args:
        instructor_id (int): Instructor id
        section_number (Optional[int]): Section number (optional)
        course_code (Optional[str]): Course code (optional)

    Returns:
        RecordsDroppedResponse: RecordsDroppedResponse model
    """
    role = check_is_instructor(db_connection, instructor_id)
    if role == UserRole.NOT_FOUND or role != UserRole.INSTRUCTOR:
        logger.info('List Class Dropped not authorized for role')
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'List Class Dropped not authorized for role: {role}')
    result = get_dropped_students(db_connection, instructor_id, course_code, section_number)
    logger.info('Successfully executed list_dropped')
    return RecordsDroppedResponse(dropped_students = result)

@app.post(path="/dropStudent", operation_id="instructor_drop_student", response_model=DroppedResponse)
async def instructor_drop_student(DropRequest: DropStudentRequest, db_connection = Depends(get_db)):
    """API to drop a student from a section.

    Args:
        instructor_id (int): Instructor id
        student_id (int): Student id
        section_number (int): Section number
        course_code (str): Course code

    Returns:
        droppedResponse: droppedResponse model
    """
    role = check_is_instructor(db_connection, DropRequest.instructor_id)
    # # check if action is being perform by instructor 
    if role == UserRole.NOT_FOUND or role != UserRole.INSTRUCTOR:
        logger.info('Drop Student not authorized for role')
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'Drop Student not authorized for role: {role}')
    # # check if instructor teaches the section 
    check_instructor = check_is_instructor_of_section(db_connection, DropRequest)
    if check_instructor == False:
        logger.info('Instructor does not teach the section')
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'Instructor does not teach the section')
    # # check if student is enrolled in the section or waitlisted
    check_status = check_is_enrolled(db_connection, DropRequest)
    if check_status == False:
        logger.info('Student is not enrolled in the section')
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail= f'Student is not enrolled in the section')
    try:    
        result = drop_student(db_connection, DropRequest)
        logger.info('Successfully executed drop_student')
        if result == QueryStatus.SUCCESS:
            return DroppedResponse(drop_status = "Student was dropped")
    except DBException as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=err.error_detail)
