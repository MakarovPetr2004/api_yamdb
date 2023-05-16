# Simple Votings

Гайд как запустить скаченный проект:
1) Открываете терминал в скаченном проекте, и вводите следующие команды
2) python3 -m venv venv
3) source ./venv/bin/activate
4) pip install --upgrade pip
5) pip install django==4.0
6) cd simple_votings
7) python3 manage.py makemigrations
8) python3 manage.py migrate
9) python3 manage.py runserver

Как убрать ошибки импорта в Pycharm:
1) Нажимаете правой кнопкой мыши на папку где хранится manage.py
2) Нажимаете на Mark Directory as -> Sources Root
![пример](https://i.imgur.com/pCxUHzd.jpeg)

## Форматтинг кода
Тот, кто после `{{`, `{%` и перед `%}`, `}}` в html не поставит проблы, получит по жопе.

Тот, кто поставит между функциями не два пробела, получит по жопе.

Тот, кто поставит между методами в классе не один пробел, получит по жопе.

Тот, кто сделает пустой словарь, и после будет его изменять, как вот тут:
```py
context = {}
context['data'] = {"Some data"}
context['id'] = id
```
получит по жопе.

Тот, кто не будет соблюдать [PEP 8](https://www.python.org/dev/peps/pep-0008/), получит по жопе.*

Незнание форматтинга кода - не освобождает от ответственности.

*Исключением является максимальная длина строки.
