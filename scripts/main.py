from TaskGen import TaskGenerator, problem_directory_parser

gen = TaskGenerator()
gen.generate_task(title='Линейное возрастание сложности', author='Даниил Гафни', n=10, show_solutions=True,
                  method='linear_low', topics=['комбинаторика'], min_diff=2, max_diff=4)
