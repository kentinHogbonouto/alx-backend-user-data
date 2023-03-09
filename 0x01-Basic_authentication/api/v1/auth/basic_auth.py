#!/usr/bin/env python3
""" Class to manage Authentication """
from flask import request
from typing import List, TypeVar, Tuple
from api.v1.auth.auth import Auth
from api.v1.views.users import User
import re
import base64


class BasicAuth(Auth):
    """ Class to manage Basic Authentication """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extract base64 authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        # Checking if the authorization_header starts with the word basic
        if re.match(r'Basic .*', authorization_header) is None:
            return None
        # Returning the value after basic
        return (re.search(r'(?<=Basic ).*', authorization_header).group(0))

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Decodes a base64 header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_auth_header = base64.b64decode(base64_authorization_header)
            return decoded_auth_header.decode('utf-8')
        # except base64.binascii.Error:
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> Tuple[str, str]:
        """
        Extract username and password from decoded auth header
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if re.search(':', decoded_base64_authorization_header) is None:
            return (None, None)

        # Password that includes a : is not supported

        # email = re.match('.*(?=:)',
        #                  decoded_base64_authorization_header).group(0)
        # password = re.search('(?<=:).*',
        #                      decoded_base64_authorization_header).group(0)

        # Password that includes a : is supported

        credentials = decoded_base64_authorization_header.split(':')
        email = credentials.pop(0)
        password = ":".join(credentials)
        return(email, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Fetch user instance based on credentials """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        user = User.search({'email': user_email})
        if len(user) == 0:
            return None
        else:
            if user[0].is_valid_password(user_pwd) is False:
                return None
            return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user """
        auth = self.authorization_header(request)
        extracted_auth = self.extract_base64_authorization_header(auth)
        decoded_auth = self.decode_base64_authorization_header(extracted_auth)
        user_credentials = self.extract_user_credentials(decoded_auth)
        user = self.user_object_from_credentials(user_credentials[0],
                                                 user_credentials[1])
        return user
