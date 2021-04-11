import requests


class ServiceHandler:
    endpoint = ""
    payload = {}

    def get(self, **kwargs):
        req = requests.get(self.endpoint, params=self.payload)
        return req.json()


class ClassServiceHandler(ServiceHandler):
    endpoint = "http://localhost:12300/api/class"

    def __init__(self, **kwargs):
        classcode = kwargs.get('classcode')
        self.endpoint = f"{self.endpoint}/{classcode}"

if __name__ == "__main__":
    csh = ClassServiceHandler(classcode="21E1_1")
    print(csh.get())
