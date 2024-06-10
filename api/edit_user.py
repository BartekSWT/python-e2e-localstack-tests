from api.base_api import BaseAPI
from api.data.edit import EditUserDto

class EditUser(BaseAPI):
    def api_call(self, username: str, user_data: EditUserDto, token: str):
        user_dict = user_data.to_dict()
        headers = {"Authorization": f"Bearer {token}"}
        response = self.make_request("PUT", f"users/{username}", json=user_dict, headers=headers)
        return response
