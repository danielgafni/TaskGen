import os
import time as t
import pandas as pd
import numpy as np
from datetime import date
from pylatex import Document, Package, Command, Section
from pylatex.utils import NoEscape


def add_problem_to_task(doc_task, doc_answer, problem, show_solutions=False):
    path = problem['path']
    print(f'Adding problem to task from {path}')
    text_file = open(path + r'\text.txt', 'r') #encoding='utf-8'
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
    name, author, date, topics, difficulty = None, None, None,[] , None
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
    if os.path.exists(path + r'\topics.txt'):
        file = open(path + r'\topics.txt', 'r')
        topics = file.readlines()
        file.close()

    return name, author, date, topics, difficulty


def filter_topics(data, given_topics=None):
    if given_topics is None:
        given_topics = ['разное']
    else:
        given_topics = list(map(lambda x: x.lower(), given_topics))
    print(f'Filtering topics {given_topics}...')
    data_for_output = pd.DataFrame(columns=data.columns)
    for index, problem in data.iterrows():
        for topic in given_topics:
            if topic in problem['topics']:
                data_for_output = data_for_output.append(problem)
                break
    return data_for_output


def filter_difficulty(data, min_diff=0, max_diff=120, list_of_difficulties=None, method='random', n=1, seed=0):
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
            if problems_by_difficulty[d % (len(problems_by_difficulty)-1)].shape[0] >\
                    numbers[d % (len(problems_by_difficulty)-1)]:
                data_for_output = data_for_output.append(problems_by_difficulty[d % (len(problems_by_difficulty)-1)].
                                                         iloc[numbers[d % (len(problems_by_difficulty)-1)], :])
                numbers[d % len(problems_by_difficulty)] += 1
                i += 1
                d += 1
            else:
                d += 1

    if method == 'list_low':
        problems_by_difficulty = []
        a = 0
        for d in list_of_difficulties:
            problems_by_difficulty.append(data_sorted[data_sorted['difficulty'] == d])
        numbers = [0] * len(problems_by_difficulty)
        i = 0
        d = 0
        while i < n:
            a +=1
            if a == 100:
                break
            if problems_by_difficulty[d % (len(problems_by_difficulty) - 1)].shape[0] >\
                    numbers[d % (len(problems_by_difficulty) - 1)]:
                data_for_output = data_for_output.append(
                    problems_by_difficulty[d % (len(problems_by_difficulty) - 1)].iloc[
                    numbers[d % (len(problems_by_difficulty) - 1)], :])
                numbers[d % len(problems_by_difficulty)] += 1
                i += 1
                d += 1
            else:
                d += 1

    return data_for_output.sort_values('difficulty')


def unique(a):
    uniques = []
    for element in a:
        if element not in uniques:
            uniques.append(element)
    return uniques


class Problem:
    def __init__(self, path=None, name=None, author=None, date=None, difficulty=None, topics=['разное'],
                 text='Тест', answer='Ответ', hint='Подсказка', solution='Решение'):
        self.path = path
        self.name = name
        self.author = author
        self.date = date
        self.difficulty = difficulty
        self.topics = topics
        self.text = text
        self.hint = hint
        self.solution = solution
        colnames = ['name', 'path', 'author', 'date', 'difficulty', 'topics']
        self.df = pd.DataFrame([[name, path, author, date, difficulty, topics]],
                                  columns = colnames)


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
        self.colnames = ['name', 'path', 'author', 'date', 'difficulty', 'topics']
        self.data = pd.DataFrame(columns=self.colnames)

        self.create_directories()
        self.load_data()
        self.create_database()
        print(f'Data contains topics: {self.topics}')
        print('Task generator ready!')

    def show_topics(self):
        self.topics = []
        for index, problem in self.data.iterrows():
            self.topics = list(set(self.topics + problem['topics']))
        print(f'Data contains topics: {self.topics}')

    def load_problem(self, path):
        print(f'Loading problem from {path}')
        file_properties = open(f'{path}//properties.txt', 'r')
        file_topics = open(f'{path}\\topics.txt')
        topics = file_topics.read().split(',')
        name, author, date, difficulty = '', '', None, None
        properties = file_properties.read().split(',')
        name = properties[0]
        date = int(properties[1])
        author = properties[2]
        difficulty = int(properties[3])
        problem = pd.DataFrame([[name, path, author, date, difficulty, topics]], columns=self.colnames)
        self.data = self.data.append(problem)

    def load_data(self):
        self.data = pd.DataFrame(columns=self.colnames)
        for file in os.listdir(self.datapath):
            foldername = os.fsdecode(file)
            self.load_problem(f'{self.datapath}\\{foldername}')
        print(f'Data loaded from "{self.datapath}"')
        self.show_topics()

    def load_data_from_csv(self, path, sep=';'):
        data = pd.read_csv(path, sep=sep)
        print('Are you sure input data is correct? It must be a .csv file with columns:\n'
              'author, difficulty, date, text, topics, answer, hint, solution\n'
              'Not all of them must be filled. The order is not necessary.')
        print('Are you sure? Y/N')
        ans = input().lower()
        if ans != 'y':
            print('Breaking data import...')
            return None
        for index, row in data.iterrows():
            path = self.datapath + r'\\' + str(len(os.listdir(self.datapath)) + 1)
            if not os.path.exists(path):
                os.makedirs(path)

            print(f'loading to data problem with index {index}')

            file_properties = open(path + r'\\properties.txt', 'w')

            if 'name' in data.columns:
                file_properties.write(str(row['name']) + ',')
            else:
                file_properties.write(',')
            if 'date' in data.columns:
                file_properties.write(str(int(row['date'])) + ',')
            else:
                file_properties.write(',')
            if 'author' in data.columns:
                file_properties.write(str(row['author']) + ',')
            else:
                file_properties.write(',')
            if 'difficulty' in data.columns:
                file_properties.write(str(int(row['difficulty'])))

            file_properties.close()

            file_topics = open(path + r'\\topics.txt', 'w')
            topics = row['topics'].replace(' ', '').split(',')
            for topic in topics[:-1]:
                file_topics.write(topic + ',')
            file_topics.write(topics[-1])
            file_topics.close()

            file_text = open(path + r'\\text.txt', 'w')
            file_text.write(str(row['text']))
            file_text.close()
            file_answer = open(path + r'\\answer.txt', 'w')
            file_answer.write(str(row['answer']))
            file_answer.close()
            file_hint = open(path + r'\\hint.txt', 'w')
            file_hint.write(str(row['hint']))
            file_hint.close()
            file_solution = open(path + r'\\solution.txt', 'w')

            file_solution.write(str(row['solution']))
            file_solution.close()

        self.load_data()

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
                      list_of_difficulties=None, method='random', seed=0, show_solutions=False):
        """

        :param title: title of the task
        :param author: author of the task
        :param date: date to be print in the task
        :param n: number of problems in the task
        :param topics: a list of topics for the task
        :param min_diff: the low border of difficulty
        :param max_diff: the high border of difficulty
        :param method: the method of generation: 'random', 'linear_low', 'list_low'
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
                                                list_of_difficulties=list_of_difficulties,
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
