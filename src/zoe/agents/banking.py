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

import uuid
import datetime

import zoe

class BankingAgent:
    def __init__(self, host, port, serverhost, serverport, db = "/tmp/zoe-banking.sqlite3"):
        self._listener = zoe.Listener(host, port, self, serverhost, serverport)
        self._model = zoe.Banking(db)

    def start(self):
        self._listener.start()

    def stop(self):
        self._listener.stop()

    def receive(self, parser):
        tags = parser.tags()
        if "entry" in tags:
            self.entry(parser)
        if "notify" in tags:
            self.notify(parser.get("year"), parser)

    def entry(self, parser):
        y = parser.get("year")
        ts = parser.get("date")
        amount = parser.get("amount")
        what = parser.get("what")
        if not y or y == "":
            y2, m2, d2 = ts.split("-")
            y = zoe.Courses.courseyears(y2)
        self._model.entry(y, ts, amount, what)
        self._listener.log("banking", "info", "New entry: " + y + ", " + ts + ", " + str(amount) + ", " + what, parser)
        self.notify(y, parser)

    def notify(self, year, original = None):
        movements = self._model.movements(year)
        aMap = {"src":"banking", "topic":"banking", "tag":["banking", "notification"], "year":str(year)}
        ids = []
        balance = 0
        for movement in movements:
            (uuid, year, ts, amount, what) = movement
            aMap[uuid + "-year"] = year
            aMap[uuid + "-date"] = ts
            aMap[uuid + "-amount"] = str(amount)
            aMap[uuid + "-what"] = what
            balance = balance + amount
            ids.append(uuid)
        aMap["balance"] = str(balance)
        aMap["ids"] = ids
        self._listener.sendbus(zoe.MessageBuilder(aMap, original).msg())
        self._listener.log("banking", "info", "Sending banking notification for year " + str(year), original)

