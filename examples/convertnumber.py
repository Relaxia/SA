

class ConvertNumber:
    """class to convert a combination of numbers and strings to a number"""

    numbers = {'en':0, '': 1, 'eins': 1, 'ein': 1, 'eine': 1, 'zwei': 2, 'drei': 3, 'vier': 4, 'fünf': 5, 'sechs': 6,
                    'sieben': 7,
                    'acht': 8, 'neun': 9, 'zehn': 10, 'elf': 11, 'zwölf': 12, 'dreizehn': 13, 'vierzehn': 14,
                    'fünfzehn': 15,
                    'sechszehn': 16, 'siebzehn': 17, 'achtzehn': 18, 'neunzehn': 19,
                    'zwanzig': 20, 'dreissig': 30, 'vierzig': 40, 'fünfzig': 50, 'sechzig': 60,
                    'siebzig': 70, 'achtzig': 80, 'neunzig': 90}

    def setnum(self, text):
        """sets the numstring equal to text
        :param text: sentence to convert
        :return: None
        """

        self.numstring = text.replace('"','').replace("'","").replace('[','').replace(']','')

    def getnum(self):
        """gets the final number
        :return: number (int) - final number
        """

        self.number = self.convert_sent(self.numstring)
        return self.number

    def convert_sent(self, text,):
        """searches a sentences for numbers and words that equal numbers and converts them to a number
        :param text: sentence to convert
        :return: interresult (int) - final number
        """

        result = []
        interresult = 0
        textarr = text.split()

        for j in range(0, len(textarr)):

            interres = self.isnumeric(textarr[j])
            try:
                if interres == 1 and self.isnumeric(textarr[j + 1]) == -1:
                    continue
                elif interres > 0:
                    result.append(interres)
                elif interres == 0:
                    # case word = 'nein'
                    result.append(-1)
                else:
                    continue
            except IndexError:
                if interres > 0:
                    result.append(interres)
                elif interres == 0:
                    # case word = 'nein'
                    result.append(-1)
                else:
                    continue
        if len(result) == 1:
            interresult = result[0]

        for i in range(0, len(result)-1):
            if i == 0:
                interresult = result[i]
            if result[i] == -1:
                interresult = result[i+1]
                continue
            if result[i+1] % 1000 == 0 and result[i+1] != 1000:
                interresult = (interresult + (result[i+1]/1000))*1000
            elif result[i+1] == 1000:
                interresult = interresult * result[i+1]
            else:
                interresult = interresult + result[i+1]

        return interresult

    def isnumeric(self, text):
        """checks if a given string is numeric
        :param text: string to check
        :return: res (int) - final number
        """

        res = -1

        if text == 'nein':
            res = 0
            return res

        try:
            res = int(text)
            return res
        except ValueError:
            try:
                res = self.milsplit(text)
                return res
            except KeyError:
                return res
        return res

    def milsplit(self, text):
        """checks if the word contains 'million' and splits accordingly
        transcription gets done by calling tsdsplit and checks for the word before 'million' in the dict
        :param text: word of a number
        :return: result (int) - final number
        """

        if 'million' in text:
            milspl = text.split('million')
            if milspl[0] != '':
                result = self.tsdsplit(milspl[0])*1000000 + self.tsdsplit(milspl[1])
            else:
                result = self.numbers[milspl[0]]*1000000 + self.tsdsplit(milspl[1])
        else:
            result = self.tsdsplit(text)

        return result

    def tsdsplit(self, text):
        """checks if the word contains 'tausend' and splits accordingly
        transcription gets done by calling hunsplit and checks for the word before 'tausend' in the dict
        :param text: word of a number
        :return: result (int) - final number
        """

        if 'tausend' in text:
            tsdspl = text.split('tausend')
            if tsdspl[0] != '':
                result = self.hunsplit(tsdspl[0])*1000 + self.hunsplit(tsdspl[1])
            else:
                result = self.numbers[tsdspl[0]]*1000 + self.hunsplit(tsdspl[1])
        else:
            result = self.hunsplit(text)

        return result

    def hunsplit(self, text):
        """checks if the word contains 'hundert' and splits accordingly
        transcription gets done by calling undsplit and checks for the word before 'hundert' in the dict
        :param text: word of a number
        :return: result (int) - final number
        """

        if 'hundert' in text:
            hunspl = text.split('hundert')

            result = self.numbers[hunspl[0]]*100 + self.undsplit(hunspl[1])


        else:
            result = self.undsplit(text)

        return result

    def undsplit(self, text):
        """checks if the word contains 'und' and splits accordingly
        checks for the words in the number dict and transcribes accordingly
        :param text: word of a number
        :return: result (int) - final number
        """

        if 'und' in text:
            undspl = text.split('und')
            if undspl[0] != '':
                ones = self.numbers[undspl[0]]
            else:
                ones = 0
            tens = self.numbers[undspl[1]]
            result = tens + ones
        else:
            if text != '':
                result = self.numbers[text]
            else:
                result = 0

        return result

