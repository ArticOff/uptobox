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

from asyncio import (
    get_event_loop,
    gather
)
from json import (
    loads,
    JSONDecodeError
)
from typing import Optional

from aiohttp import ClientSession

from .Gateway import Route

def close(
    session: ClientSession = None
) -> None:
    if session is None:
        raise SyntaxError("Missing the \"session\" argument.")
    async def close_runner():
        await session.close()
    get_event_loop().run_until_complete(close_runner())
    return

def openURL(
    session: callable = None,
    url: str = None,
    data: Optional[dict] = None,
    _base: Optional[str] = None
) -> dict:
    if session is None:
        close(session)
        raise SyntaxError("Missing the \"session\" argument.")
    if url is None:
        close(session)
        raise SyntaxError("Missing the \"url\" argument.")
    async def open_runner() -> dict:
        if data:
            return loads(await (await session(
                url=str(Route(url ,_base)),
                data=data)
            ).read())
        else:
            return loads(await (await session(
                url=str(Route(url, _base)))
            ).read())
    try:
        response = get_event_loop().run_until_complete(gather(open_runner()))
    except TypeError:
        close(session)
        raise TypeError("'ClientSession' object is not callable")
    except JSONDecodeError:
        async def _open_runner():
            return await session(url=str(Route(url)))
        response = get_event_loop().run_until_complete(_open_runner())
    try:
        return vars()["response"][0]
    except TypeError:
        return (vars()["response"])._url

def runEvent(
    self: object() = None,
    name: str = None,
    data: list = None
) -> None:
    if self is None:
        raise SyntaxError("Missing the \"self\" argument.")
    if name is None:
        raise SyntaxError("Missing the \"name\" argument.")
    data = data or []
    for event in self.events:
        if event == name:
            try:
                if data:
                    return self.__getattribute__(event)(*data)
                self.__getattribute__(event)()
            except AttributeError:
                pass