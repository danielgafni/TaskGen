from TaskGen import TaskGenerator, problem_directory_parser


'''Создание генератора задач'''
gen = TaskGenerator()

'''Загрузка задач из таблицы. Выполнять только один раз.'''
# gen.load_data_from_csv(r'D:\Files\Programming\TaskGen\comb.csv')

'''Генерация листочка'''
gen.generate_task(title='Автоматически сгенерированный листочек с линейным возрастанием сложности задач',
                  author='Даниил Гафни', n=10, show_solutions=True,
                  method='linear_low', topics=['комбинаторика'], min_diff=50, max_diff=76)
