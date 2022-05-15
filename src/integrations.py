from fastapi import HTTPException
import requests

class UserService:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
    
    def userContainsRole(self, jwttoken: str, roleName: str) -> bool:
        try:
            response = requests.get(self.endpoint + "userContainsRole", data={ "roleName": roleName }, headers={ "Authorization": jwttoken })
        except:
            raise HTTPException(408, "Cannot reach " + self.endpoint)
        hasAccess = response.json()
        return hasAccess
    
    def getUserId(self, jwttoken: str) -> str:
        try:
            response = requests.get(self.endpoint + "user/info", headers={ "Authorization": jwttoken })
        except:
            raise HTTPException(408, "Cannot reach " + self.endpoint)
        user = response.json()
        return user['username']