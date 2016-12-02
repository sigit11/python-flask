from Sparse.classes.common.auth import auth
from Sparse.classes.common.dbconnector import dbconnector

import MySQLdb
import MySQLdb.cursors
import bcrypt
import string
import datetime

class users(object):
    """description of class"""

    def __init__(self, authObj, redisObj):
        self.authObj = authObj
        self.redisObj = redisObj

    def user_login(self, configDB, userAuthInfo = {}):
        dbObj = dbconnector()
        condition = "WHERE email = '" +userAuthInfo['email']+ "'"
        db1start = datetime.datetime.now()
        userData = dbObj.db_select_columns(configDB, ['email', 'password', 'salt', 'account_id', 'status'], 'account', condition, fetch = 'one')
        print((datetime.datetime.now() - db1start).microseconds)
        if userData['status'] == None or userData['status'] == 'error':
            return {'statusCode' : 401, 'status': 'Email or Password is not match 1'}
        else:
            if userData['data'][4] == 0 or userData['status'] == 'error':
                return {'statusCode' : 401, 'status': 'User does not exist or deactivated. Please contact support for further information.'}
            else:
                
                encodedPassword = str(userAuthInfo['password']).encode('utf-8')
                db1start = datetime.datetime.now()
                hashed = bcrypt.checkpw(encodedPassword, userData['data'][1].encode('utf-8'))
                print((datetime.datetime.now() - db1start).microseconds)
                if hashed is False:
                    return {'statusCode' : 401, 'status': 'Email or Password is not match 2'}
                else:
                    payload = {
                        'userID' : userData['data'][3],
                        'email' : userAuthInfo['email']
                    }
                    db1start = datetime.datetime.now()
                    userToken = self.authObj.encode(payload)
                    print((datetime.datetime.now() - db1start).microseconds)
                    try:
                        db1start = datetime.datetime.now()
                        self.redisObj.set(userToken['token'], userData['data'][3])
                        print((datetime.datetime.now() - db1start).microseconds)
                    except:
                        return {'statusCode' : 500, 'status': 'Something happened on the server. Please contact support for further information.'}
                    return {'statusCode' : 200, 'status': 'Success', 'token':str(userToken['token'])}

    def user_logout(self, userAuthInfo = {}):
        try:
            tokenStatus = self.redisObj.get(userAuthInfo['token'])
            if tokenStatus == None:
                return {'statusCode' : 400, 'statusMessage' : 'Account is not login yet'}
            else:
                self.redisObj.delete(userAuthInfo['token'])
                return {'statusCode' : 200, 'statusMessage' : 'Successfully logout'}
        except:
            return {'statusCode' : 500, 'status': 'Something happened on the server. Please contact support for further information.'}

    def user_session(self, loginInfo):
        checkTokenStatus = self.redisServerObj.get(loginInfo['token'])
        if checkTokenStatus == None:
            return False
        else:
            return True


