# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# pylint: disable=invalid-overridden-method,useless-super-delegation

# <AsyncAuthSnippet>
from azure.identity import DeviceCodeCredential

# This class is an async wrapper around the DeviceCodeCredential
# class from azure.identity. Once azure.identity provides an async version
# of DeviceCodeCredential this will no longer be necessary
class AsyncDeviceCodeCredential(DeviceCodeCredential):
    async def get_token(self, *scopes, **kwargs):
        return super().get_token(*scopes, **kwargs)

    async def __aenter__(self):
        return

    async def __aexit__(self, exc_type, exc_value, traceback):
        return

    async def close(self):
        return
# </AsyncAuthSnippet>
