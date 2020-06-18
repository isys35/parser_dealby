from requests.exceptions import SSLError


class ErrorRequest(SSLError):
    pass