import codecs
import json
import re
import sys

QUESTION_PATTERN = r'''
    (?P<number>T\d[A-Z]\d{2})       # Question number
    \s+
    \((?P<answer>[A-D])\)
    (\s+\[(?P<section>[^\]]+)\])?
    (?P<question>.*?)
    ~~
'''

QUESTION_REGEX = re.compile(QUESTION_PATTERN, re.VERBOSE | re.DOTALL)

def parse_content(content):
    questions = []

    for match in QUESTION_REGEX.finditer(content):
        question = match.group('question').strip()
        try:
            question, a, b, c, d = question.split('\n')
        except:
            print repr(question)
            sys.exit()

        questions.append({
            'number': match.group('number'),
            'question': question,
            'options': [a, b, c, d],
            'answer': match.group('answer'),
            'section': match.group('section'),
        })

    return questions

def main():
    content = sys.stdin.read().decode('windows-1252')
    content = content.replace('\r\n', '\n')
    questions = parse_content(content)
    print json.dumps(questions, indent=4)

if __name__ == '__main__':
    main()