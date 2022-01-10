from enum import Enum


class Method(str, Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"
    HEAD = "HEAD"
    OPTION = "OPTION"
    PATCH = "PATCH"
    TRACE = "TRACE"
