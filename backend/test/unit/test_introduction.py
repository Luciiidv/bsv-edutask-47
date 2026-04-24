from src.controllers.usercontroller import UserController

def hasAttribute(obj: dict, attribute: str):
    """
    Checks if the given object has the specified attribute.
    
    attributes:
        obj (dict): The object to check.
        attribute (str): The key which potenially occurs in the object dict.

    returns:
        bool: True if the object has the attribute, False otherwise.
    """
    return (attribute in obj)

class ValidationHelper:
    def __init__(self, usercontroller: UserController):
        self.usercontroller = usercontroller

    def validateAge(self, userid: str):
        """
        Validate the age of a given user
        
        attributes:
            userid (str): string id of the user object.
            
        returns:
            "invalid" -- if the age is below 0 or above 120
            "valid" -- if the user is of age
            "underaged" -- otherwise
        """
        user = self.usercontroller.get(id=userid)

        if user['age'] < 0 or user['age'] > 120:
            return "invalid"
        if user['age'] > 18:
            return "valid"
        return "underaged"

