# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# <AppAuthConfigSnippet>
from configparser import SectionProxy
from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.users_request_builder import UsersRequestBuilder

class Graph:
    settings: SectionProxy
    client_credential: ClientSecretCredential
    app_client: GraphServiceClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['tenantId']
        client_secret = self.settings['clientSecret']

        self.client_credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        self.app_client = GraphServiceClient(self.client_credential) # type: ignore
# </AppAuthConfigSnippet>

    # <GetAppOnlyTokenSnippet>
    async def get_app_only_token(self):
        graph_scope = 'https://graph.microsoft.com/.default'
        access_token = await self.client_credential.get_token(graph_scope)
        return access_token.token
    # </GetAppOnlyTokenSnippet>

    # <GetUsersSnippet>
    async def get_users(self):
        query_params = UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
            # Only request specific properties
            select = ['displayName', 'id', 'mail'],
            # Get at most 25 results
            top = 25,
            # Sort by display name
            orderby= ['displayName']
        )
        request_config = UsersRequestBuilder.UsersRequestBuilderGetRequestConfiguration(
            query_parameters=query_params
        )

        users = await self.app_client.users.get(request_configuration=request_config)
        return users
    # </GetUsersSnippet>

    # <MakeGraphCallSnippet>
    async def make_graph_call(self):
        # INSERT YOUR CODE HERE
        return
    # </MakeGraphCallSnippet>
