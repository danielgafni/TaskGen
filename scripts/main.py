from TaskGen import TaskGenerator, problem_directory_parser


'''Создание генератора задач'''
gen = TaskGenerator()

'''Загрузка задач из таблицы. Выполнять только один раз.'''
#  gen.load_data_from_csv(r'D:\Files\Programming\TaskGen\comb.csv')

'''Генерация листочка'''
gen.generate_task(title='Случайнай комбинаторика2',
                  author='Даниил Гафни', n=10, show_solutions=True,
                  method='random', topics=['комбинаторика'], min_diff=50, max_diff=76, seed='random')