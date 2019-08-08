**Генератор листочков**

Это генератор листочков с задачами.

**Описание параметров генерации**

```python
generate_task(self, title='A task', author='', date=None, n=0, topics=None, min_diff=0, max_diff=20,
              list_of_difficulties=None, method='random', seed=0, show_solutions=False):
        """

        :param title: title of the document.
        :param author: author of the document.
        :param date: date to be displayed in the document. Leave empty for today's date.
        :param n: number of problems in the document.
        :param topics: topics of the problems in the document.
        :param min_diff: minimal difficulty of the problems.
        :param max_diff: maximum difficulty of the problems.
        :param list_of_difficulties: a list of difficulties for 'list_low' method.
        :param method:
        	'random' - random difficulties;
            'linear_low' - a linear increase of difficulty of the problems.
                More easy problems;
            'list_low' - problems will have difficulties, specified in the list.
                More easy problems.
        :param seed: the seed for random. 0 by default, use 'random' for random seed.
        :param show_solutions:
        	True to show solutions in the answers file
        	False to hide them.
        """
```

title: Название листочка.

author: Автор листочка.

date: Дата создания листочка. По умолчанию - сегодняшняя дата.

n: Количество задач в листочке.

topics: Список тем задач для листочка. На данный момент лучше использовать одну тему.

min_diff: Нижняя граница сложности задач в листочке. Первая цифра соответствует номеру класса, а вторая - сложности. 

max_diff: Верхняя граница сложности задач в листочке. Первая цифра соответствует номеру класса, а вторая - сложности. 

list_of_difficulties: список сложностей для метода 'list_low'.

method: Метод генерации листочка. Варианты:
'random' - задачи случайной сложности
'linear_low' - в листочек обязательно войдут задачи всех сложностей от min_diff до max_diff. Распределение по сложностям по возможности равномерное с незначительным перевесом в сторону легких задач.
'list_low' - в листочек войдут задачи указанных в списке сложностей. Распределение по сложностям по возможности равномерное с незначительным перевесом в сторону легких задач.

seed: Зерно для случайной генерации. При значении 'random' зерно будет случайно.

show_solutions: Этот параметр определяет, показывать ли в листочке с ответами решения. Если он равен False, то решения задач не будут отображаться в финальном .pdf файле, но будут присутствовать в коде .tex файла.

**Для работы требуются:**

perl
pandas
pylatex