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
import uuid
import threading

class ActivitiesCmd:
    def __init__(self, tome = None):
        self._listener = zoe.Listener(None, None, self, "localhost", 30000)
        self._tome = tome
        self._lock = threading.Lock()

    def feedback(self, objects, msg):
        if "feedback" in objects["context"]:
            objects["context"]["feedback"].feedback(msg)

    def execute(self, objects):
        self.feedback(objects, "Voy a generar la memoria")

        # Prepare a "generate memo" message
        aMap = {"dst":"activities", "tag":"memo", "_cid":uuid.uuid4()}
        trigger = zoe.MessageBuilder(aMap).msg()

        # Send the message and stalk topic "activities" for a message from agent "activities" 
        # with the same CID of the trigger message.
        # When the message is received, call self.memoready
        # Use a 30 seconds timeout
        msgparams = ("activities", "activities", trigger)
        self._stalker = zoe.StalkerAgent("localhost", 0, "localhost", 30000, msgparams, self.memoready, objects, timeout = 30)
        self._stalker.start()
        
        # Synchronize threads
        with self._lock:
            pass

        # Get the memo
        f = objects["memo"]
        if not f:
            self.feedback(objects, "Ha habido un error")
            return objects

        # Send the memo to every user in the original command
        mails = self.mails(objects)
        for u in mails:
            self.feedback(objects, "Enviando la memoria a " + u)
            params = {"dst":"mail", "to":u, "subject":"Memoria de actividades", "att":f}
            msg = zoe.MessageBuilder(params).msg()
            self._listener.sendbus(msg)

        self.feedback(objects, "Memoria enviada")

    def mails(self, objects):
        if self._tome:
            user = objects["context"]["sender"]
            return [ user["mail"] ]
        else:
            return [ x["mail"] for x in objects["users"] ]

    def memoready(self, parser, objects):
        self.feedback(objects, "La memoria se ha generado")
        with self._lock:
            objects["memo"] = parser.get("memo")
        self._stalker.stop()

ActivitiesCmd.commands = [
    ("envía la memoria de actividades a <u>", ActivitiesCmd()),
    ("envíame la memoria de actividades", ActivitiesCmd(tome = True)),
    ("dame la memoria de actividades", ActivitiesCmd(tome = True)),
]

