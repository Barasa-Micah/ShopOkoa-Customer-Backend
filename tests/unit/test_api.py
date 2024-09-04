import pytest
import logging

logger = logging.getLogger(__name__)

subject_pk = None

ACCESS_TOKEN = None


@pytest.mark.django_db
def test_account_registration(api_client) -> None:
    """
    Test the create account API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "username": "DummyUser",
        "email": "dummyuser23@gmail.com",
        "password1": "Programmer@2024",
        "password2": "Programmer@2024",
        "first_name": "Dummy",
        "last_name": "User"
    }

    # Create account
    response_create = api_client.post("/api/v1/auth/registration/", data=payload, format="json")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["user"]["username"] == payload["username"]
    assert response_create.data["user"]["email"] == payload["email"]
    assert response_create.data["user"]["first_name"] == payload["first_name"]
    assert response_create.data["user"]["last_name"] == payload["last_name"]
    global ACCESS_TOKEN
    ACCESS_TOKEN = response_create.data["access_token"]
    print(ACCESS_TOKEN)


@pytest.mark.django_db
def test_create_cocurricularactivity(api_client) -> None:
    """
    Test the create cocurricular activities API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "cocurricularActivity": "Football"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create cocurricular activity
    response_create = api_client.post(
        "/api/v1/classifyme/cocurricular-activities/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created cocurricular activity with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["cocurricularActivity"] == payload["cocurricularActivity"]

    # Get cocurricular activity
    response_get = api_client.get(
        f"/api/v1/classifyme/cocurricular-activities/{pk}/", format="json")
    logger.info(f"Read cocurricular activity with pk: {pk}")
    logger.info(f"Response: {response_get.data}")
    assert response_get.status_code == 200
    assert response_get.data["cocurricularActivity"] == payload["cocurricularActivity"]


@pytest.mark.django_db
def test_patch_cocurricularactivity(api_client) -> None:
    """
    Test the patch cocurricular activities API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "cocurricularActivity": "Table Tennis"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create cocurricular activity
    response_create = api_client.post(
        "/api/v1/classifyme/cocurricular-activities/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created cocurricular activity with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["cocurricularActivity"] == payload["cocurricularActivity"]

    # Update cocurricular activity
    payload["cocurricularActivity"] = "Athletics"
    response_update = api_client.patch(
        f"/api/v1/classifyme/cocurricular-activities/{pk}/", data=payload, format="json")
    logger.info(f"Updated cocurricular activity with pk: {pk}")
    logger.info(f"Response: {response_update.data}")
    assert response_update.status_code == 200
    assert response_update.data["cocurricularActivity"] == payload["cocurricularActivity"]

    # Cocurricular activity does not exist
    response_update = api_client.patch(
        f"/api/v1/classifyme/cocurricular-activities/{pk + '1'}/", data=payload, format="json")
    logger.info(f"Updated cocurricular activity with pk: {pk + '1'}")
    logger.info(f"Response: {response_update.data}")
    assert response_update.status_code == 404


@pytest.mark.django_db
def test_delete_cocurricularactivity(api_client) -> None:
    """
    Test the delete cocurricular activities API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "cocurricularActivity": "Racket Sports"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create cocurricular activity
    response_create = api_client.post(
        "/api/v1/classifyme/cocurricular-activities/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created cocurricular activity with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["cocurricularActivity"] == payload["cocurricularActivity"]

    # Delete cocurricular activity
    response_delete = api_client.delete(
        f"/api/v1/classifyme/cocurricular-activities/{pk}/", format="json")
    logger.info(f"Deleted cocurricular activity with pk: {pk}")
    logger.info(f"Response: {response_delete.data}")
    assert response_delete.status_code == 204

    # Cocurricular activity does not exist
    response_delete = api_client.delete(
        f"/api/v1/classifyme/cocurricular-activities/{pk + '1'}/", format="json")
    logger.info(f"Deleted cocurricular activity with pk: {pk + '1'}")
    logger.info(f"Response: {response_delete.data}")
    assert response_delete.status_code == 404


@pytest.mark.django_db
def test_create_interest(api_client) -> None:
    """
    Test the create interest API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "Interest": "Music"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create interest
    response_create = api_client.post(
        "/api/v1/classifyme/interests/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created interest with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["Interest"] == payload["Interest"]

    # Get interest
    response_get = api_client.get(
        f"/api/v1/classifyme/interests/{pk}/", format="json")
    logger.info(f"Read interest with pk: {pk}")
    logger.info(f"Response: {response_get.data}")
    assert response_get.status_code == 200
    assert response_get.data["Interest"] == payload["Interest"]


@pytest.mark.django_db
def test_patch_interest(api_client) -> None:
    """
    Test the patch interest API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "Interest": "Dance"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create interest
    response_create = api_client.post(
        "/api/v1/classifyme/interests/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created interest with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["Interest"] == payload["Interest"]

    # Update interest
    payload["Interest"] = "Sports"
    response_update = api_client.patch(
        f"/api/v1/classifyme/interests/{pk}/", data=payload, format="json")
    logger.info(f"Updated interest with pk: {pk}")
    logger.info(f"Response: {response_update.data}")
    assert response_update.status_code == 200
    assert response_update.data["Interest"] == payload["Interest"]

    # Interest does not exist
    response_update = api_client.patch(
        f"/api/v1/classifyme/interests/{pk + '1'}/", data=payload, format="json")
    logger.info(f"Updated interest with pk: {pk + '1'}")
    logger.info(f"Response: {response_update.data}")
    assert response_update.status_code == 404


@pytest.mark.django_db
def test_delete_interest(api_client) -> None:
    """
    Test the delete interest API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "Interest": "Reading"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create interest
    response_create = api_client.post(
        "/api/v1/classifyme/interests/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created interest with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["Interest"] == payload["Interest"]

    # Delete interest
    response_delete = api_client.delete(
        f"/api/v1/classifyme/interests/{pk}/", format="json")
    logger.info(f"Deleted interest with pk: {pk}")
    logger.info(f"Response: {response_delete.data}")
    assert response_delete.status_code == 204

    # Interest does not exist
    response_delete = api_client.delete(
        f"/api/v1/classifyme/interests/{pk + '1'}/", format="json")
    logger.info(f"Deleted interest with pk: {pk + '1'}")
    logger.info(f"Response: {response_delete.data}")
    assert response_delete.status_code == 404


@pytest.mark.django_db
def test_create_personality(api_client) -> None:
    """
    Test the create personality API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "personalityType": "INTJ"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create personality
    response_create = api_client.post(
        "/api/v1/classifyme/personality/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created personality with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["personalityType"] == payload["personalityType"]

    # Get personality
    response_get = api_client.get(
        f"/api/v1/classifyme/personality/{pk}/", format="json")
    logger.info(f"Read personality with pk: {pk}")
    logger.info(f"Response: {response_get.data}")
    assert response_get.status_code == 200
    assert response_get.data["personalityType"] == payload["personalityType"]


@pytest.mark.django_db
def test_patch_personality(api_client) -> None:
    """
    Test the patch personality API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "personalityType": "ISTJ"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create personality
    response_create = api_client.post(
        "/api/v1/classifyme/personality/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created personality with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["personalityType"] == payload["personalityType"]

    # Update personality
    payload["personalityType"] = "ISTP"
    response_update = api_client.patch(
        f"/api/v1/classifyme/personality/{pk}/", data=payload, format="json")
    logger.info(f"Updated personality with pk: {pk}")
    logger.info(f"Response: {response_update.data}")
    assert response_update.status_code == 200
    assert response_update.data["personalityType"] == payload["personalityType"]

    # Personality does not exist
    response_update = api_client.patch(
        f"/api/v1/classifyme/personality/{pk + '1'}/", data=payload, format="json")
    logger.info(f"Updated personality with pk: {pk + '1'}")
    logger.info(f"Response: {response_update.data}")
    assert response_update.status_code == 404


@pytest.mark.django_db
def test_delete_personality(api_client) -> None:
    """
    Test the delete personality API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "personalityType": "ESTP"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create personality
    response_create = api_client.post(
        "/api/v1/classifyme/personality/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created personality with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["personalityType"] == payload["personalityType"]

    # Delete personality
    response_delete = api_client.delete(
        f"/api/v1/classifyme/personality/{pk}/", format="json")
    logger.info(f"Deleted personality with pk: {pk}")
    logger.info(f"Response: {response_delete.data}")
    assert response_delete.status_code == 204

    # Personality does not exist
    response_delete = api_client.delete(
        f"/api/v1/classifyme/personality/{pk + '1'}/", format="json")
    logger.info(f"Deleted personality with pk: {pk + '1'}")
    logger.info(f"Response: {response_delete.data}")
    assert response_delete.status_code == 404


@pytest.mark.django_db
def test_create_studentfeedback(api_client) -> None:
    """
    Test the create student feedback API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "feedback_type": "Course Recommendations",
        "feedback": "I like the course",
        "rating": "5"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create student feedback
    response_create = api_client.post(
        "/api/v1/classifyme/student-feedback/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created student feedback with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["feedback_type"] == payload["feedback_type"]
    assert response_create.data["feedback"] == payload["feedback"]
    assert response_create.data["rating"] == payload["rating"]

    # Get student feedback
    response_get = api_client.get(
        f"/api/v1/classifyme/student-feedback/{pk}/", format="json")
    logger.info(f"Read student feedback with pk: {pk}")
    logger.info(f"Response: {response_get.data}")
    assert response_get.status_code == 200
    assert response_get.data["feedback_type"] == payload["feedback_type"]
    assert response_get.data["feedback"] == payload["feedback"]
    assert response_get.data["rating"] == payload["rating"]


@pytest.mark.django_db
def test_patch_studentfeedback(api_client) -> None:
    """
    Test the patch student feedback API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "feedback_type": "Course Recommendations",
        "feedback": "I like the course",
        "rating": "5"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create student feedback
    response_create = api_client.post(
        "/api/v1/classifyme/student-feedback/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created student feedback with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["feedback_type"] == payload["feedback_type"]
    assert response_create.data["feedback"] == payload["feedback"]
    assert response_create.data["rating"] == payload["rating"]

    # Update student feedback
    payload["feedback_type"] = "Course Recommendations"
    payload["feedback"] = "I like the course"
    payload["rating"] = "4"
    response_update = api_client.patch(
        f"/api/v1/classifyme/student-feedback/{pk}/", data=payload, format="json")
    logger.info(f"Updated student feedback with pk: {pk}")
    logger.info(f"Response: {response_update.data}")
    assert response_update.status_code == 200
    assert response_update.data["feedback_type"] == payload["feedback_type"]
    assert response_update.data["feedback"] == payload["feedback"]
    assert response_update.data["rating"] == payload["rating"]

    # Student feedback does not exist
    response_update = api_client.patch(
        f"/api/v1/classifyme/student-feedback/{pk + '1'}/", data=payload, format="json")
    logger.info(f"Updated student feedback with pk: {pk + '1'}")
    logger.info(f"Response: {response_update.data}")
    assert response_update.status_code == 404


@pytest.mark.django_db
def test_delete_studentfeedback(api_client) -> None:
    """
    Test the delete student feedback API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "feedback_type": "Course Recommendations",
        "feedback": "I like the course",
        "rating": "5"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create student feedback
    response_create = api_client.post(
        "/api/v1/classifyme/student-feedback/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created student feedback with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["feedback_type"] == payload["feedback_type"]
    assert response_create.data["feedback"] == payload["feedback"]
    assert response_create.data["rating"] == payload["rating"]

    # Delete student feedback
    response_delete = api_client.delete(
        f"/api/v1/classifyme/student-feedback/{pk}/", format="json")
    logger.info(f"Deleted student feedback with pk: {pk}")
    logger.info(f"Response: {response_delete.data}")
    assert response_delete.status_code == 204

    # Student feedback does not exist
    response_delete = api_client.delete(
        f"/api/v1/classifyme/student-feedback/{pk + '1'}/", format="json", headers=headers)
    logger.info(f"Deleted student feedback with pk: {pk + '1'}")
    logger.info(f"Response: {response_delete.data}")
    assert response_delete.status_code == 404


@pytest.mark.django_db
def test_create_subject(api_client) -> None:
    """
    Test the create subject API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "subjectName": "Mathematics"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create subject
    response_create = api_client.post(
        "/api/v1/classifyme/subjects/", data=payload, format="json")
    pk = response_create.data["pk"]
    global subject_pk
    subject_pk = pk
    logger.info(f"Created subject with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["subjectName"] == payload["subjectName"]

    # Get subject
    response_get = api_client.get(
        f"/api/v1/classifyme/subjects/{pk}/", format="json")
    logger.info(f"Read subject with pk: {pk}")
    logger.info(f"Response: {response_get.data}")
    assert response_get.status_code == 200
    assert response_get.data["subjectName"] == payload["subjectName"]


@pytest.mark.django_db
def test_patch_subject(api_client) -> None:
    """
    Test the patch subject API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "subjectName": "Mathematics"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create subject
    response_create = api_client.post(
        "/api/v1/classifyme/subjects/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created subject with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["subjectName"] == payload["subjectName"]

    # Update subject
    payload["subjectName"] = "English"
    response_update = api_client.patch(
        f"/api/v1/classifyme/subjects/{pk}/", data=payload, format="json")
    logger.info(f"Updated subject with pk: {pk}")
    logger.info(f"Response: {response_update.data}")
    assert response_update.status_code == 200
    assert response_update.data["subjectName"] == payload["subjectName"]

    # Subject does not exist
    response_update = api_client.patch(
        f"/api/v1/classifyme/subjects/{pk + '1'}/", data=payload, format="json")
    logger.info(f"Updated subject with pk: {pk + '1'}")
    logger.info(f"Response: {response_update.data}")
    assert response_update.status_code == 404


@pytest.mark.django_db
def test_delete_subject(api_client) -> None:
    """
    Test the delete subject API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "subjectName": "Mathematics"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create subject
    response_create = api_client.post(
        "/api/v1/classifyme/subjects/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created subject with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["subjectName"] == payload["subjectName"]

    # Delete subject
    response_delete = api_client.delete(
        f"/api/v1/classifyme/subjects/{pk}/", format="json")
    logger.info(f"Deleted subject with pk: {pk}")
    logger.info(f"Response: {response_delete.data}")
    assert response_delete.status_code == 204

    # Subject does not exist
    response_delete = api_client.delete(
        f"/api/v1/classifyme/subjects/{pk + '1'}/", format="json")
    logger.info(f"Deleted subject with pk: {pk + '1'}")
    logger.info(f"Response: {response_delete.data}")
    assert response_delete.status_code == 404


@pytest.mark.django_db
def test_create_studentIndividualSubjectPerformance(api_client) -> None:
    """
    Test the create student individual subject performance API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "examName": "KCSE",
        "examType": "National Exam",
        "grade": "A",
        "averageMarks": "80",
        "term": "Term 1",
        "year": "2021",
        "subject": f"{subject_pk}"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create student individual subject performance
    response_create = api_client.post(
        "/api/v1/classifyme/student-individual-subject-performance/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created student individual subject performance with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["examName"] == payload["examName"]
    assert response_create.data["examType"] == payload["examType"]
    assert response_create.data["grade"] == payload["grade"]
    assert response_create.data["averageMarks"] == payload["averageMarks"]
    assert response_create.data["term"] == payload["term"]
    assert response_create.data["year"] == payload["year"]
    assert response_create.data["subject"] == payload["subject"]

    # Get student individual subject performance
    response_get = api_client.get(
        f"/api/v1/classifyme/student-individual-subject-performance/{pk}/", format="json")
    logger.info(f"Read student individual subject performance with pk: {pk}")
    logger.info(f"Response: {response_get.data}")
    assert response_get.status_code == 200
    assert response_get.data["examName"] == payload["examName"]
    assert response_get.data["examType"] == payload["examType"]
    assert response_get.data["grade"] == payload["grade"]
    assert response_get.data["averageMarks"] == payload["averageMarks"]
    assert response_get.data["term"] == payload["term"]
    assert response_get.data["year"] == payload["year"]
    assert response_get.data["subject"] == payload["subject"]


@pytest.mark.django_db
def test_patch_studentIndividualSubjectPerformance(api_client) -> None:
    """
    Test the patch student individual subject performance API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "examName": "KCSE",
        "examType": "National Exam",
        "grade": "A-",
        "averageMarks": "80",
        "term": "Term 1",
        "year": "2021",
        "subject": f"{subject_pk}"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create student individual subject performance
    response_create = api_client.post(
        "/api/v1/classifyme/student-individual-subject-performance/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created student individual subject performance with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["examName"] == payload["examName"]
    assert response_create.data["examType"] == payload["examType"]
    assert response_create.data["grade"] == payload["grade"]
    assert response_create.data["averageMarks"] == payload["averageMarks"]
    assert response_create.data["term"] == payload["term"]
    assert response_create.data["year"] == payload["year"]
    assert response_create.data["subject"] == payload["subject"]

    # Update student individual subject performance
    payload["examName"] = "KCSE"
    payload["examType"] = "National Exam"
    payload["grade"] = "A"
    payload["averageMarks"] = "81"
    payload["term"] = "Term 1"
    payload["year"] = "2021"
    payload["subject"] = f"{subject_pk}"
    response_update = api_client.patch(
        f"/api/v1/classifyme/student-individual-subject-performance/{pk}/", data=payload, format="json")
    logger.info(f"Updated student individual subject performance with pk: {pk}")
    logger.info(f"Response: {response_update.data}")
    assert response_update.status_code == 200
    assert response_update.data["examName"] == payload["examName"]
    assert response_update.data["examType"] == payload["examType"]
    assert response_update


@pytest.mark.django_db
def test_delete_studentIndividualSubjectPerformance(api_client) -> None:
    """
    Test the delete student individual subject performance API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "examName": "KCSE",
        "examType": "National Exam",
        "grade": "A",
        "averageMarks": "80",
        "term": "Term 1",
        "year": "2021",
        "subject": f"{subject_pk}"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create student individual subject performance
    response_create = api_client.post(
        "/api/v1/classifyme/student-individual-subject-performance/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created student individual subject performance with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["examName"] == payload["examName"]
    assert response_create.data["examType"] == payload["examType"]
    assert response_create.data["grade"] == payload["grade"]
    assert response_create.data["averageMarks"] == payload["averageMarks"]
    assert response_create.data["term"] == payload["term"]
    assert response_create.data["year"] == payload["year"]
    assert response_create.data["subject"] == payload["subject"]

    # Delete student individual subject performance
    response_delete = api_client.delete(
        f"/api/v1/classifyme/student-individual-subject-performance/{pk}/", format="json")
    logger.info(f"Deleted student individual subject performance with pk: {pk}")
    logger.info(f"Response: {response_delete.data}")
    assert response_delete.status_code == 204

    # Student individual subject performance does not exist
    response_delete = api_client.delete(
        f"/api/v1/classifyme/student-individual-subject-performance/{pk + '1'}/", format="json")
    logger.info(f"Deleted student individual subject performance with pk: {pk + '1'}")
    logger.info(f"Response: {response_delete.data}")
    assert response_delete.status_code == 404


@pytest.mark.django_db
def test_create_studentOverallTermPerformance(api_client) -> None:
    """
    Test the create student overall term performance API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "year": "2021",
        "examType": "National Exam",
        "grade": "A",
        "points": "81",
        "term": "Term 1",
        "examName": "KCSE"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create student overall term performance
    response_create = api_client.post(
        "/api/v1/classifyme/student-overall-term-performance/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created student overall term performance with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["year"] == payload["year"]
    assert response_create.data["examType"] == payload["examType"]
    assert response_create.data["grade"] == payload["grade"]
    assert response_create.data["points"] == payload["points"]
    assert response_create.data["term"] == payload["term"]
    assert response_create.data["examName"] == payload["examName"]

    # Get student overall term performance
    response_get = api_client.get(
        f"/api/v1/classifyme/student-overall-term-performance/{pk}/", format="json")
    logger.info(f"Read student overall term performance with pk: {pk}")
    logger.info(f"Response: {response_get.data}")
    assert response_get.status_code == 200
    assert response_get.data["year"] == payload["year"]
    assert response_get.data["examType"] == payload["examType"]
    assert response_get.data["grade"] == payload["grade"]
    assert response_get.data["points"] == payload["points"]
    assert response_get.data["term"] == payload["term"]
    assert response_get.data["examName"] == payload["examName"]


@pytest.mark.django_db
def test_create_topics(api_client) -> None:
    """
    Test the create topics API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "topicName": "Mathematics",
        "isFavorite": "True",
        "subject": f"{subject_pk}"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create topics
    response_create = api_client.post(
        "/api/v1/classifyme/topics/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created topics with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["topicName"] == payload["topicName"]
    assert response_create.data["isFavorite"] == payload["isFavorite"]
    assert response_create.data["subject"] == payload["subject"]

    # Get topics
    response_get = api_client.get(
        f"/api/v1/classifyme/topics/{pk}/", format="json")
    logger.info(f"Read topics with pk: {pk}")
    logger.info(f"Response: {response_get.data}")
    assert response_get.status_code == 200
    assert response_get.data["topicName"] == payload["topicName"]
    assert response_get.data["isFavorite"] == payload["isFavorite"]
    assert response_get.data["subject"] == payload["subject"]


@pytest.mark.django_db
def test_patch_topics(api_client) -> None:
    """
    Test the patch topics API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "topicName": "Mathematics",
        "isFavorite": "True",
        "subject": f"{subject_pk}"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create topics
    response_create = api_client.post(
        "/api/v1/classifyme/topics/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created topics with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["topicName"] == payload["topicName"]
    assert response_create.data["isFavorite"] == payload["isFavorite"]
    assert response_create.data["subject"] == payload["subject"]

    # Update topics
    payload["topicName"] = "English"
    payload["isFavorite"] = "False"
    payload["subject"] = f"{subject_pk}"
    response_update = api_client.patch(
        f"/api/v1/classifyme/topics/{pk}/", data=payload, format="json")
    logger.info(f"Updated topics with pk: {pk}")
    logger.info(f"Response: {response_update.data}")
    assert response_update.status_code == 200
    assert response_update.data["topicName"] == payload["topicName"]
    assert response_update.data["isFavorite"] == payload["isFavorite"]
    assert response_update.data["subject"] == payload["subject"]

    # Topics does not exist
    response_update = api_client.patch(
        f"/api/v1/classifyme/topics/{pk + '1'}/", data=payload, format="json")
    logger.info(f"Updated topics with pk: {pk + '1'}")
    logger.info(f"Response: {response_update.data}")
    assert response_update.status_code == 404


@pytest.mark.django_db
def test_delete_topics(api_client) -> None:
    """
    Test the delete topics API
    :param api_client: APIClient
    :return: None
    """

    payload = {
        "topicName": "Mathematics",
        "isFavorite": "True",
        "subject": f"{subject_pk}"
    }

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {ACCESS_TOKEN}",
    )

    # Create topics
    response_create = api_client.post(
        "/api/v1/classifyme/topics/", data=payload, format="json")
    pk = response_create.data["pk"]
    logger.info(f"Created topics with pk: {pk}")
    logger.info(f"Response: {response_create.data}")
    assert response_create.status_code == 201
    assert response_create.data["topicName"] == payload["topicName"]
    assert response_create.data["isFavorite"] == payload["isFavorite"]
    assert response_create.data["subject"] == payload["subject"]

    # Delete topics
    response_delete = api_client.delete(
        f"/api/v1/classifyme/topics/{pk}/", format="json")
    logger.info(f"Deleted topics with pk: {pk}")
    logger.info(f"Response: {response_delete.data}")
    assert response_delete.status_code == 204

    # Topics does not exist
    response_delete = api_client.delete(
        f"/api/v1/classifyme/topics/{pk + '1'}/", format="json")
    logger.info(f"Deleted topics with pk: {pk + '1'}")
    logger.info(f"Response: {response_delete.data}")
    assert response_delete.status_code == 404