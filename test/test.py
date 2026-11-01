import unittest
from unittest.mock import Mock, patch

from minerva.Blueprints.Student import Student
from minerva.helper.api import ZermeloAPIClient, ZermeloAPIError


class FakeResponse:
    def __init__(self, payload=None, status_code=200, text="", headers=None):
        self.payload = payload
        self.status_code = status_code
        self.text = text
        self.headers = headers or {}

    def json(self):
        if self.payload is None:
            raise ValueError("Response is not JSON")
        return self.payload


class ZermeloAPIClientTests(unittest.TestCase):
    def test_client_requires_credentials(self):
        with self.assertRaises(ValueError):
            ZermeloAPIClient()

    def test_client_builds_base_url_and_authorization_header(self):
        client = ZermeloAPIClient("school", "Bearer test-token")

        self.assertEqual(
            client.base_url,
            "https://school.zportal.nl/api/v3/",
        )
        self.assertEqual(
            client.session.headers["Authorization"],
            "Bearer test-token",
        )

    def test_client_accepts_user_created_configuration_without_dotenv(self):
        user_configuration = {
            "school": "my-school",
            "authorization": "Bearer user-created-token",
        }

        client = ZermeloAPIClient(**user_configuration)

        self.assertEqual(client.school, "my-school")
        self.assertEqual(
            client.session.headers["Authorization"],
            "Bearer user-created-token",
        )

    @patch("minerva.helper.api.log_api_message")
    def test_get_endpoint_returns_api_data(self, log_api_message):
        client = ZermeloAPIClient("school", "Bearer test-token")
        client.session.get = Mock(
            return_value=FakeResponse(
                {
                    "response": {
                        "status": 200,
                        "data": [{"id": 42, "firstName": "Dani"}],
                    }
                }
            )
        )

        result = client.get_endpoint("students", "fields=id,firstName")

        self.assertEqual(result, [{"id": 42, "firstName": "Dani"}])
        client.session.get.assert_called_once_with(
            "https://school.zportal.nl/api/v3/students?fields=id,firstName",
            timeout=30,
        )
        log_api_message.assert_called_once()

    @patch("minerva.helper.api.log_api_message")
    def test_get_endpoint_raises_for_unauthorized_response(self, _log_api_message):
        client = ZermeloAPIClient("school", "Bearer expired-token")
        client.session.get = Mock(
            return_value=FakeResponse(
                {"response": {"status": 401, "message": "Unauthorized"}}
            )
        )

        with self.assertRaisesRegex(ZermeloAPIError, "Token expired"):
            client.get_endpoint("students", "")

    @patch("minerva.helper.api.log_api_message")
    def test_get_endpoint_reports_non_json_response(self, _log_api_message):
        client = ZermeloAPIClient("school", "Bearer test-token")
        client.session.get = Mock(
            return_value=FakeResponse(
                status_code=502,
                text="Bad Gateway",
                headers={"Content-Type": "text/html"},
            )
        )

        with self.assertRaisesRegex(ZermeloAPIError, "non-JSON response"):
            client.get_endpoint("students", "")


class StudentTests(unittest.TestCase):
    def test_student_round_trips_through_tuple(self):
        student = Student(
            {
                "id": 7,
                "student": "student-7",
                "departmentOfBranch": 2,
                "mentorGroup": None,
                "mainGroup": 3,
                "groupInDepartments": [10, 11],
                "fullName": "Dani Test",
                "schoolInSchoolYear": 2026,
                "firstName": "Dani",
                "lastName": "Test",
                "departmentOfBranchCode": "VWO",
                "mainGroupName": "V6A",
                "prefix": None,
            }
        )

        restored = Student.from_tuple(student.to_tuple())

        self.assertEqual(restored.id, student.id)
        self.assertEqual(restored.fullName, student.fullName)
        self.assertEqual(restored.groupInDepartments, [10, 11])


if __name__ == "__main__":
    unittest.main()