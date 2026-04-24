import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController

@pytest.mark.parametrize("users, email, expected, print_message", 
[
    # Testing if it returns a valid e-mail user when logging in succeed
    ([{'email': "test1@test.se"}], "test1@test.se", {'email': "test1@test.se"}, None),

    # Testing if it returns the first user if multiple users are associated to that e-mail address, should print “Error: more than one user found with mail {email}”
    ([{'email': "test1@test.se"}, {'email': "test1@test.se"}], "test1@test.se", {'email': "test1@test.se"}, 'Error: more than one user found with mail test1@test.se\n'),

    # Testing if returns “None” if no user is associated with that e-mail address.
    ([], "test255@test.se", None, None)
])
def test_get_user_by_email(users, email, expected, print_message, capsys):
    mocked_controller = mock.MagicMock()
    mocked_controller.find.return_value = users

    sut = UserController(mocked_controller)

    result = sut.get_user_by_email(email)
    captured = capsys.readouterr()

    assert result == expected
    assert captured.out == (print_message or "")

# Testing if ValueError raises if trying to use an invalid e-mail address, should be <local-part>@<domain>.<host>
def test_invalid_email_raises():
    mocked_controller = mock.MagicMock()
    mocked_controller.find.return_value = []

    sut = UserController(mocked_controller)
    # Act / Assert
    with pytest.raises(ValueError):
        sut.get_user_by_email("invalid-email")

# Testing if Exception raises in case any database operation fails
def test_exception_raises():
    mocked_controller = mock.MagicMock()
    mocked_controller.find.side_effect = Exception('Database error')

    sut = UserController(mocked_controller)
    # Act / Assert
    with pytest.raises(Exception):
        sut.get_user_by_email("test@test.se")
