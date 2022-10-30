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

__author__ = 'Artic'
__version__ = '1.0.0'
__description__ = 'A simple API wrapper for Uptobox.'

import asyncio, json
from warnings import warn

import aiohttp

from Uptobox.Error import (
    LoginError,
    Logout,
    AsyncEvent,
    NeedPremium,
    PointsError,
    ConversionError
)
from Uptobox.Types import (
    User,
    File
)
from Uptobox.Gateway import (
    Route,
    StatusCode
)
from Uptobox.Core import (
    close,
    openURL
)

class Client:
    def __init__(
        self,
        token: str = None,
        ssl_download: bool = False,
        direct_download: bool = False,
        security_lock: bool = False
    ) -> None:
        self.token: str = token
        self.headers: dict[str: str] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(
            headers=self.headers
        )
        self.user: User = User(
            token=self.token,
            session=self.session
        )
        self.events: list = []
        self.force_https: int = 1 if ssl_download else 0
        self.direct_download: int = 1 if direct_download else 0
        self.security_lock: int = 1 if security_lock else 0
        if self.token is None:
            close(self.session)
            raise LoginError("The token is missing .")
        pass

    def fetchFile(
        self,
        code: str = None
    ) -> File:
        return File(
            fcode=code,
            session=self.session
        )
    
    def listen(self):
        def decorator(func):
            if asyncio.iscoroutinefunction(func):
                close(self.session)
                raise AsyncEvent(f'Unable to execute an asynchronous function. ({func.__name__})')
            self.events.append(func.__name__)
            self.__setattr__(func.__name__, func)
            return func
        return decorator
    
    def convert(
        self,
        points: int = None
    ) -> None:
        if points is None:
            close(self.session)
            raise SyntaxError("Missing the \"points\" argument.")
        if points > self.user.points:
            close(self.session)
            raise PointsError(f"You only have {self.user.points} points.")
        data = {
            "token": self.token,
            "points": points
        }
        response: dict = openURL(self.session.post, "/user/requestPremium", data)
        if response["statusCode"] == StatusCode.MISSING_TOKEN and self.token:
            warn("The function \"convert()\" is not available at the moment.")
        if response["statusCode"] == StatusCode.UNSUPPORTED_CONVERSION:
            close(self.session)
            raise ConversionError(response["message"])
        return

    def login(
        self
    ) -> None:
        async def login_runner() -> None:
            response: dict = json.loads(await (await self.session.get(str(Route(f"/user/me?token={self.token}")))).read())
            if response["statusCode"] == StatusCode.INVALID_TOKEN:
                close(self.session)
                raise LoginError(response["message"])
            if self.force_https == 1:
                ssl_data = {
                    "token": self.token,
                    "ssl": self.force_https
                }
                response_ssl: dict = json.loads(await (await self.session.patch(str(Route("/user/settings")), data=ssl_data)).read())
                if response_ssl["statusCode"] == StatusCode.MISSING_TOKEN and self.token:
                    close(self.session)
                    raise NeedPremium("This is a premium feature. Your account should be premium to request this endpoint.")
                if response_ssl["statusCode"] == StatusCode.INVALID_PARAMETER:
                    close(self.session)
                    raise SyntaxError("Expect a bool.")
            if self.direct_download == 1:
                ddl_data = {
                    "token": self.token,
                    "directDownload": self.direct_download
                }
                response_ddl: dict = json.loads(await (await self.session.patch(str(Route("/user/settings")), data=ddl_data)).read())
                if response_ssl["statusCode"] == StatusCode.MISSING_TOKEN and self.token:
                    close(self.session)
                    raise NeedPremium("This is a premium feature. Your account should be premium to request this endpoint.")
                if response_ddl["statusCode"] == StatusCode.INVALID_PARAMETER:
                    close(self.session)
                    raise SyntaxError("Expect a bool.")
            if self.security_lock == 1:
                slck_data = {
                    "token": self.token,
                    "securityLock": self.security_lock
                }
                response_slck: dict = json.loads(await (await self.session.patch(str(Route("/user/securityLock")), data=slck_data)).read())
                if response_slck["statusCode"] == StatusCode.MISSING_TOKEN and self.token:
                    close(self.session)
                    raise NeedPremium("This is a premium feature. Your account should be premium to request this endpoint.")
                if response_slck["statusCode"] == StatusCode.INVALID_PARAMETER:
                    close(self.session)
                    raise SyntaxError("Expect a bool.")
            return
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(login_runner())
            for event in self.events:
                if event == "on_connect":
                    try:
                        self.__getattribute__(event)()
                    except AttributeError:
                        pass
            loop.run_forever()
        except KeyboardInterrupt:
            loop.stop()
            loop.run_forever()
            loop.run_until_complete(self.session.close())
            raise Logout("Logged out.")
    
    def logout(
        self
    ) -> None:
        close(self.session)
        return
