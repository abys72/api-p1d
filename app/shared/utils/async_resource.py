from flask import request
from flask_restful import Resource


class AsyncResource(Resource):

    async def dispatch_request(self, *args, **kwargs):
        method = getattr(self, request.method.lower(), None)
        if method is None:
            return super().dispatch_request(*args, **kwargs)

        return await method(*args, **kwargs)
