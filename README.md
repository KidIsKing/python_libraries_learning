# **Изучение библиотек Python**

*Практика и теория разных библиотек python для ML-инженера.*

## Библиотеки:

1.  *Pandas*
2.  *NumPy*
3.  *PyTorch*
4.  *re*
5.  *Matplotlib*
6.  *Pytest*
7.  *Streamlit*

## **Pandas**

> Популярная библиотека с открытым исходным кодом на языке [Python](https://en.wikipedia.org/wiki/Python), предназначенная для быстрой обработки и глубокого анализа табличных данных.

В репозитории есть код с туториалов: [PANDAS - EXCEL ПРОГРАММИСТА](https://www.youtube.com/watch?v=JUH3UdOxgB0) (`pandas\guide\tutorial2.ipynb`) и [Complete Python Pandas Data Science Tutorial! (2025 Updated Edition)](https://www.youtube.com/watch?v=2uvysYbKdjM) (`pandas\guide\tutorial1.ipynb`) и практического применения [pandas](https://pandas.pydata.org/): контесты от УрФУ в рамках курса "Анализ данных и искусственный интеллект" (`pandas\practice\UrFU_ADaAI_contest`) и в рамках курса "Сбор и верификация данных" (`pandas\practice\UrFU_SaVD_contest`) и просто упражнения с курса "Сбор и верификация данных" (`pandas\practice\UrFU_SaVD`). Здесь же базы данных, на которых практиковалась библиотека.

## **NumPy**

> [NumPy](https://numpy.org/) (Numerical Python) - это популярная бесплатная библиотека для языка программирования Python, которая создана для работы с большими многомерными массивами и матрицами, а также для быстрых математических вычислений над ними.

В проекте присутствуют теория со всеми основными инструментами numpy по видео: [NUMPY - ГЕРОИ НЕ НОСЯТ ПЛАЩИ](https://www.youtube.com/watch?v=cVRvMV6F9MQ&t=1s) (`numpy\guide\tutorial.py`) и практика контестов от УрФУ в рамках курса "Анализ данных и искусственный интеллект" (`numpy\practice\NumPy_contest.ipynb`) и найденному в интернете (`numpy\practice\NumPy_contest.ipynb`) по этой библиотеке.

## **PyTorch**

> Популярный фреймворк (библиотека) с открытым исходным кодом для [машинного обучения](https://ru.wikipedia.org/wiki/PyTorch) и глубокого обучения, созданный на базе языка Python и разработанный в основном командой Meta AI (ранее Facebook AI Research).

В репозитории есть практика работы с [pytorch](https://pytorch.org/), данные и обученные модели. Работа велась по видеороликам: [НЕЙРОННЫЕ СЕТИ - ТЕОРИЯ И ПРАКТИКА В PYTORCH](https://www.youtube.com/watch?v=bUhyrgvkVFc&t=3s) (`pytorch\guide\part_1`) - важнейшие определения нейронных сетей и обученная нейросеть, решающая задачу классификации видов Ириса по табличным данным, и [PYTORCH С НУЛЯ — ТЕНЗОРЫ И НЕЙРОСЕТИ](https://www.youtube.com/watch?v=8l_aDqLRrVg) (`pytorch\guide\part_2`) - виды тензоров, загрузка данных и обученная нейросеть, решающая задачу регрессии оценки вин по табличным данным и оценкам сомелье.

## **re**

> Модуль re в Python - это встроенная библиотека для работы с [регулярными выражениями](https://docs.python.org/3/library/re.html), которая позволяет искать, изменять и анализировать текст по заданным шаблонам.

Присутствует код с туториала по [re](https://docs.python.org/3/library/re.html) (`re\guide\tutorial.py`).

## **Matplotlib**

> Популярная библиотека на языке программирования Python для визуализации данных. Она позволяет превращать обычные списки и массивы чисел в наглядные двумерные (2D) и трехмерные (3D) графики.

В проекте есть директория работы с теорией [matplotlib](https://matplotlib.org/) по видеогайду: [MATPLOTLIB - МОИ 50 ОТТЕНКОВ](https://www.youtube.com/watch?v=PR0VAjZnLjk) (`matplotlib\guide`) и блокнот с практикой этой библиотеки на контесте от УрФУ в рамках курса "Сбор и верификация данных" (`matplotlib\practice\main.ipynb`) с визуализацией самых различных графиков.

## **Pytest**

> Популярный фреймворк (набор инструментов и правил) для написания и запуска автоматических тестов на языке программирования Python.

В репозитории есть две директории с отработкой теории по [pytest](https://docs.pytest.org/en/stable/) по видео: [БЕГУЩИЙ ПО PYTEST](https://www.youtube.com/watch?v=JcyaHQgkty8) (`pytest\guide\part_1`) - тестирование утилиты для строк с использованием **параметризации**, **фикстур** и **моков** и [Основы Pytest за 20 минут](https://www.youtube.com/watch?v=pH_oIGDTY-g) (`pytest\guide\part_2`) - тесты для "библиотеки" с разбором всех пограничных и случаев.

## **Streamlit**

> Бесплатный фреймворк с открытым исходным кодом на языке Python, который позволяет превращать обычные скрипты в интерактивные веб-приложения за пару минут.

В проекте присутствует директория с несколькими задеплоенными веб-приложениями для изучения [фреймворка](https://streamlit.io/) на практике по видеогайду: [STREAMLIT - Я PYTHON ФРОНТЕНДЕР](https://www.youtube.com/watch?v=yEFEla3SI7M&t=891s):

1.  **Конвертер валют** с разбором базовых методов фреймворка и работы с библиотекой [requests](https://pypi.org/project/requests/) для актуальный курсов валют (`streamlit\currency_converter.py`), ссылка: https://yana-currency-converter.streamlit.app/.
2.  **Генератор паролей** с использованием встроенных библиотек [string](https://docs.python.org/3/library/string.html) и [random](https://docs.python.org/3/library/random.html) для создания паролей различной длины и пользовательской возможностью использовать спец. символы при генерации или нет (`streamlit\password_generator.py`) ссылка: https://yana-password-generator.streamlit.app/.
3.  **Графический калькулятор**, использующий numpy для работы с массивами и matplotlib для визуализации графиков пользователя, позволяющий строить график, выбирать его границы, количество точек графика (плавность), и красивый интерфейс с [сайдбаром](https://docs.streamlit.io/develop/api-reference/layout/st.sidebar) (`streamlit\graphing_calculator.py`) ссылка: https://yana-graphing-calculator.streamlit.app/.