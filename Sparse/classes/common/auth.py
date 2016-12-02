import datetime
import jwt

class auth(object):
    """description of class"""

    def __init__(self, secretKey = '', algorithm = ''):
        self.secretKey = secretKey
        self.algorithm = algorithm

    def encode(self, payload = {}):
        try:
            payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=23)
            payload['iat'] = datetime.datetime.utcnow()
            print(self.secretKey)
            encodedToken = jwt.encode(payload, self.secretKey, algorithm=self.algorithm)
            print(encodedToken)
            return {'token':encodedToken}
        except:
            return {'status':'error'}

    def decode(self, token):
        try:
            decodedToken = jwt.decode(token, self.secretKey, verify = True, algorithms = self.algorithm)
            return decodedToken
        except:
            return False

    def verify(self, token):
        try:
            decodedToken = jwt.decode(token, self.secretKey, verify = True, algorithms = self.algorithm)
            return decodedToken
        except:
            return False