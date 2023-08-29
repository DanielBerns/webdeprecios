import os
from pathlib import Path
import sys
from typing import Optional, List, Dict
import json

import requests

# https://firebase.google.com/docs/reference/rest/auth

sign_in_with_custom_token_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken"

id_token_url = "https://securetoken.googleapis.com/v1/token"

sign_up_with_email_and_password_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"

sign_in_with_email_and_password_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

sign_in_anonymously_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"

sign_in_with_OAuth_credential_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp"

fetch_providers_for_email_url = "https://identitytoolkit.googleapis.com/v1/accounts:createAuthUri"

send_password_reset_email_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"

verify_password_reset_code_url = "https://identitytoolkit.googleapis.com/v1/accounts:resetPassword"

confirm_password_reset_url = "https://identitytoolkit.googleapis.com/v1/accounts:resetPassword"

change_email_url = "https://identitytoolkit.googleapis.com/v1/accounts:update"

change_password_url = "https://identitytoolkit.googleapis.com/v1/accounts:update"

update_profile_url = "https://identitytoolkit.googleapis.com/v1/accounts:update"

get_user_data_url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup"

link_with_email_and_password_url = "https://identitytoolkit.googleapis.com/v1/accounts:update"

link_with_OAuth_credential_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp"

unlink_provider_url = "https://identitytoolkit.googleapis.com/v1/accounts:update"

send_email_verification_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"

confirm_email_verification_code_url = "https://identitytoolkit.googleapis.com/v1/accounts:update"

delete_account_url = "https://identitytoolkit.googleapis.com/v1/accounts:delete"

# https://medium.com/better-programming/user-management-with-firebase-and-python-749a7a87b2b6


