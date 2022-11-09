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

from typing import Union
from datetime import datetime

from aiohttp import ClientSession

from .Gateway import (
    StatusCode
)
from .Core import (
    close,
    openURL
)

class User:
    def __init__(
        self,
        token: str = None,
        session: ClientSession = None
    ) -> None:
        self.token: str = token
        self.session: ClientSession = session
        if self.token is None:
            close(self.session)
            raise SyntaxError("Missing the \"token\" argument.")
        if self.session is None:
            close(self.session)
            raise SyntaxError("Missing the \"session\" argument.")
        self.getInfos()
        pass

    def __str__(
        self
    ) -> str:
        return f"<class 'User' [{self.response}]>"
    
    def getInfos(self) -> None:
        self.response: dict = openURL(self.session.get, f"/user/me?token={self.token}")
        return

    def IsPremium(
        self
    ) -> bool:
        if self.response["data"]["premium"] == 1:
            return True
        return False

    def Name(
        self
    ) -> str:
        return self.response["data"]["login"]
    
    def Email(
        self
    ) -> str:
        return self.response["data"]["email"]

    def Points(
        self
    ) -> Union[float, int]:
        if float(self.response["data"]["point"]).is_integer():
            return int(float(self.response["data"]["point"]))
        return float(self.response["data"]["point"])

    def PremiumExpire(
        self
    ) -> datetime:
        return datetime.strptime(self.response["data"]["premium_expire"], "%Y-%m-%d %H:%M:%S")

    def SecurityLock(
        self
    ) -> int:
        return self.response["data"]["securityLock"]
    
    def DirectDownload(
        self
    ) -> int:
        return self.response["data"]["directDownload"]
    
    def SSLDownload(
        self
    ) -> int:
        return self.response["data"]["sslDownload"]
    
    isPremium: bool = property(IsPremium)
    name: str = property(Name)
    email: str = property(Email)
    points: Union[float, int] = property(Points)
    premiumExpire: datetime = property(PremiumExpire)
    securityLock: int = property(SecurityLock)
    directDownload: int = property(DirectDownload)
    sslDownload: int = property(SSLDownload)

class File:
    def __init__(
        self,
        fcode: str = None,
        session: ClientSession = None
    ) -> None:
        self.fcode: str = fcode
        self.session: ClientSession = session
        if self.fcode is None:
            close(self.session)
            raise SyntaxError("Missing the \"code\" argument.")
        if session is None:
            close(self.session)
            raise SyntaxError("Missing the \"session\" argument.")
        self.getInfos()
        pass

    def __str__(
        self
    ) -> str:
        return f"<class 'File' [{self.response}]>"

    def getInfos(self) -> None:
        self.response: dict = openURL(self.session.get, f"/link/info?fileCodes={self.fcode}")
        try:
            if self.response["data"]["list"][0]["error"]["code"] == StatusCode.FILE_NOT_FOUND:
                close(self.session)
                raise FileNotFoundError(self.response["data"]["list"][0]["error"]["message"])
        except KeyError:
            pass
        return
    
    def Code(
        self
    ) -> str:
        return self.response["data"]["list"][0]["file_code"]
    
    def Name(
        self
    ) -> str:
        return self.response["data"]["list"][0]["file_name"]

    def FileSize(
        self
    ) -> int:
        return self.response["data"]["list"][0]["file_size"]
    
    def AvailableUts(
        self
    ) -> bool:
        return self.response["data"]["list"][0]["available_uts"]
    
    def NeedPremium(
        self
    ) -> bool:
        return self.response["data"]["list"][0]["need_premium"]
    
    def Subtitles(
        self
    ) -> list[dict]:
        return self.response["data"]["list"][0]["subtitles"]
    
    def DownloadURL(
        self
    ) -> str:
        return f"https://uptobox.com/{self.code}"
    
    def StreamURL(
        self
    ) -> str:
        return f"https://uptostream.com/{self.code}"

    def size(
        self,
        format: str = None
    ) -> float:
        formats: dict = {
            "o": 1,
            "ko": 1000,
            "mo": 1000000,
            "go": 1000000000,
            "to": 1000000000000
        }
        if format is None:
            close(self.session)
            raise SyntaxError("Missing the \"format\" argument.")
        format = formats.get(format.lower())
        return round(self.fileSize/format, 3)

    code = property(Code)
    name = property(Name)
    fileSize = property(FileSize)
    availableUTS = property(AvailableUts)
    needPremium = property(NeedPremium)
    subtitles = property(Subtitles)
    downloadURL = property(DownloadURL)
    streamURL = property(StreamURL)