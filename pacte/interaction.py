# Copyright (c) 2017 App Annie Inc. All rights reserved.


class Interaction(object):
    """
    Builder for interaction dictionaries
    """

    def __init__(self, provider_state=None, description=None, request=None, response=None):
        self.provider_state = provider_state
        self.description = description
        self.request = request
        self.response = response

    def given(self, provider_state):
        self.provider_state = provider_state
        return self

    def upon_receiving(self, description):
        self.description = description
        return self

    def with_request(self, method, path, query=None, headers=None, body=None):
        self.request = {
            'method': method.upper(),
            'path': path.lower(),
        }

        if query is not None:
            self.request['query'] = query.lower()

        if headers is not None:
            self.request['headers'] = headers

        if body is not None:
            self.request['body'] = body

        return self

    def will_respond_with(self, status, headers=None, body=None):
        self.response = {
            'status': status
        }

        if headers is not None:
            self.response['headers'] = headers

        if body is not None:
            self.response['body'] = body

        return self

    def equals(self, interaction):
        return (
            interaction.request == self.request
            and interaction.response == self.response
        )

    def to_dict(self):
        return {
            'providerState': self.provider_state,
            'description': self.description,
            'request': self.request,
            'response': self.response
        }

    @classmethod
    def from_dict(cls, interaction):
        return cls(
            provider_state=interaction['providerState'],
            description=interaction['description'],
            request=interaction['request'],
            response=interaction['response'],
        )
