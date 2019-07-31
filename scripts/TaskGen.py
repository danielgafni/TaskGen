import os
import time as t
import random
import string
from distutils.dir_util import copy_tree
import numpy as np
import pandas as pd
from datetime import date
from pylatex import Document, Package, Command, Section
from pylatex.utils import NoEscape


class TaskGenerator:
    def __init__(self, path=None):
        """

        :param path: The path to the root directory of the database.
        """
        self.today = date.today()
        if path is None:
            os.chdir('..')
            path = os.path.abspath(os.curdir)
        self.path = path
        print(f'The script is running at "{self.path}"')
        self.datapath = self.path + r'\data'
        self.taskspath = self.path + r'\tasks'
        self.databasepath = self.path + r'\database'
        self.datapath = self.path + '\\data'
        self.colnames = ['name', 'path', 'author', 'date', 'topic1', 'topic2', 'topic3', 'difficulty']
        self.data = pd.DataFrame(columns=self.colnames)

        self.create_directories()
        self.load_data()
        self.create_database()
        self.topics = unique(np.concatenate([self.data.topic1.unique(),
                                             self.data.topic2.unique(), self.data.topic3.unique()]))
        print(f'Data contains topics: {self.topics}')
        print('Task generator ready!')

    def load_data(self):
        for file in os.listdir(self.datapath):
            foldername = os.fsdecode(file)
            self.import_problem(f'{self.datapath}\\{foldername}')
        print(f'Data loaded from "{self.datapath}"')

    def load_data_from_csv(self, path, sep=';'):
        max_n = len(os.listdir(self.datapath))
        data = pd.read_csv(path, sep=sep)
        print('Are you sure input data is correct? It must be a .csv file with columns:\n'
              'author, difficulty, date, text, topic1, topic2, topic3, answer, hint, solution\n'
              'Not all of them must be filled. The order is not necessary.')
        print('Are you sure? Y/N')
        ans = input().lower()
        if ans != 'y':
            print('Breaking data import...')
            return None
        for index, row in data.iterrows():
            for colname in data.columns:
                path = self.datapath + r'\\' + str(max_n + index)
                if not os.path.exists(path):
                    os.makedirs(path)
                file = open(path + r'\\' + str(colname) + '.txt', 'w')
                file.write(str(row[colname]))
                file.close()

    def clear_copies(self):
        pass

    def create_database(self):
        self.data.to_csv(self.databasepath + r'/database.csv', sep=';', index=False, encoding='utf-8')
        print(f'Database created at "{self.databasepath}"')

    def create_docs(self, title='A task', author='', date=None):
        print('Generating documents...')
        doc_task = Document(documentclass='article', document_options=['a4paper', '11pt'], inputenc='utf8')
        doc_task.packages.append(Package('inputenc', options=['utf8']))
        doc_task.packages.append(Package('babel', options=['english', 'russian']))
        doc_task.packages.append(Package('mathtext'))
        doc_task.packages.append(Package('geometry',
                                         options=['a4paper', 'margin=1.5truecm', 'top=1.3truecm', 'bottom=1.0truecm']))
        doc_task.packages.append(Package('fontenc', options=['T2A']))
        doc_task.packages.append(Package('amsmath'))
        doc_task.packages.append(Package('amsthm'))
        doc_task.packages.append(Package('amsfonts'))
        doc_task.packages.append(Package('mathabx'))
        doc_task.packages.append(Package('graphicx'))
        doc_task.packages.append(Package('tabularx'))

        doc_task.preamble.append(Command('theoremstyle', 'definition'))
        #doc_task.append(NoEscape(r'\theoremstyle{definition}'))
        #doc_task.preamble.append(Command('newtheorem', arguments=r'\hspace{-25pt}\fbox{\phantom{123}} Задача', options='Ex'))
        doc_task.preamble.append(NoEscape(r'\newtheorem{Ex}{\hspace{-25pt}\fbox{\phantom{123}} Задача}'))

        doc_task.preamble.append(Command('title', title))
        doc_task.preamble.append(Command('author', author))
        doc_task.preamble.append(Command('date', date))
        doc_task.append(NoEscape(r'\maketitle'))

        doc_answer = Document(documentclass='article', document_options=['a4paper', '11pt'], inputenc='utf8')
        doc_answer.packages.append(Package('inputenc', options=['utf8']))
        doc_answer.packages.append(Package('babel', options=['english', 'russian']))
        doc_answer.packages.append(Package('mathtext'))
        doc_answer.packages.append(Package('geometry',
                                         options=['a4paper', 'margin=1.5truecm', 'top=1.3truecm', 'bottom=1.0truecm']))
        doc_answer.packages.append(Package('fontenc', options=['T2A']))
        doc_answer.packages.append(Package('amsmath'))
        doc_answer.packages.append(Package('amsthm'))
        doc_answer.packages.append(Package('amsfonts'))
        doc_answer.packages.append(Package('mathabx'))
        doc_answer.packages.append(Package('graphicx'))
        doc_answer.packages.append(Package('tabularx'))

        doc_answer.preamble.append(Command('title', f'{title} - ответы'))
        doc_answer.preamble.append(Command('author', author))
        doc_answer.preamble.append(Command('date', date))
        doc_answer.append(NoEscape(r'\maketitle'))

        return doc_task, doc_answer

    def import_problem(self, path):
        """
        Method to add a problem to the database.
        The problem folder can (but not must) contain:
            text.txt, solution.txt, answer.txt, hint.txt, name.txt, author.txt, date.txt,
            topic1.txt, topic2.txt, topic3.txt, difficulty.txt
        :param path: the path to the problem directory.
        """
        #  Loading problem properties
        name, author, date, topic1, topic2, topic3, difficulty = problem_directory_parser(path)
        #  Appending problem to DataFrame
        problem = pd.DataFrame([[name, path, author, date, topic1, topic2, topic3, difficulty]], columns=self.colnames)
        self.data = self.data.append(problem)

    def create_directories(self):
        """
        Creates internal directories if they don't exist yet.
        """
        if not os.path.exists(self.datapath):
            os.makedirs(self.datapath)
        if not os.path.exists(self.taskspath):
            os.makedirs(self.taskspath)
        if not os.path.exists(self.databasepath):
            os.makedirs(self.databasepath)

