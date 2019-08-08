from TaskGen import TaskGenerator, problem_directory_parser


'''Создание генератора задач'''
gen = TaskGenerator()

'''Загрузка задач из таблицы. Выполнять только один раз.'''
#gen.load_data_from_csv(r'D:\Files\Programming\TaskGen\comb_modified.csv', sep='\t')

'''Показать все темы'''
#gen.show_topics()

'''Генерация листочка'''
gen.generate_task(title='Случайнай комбинаторика2',
                  author='Даниил Гафни', n=40, show_solutions=True,
                  method='linear_low', topics=['комбинаторика'], min_diff=0, max_diff=120, seed=1,
                  list_of_difficulties=[60, 70])
