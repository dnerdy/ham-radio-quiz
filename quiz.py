import argparse
import json
import os
import random
import sys
import time

def keyed_questions(f):
    questions = {question['number']: question for question in json.load(f)}
    return questions

def keyed_answers(f):
    f.seek(0)
    answers = dict(line.split() for line in f)
    return answers

def getanswer(questions, number):
    return questions[number]['answer']

def getquestion(questions, number):
    return questions[number]['question']

def getoptions(questions, number):
    return questions[number]['options']

def incorrect_answer(answer):
    return '*' in answer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--score', action='store_true', default=False)
    parser.add_argument('-r', '--retry', action='store_true', default=False)
    parser.add_argument('-q', '--questions', default='questions-technician.json', type=argparse.FileType('r'))
    parser.add_argument('-a', '--answers', default='answers.log', type=argparse.FileType('a+'))
    
    arguments = parser.parse_args()

    questions = keyed_questions(arguments.questions)
    answers = keyed_answers(arguments.answers)

    if arguments.score:
        incorrect_count = 0

        for number, answer in answers.items():
            if incorrect_answer(answer):
                incorrect_count += 1

        print 'Score: {}/{}'.format(len(answers)-incorrect_count, len(answers))
        sys.exit(0)

    if arguments.retry:
        numbers = list({number for number in answers if incorrect_answer(answers[number])})
    else:
        numbers = list(questions)
        numbers = [number for number in numbers if number not in answers]
    
    random.shuffle(numbers)
    total = len(numbers)

    while len(numbers):
        number = numbers.pop()

        if arguments.retry:
            current = total - len(numbers)
            out_of = total
        else:
            current = len(answers) + 1
            out_of = len(questions)

        print '{}/{} - {}'.format(current, out_of, number)

        print getquestion(questions, number)
        for option in getoptions(questions, number):
            print option
        
        answer = None
        while answer not in ('A', 'B', 'C', 'D'):
            answer = raw_input('>>> ').upper()

        if answer == getanswer(questions, number):
            print '*** Correct!'
            arguments.answers.write('{} {}\n'.format(number, answer))
        else:
            print '--- Incorrect (Answer: {})'.format(getanswer(questions, number))
            arguments.answers.write('{} {}*\n'.format(number, answer))

        answers[number] = answer

        print
        time.sleep(0.5)

if __name__ == '__main__':
    main()