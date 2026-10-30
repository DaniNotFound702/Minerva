import sys
import datetime
from os.path import dirname, abspath
sys.path.insert(0, abspath(dirname(dirname(__file__))))
from ..helper.api import ZermeloAPIClient

class ZermeloMain:
    def __init__(self, api_client: ZermeloAPIClient):
        self.api_client = api_client

    def appointments(self, schoolYear_id, schoolYear, user_id):

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

        data = self.api.get_endpoint("appointments", "schoolInSchoolYear=" + str(schoolYear_id) + "&user=" + str(user_id) + "&start=" + str(start) + "&end=" + str(end) + "&fields=" + ",".join(fields))
        return data


    def branchesofschools(self):
        fields = ("branch", "id", "schoolInSchoolYear", "name")
        data = self.api.get_endpoint("branchesofschools", "&fields=" + ",".join(fields))
        return data

    def departmentsofbranches(self): 
        fields = ("branchOfSchoolCode", "educationType", "educations", "mainGroupAuthority", "profiles", "schoolInSchoolYearId", "schoolInSchoolYearName", "teacherTeams", "teachingLevel", "weekTimeTable", "yearOfEducation")
        data = self.api.get_endpoint("departmentsofbranches", "fields=" + ",".join(fields))
        return data

    def branches(self):
        fields = ("name", "code", "somCode", "somUuid")
        data = self.api.get_endpoint("branches", "fields=" + ",".join(fields))
        return data

    def choosableindepartments(self):
        fields = ("courseType", "departmentOfBranchCode", "excludedSegments", "iltCode", "isExam", "lessonHoursInClassPeriods", "qualifiedCode", "scheduleCode", "scroungeSegments", "sectionOfBranch", "sectionOfBranchAbbreviation", "studentCanEdit", "subjectCode", "subjectName", "subjectScheduleCode", "subjectType")
        data = self.api.get_endpoint("choosableindepartments", "fields=" + ",".join(fields))
        return data

    def groupindepartments(self):
        fields = ("id", "departmentOfBranch", "extendedName", "isMainGroup", "isMentorGroup", "name")
        data = self.api.get_endpoint("groupindepartments", "fields=" + ",".join(fields))
        return data

    def holidays(self):
        fields = ("id", "start", "end", "schoolInSchoolYear", "name")
        data = self.api.get_endpoint("holidays", "fields=" + ",".join(fields))
        return data

    def locationofbranches(self):
        fields = ("id", "schoolInSchoolYear")
        data = self.api.get_endpoint("locationofbranches", "fields=" + ",".join(fields))
        return data



    def schoolsinschoolyears(self, schoolYear):
        fields = ("archived", "archivedTime", "id", "name", "school","year", "branchOfSchools", "project", "projectName", "schoolHrmsCode", "schoolName")
        data = self.api.get_endpoint("schoolsinschoolyears","schoolInSchoolYear=" + str(schoolYear) + "&fields=" + ",".join(fields))
        return data

    def timeslotnames(self, schoolYear):
        fields = ("code","id", "schoolInSchoolYear")
        data = self.api.get_endpoint("timeslotnames", "fields=" + ",".join(fields))
        return data

    def studentsindepartments (self, schoolYear):
        fields = ("id","student","departmentOfBranch","mentorGroup","mainGroup","groupInDepartments","fullName","schoolInSchoolYear","firstName","lastName","departmentOfBranchCode","mainGroupName","prefix")
        data = self.api.get_endpoint("studentsindepartments", "schoolInSchoolYear=" + str(schoolYear) + "&fields=" + ",".join(fields))
        return data

    def subjectselectionsubjects(self, schoolYear):
        fields = ("id", "schoolInSchoolYear")
        data = self.api.get_endpoint("subjectselectionsubjects", "schoolInSchoolYear=" + str(schoolYear) + "&fields=" + ",".join(fields))
        return data

