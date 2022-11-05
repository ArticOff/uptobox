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

import asyncio, json, sys, time
from typing import (
    NoReturn
)

import aiohttp

from .Error import (
    ClientError,
    LoginError,
    Logout,
    AsyncEvent
)
from .Types import (
    User,
    File
)
from .Gateway import (
    Route,
    StatusCode
)
from .Core import (
    close,
    openURL,
    runEvent
)
from .Constants import (
    EXIT_FAILURE,
    EXIT_SUCCESS
)

class Client:
    def __init__(
        self,
        token: str = None,
        ssl_download: bool = False,
        direct_download: bool = False,
        security_lock: bool = False,
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

    def __content_type__(
        self,
        new: str = None
    ) -> None:
        if new is None:
            raise SyntaxError("Missing hte \"new\" argument.")
        self.content_type = new
        return

    def __event__(
        self,
        name: str = None,
        data: list = None
    ) -> None:
        runEvent(
            self=self,
            name=name,
            data=data
        )
        return
    
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
            self.__event__(
                name="on_error",
                data=[ClientError.PointsError(f"You only have {self.user.points} points.")]
            )
            return
        data: dict = {
            "token": self.token,
            "points": points
        }
        response: dict = openURL(self.session.post, "/user/requestPremium", data)
        if response["statusCode"] == StatusCode.MISSING_TOKEN and self.token:
            self.__event__(
                name="on_error",
                data=[ClientError.Warning("The function \"convert()\" is not available at the moment.")]
            )
            return
        if response["statusCode"] == StatusCode.UNSUPPORTED_CONVERSION:
            self.__event__(
                name="on_error",
                data=[response["message"]]
            )
            return
        return

    def upload(
        self,
        file: str = None
    ) -> str:
        if file is None:
            raise SyntaxError("Missing the \"file\" argument.")
        data: dict = {
            "token": self.token
        }
        url: str = openURL(self.session.get, "/upload", data)["data"]["uploadLink"]
        formdata = aiohttp.FormData()
        formdata.add_field(
            name="files",
            value=open(file=file, mode="rb").read(),
            content_type="multipart/form-data",
            filename=file
        )
        response: dict = openURL(self.session.post, url, formdata, "https:")
        _list: list = []
        for file in response:
            _list.append(file)
        else:
            return _list

    def download(
        self,
        code: str = None
    ) -> str:
        if code is None:
            raise SyntaxError("Missing the \"code\" argument.")
        waitingToken: dict = openURL(self.session.get, f"/link?token={self.token}&file_code={code}")
        if waitingToken["statusCode"] == StatusCode.INVALID_PARAMETER:
            close(self.session)
            self.__event__(
                name="on_error",
                data=[ClientError.InvalidParameter("Bad file code.")]
            )
            sys.exit(EXIT_FAILURE)
        try:
            time.sleep(waitingToken['data']['waiting'])
        except KeyError as e:
            if "waiting" in str(e):
                return openURL(self.session.get, waitingToken["data"]["dlLink"])
        response: dict = openURL(self.session.get, f"/link?token={self.token}&file_code={code}&waitingToken={waitingToken['data']['waitingToken']}")
        return openURL(self.session.get, response["data"]["dlLink"])
    
    def createVoucher(
        self,
        time: str = None,
        quantity: int = None
    ) -> None:
        if time is None:
            raise SyntaxError("Missing the \"time\" argument.")
        if quantity is None:
            raise SyntaxError("Missing the \"quantity\" argument.")
        data: dict = {
            "token": self.token,
            "time": time,
            "quantity": quantity
        }
        response: dict = openURL(self.session.post, "/user/createVoucher", data)
        if response["statusCode"] == StatusCode.INVALID_PARAMETER:
            self.__event__(
                name="on_error",
                data=[ClientError.InvalidParameter("The function \"upload()\" don't work yet.")]
            )
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
                    self.__event__(
                        name="on_error",
                        data=[ClientError.Warning("The function \"convert()\" is not available at the moment.")]
                    )
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
                    self.__event__(
                        name="on_error",
                        data=[ClientError.NeedPremium("This is a premium feature. Your account should be premium to request this endpoint.")]
                    )
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
                    self.__event__(
                        name="on_error",
                        data=[ClientError.NeedPremium("This is a premium feature. Your account should be premium to request this endpoint.")]
                    )
                if response_slck["statusCode"] == StatusCode.INVALID_PARAMETER:
                    close(self.session)
                    raise SyntaxError("Expect a bool.")
            return
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(login_runner())
            self.__event__(
                name="on_connect"
            )
            loop.run_forever()
        except KeyboardInterrupt:
            loop.stop()
            loop.run_forever()
            loop.run_until_complete(self.session.close())
            raise Logout("Logged out.")
    
    def logout(
        self
    ) -> NoReturn:
        close(self.session)
        self.__event__(
            name="on_logout"
        )
        sys.exit(EXIT_SUCCESS)