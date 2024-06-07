from api.mail_api import MailAPI


class GetMessages(MailAPI):
    def api_call(self):
        response = self.make_request("GET", "api/v2/messages")
        return response
