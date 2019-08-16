from unittest import TestCase
from examples.convertsentence import ConvertSent

class TestConvertSent(TestCase):
    """Test class to test the ConvertSent class
    """

    def test_init(self):
        """test the init method of ConvertSent
        :return:
        """
        cnv = ConvertSent()

        self.assertIsNotNone(cnv.cities)
        self.assertIsNotNone(cnv.streets)

    def test_findstreet(self):
        """test the find_street method of ConvertSent
        :return:
        """
        cnv = ConvertSent()
        text = 'adolf wohnt an der adickesstraße'
        res = cnv.find_street(text)

        self.assertEqual(res, 'adickesstraße')

        text = 'adickesstraße'
        res = cnv.find_street(text)

        self.assertEqual(res, 'adickesstraße')

        #from here on there are cases that should give a None back because they are in streets.txt but not a actual name
        text = 'blabla bla blup'
        res = cnv.find_street(text)

        self.assertEqual(res, None)

        text = 'blabla in'
        res = cnv.find_street(text)

        self.assertEqual(res, None)

        text = 'blabla an'
        res = cnv.find_street(text)

        self.assertEqual(res, None)

        text = 'blabla und'
        res = cnv.find_street(text)

        self.assertEqual(res, None)

    def test_findcity(self):
        """tests the find_city method of ConvertSent
        :return:
        """
        cnv = ConvertSent()
        text = 'die falkenhagener wohnen am falkenhagener feld'
        res = cnv.find_city(text)

        self.assertEqual(res, 'falkenhagener feld')

        text = 'falkenhagener falkenhagener feld'
        res = cnv.find_city(text)

        self.assertEqual(res, 'falkenhagener feld')

        text = 'blabla blup'
        res = cnv.find_city(text)

        self.assertEqual(res, None)
