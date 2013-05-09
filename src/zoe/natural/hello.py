# -*- coding: utf-8 -*-
#
# This file is part of Zoe Assistant - https://github.com/guluc3m/gul-zoe
#
# Copyright (c) 2013 David Muñoz Díaz <david@gul.es> 
#
# This file is distributed under the MIT LICENSE
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import zoe

class HelloCmd:
    def __init__(self, fromdef):
        self._listener = zoe.Listener(None, None, self, "localhost", 30000, True)
        self._fromdef = fromdef

    def execute(self, objects):
        users = objects["users"]
        if self._fromdef is None:
            f = None
            t = users
        else:
            f = users[self._fromdef]
            t = [x for x in users if f != x]

        for u in t:
            if f:
                text = "hello from @" + f["twitter"] + "!"
            else:
                text = "hello!"
            params = {"dst":"twitter", "to":u["twitter"], "msg":text}
            msg = zoe.MessageBuilder(params).msg()
            self._listener.sendbus(msg)
        return {"feedback-string":"Mensaje enviado"}