# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2022-present Artic

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from .Constants import BASE

class Route:
    def __init__(
        self,
        url: str = None,
        _base: str = None
    ) -> None:
        self.base = _base or BASE
        self.url: str = url
        if self.url is None:
            raise SyntaxError("Missing the \"url\" argument.")
        pass

    def __str__(
        self
    ) -> str:
        return f"{self.base}{self.url}"

class StatusCode:
    SUCCESS: int = 0
    AN_ERROR_OCCURED: int = 1
    INVALID_CREDENTIALS: int = 2
    EXPECT_AT_LEAST_ONE_VALUE: int = 3
    WRONG_FORMAT: int = 4
    NEED_PREMIUM_ACCOUNT: int = 5
    MISSING_PARAMETER: int = 6
    INVALID_PARAMETER: int = 7
    INSUFFICIENT_CREDIT: int = 8
    UNSUPPORTED_FIELD: int = 9
    UNPROCESSABLE_REQUEST: int = 10
    TOO_MUCH_FAIL_ATTEMPT: int = 11
    MISSING_TOKEN: int = 12
    INVALID_TOKEN: int = 13
    VOUCHER_IS_ALREADY_USED: int = 14
    UNSUPPORTED_CONVERSION: int = 15
    WAITING_NEEDED: int = 16
    PASSWORD_REQUIRED: int = 17
    DATA_UNCHANGED: int = 18
    INVALID_VOUCHER: int = 19
    NOT_AVAILABLE: int = 20
    PERMISSION_DENIED: int = 21
    PERMISSION_GRANTED: int = 22
    REQUEST_HAS_FAILED: int = 23
    REQUEST_HAS_SUCCEEDED_PARTIALLY: int = 24
    SERVER_TEMPRORARILY_UNAVAILABLE: int = 25
    INVALID_PASSWORD: int = 26
    REQUIRED_AN_AUTHENTICATED_USER: int = 27
    FILE_NOT_FOUND: int = 28
    YOU_HAVE_REACHED_THE_STREAMING_LIMIT_FOR_TODAY: int = 29
    FOLDER_NOT_FOUND: int = 30
    EXPECT_A_NUMERIC_VALUE: int = 31
    LIMIT_REACHED: int = 32
    INVALID_DATA: int = 34
    FILE_WILL_BE_AVAILABLE_SOON: int = 35
    NO_SUBSCRIPTION_FOUND: int = 36
    STREAM_IS_NOT_AVAILABLE: int = 37
    FILESIZE_NEED_PREMIUM: int = 38
    YOU_NEED_TO_WAIT_BEFORE_REQUESTING_A_NEW_DOWNLOAD_LINK: int = 39