class FirebaseAPI:
    def __init__(self) -> None:
        self._api_key = os.environ.get("FIREBASE_WEB_API_KEY")
        
    @property
    def api_key(self) -> str:
        return self._api_key
    
    def post_request(self, 
                     url: str, 
                     payload: str, 
                     headers=None) -> Dict:
        r = requests.post(url,
                          params={"key": self.api_key},
                          data=payload,
                          headers=headers)
        return r.json()

    def sign_in_with_custom_token(self, 
                                  custom_token: str) -> Dict:
        payload = json.dumps({
            "token": custom_token,
            "returnSecureToken": True
            })
        return self.post_request(sign_in_with_custom_token_url, payload)
    
    def id_token(self, 
                 refresh_token: str) -> Dict:
        payload = json.dumps({
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
            })
        return self.post_request(id_token_url, payload)

    def sign_up_with_email_and_password(self, 
                                        email: str, 
                                        password: str) -> Dict:
        payload = json.dumps({
            "email": email,
            "password": password,
            "returnSecureToken": True
            })
        return self.post_request(sign_up_with_email_and_password_url, payload)
    
    def sign_in_with_email_and_password(self, 
                                        email: str, 
                                        password: str) -> Dict:
        payload = json.dumps({
            "email": email,
            "password": password,
            "returnSecureToken": True
            })
        return self.post_request(sign_in_with_email_and_password_url, payload)
    
    def sign_in_anonymously(self) -> Dict:
        payload = json.dumps({
            "returnSecureToken": True
            })
        return self.post_request(sign_in_anonymously_url, payload)

    def sign_in_with_OAuth_credential(self, 
                                      request_uri: str, 
                                      post_body: str, 
                                      return_idp_credential: bool) -> Dict:
        payload = json.dumps({
            "requestUri": request_uri,
            "postBody": post_body,
            "returnIdpCredential": return_idp_credential,
            "returnSecureToken": True
            })
        return self.post_request(sign_in_with_OAuth_credential_url, payload)
    
    def fetch_providers_for_email(self, 
                                  identifier: str, 
                                  continue_uri: str) -> Dict:
        payload = json.dumps({
            "identifier": identifier,
            "continueUri": continue_uri
            })
        return self.post_request(sign_in_with_OAuth_credential_url, payload)
    
    def send_password_reset_email(self, 
                                  email: str, 
                                  locale: Optional[str]) -> Dict:
        payload = json.dumps({
            "requestType": "PASSWORD_RESET",
            "email": email
            })
        headers = {"X-Firebase-Locale": locale} if locale else None
        return self.post_request(send_password_reset_email_url, payload, headers=headers)

    def verify_password_reset_code(self, 
                                   oobCode: str) -> Dict:
        payload = json.dumps({
            "oobCode": oobCode
        })
        return self.post_request(verify_password_reset_code_url, payload)
    
    def confirm_password_reset_code(self, 
                                    oobCode: str, 
                                    new_password: str) -> Dict:
        payload = json.dumps({
            "oobCode": oobCode,
            "newPassword": new_password
        })
        return self.post_request(confirm_password_reset_code_url, payload)
    
    def change_email(self, 
                     id_token: str, 
                     email: str, 
                     locale: Optional[str]=None) -> Dict:
        payload = json.dumps({
            "oobCode": oobCode,
            "email": email
        })        
        headers = {"X-Firebase-Locale": locale} if locale else None
        return self.post_request(change_email_url, payload, headers=headers)
    
    def change_password(self, 
                        id_token: str, 
                        new_password: str) -> Dict:
        payload = json.dumps({
            "idToken": id_token,
            "newPassword": new_password
        })        
        return self.post_request(change_email_url, payload)

    def update_profile(self, 
                       id_token: str, 
                       display_name: Optional[str]=None, 
                       photo_url: Optional[str]=None, 
                       delete_attribute: Optional[List[str]]=None) -> Dict:
        data = {"idToken": id_token}
        if display_name:
            data["displayName"] = display_name
        if photo_url:
            data["photoUrl"] = photo_url
        if delete_attribute:
            data["deleteAttribute"] = delete_attribute
        payload = json.dumps(data)
        return self.post_request(update_profile_url, payload)
            
    def get_user_data(self, 
                      id_token: str) -> Dict:
        payload = json.dumps({"idToken": id_token})
        return self.post_request(get_user_data_url, payload)
    
    def link_with_email_and_password(self, 
                                     id_token: str, 
                                     email: str, 
                                     password: str) -> Dict:
        payload = json.dumps({"idToken": id_token, 
                              "email": email, 
                              "password": password, 
                              "returnSecureToken": True})
        return self.post_request(link_with_email_and_password_url, payload)
    
    def link_with_OAuth_credential(self, 
                                   id_token: str, 
                                   request_uri: str, 
                                   post_body: str, 
                                   return_idp_credential: bool) -> Dict:
        payload = json.dumps({"idToken": id_token,
                              "requestUri": request_uri,
                              "postBody": post_body,
                              "returnIdpCredential": return_idp_credential,
                              "returnSecureToken": True})
        return self.post_request(link_with_OAuth_credential_url, payload)
    
    def unlink_provider(self, 
                        id_token: str, 
                        delete_provider: List[str]) -> Dict:
        payload = json.dumps({"idToken": id_token,
                              "deleteProvider": deleteProvider})
        return self.post_request(unlink_provider_url, payload)        
        
    def send_email_verification(self, 
                                id_token: str, 
                                locale: Optional[str]) -> Dict:
        payload = json.dumps({"idToken": id_token, "requestType": "VERIFY_EMAIL"})
        headers = {"X-Firebase-Locale": locale} if locale else None
        return self.post_request(send_email_verification_url, payload, headers=headers)

    def confirm_email_verification_code(self, 
                                        oob_code: str) -> Dict:
        payload = json.dumps({"oobCode": oob_code})
        return self.post_request(confirm_email_verification_code_url, payload)

    def delete_account(self, id_token: str) -> Dict:
        payload = json.dumps({"idToken": id_token})
        return self.post_request(delete_acount_url, payload)        


