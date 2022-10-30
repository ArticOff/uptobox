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
from json import loads
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
    data: Optional[dict] = None
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
                url=str(Route(url)),
                data=data)
            ).read())
        else:
            return loads(await (await session(
                url=str(Route(url)))
            ).read())
    try:
        response = get_event_loop().run_until_complete(gather(open_runner()))
    except TypeError:
        close(session)
        raise TypeError("'ClientSession' object is not callable")
    return vars()["response"][0]
