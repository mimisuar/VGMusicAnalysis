import requests, json

class IGDBWrapperException(Exception):
    def __str__(self):
        return "IGDBWrapperException: " + Exception.__str__(self)

auth_url = "https://id.twitch.tv/oauth2/token?client_id={0}&client_secret={1}&grant_type=client_credentials"

class IGDBWrapper:
    def __init__(self, client_id, auth_token):
        self.client_id = client_id
        self.auth_token = auth_token
        self.access_token = ""

    def auth(self):
        """ 
        Authenticate with IGDB.
        """

        request = requests.post(auth_url.format(self.client_id, self.auth_token))

        if request.status_code == requests.codes.ok:
            auth_res = json.loads(request.text)
            self.access_token = auth_res["access_token"]
        else:
            request.raise_for_status()

    def 