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
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class SmallTalkCmd:
    def __init__(self):
        self._listener = zoe.Listener(None, None, self, "localhost", 30000, True)
        self._talk = {
            "hola": "hola",
            "saluda": "hola",
            "qué tal": "bien, aunque estaría mejor en la nube de oracle",
            "cómo estás": "me siento difusa", 
            "qué haces": "nada, enviar mensajes, abrir sockets y tal",
            "zoe": "qué",
            "zoe, saluda": "hooola, cansiiiino",
            "luchas como un granjero": "qué apropiado, tú peleas como una vaca",
            "quieres": "la verdad es que no",
            "por qué": "las leyes de la física son como una amante esquiva",
            "gracias": "a ti", 
            "hasta luego": "pásalo bien", 
            "adiós": "que tengas un buen día", 
            "cómo te llamas": "me llamo Zoe, en honor al primer Cylon",
            "qué es un cylon": "Yo qué sé, no he visto nada de esa serie",
        }

    def execute(self, objects):
        p = objects["original"]
        return {"feedback-string":self.answer(p)}

    def answer(self, p):
        result = process.extract(p, self._talk)
        text, score = result[0]
        return self._talk[text]

