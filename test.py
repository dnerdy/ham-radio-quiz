from parse import parse_content
import unittest

CONTENT = '''
T1A01 (D) [97.3(a)(4)]
For whom is the Amateur Radio Service intended?
A. Persons who have messages to broadcast to the public
B. Persons who need communications for the activities of their immediate family members, relatives and friends
C. Persons who need two-way communications for personal reasons
D. Persons who are interested in radio technique solely with a personal aim and without pecuniary interest
~~


T1A02 (C)
What agency regulates and enforces the rules for the Amateur Radio Service in the United States?
A. FEMA
B. The ITU
C. The FCC
D. Homeland Security
~~
'''

class ParseContentTestCase(unittest.TestCase):
    def test(self):
        questions = parse_content(CONTENT)
        self.assertEqual(len(questions), 2)

if __name__ == '__main__':
    unittest.main()