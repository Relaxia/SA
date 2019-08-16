import tkinter
import unittest
from examples import frontend2
from tkinter import *


class Test_Frontend(unittest.TestCase):
    """
    Testclass to test the Frontend2
    """
    def test_init_window(self):
        """tests the init method of frontend2
        :return:
        """
        # instantiate the frontend
        root = Tk()
        fend = frontend2.Window(root)
        fend.init_window()

        # test if it initiates a mic to text instance
        self.assertIsNotNone(fend.mic)

        # test if buttons and labels are correctly created
        self.assertEqual(fend.quitButton['text'], 'Exit')
        self.assertEqual(fend.resultButton['text'], 'Show me what you got')
        self.assertEqual(fend.commandButton['text'], 'Start listening')

        # test if the 3 buttons and 2 labels are packed into the main window
        self.assertIsNotNone(fend.children['!button'])
        self.assertIsNotNone(fend.children['!button2'])
        self.assertIsNotNone(fend.children['!button3'])

        self.assertIsNotNone(fend.children['!label'])
        self.assertIsNotNone(fend.children['!label2'])

    def test_client_exit(self):
        """tests the client_exit method of the frontend (exit button)
        :return:
        """
        # instantiate the frontend
        root = Tk()
        fend = frontend2.Window(root)
        fend.init_window()

        # check if it exits the code
        with self.assertRaises(SystemExit):
            fend.client_exit()

        # check if it also set the switch of the mic to text instance to false
        self.assertFalse(fend.mic.switch)

    def test_show_results(self):
        """tests the show_results method of the frontend (show me what you got button)
        :return:
        """
        # instantiate the frontend
        root = Tk()
        fend = frontend2.Window(root)
        fend.init_window()

        # update results
        fend.show_results()

        #check that the variables are intialized
        self.assertIsNotNone(fend.dic)
        self.assertIsNotNone(fend.street)
        self.assertIsNotNone(fend.capital)
        self.assertIsNotNone(fend.income)
        self.assertIsNotNone(fend.price)

    def test_write(self):
        """tests the different write methods which are executed if a candidate is clicked
        :return:
        """
        root = Tk()
        fend = frontend2.Window(root)
        fend.init_window()
        string_to_test = 'abc'

        # we write to the label and then check the text of the label
        fend.writep(string_to_test)
        self.assertEqual(fend.pricelabel['text'], "Kaufpreis: " + string_to_test)

        fend.writei(string_to_test)
        self.assertEqual(fend.incomelabel['text'], "Einkommen: " + string_to_test)

        fend.writec(string_to_test)
        self.assertEqual(fend.capitallabel['text'], "Eigenmittel: " + string_to_test)

        fend.writel(string_to_test)
        self.assertEqual(fend.locationlabel['text'], "Ort: " + string_to_test)

        fend.writes(string_to_test)
        self.assertEqual(fend.streetlabel['text'], "Strasse: " + string_to_test)

if __name__ == '__main__':
    unittest.main()
