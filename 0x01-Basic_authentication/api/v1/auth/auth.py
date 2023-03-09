#!/usr/bin/env python3
""" Class to manage Authentication """
from flask import request
from typing import List, TypeVar
import re


class Auth():
    """ Class to manage Authentication """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks of authuntication is required
            Returns:
                True if authentication is required
                    (path is not found in excluded_paths)
                False if authentication is not required
                    (path is found in excluded_paths)
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        # # Making the method slash tolerent
        if path[-1] != '/':
            path = path + '/'

        #  Allowing * at the end of excluded paths
        for excluded_path in excluded_paths:
            if excluded_path[-1] == '*':
                excluded_path = excluded_path[:-1]
            match = re.match(excluded_path, path)
            if match is None:
                return True
            else:
                return False

    def authorization_header(self, request=None) -> str:
        """ Handles the authorization header """
        if request is None:
            return None
        auth = request.headers.get("Authorization")
        if auth is None:
            return None
        return auth

    def current_user(self, request=None) -> TypeVar('User'):
        """ Handles current user """
        return None