########################################################################################################################

    def generate_task(self, title='A task', author='', date=None, n=0, topics=None, min_diff=0, max_diff=20,
                      method='random', seed=0, show_solutions=False):
        """

        :param title: title of the task
        :param author: author of the task
        :param date: date to be print in the task
        :param n: number of problems in the task
        :param topics: a list of topics for the task
        :param min_diff: the low border of difficulty
        :param min_diff: the high border of difficulty
        :param method: the method of generation
        :param seed: use 'random' to get random problems. Use a value to get the same problems.
        :param show_solutions: True to show solutions in the answers document or False to not
        """
        if seed == 'random':
            seed = int(t.time())
            print(f'Using random seed {seed}')
        np.random.seed(seed)
        if date is None:
            date = str(self.today)
        if topics is None:
            topics = ['разное']

        doc_task, doc_answer = self.create_docs(title=title, author=author, date=date)

        data_for_generation = filter_topics(self.data, topics)

        data_for_generation = filter_difficulty(data_for_generation, min_diff=min_diff,
                                                max_diff=max_diff, method=method, n=n, seed=seed)

        for index, problem in data_for_generation.iterrows():
            add_problem_to_task(doc_task=doc_task, doc_answer=doc_answer, problem=problem,
                                show_solutions=show_solutions)

        path = self.taskspath + f'\\{date}' + f'\\{title}'

        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.exists(path):
            os.makedirs(path)

        doc_task.generate_pdf(f'{path}\\{date}_{title}_{author}_task', clean_tex=False, clean=True)
        doc_answer.generate_pdf(f'{path}\\{date}_{title}_{author}_answers', clean_tex=False, clean=True)
        print(f'Generation complete! You can find your task at "{path}"')


