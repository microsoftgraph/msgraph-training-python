# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <UserAuthConfigSnippet>
import sys
import json
from azure.identity import DeviceCodeCredential, ClientSecretCredential
from msgraph.core import GraphClient

# Assign variables to the module so they stay set
this = sys.modules[__name__]

def initialize_graph_for_user_auth(config):
    this.settings = config
    client_id = this.settings['clientId']
    tenant_id = this.settings['authTenant']
    graph_scopes = this.settings['graphUserScopes'].split(' ')

    this.device_code_credential = DeviceCodeCredential(client_id, tenant_id = tenant_id)
    this.user_client = GraphClient(credential=this.device_code_credential, scopes=graph_scopes)
# </UserAuthConfigSnippet>

# <GetUserTokenSnippet>
def get_user_token():
    graph_scopes = this.settings['graphUserScopes']
    access_token = this.device_code_credential.get_token(graph_scopes)
    return access_token.token
# </GetUserTokenSnippet>

# <GetUserSnippet>
def get_user():
    endpoint = '/me'
    # Only request specific properties
    select = 'displayName,mail,userPrincipalName'
    request_url = f'{endpoint}?$select={select}'

    user_response = this.user_client.get(request_url)
    return user_response.json()
# </GetUserSnippet>

# <GetInboxSnippet>
def get_inbox():
    endpoint = '/me/mailFolders/inbox/messages'
    # Only request specific properties
    select = 'from,isRead,receivedDateTime,subject'
    # Get at most 25 results
    top = 25
    # Sort by received time, newest first
    order_by = 'receivedDateTime DESC'
    request_url = f'{endpoint}?$select={select}&$top={top}&$orderBy={order_by}'

    inbox_response = this.user_client.get(request_url)
    return inbox_response.json()
# </GetInboxSnippet>

# <SendMailSnippet>
def send_mail(subject: str, body: str, recipient: str):
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

    this.user_client.post(request_url,
                          data=json.dumps(request_body),
                          headers={'Content-Type': 'application/json'})
# </SendMailSnippet>

# <AppOnyAuthConfigSnippet>
def ensure_graph_for_app_only_auth():
    if not hasattr(this, 'client_credential'):
        client_id = this.settings['clientId']
        tenant_id = this.settings['tenantId']
        client_secret = this.settings['clientSecret']

        this.client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)

    if not hasattr(this, 'app_client'):
        this.app_client = GraphClient(credential=this.client_credential,
                                      scopes=['https://graph.microsoft.com/.default'])
# </AppOnyAuthConfigSnippet>

# <GetUsersSnippet>
def get_users():
    ensure_graph_for_app_only_auth()

    endpoint = '/users'
    # Only request specific properties
    select = 'displayName,id,mail'
    # Get at most 25 results
    top = 25
    # Sort by display name
    order_by = 'displayName'
    request_url = f'{endpoint}?$select={select}&$top={top}&$orderBy={order_by}'

    users_response = this.app_client.get(request_url)
    return users_response.json()
# </GetUsersSnippet>

# <MakeGraphCallSnippet>
def make_graph_call():
    # INSERT YOUR CODE HERE
    # Note: if using app_client, be sure to call
    # ensure_graph_for_app_only_auth before using it
    # ensure_graph_for_app_only_auth()
    return
# </MakeGraphCallSnippet>
