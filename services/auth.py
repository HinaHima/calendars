from calendars.models import Company

class Auth:
    @staticmethod
    def client(auth_header_value: str) -> int:
        try:
            if (auth_header_value == None): raise AuthException("No auth header value.")
            #        
            auth_header_value = auth_header_value.split(' ')
            if (len(auth_header_value) != 2): raise AuthException("Wrong auth header value.")
            #
            if (auth_header_value[0] != 'Client'): raise AuthException("Wrong auth type.")
            #            
            company = Company.query.filter_by(cid=auth_header_value[1]).first()
            if (company == None): raise AuthException("No company found.")
            #
            return company.id
        except AuthException as e:
            raise AuthException(str(e))
        except Exception as e:
            raise AuthException("Unhandled exception. Original:" + str(e))

class AuthException(Exception):
    pass
