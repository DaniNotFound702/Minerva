import sys
import datetime
from os.path import dirname, abspath
sys.path.insert(0, abspath(dirname(dirname(__file__))))
from helper.api import get_endpoint


def appointments(schoolYear_id, schoolYear, user_id):

    fields = (
        "id", "appointmentInstance", "start", "end", "startTimeSlot", "endTimeSlot",
        "branch", "type", "groupsInDepartments", "locationsOfBranch", "optional",
        "valid", "cancelled", "cancelledReason", "modified", "teacherChanged",
        "groupChanged", "locationChanged", "timeChanged", "moved", "created",
        "hidden", "changeDescription", "schedulerRemark", "content", "lastModified",
        "new", "choosableInDepartments", "choosableInDepartmentCodes",
        "extraStudentSource", "onlineLocationUrl", "expectedStudentCount",
        "expectedStudentCountOnline", "udmUUID", "creator", "onlineStudents",
        "appointmentLastModified", "remark", "availableSpace", "subjects",
        "teachers", "onlineTeachers", "availableSpace", "branch", "cancelledReason",
        "choosableInDepartments", "creator", "expectedStudentCount", 
        "expectedStudentCountOnline", "extraStudentSource", "groupsInDepartments",
        "locationsOfBranch", "modified", "moved", "new", "onlineLocationUrl", "onlineStudents", "onlineTeachers", "remark", "udmUUID"
    )
    # schooljaar `year` loopt van 1 aug `year` t/m 31 jul `year + 1`
    start = int(datetime.datetime(int(schoolYear), 8, 1).timestamp())
    end = int(datetime.datetime(int(schoolYear) + 1, 7, 31).timestamp())

    data = get_endpoint("appointments", "schoolInSchoolYear=" + str(schoolYear_id) + "&user=" + str(user_id) + "&start=" + str(start) + "&end=" + str(end) + "&fields=" + ",".join(fields))
    return data


def branchesofschools():
    fields = ("branch", "id", "schoolInSchoolYear", "name")
    data = get_endpoint("branchesofschools", "&fields=" + ",".join(fields))
    return data


def departmentsofbranches (): 
    fields = ("branchOfSchoolCode", "educationType", "educations", "mainGroupAuthority", "profiles", "schoolInSchoolYearId", "schoolInSchoolYearName", "teacherTeams", "teachingLevel", "weekTimeTable", "yearOfEducation")
    data = get_endpoint("departmentsofbranches", "fields=" + ",".join(fields))
    return data

def branches():
    fields = ("name", "code", "somCode", "somUuid")
    data = get_endpoint("branches", "fields=" + ",".join(fields))
    return data

def choosableindepartments():
    fields = ("courseType", "departmentOfBranchCode", "excludedSegments", "iltCode", "isExam", "lessonHoursInClassPeriods", "qualifiedCode", "scheduleCode", "scroungeSegments", "sectionOfBranch", "sectionOfBranchAbbreviation", "studentCanEdit", "subjectCode", "subjectName", "subjectScheduleCode", "subjectType")
    data = get_endpoint("choosableindepartments", "fields=" + ",".join(fields))
    return data

def groupindepartments():
    fields = ("id", "departmentOfBranch", "extendedName", "isMainGroup", "isMentorGroup", "name")
    data = get_endpoint("groupindepartments", "fields=" + ",".join(fields))
    return data

def holidays():
    fields = ("id", "start", "end", "schoolInSchoolYear", "name")
    data = get_endpoint("holidays", "fields=" + ",".join(fields))
    return data

def locationofbranches():
    fields = ("id", "student", "departmentOfBranch", "mentorGroup", "mainGroup", "groupInDepartments", "fullName", "schoolInSchoolYear", "firstName", "lastName", "departmentOfBranchCode", "mainGroupName", "prefix")
    data = get_endpoint("locationofbranches", "fields=" + ",".join(fields))
    return data


def schoolsinschoolyears(schoolYear):
    fields = ("archived", "archivedTime", "id", "name", "school","year", "branchOfSchools", "project", "projectName", "schoolHrmsCode", "schoolName")
    data = get_endpoint("schoolsinschoolyears","schoolInSchoolYear=" + str(schoolYear) + "&fields=" + ",".join(fields))
    return data

def timeslotnames(schoolYear):
    fields = ("code","id", "schoolInSchoolYear")
    data = get_endpoint("timeslotnames", "fields=" + ",".join(fields))
    return data

def studentsindepartments (schoolYear):
    fields = ("id","student","departmentOfBranch","mentorGroup","mainGroup","groupInDepartments","fullName","schoolInSchoolYear","firstName","lastName","departmentOfBranchCode","mainGroupName","prefix")
    data = get_endpoint("studentsindepartments", "schoolInSchoolYear=" + str(schoolYear) + "&fields=" + ",".join(fields))
    return data


def subjectselectionsubjects(schoolYear):
    fields = ("id", "schoolInSchoolYear")
    data = get_endpoint("subjectselectionsubjects", "schoolInSchoolYear=" + str(schoolYear) + "&fields=" + ",".join(fields))
    return data


