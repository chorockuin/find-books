import unittest
import paper
from googletrans import Translator

class PaperTest(unittest.TestCase):
    def test(self):
        translator = Translator()
        text="I'm Korean"
        ko_result = translator.translate(text, dest='ko')
        print(ko_result.text)

if __name__ == '__main__':
    unittest.main()