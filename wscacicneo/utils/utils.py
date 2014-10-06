import requests
import json
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.orgao import OrgaoBase


class Utils:

    def __init__(self):
        pass

    def to_url(*args):
        return '/'.join(list(args))

    def verifica_email_institucional(email):
    	if("gov.br" in email):
    		return True
    	else:
    		return False

