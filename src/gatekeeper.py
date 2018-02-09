#!/usr/bin/env python3

"""
Gatekeeper module to handle authentification / autorizathion for QI Serverless ecosystem using AWS Cognito.

"""

from sys import exit

import IPython
from warrant import Cognito
from warrant.aws_srp import AWSSRP
from warrant.exceptions import ForceChangePasswordException


class Identity(Cognito):

    def __init__(self, user_pool, client_id, username, password, new_password=None):
        """
        Identity initialization
        """
        self._user_pool = user_pool
        self._client_id = client_id
        super().__init__(user_pool, client_id, username=username)
        if new_password:
            self.forced_password_change(password, new_password)
        self.autenticate(password)

    def autenticate(self, password):
        try:
            super().authenticate(password)
        except ForceChangePasswordException:
            print("User must change their password before authenticate. Call with new_password argument.")

    def forced_password_change(self, oldpassword, newpassword):
        """
        First password reset helper to complete user sign-up
        """
        aws = AWSSRP(self.username, oldpassword, self._user_pool_id, self._client_id)
        return aws.set_new_password_challenge(newpassword)


def main():
    """
    The main function.
    """
    IPython.embed()

if __name__ == "__main__":
    exit(main())