def add_problem_to_task(doc_task, doc_answer, problem, show_solutions=False):
    path = problem['path']
    text_file = open(path + r'\text.txt', 'r')
    text = text_file.read()
    text_file.close()
    if os.path.exists(path + r'\answer.txt'):
        answer_file = open(path + r'\answer.txt', 'r')
        answer = answer_file.read()
        answer_file.close()
    else:
        answer = 'No answer'
    solution_file = open(path + r'\solution.txt', 'r')
    solution = solution_file.read()
    solution_file.close()
    hint_file = open(path + r'\hint.txt', 'r')
    hint = hint_file.read()

    doc_task.append(NoEscape(r'\begin{Ex}'))
    doc_task.append(NoEscape(text))
    doc_task.append('')
    doc_task.append(NoEscape(r'\end{Ex}'))
    doc_task.append('')
    doc_task.append(NoEscape(r'\iffalse'))
    doc_task.append(f'Автор: {problem["author"]}')
    doc_task.append(f'Дата: {problem["date"]}')
    doc_task.append(f'Название: {problem["name"]}')
    doc_task.append(r'Подсказка: \\')
    doc_task.append(NoEscape(hint))
    doc_task.append(NoEscape(r'\fi'))
    doc_task.append('')

    with doc_answer.create(Section(f'(сложность - {problem["difficulty"]})')):
        doc_answer.append(NoEscape(r'\hspace{3ex} Ответ: ' + answer + r' \\'))
        doc_answer.append('')
        if not show_solutions:
            doc_answer.append(NoEscape(r'\iffalse'))
            doc_answer.append(NoEscape(r'\hspace*{3ex} Решение: \\'))
            doc_answer.append(NoEscape(solution))
            doc_answer.append(NoEscape(r'\fi'))
        else:
            doc_answer.append(NoEscape(r'\hspace*{3ex} Решение: \\'))
            doc_answer.append(NoEscape(solution))


def problem_directory_parser(path):
    """
    :param path: path to the problem directory.
    :return: problem properties
    """
    name, author, date, topic1, topic2, topic3, difficulty = None, None, None, '', '', '', None
    if os.path.isfile(path + r'\name.txt'):
        file = open(path + r'\name.txt', 'r')
        name = file.read()
        file.close()
    if os.path.exists(path + r'\author.txt'):
        file = open(path + r'\author.txt', 'r')
        author = file.read()
        file.close()
    if os.path.exists(path + r'\date.txt'):
        file = open(path + r'\date.txt', 'r')
        date = file.read()
        file.close()
    if os.path.exists(path + r'\topic1.txt'):
        file = open(path + r'\topic1.txt', 'r')
        topic1 = file.read()
        file.close()
    if os.path.exists(path + r'\topic2.txt'):
        file = open(path + r'\topic2.txt', 'r')
        topic2 = file.read()
        file.close()
    if os.path.exists(path + r'\topic3.txt'):
        file = open(path + r'\topic3.txt', 'r')
        topic3 = file.read()
        file.close()
    if os.path.exists(path + r'\difficulty.txt'):
        file = open(path + r'\difficulty.txt', 'r')
        difficulty = int(file.read())
        file.close()

    return name, author, date, topic1, topic2, topic3, difficulty


def filter_topics(data, topics):
    print(f'Filtering topics {topics}...')
    data_for_output = pd.DataFrame(columns=data.columns)
    for index, problem in data.iterrows():
        for topic in topics:
            if topic in [problem['topic1'], problem['topic2'], problem['topic3']]:
                data_for_output = data_for_output.append(problem)
                break
    return data_for_output


def filter_difficulty(data, min_diff=1, max_diff=20, method='random', n=1, seed=0):
    print(f'Filtering difficulty from {min_diff} to {max_diff} by {method} method...')
    data_sorted = data.sort_values('difficulty')
    if n > data_sorted.shape[0]:
        print(f'Given filters only leave {data_sorted.shape[0]} problems. Returning them all...')
        return data_sorted

    data_for_output = pd.DataFrame(columns=data.columns)
    if method == 'random':
        data_for_output = data_sorted.sample(n=n, random_state=seed)

    if method == 'linear_low':
        problems_by_difficulty = []
        for d in range(min_diff, max_diff + 1):
            problems_by_difficulty.append(data_sorted[data_sorted['difficulty'] == d])
        numbers = [0] * len(problems_by_difficulty)
        i = 0
        d = 0
        while i < n:
            if problems_by_difficulty[d % (len(problems_by_difficulty)-1)].shape[0] > numbers[d % (len(problems_by_difficulty)-1)]:
                data_for_output = data_for_output.append(problems_by_difficulty[d % (len(problems_by_difficulty)-1)].iloc[numbers[d % (len(problems_by_difficulty)-1)], :])
                numbers[d % len(problems_by_difficulty)] += 1
                i += 1
                d += 1
            else:
                d += 1
    if method == 'constant':
        data_for_output = data_sorted[data_sorted['difficulty'] == min_diff]

    return data_for_output.sort_values('difficulty')


def unique(a):
    uniques = []
    for element in a:
        if element not in uniques:
            uniques.append(element)
    return uniques
