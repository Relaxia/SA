import unittest
from examples.convertnumber import ConvertNumber as cnv


class TestConvertNumber(unittest.TestCase):
    """Testclass to test the ConvertNumber class
    """

    def test_setnumber(self):
        """Tests the setnum method of convernumber
        :return:
        """
        convert1 = cnv()

        convert1.setnum('einhundertdreiundzwanzig')
        self.assertEqual(convert1.numstring, 'einhundertdreiundzwanzig')

    def test_getnumber(self):
        """Tests the getnum method of convernumber
                :return:
                """
        convert = cnv()

        convert.setnum('einhundertdreiundzwanzig')
        self.assertEqual(convert.getnum(), 123)

    def test_undsplit(self):
        """Tests the undsplit method of convernumber
                :return:
                """
        convert2 = cnv()
        # normal case where tens != 0 and ones != 0
        self.assertEqual(convert2.undsplit('einundzwanzig'), 21)
        # special case 1 only one word
        self.assertEqual(convert2.undsplit('fünf'), 5)
        self.assertEqual(convert2.undsplit('fünfzig'), 50)
        # special case 2 empty string
        self.assertEqual(convert2.undsplit(''), 0)

    def test_hunsplit(self):
        """Tests the hunsplit method of convernumber
                :return:
                """
        convert3 = cnv()
        # normal case
        self.assertEqual(convert3.hunsplit('dreihundertvierzehn'), 314)
        # case no tens no ones
        self.assertEqual(convert3.hunsplit('zweihundert'), 200)
        # case no tens
        self.assertEqual(convert3.hunsplit('dreihundertundzwei'), 302)
        # case no ones
        self.assertEqual(convert3.hunsplit('vierhundertfünfzig'), 450)
        # case nothing before nothing behind
        self.assertEqual(convert3.hunsplit('hundert'), 100)

    def test_tsdsplit(self):
        """Tests the tsdsplit method of convernumber
                :return:
                """
        convert4 = cnv()
        # normal case
        self.assertEqual(convert4.tsdsplit('zweihunderteinundzwanzigtausendvierhundertdreiundfünfzig'),
                         221453)
        # case nothing behind
        self.assertEqual(convert4.tsdsplit('zweihundertfünfzehntausend'), 215000)
        # case nothing in front
        self.assertEqual(convert4.tsdsplit('tausendvierhundertfünfzig'), 1450)
        # case nothing in front nothing behind
        self.assertEqual(convert4.tsdsplit('tausend'), 1000)

    def test_milsplit(self):
        """Tests the milsplit method of convernumber
                :return:
                """
        convert5 = cnv()
        # normal case
        self.assertEqual(
            convert5.milsplit('einemilliondreihundertvierundzwanzigtausendsiebenhundertneunundachtzig'),
            1324789)
        # case nothing behind
        self.assertEqual(convert5.milsplit('fünfundzwanzigmillionen'), 25000000)
        # case nothing in front
        self.assertEqual(convert5.milsplit('millionundzwei'), 1000002)
        # case nothing in front nothing behind
        self.assertEqual(convert5.milsplit('million'), 1000000)

    def test_convertsent(self):
        """Tests the convert_sent method of convernumber which automatically tests also the isnumeric method
                :return:
                """
        convert6 = cnv()

        convert6.setnum("also haben wir hundertunddrei nein hundert 4 tausend")
        self.assertEqual(convert6.getnum(), 104000)

        convert6.setnum("also ein haben wir hundertunddrei nein tausend")
        self.assertEqual(convert6.getnum(), 1000)

        convert6.setnum(" ")
        self.assertEqual(convert6.getnum(), 0)

        convert6.setnum("fünfundzwanzig")
        self.assertEqual(convert6.getnum(), 25)

        convert6.setnum("albert ein")
        self.assertEqual(convert6.getnum(), 1)

if __name__ == '__main__':
    unittest.main()
