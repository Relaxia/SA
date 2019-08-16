# You need to install pyaudio to run this example
# pip install pyaudio
# You also need the watson developer cloud
# pip install --upgrade watson-developer-cloud

# When using a microphone, the AudioSource `input` parameter would be
# initialised as a queue. The pyaudio stream would be continuously adding
# recordings to the queue, and the websocket client would be sending the
# recordings to the speech to text service

from __future__ import print_function

import os
from queue import Queue, Full

import pyaudio
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback, AudioSource
from threading import Thread
from time import sleep
import examples.convertsentence as ConvSent
import examples.convertnumber as ConvNumb
#from examples.convertnumber import ConvertNumber as ConvNumb
#from examples.convertsentence import ConvertSent as ConvSent
import json



class MicrophoneToText:

    def __init__(self):
        """initialize the Microphone to Text service"""

        self.switch = True

        try:
            from Queue import Queue, Full
        except ImportError:
            from queue import Queue, Full

        ###############################################
        #### Initalize queue to store the recordings ##
        ###############################################
        self.CHUNK = 1024
        # Note: It will discard if the websocket client can't consumme fast enough
        # So, increase the max size as per your choice
        self.BUF_MAX_SIZE = self.CHUNK * 100
        # Buffer to store audio
        self.q = Queue(maxsize=int(round(self.BUF_MAX_SIZE / self.CHUNK)))

        # Create an instance of AudioSource
        self.audio_source = AudioSource(self.q, True, True)

        #with open('result.txt', 'w') as f:
            #pass


        # Create a results txt file
        self.result = open('result.txt', 'a+', encoding='utf-8')

        # Create a results dictionary
        self.keywords = dict({
            'street': [],
            'location': [],
            'capital': [],
            'income': [],
            'price': []
        })

        self.keywordsshort = dict()
        self.resultkeywords = dict({
            'street': [],
            'location': [],
            'capital': [],
            'income': [],
            'price': []
        })

        self.convs = ConvSent.ConvertSent()
        self.conv = ConvNumb.ConvertNumber()

        ###############################################
        #### Prepare Speech to Text Service ########
        ###############################################

        # initialize speech to text service
        self.speech_to_text = SpeechToTextV1(
            #nicis key
            #iam_apikey='aBOJ7l-LsQuJDc9vdMcyomvfv9PeqKTToplptgmjPRlA',
            #url='https://gateway-lon.watsonplatform.net/speech-to-text/api')
            iam_apikey='SWm4Cbisst2AihTyz42f6RXVZjaLLX6UTcal_PQxtADf',
            url='https://stream-fra.watsonplatform.net/speech-to-text/api')

        ###############################################
        #### Prepare the for recording using Pyaudio ##
        ###############################################
        # Variables for recording the speech
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        # instantiate pyaudio
        self.audio = pyaudio.PyAudio()

        # open stream using callback
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.pyaudio_callback,
            start=False
        )

    def switchoff(self):
        """Method to end the Microphone to Text service which closes all open connections and recordings
        :return: None
        """

        self.switch = False

        self.audio_source.completed_recording()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.result.close()

    def recognize_using_weboscket(self, *args):
        """Initiate the recognize service and pass the audio source
        :return: None
        """

        self.mycallback = MyRecognizeCallback()
        self.speech_to_text.recognize_using_websocket(audio=self.audio_source,
                                                      content_type='audio/l16; rate=44100',
                                                      model='de-DE_BroadbandModel',
                                                      recognize_callback=self.mycallback,
                                                      interim_results=True)

    def analyze_txt(self):
        """analyzes the working txt file to find specific keywords and stores the results in a dict structure
        note: this method runs as long as the Microphone to Text service is active and gets executed all 5 seconds
        :return: None
        """

        while self.switch:
            with open('result.txt', 'r') as f:
                for text in f:
                    # text = text.lower()
                    if 'straße' in text or 'adreße' in text or 'adresse' in text or 'strasse' in text or 'weg' in text:
                        self.keywords['street'].append(self.find_word(text))
                    if 'ort' in text or 'postleitzahl' in text or 'in' in text:
                        self.keywords['location'].append(self.find_word(text))
                    if 'eigenmittel' in text or 'eigenkapital' in text:
                        self.keywords['capital'].append(self.find_word(text))
                    if 'einkommen' in text or 'verdiene' in text or 'verdienen' in text:
                        self.keywords['income'].append(self.find_word(text))
                    if 'kaufpreis' in text or 'koste' in text:
                        self.keywords['price'].append(self.find_word(text))
            self.keywordsshort = {k: list(set(v)) for k, v in self.keywords.items()}
            sleep(5)

    def find_correct_keyword(self):
        """finds in the sentences with keywords in them the essential information
        :return: None
        """

        for k, v in self.keywordsshort.items():
            #bindwords = ['lautet', 'ist', 'sind', 'beträgt']
            uselesswords = ['ähm', 'äh', 'ä', 'hh', ' ', 'oh', 'uh', 'und', '[geräusch]']
            for x in v:
                #for y in bindwords:
                    #if y in x:
                        #vals = x.split(y)
                        #val = vals[1]

                        val = x
                        if val in uselesswords:
                            continue
                        if k == 'street':
                            print("val:" + val)
                            to_append = self.convs.find_street(val)
                            print(to_append)
                            if to_append != None and to_append != 'straße':
                                self.resultkeywords[k].append(to_append)
                        elif k == 'location':
                            to_append1 = self.convs.find_city(val)
                            if to_append1 != None:
                                self.resultkeywords[k].append(to_append1)
                        else:
                            self.conv.setnum(val)
                            to_append2 = self.conv.getnum()
                            if to_append2 != 0:
                                self.resultkeywords[k].append(to_append2)

            self.resultkeywords = {k: list(set(v)) for k, v in self.resultkeywords.items()}

    def print_results(self):
        """returns the final dict structure of results
        :return: dict with resultkeywords
        """

        print(self.keywordsshort)
        self.find_correct_keyword()
        print(self.resultkeywords)
        return self.resultkeywords

    def find_word(self, text):
        """finds the transcript in a json formatted text input
        :param text: json formatted string
        :return: the actual transcribed sentence
        """

        words = text.split('transcript":')
        words = words[1].split('}')
        word = words[0]
        return word

    def pyaudio_callback(self, in_data, frame_count, time_info, status):
        """puts a recording in the queue
        :param in_data: the recording to put in the queue
        :param frame_count: frame count if its specific otherwise not used
        :param time_info: timestamp if its specific otherwise not used
        :param status: status if its specific otherwise not used
        :return: None, the queue continues
        """

        try:
            self.q.put(in_data)
        except Full:
            pass  # discard
        return (None, pyaudio.paContinue)

    def threader(self):
        """Starts a thread to start the Microphone to Text service
        :return: None
        """

        main_thread = Thread(target=self.main)
        main_thread.start()

    def main(self):
        """Start the recording, start the Microphone to Text service in a separate thread
        and start analyzing in a separate thread
        :return: None
        """

        print("Enter CTRL+C or CTRL+F2 if in pycharm to end recording...")
        self.stream.start_stream()

        try:
            recognize_thread = Thread(target=self.recognize_using_weboscket, args=())
            recognize_thread.start()

            analyze_thread = Thread(target=self.analyze_txt(), )
            analyze_thread.start()

            while self.switch:
                pass

        except KeyboardInterrupt:
            # stop recording for developing purposes with keyboardinterrupt
            self.audio_source.completed_recording()
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            self.result.close()


