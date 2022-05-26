# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <UserAuthConfigSnippet>
import json
from configparser import SectionProxy
from types import NoneType
from azure.identity import DeviceCodeCredential, ClientSecretCredential
from msgraph.core import GraphClient

class Graph:
    settings: SectionProxy
    device_code_credential: DeviceCodeCredential
    user_client: GraphClient
    client_credential: ClientSecretCredential
    app_client: GraphClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['authTenant']
        graph_scopes = self.settings['graphUserScopes'].split(' ')

        self.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
        self.user_client = GraphClient(credential=self.device_code_credential, scopes=graph_scopes)
# </UserAuthConfigSnippet>

    # <GetUserTokenSnippet>
    def get_user_token(self):
        graph_scopes = self.settings['graphUserScopes']
        access_token = self.device_code_credential.get_token(graph_scopes)
        return access_token.token
    # </GetUserTokenSnippet>

    # <GetUserSnippet>
    def get_user(self):
        endpoint = '/me'
        # Only request specific properties
        select = 'displayName,mail,userPrincipalName'
        request_url = f'{endpoint}?$select={select}'

        user_response = self.user_client.get(request_url)
        return user_response.json()
    # </GetUserSnippet>

    # <GetInboxSnippet>
    def get_inbox(self):
        endpoint = '/me/mailFolders/inbox/messages'
        # Only request specific properties
        select = 'from,isRead,receivedDateTime,subject'
        # Get at most 25 results
        top = 25
        # Sort by received time, newest first
        order_by = 'receivedDateTime DESC'
        request_url = f'{endpoint}?$select={select}&$top={top}&$orderBy={order_by}'

        inbox_response = self.user_client.get(request_url)
        return inbox_response.json()
    # </GetInboxSnippet>

    # <SendMailSnippet>
    def send_mail(self, subject: str, body: str, recipient: str):
        request_body = {
            'message': {
                'subject': subject,
                'body': {
                    'contentType': 'text',
                    'content': body
                },
                'toRecipients': [
                    {
                        'emailAddress': {
                            'address': recipient
                        }
                    }
                ]
            }
        }

        request_url = '/me/sendmail'

        self.user_client.post(request_url,
                              data=json.dumps(request_body),
                              headers={'Content-Type': 'application/json'})
    # </SendMailSnippet>

    # <AppOnyAuthConfigSnippet>
    def ensure_graph_for_app_only_auth(self):
        if not hasattr(self, 'client_credential'):
            client_id = self.settings['clientId']
            tenant_id = self.settings['tenantId']
            client_secret = self.settings['clientSecret']

            self.client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)

        if not hasattr(self, 'app_client'):
            self.app_client = GraphClient(credential=self.client_credential,
                                          scopes=['https://graph.microsoft.com/.default'])
    # </AppOnyAuthConfigSnippet>

    # <GetUsersSnippet>
    def get_users(self):
        self.ensure_graph_for_app_only_auth()

        endpoint = '/users'
        # Only request specific properties
        select = 'displayName,id,mail'
        # Get at most 25 results
        top = 25
        # Sort by display name
        order_by = 'displayName'
        request_url = f'{endpoint}?$select={select}&$top={top}&$orderBy={order_by}'

        users_response = self.app_client.get(request_url)
        return users_response.json()
    # </GetUsersSnippet>

    # <MakeGraphCallSnippet>
    def make_graph_call(self):
        # INSERT YOUR CODE HERE
        # Note: if using app_client, be sure to call
        # ensure_graph_for_app_only_auth before using it
        # self.ensure_graph_for_app_only_auth()
        return
    # </MakeGraphCallSnippet>
