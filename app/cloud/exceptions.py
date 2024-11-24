class BaseCloudException(Exception):
    pass


class InvalidApiKey(BaseCloudException):
    pass


class NotFound(BaseCloudException):
    pass


class InternalError(BaseCloudException):
    pass


class ClientError(BaseCloudException):
    pass
