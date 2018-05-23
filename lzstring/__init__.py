#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from builtins import range
from builtins import chr
from future import standard_library

standard_library.install_aliases()
from builtins import object


class LZString(object):
    def __init__(self):
        self.keyStrBase64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
        self.keyStrUriSafe = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-$'
        self.baseReverseDict = {}

    def getBaseValue(self, alphabet, character):
        if alphabet not in self.baseReverseDict:
            self.baseReverseDict[alphabet] = {}
            for i in xrange(len(alphabet)):
                self.baseReverseDict[alphabet][alphabet[i]] = i

        return self.baseReverseDict[alphabet][character]

    def compressToBase64(self, input_string):
        if input_string is None:
            return ''

        res = self._compress(input_string, 6, lambda i: self.keyStrBase64[i])

        len_remainder = len(res) % 4

        if len_remainder == 3:
            return res + '='
        elif len_remainder == 2:
            return res + '=='
        elif len_remainder == 1:
            return res + '==='
        else:
            return res

    def decompressFromBase64(self, input_string):
        if input_string is None:
            return ''
        elif input_string == '':
            return None

        return self._decompress(len(input_string), 32, lambda i: self.getBaseValue(self.keyStrBase64, input_string[i]))

    def compressToUTF16(self, input_string):
        if input_string is None:
            return ''

        return self._compress(input_string, 15, lambda i: chr(i + 32)) + ' '

    def decompressFromUTF16(self, input_string):
        if input_string is None:
            return ''
        elif input_string == '':
            return None

        return self._decompress(len(input_string), 16384, lambda i: ord(input_string[i]) - 32)

    def compressToEncodedURIComponent(self, input_string):
        if input_string is None:
            return ''

        return self._compress(input_string, 6, lambda i: self.keyStrUriSafe[i])

    def decompressFromEncodedURIComponent(self, input_string):
        if input_string is None:
            return ''
        elif input_string == '':
            return None

        input_string = input_string.replace(' ', '+')
        return self._decompress(len(input_string), 32, lambda i: self.getBaseValue(self.keyStrUriSafe, input_string[i]))

    def compress(self, uncompressed):
        return self._compress(uncompressed, 16, lambda i: chr(i))

    @staticmethod
    def _compress(uncompressed, bitsPerChar, getCharFromInt):
        if uncompressed is None:
            return ''

        value = 0
        context_dictionary = {}
        context_dictionaryToCreate = {}
        context_c = ''
        context_wc = ''
        context_w = ''
        context_enlargeIn = 2

        context_dictSize = 3
        context_numBits = 2
        context_data_string = ''
        context_data_val = 0
        context_data_position = 0

        uncompressed = uncompressed

        for ii in range(len(uncompressed)):
            context_c = uncompressed[ii]

            if not context_c in context_dictionary:
                context_dictionary[context_c] = context_dictSize
                context_dictSize += 1
                context_dictionaryToCreate[context_c] = True

            context_wc = context_w + context_c

            if context_wc in context_dictionary:
                context_w = context_wc
            else:
                if context_w in context_dictionaryToCreate:
                    if ord(context_w[0]) < 256:
                        for i in range(context_numBits):
                            context_data_val = (context_data_val << 1)

                            if context_data_position == (bitsPerChar - 1):
                                context_data_position = 0
                                context_data_string += getCharFromInt(context_data_val)
                                context_data_val = 0
                            else:
                                context_data_position += 1

                        value = ord(context_w[0])

                        for i in range(8):
                            context_data_val = (context_data_val << 1) | (value & 1)

                            if context_data_position == (bitsPerChar - 1):
                                context_data_position = 0
                                context_data_string += getCharFromInt(context_data_val)
                                context_data_val = 0
                            else:
                                context_data_position += 1

                            value = value >> 1
                    else:
                        value = 1

                        for i in range(context_numBits):
                            context_data_val = (context_data_val << 1) | value

                            if context_data_position == (bitsPerChar - 1):
                                context_data_position = 0
                                context_data_string += getCharFromInt(context_data_val)
                                context_data_val = 0
                            else:
                                context_data_position += 1

                            value = 0

                        value = ord(context_w[0])

                        for i in range(16):
                            context_data_val = (context_data_val << 1) | (value & 1)

                            if context_data_position == (bitsPerChar - 1):
                                context_data_position = 0
                                context_data_string += getCharFromInt(context_data_val)
                                context_data_val = 0
                            else:
                                context_data_position += 1

                            value = value >> 1

                    context_enlargeIn -= 1

                    if context_enlargeIn == 0:
                        context_enlargeIn = pow(2, context_numBits)
                        context_numBits += 1

                    context_dictionaryToCreate.pop(context_w, None)
                    # del context_dictionaryToCreate[context_w]
                else:
                    value = context_dictionary[context_w]

                    for i in range(context_numBits):
                        context_data_val = (context_data_val << 1) | (value & 1)

                        if context_data_position == (bitsPerChar - 1):
                            context_data_position = 0
                            context_data_string += getCharFromInt(context_data_val)
                            context_data_val = 0
                        else:
                            context_data_position += 1

                        value = value >> 1

                context_enlargeIn -= 1

                if context_enlargeIn == 0:
                    context_enlargeIn = pow(2, context_numBits)
                    context_numBits += 1

                context_dictionary[context_wc] = context_dictSize
                context_dictSize += 1
                context_w = context_c
        if context_w != '':
            if context_w in context_dictionaryToCreate:
                if ord(context_w[0]) < 256:
                    for i in range(context_numBits):
                        context_data_val = (context_data_val << 1)

                        if context_data_position == (bitsPerChar - 1):
                            context_data_position = 0
                            context_data_string += getCharFromInt(context_data_val)
                            context_data_val = 0
                        else:
                            context_data_position += 1

                    value = ord(context_w[0])

                    for i in range(8):
                        context_data_val = (context_data_val << 1) | (value & 1)

                        if context_data_position == (bitsPerChar - 1):
                            context_data_position = 0
                            context_data_string += getCharFromInt(context_data_val)
                            context_data_val = 0
                        else:
                            context_data_position += 1

                        value = value >> 1
                else:
                    value = 1

                    for i in range(context_numBits):
                        context_data_val = (context_data_val << 1) | value

                        if context_data_position == (bitsPerChar - 1):
                            context_data_position = 0
                            context_data_string += getCharFromInt(context_data_val)
                            context_data_val = 0
                        else:
                            context_data_position += 1

                        value = 0

                    value = ord(context_w[0])

                    for i in range(16):
                        context_data_val = (context_data_val << 1) | (value & 1)

                        if context_data_position == (bitsPerChar - 1):
                            context_data_position = 0
                            context_data_string += getCharFromInt(context_data_val)
                            context_data_val = 0
                        else:
                            context_data_position += 1

                        value = value >> 1

                context_enlargeIn -= 1

                if context_enlargeIn == 0:
                    context_enlargeIn = pow(2, context_numBits)
                    context_numBits += 1

                context_dictionaryToCreate.pop(context_w, None)
                # del context_dictionaryToCreate[context_w]
            else:
                value = context_dictionary[context_w]

                for i in range(context_numBits):
                    context_data_val = (context_data_val << 1) | (value & 1)

                    if context_data_position == (bitsPerChar - 1):
                        context_data_position = 0
                        context_data_string += getCharFromInt(context_data_val)
                        context_data_val = 0
                    else:
                        context_data_position += 1

                    value = value >> 1

            context_enlargeIn -= 1

            if context_enlargeIn == 0:
                context_enlargeIn = pow(2, context_numBits)
                context_numBits += 1

        value = 2

        for i in range(context_numBits):
            context_data_val = (context_data_val << 1) | (value & 1)

            if context_data_position == (bitsPerChar - 1):
                context_data_position = 0
                context_data_string += getCharFromInt(context_data_val)
                context_data_val = 0
            else:
                context_data_position += 1

            value = value >> 1

        while True:
            context_data_val = (context_data_val << 1)

            if context_data_position == (bitsPerChar - 1):
                context_data_string += getCharFromInt(context_data_val)
                break
            else:
                context_data_position += 1

        return context_data_string

    def decompress(self, compressed):
        if compressed is None:
            return ''
        elif compressed == '':
            return None

        return self._decompress(len(compressed), 32768, lambda i: compressed[i])

    @staticmethod
    def _decompress(length, reset_value, get_next_value):
        dictionary = {}
        enlargeIn = 4
        dictSize = 4
        numBits = 3
        (entry, result, w, c) = ('', '', '', '')
        (i, nnext, bits, resb, maxpower, power) = (0, 0, 0, 0, 0, 0)

        data_val = get_next_value(0)
        data_position = reset_value
        data_index = 1

        for i in range(3):
            # dictionary[i] = i
            dictionary[i] = ''

        bits = 0
        maxpower = pow(2, 2)
        power = 1

        while power != maxpower:
            resb = data_val & data_position
            data_position >>= 1

            if data_position == 0:
                data_position = reset_value
                data_val = get_next_value(data_index)
                data_index += 1

            bits |= (1 if resb > 0 else 0) * power
            power <<= 1

        nnext = bits
        if nnext == 0:
            bits = 0
            maxpower = pow(2, 8)
            power = 1

            while power != maxpower:
                resb = data_val & data_position
                data_position >>= 1

                if data_position == 0:
                    data_position = reset_value
                    data_val = get_next_value(data_index)
                    data_index += 1

                bits |= (1 if resb > 0 else 0) * power
                power <<= 1

            c = chr(bits)
        elif nnext == 1:
            bits = 0
            maxpower = pow(2, 16)
            power = 1

            while power != maxpower:
                if data_val is not None:
                    resb = data_val & data_position
                else:
                    resb = 0
                data_position >>= 1

                if data_position == 0:
                    data_position = reset_value
                    if data_index < length:
                        data_val = get_next_value(data_index)
                    else:
                        data_val = None
                    data_index += 1

                bits |= (1 if resb > 0 else 0) * power
                power <<= 1

            c = chr(bits)
        elif nnext == 2:
            return ''

        dictionary[3] = c
        result = c
        w = result

        while True:
            if data_index > length:
                return ''

            bits = 0
            maxpower = pow(2, numBits)
            power = 1

            while power != maxpower:
                if data_val is not None:
                    resb = data_val & data_position
                else:
                    resb = 0
                data_position >>= 1

                if data_position == 0:
                    data_position = reset_value
                    if data_index < length:
                        data_val = get_next_value(data_index)
                    else:
                        data_val = None
                    data_index += 1

                bits |= (1 if resb > 0 else 0) * power
                power <<= 1

            c = bits

            if c == 0:
                bits = 0
                maxpower = pow(2, 8)
                power = 1

                while power != maxpower:
                    resb = data_val & data_position
                    data_position >>= 1

                    if data_position == 0:
                        data_position = reset_value
                        data_val = get_next_value(data_index)
                        data_index += 1

                    bits |= (1 if resb > 0 else 0) * power
                    power <<= 1

                dictionary[dictSize] = chr(bits)
                dictSize += 1
                c = dictSize - 1
                enlargeIn -= 1
            elif c == 1:
                bits = 0
                maxpower = pow(2, 16)
                power = 1

                while power != maxpower:
                    resb = data_val & data_position
                    data_position >>= 1

                    if data_position == 0:
                        data_position = reset_value
                        data_val = get_next_value(data_index)
                        data_index += 1

                    bits |= (1 if resb > 0 else 0) * power
                    power <<= 1

                dictionary[dictSize] = chr(bits)
                dictSize += 1
                c = dictSize - 1
                enlargeIn -= 1
            elif c == 2:
                return result

            if enlargeIn == 0:
                enlargeIn = pow(2, numBits)
                numBits += 1

            if c in dictionary:
                entry = dictionary[c]
            else:
                if c == dictSize:
                    entry = w + w[0]
                else:
                    return None

            result += entry

            dictionary[dictSize] = w + entry[0]
            dictSize += 1
            enlargeIn -= 1

            w = entry

            if enlargeIn == 0:
                enlargeIn = pow(2, numBits)
                numBits += 1
