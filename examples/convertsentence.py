class ConvertSent:

    def __init__(self):
        """initializes the ConvertSent Class
        and reads the two files into variables
        """

        with open('../examples/streets.txt', 'r') as sf:
            self.streets = sf.read()
        self.streets = self.streets.lower()

        with open('../examples/cities.txt', 'r') as cf:
            self.cities = cf.read()
        self.cities = self.cities.lower()

    def find_street(self, text):
        """finds a streetname in a sentence
        :param text: sentence to search the streetname
        :return: streetname
        """
        text = text.replace('"', '')
        result = ''
        textarr = text.split()
        for i in range(0, len(textarr)):
            if textarr[i] in self.streets:
                # decide if the result is nearly empty or not to add the word with or without a space
                if len(result) < 2:
                    result = result + textarr[i]
                else:
                    result = result + ' ' + textarr[i]

                if result in self.streets:

                    # ends the function if the street is found
                    if (result + '\n') in self.streets and result != 'straße' and result != 'in' and result != '' \
                            and result != 'ein' and result != 'der' and result != 'und' and result != ' ' \
                            and result != 'an':
                        return result
                else:
                    result_list = result.split()
                    del result_list[0]
                    result = ' '.join(w for w in result_list)
                    result = result.lstrip(' ')
                    # ends the function if the street is found
                    if (result + '\n') in self.streets and result != 'straße' and result != 'in' and result != '' \
                            and result != 'ein' and result != 'der' and result != 'und' and result != ' ' \
                            and result != 'ist' and result != 'an':
                        return result
                    elif i == len(textarr)-1:
                        result_list = result.split()
                        del result_list[0]
                        result = ' '.join(w for w in result_list).lstrip(' ')
                        if (result + '\n') in self.streets and result != 'straße' and result != 'in' and result != '' \
                                and result != 'ein' and result != 'der' and result != 'und' and result != ' ' \
                                and result != 'ist' and result != 'an':
                            return result
                print(result)
        return None

    def find_city(self, text):
        """finds a cityname in a sentence
        :param text: sentence to search the cityname
        :return: cityname
        """

        result = ''
        textarr = text.split()
        for i in range(0, len(textarr)):

            if textarr[i] in self.cities:

                if len(result) < 2:
                    result = result + textarr[i]
                else:
                    result = result + ' ' + textarr[i]

                if result in self.cities:

                    # ends the function if the city is found
                    if (result + '\n') in self.cities and result != 'in':
                        return result

                else:
                    result_list = result.split()
                    del result_list[0]
                    result = ' '.join(w for w in result_list).lstrip(' ')

                    # ends the function if the city is found
                    if (result + '\n') in self.cities and result != 'in':
                        return result

        return None