class MyRecognizeCallback(RecognizeCallback):
    """define callback for the speech to text service"""

    def __init__(self):
        """initialize the callback
        :return: None
        """

        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        """print the received transcript
        :param: transcript of the transcribed audio
        :return: None
        """

        print(transcript)

    def on_connected(self):
        """print a message if connected
        :return: None
        """

        print('Connection was successful')

    def on_error(self, error):
        """print the error if one is catched
        :param error: error which was thrown
        :return: None
        """

        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        """print the error if caused by inactivity
        :param error: error which was thrown because of inactivity
        :return: None
        """

        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        """print a message if the service is listening
        :return: None
        """

        print('Service is listening')

    def on_hypothesis(self, hypothesis):
        """print the hypothesis of the transcribed audio
        :param hypothesis: hypothesis of the transcribed audio
        :return: None
        """

        print(hypothesis)

    def on_data(self, data):
        """print and if its final write the transcribed data to the result txt file
        :param data: transcription of the received audio
        :return: None
        """

        print(data)
        strdata = json.dumps(data, ensure_ascii=False)
        if '"final": true' in strdata:
            with open('result.txt', 'a+') as result:
                result.write(strdata)
                result.write("\n")

    def on_close(self):
        """print a message if the websocket connection has closed
        :return: None
        """

        print("Connection closed")

if __name__ == '__main__':
    MicrophoneToText().main()
