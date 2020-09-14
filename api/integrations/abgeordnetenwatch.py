from django.conf import settings

# Each 3rd Party integration must implement a version of this 
# class returning the data in the format expected by the main API
class ParliamentAPI:

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def politicians(self, **kwargs):
        pass

    def polls(self, **kwargs):
        pass

    def votes(self, **kwargs):
        if kwargs['poll']:
            pass
        pass

