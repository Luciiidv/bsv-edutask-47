import pytest
from unittest.mock import patch
from src.util.dao import DAO
from pymongo.errors import WriteError
from bson.objectid import ObjectId

@pytest.fixture
def dao():
    with patch("src.util.dao.getValidator") as mock_get_validator:
        from src.util.validators import getValidator
        mock_get_validator.return_value = getValidator("users")
        test_dao = DAO("_users")
        test_dao.collection.create_index("email", unique=True)
        yield test_dao
        test_dao.drop() # or .collection.drop()?

def test_case_1_create_all_required_fields_valid(dao):
    """Test Case 1: Create a user with all required fields valid"""
    user = {"firstName": "Jane", "lastName": "Doe", "email": "jane.doe@example.com"}
    res = dao.create(user)
    assert res is not None
    assert res.get("_id") is not None
    assert res.get("firstName") == user["firstName"]
    assert res.get("lastName") == user["lastName"]
    assert res.get("email") == user["email"]

    pass

def test_case_2_create_firstName_field_missing(dao):
    """Test Case 2: Create a user with firstName field missing"""
    user = {"lastName": "Doe", "email": "jane.doe@example.com"}
    with pytest.raises(WriteError):
        res = dao.create(user)

def test_case_3_create_lastName_field_missing(dao):
    """Test Case 3: Create a user with lastName field missing"""
    user = {"firstName": "Jane", "email": "jane.doe@example.com"}
    with pytest.raises(WriteError):
        res = dao.create(user)

def test_case_4_create_email_field_missing(dao):
    """Test Case 4: Create a user with email field missing"""
    user = {"firstName": "Jane", "lastName": "Doe"}
    with pytest.raises(WriteError):
        res = dao.create(user)

def test_case_5_create_all_fields_missing(dao):
    """Test Case 5: Create a user with all fields missing"""
    user = {}
    with pytest.raises(WriteError):
        res = dao.create(user)

def test_case_6_create_firstName_int_type(dao):
    """Test Case 6: Create a user with firstName field as integer"""
    user = {"firstName": 100, "lastName": "Doe", "email": "jane.doe@example.com"}
    with pytest.raises(WriteError):
        res = dao.create(user)

def test_case_7_create_lastName_int_type(dao):
    """Test Case 7: Create a user with lastName field as integer"""
    user = {"firstName": "Jane", "lastName": 200, "email": "jane.doe@example.com"}
    with pytest.raises(WriteError):
        res = dao.create(user)

def test_case_8_create_email_float_type(dao):
    """Test Case 8: Create a user with email field as float"""
    user = {"firstName": "Jane", "lastName": "Doe", "email": 2.231}
    with pytest.raises(WriteError):
        res = dao.create(user)

def test_case_9_create_email_duplicate(dao):
    """Test Case 9: Create a user with duplicate email"""
    user1 = {"firstName": "Jane", "lastName": "Doe", "email": "jane.doe@example.com"}
    dao.create(user1)
    user2 = {"firstName": "John", "lastName": "Doe", "email": "jane.doe@example.com"}
    with pytest.raises(WriteError):
        res = dao.create(user2)

def test_case_10_create_valid_with_valid_task_field(dao):
    """Test Case 10: Create a user with valid task field"""
    user = {"firstName": "Jane", "lastName": "Doe", "email": "jane.doe@example.com", "tasks": [ObjectId(), ObjectId()]}
    res = dao.create(user)
    assert res is not None
    assert res.get("_id") is not None
    assert res.get("firstName") == user["firstName"]
    assert res.get("lastName") == user["lastName"]
    assert res.get("email") == user["email"]
    assert res.get("tasks") is not None

def test_case_11_create_valid_with_empty_array_task_field(dao):
    """Test Case 11: Create a user with empty array task field"""
    user = {"firstName": "Jane", "lastName": "Doe", "email": "jane.doe@example.com", "tasks": []}
    res = dao.create(user)
    assert res is not None
    assert res.get("_id") is not None
    assert res.get("firstName") == user["firstName"]
    assert res.get("lastName") == user["lastName"]
    assert res.get("email") == user["email"]
    assert res.get("tasks") == []

def test_case_12_create_valid_with_invalid_array_task_field(dao):
    """Test Case 12: Create a user with invalid array task field"""
    user = {"firstName": "Jane", "lastName": "Doe", "email": "jane.doe@example.com", "tasks": [True, "str", 213, None]}
    with pytest.raises(WriteError):
        res = dao.create(user)

def test_case_13_create_valid_with_bool_task_field(dao):
    """Test Case 13: Create a user with bool task field"""
    user = {"firstName": "Jane", "lastName": "Doe", "email": "jane.doe@example.com", "tasks": True}
    with pytest.raises(WriteError):
        res = dao.create(user)



