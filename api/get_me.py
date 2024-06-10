from api.base_api import BaseAPI
from api.data.user_details import UserDetails

class GetMe(BaseAPI):
    def api_call(self, token):
        response = self.make_request(
            "GET", "users/me", headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        assert response.status_code == 200, "Failed to fetch user details"
        user_data = response.json()
        user_details = UserDetails(**user_data)
        return user_details
