**Описание параметров генерации**

```python
generate_task(title='A task', author='', date=None, n=0, topics=None, min_diff=0,
              max_diff=20, method='random', seed=0, show_solutions=False)

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
```

title: Название листочка.

author: Автор листочка.

date: Дата создания листочка. По умолчанию - сегодняшняя дата.

n: Количество задач в листочке.

topics: Список тем задач для листочка. На данный момент лучше использовать одну тему.

min_diff: Нижняя граница сложности задач в листочке. Первая цифра соответствует номеру класса, а вторая - сложности. 

max_diff: Верхняя граница сложности задач в листочке. Первая цифра соответствует номеру класса, а вторая - сложности. 

method: Метод генерации листочка. Варианты:
'random' - задачи случайной сложности
'linear_low' - в листочек обязательно войдут задачи всех сложностей от min_diff до max_diff. Распределение по сложностям по возможности равномерное с незначительным перевесом легких задач.

seed: Зерно для случайной генерации. При значении 'random' зерно будет случайно.

show_solutions: Этот параметр определяет, показывать ли в листочке с ответами решения. Если он равен False, то решения задач не будут отображаться в финальном .pdf файле, но будут присутствовать в коде .tex файла.

