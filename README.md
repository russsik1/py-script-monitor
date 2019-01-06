# Py-script-monitor
Py-script-monitor helps run \*.py files and track their performance

![alt text](https://github.com/russsik1/py-script-monitor/blob/master/example.png)

:ru:

Py-script-monitor позволяет запускать/завершать .py файлы с помощью панели управления.  
Скачайте архив с проектом и распакуйте. Добавьте .py файлы в каталог /apps и удалите ненужные файлы.  
Для отслеживания работы файлов доступна запись output'a (Правая панель).  
Чтобы активировать запись output'ов, добавьте следующий фрагмент кода в Ваш .py файл:
```
import logging
logname = os.path.basename(__file__)[:-3]
logpath = os.path.join(os.path.dirname(__file__), '..', 'log')
logging.basicConfig(
    filename="%s\\%s.log"%(logpath, logname),
    filemode='w',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s >> %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)
print = logging.info
```
Параметры цветов фона, шрифта, элементов доступны в файле *config.py*  
[https://py-script-monitor.herokuapp.com/](https://py-script-monitor.herokuapp.com/) - Демонстрационная версия

:us:

Py-script-monitor allows you to run/terminate .py files using the control panel.
Download the archive with the project and unpack. Add .py files to the /apps directory and delete unnecessary files.
You can track the output of your of .py files in right panel.
To activate the output recording, add the following code snippet to your .py file:
```
import logging
logname = os.path.basename(__file__)[:-3]
logpath = os.path.join(os.path.dirname(__file__), '..', 'log')
logging.basicConfig(
    filename="%s\\%s.log"%(logpath, logname),
    filemode='w',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s >> %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)
print = logging.info
```
You can change background, font, element color in *config.py*  
[https://py-script-monitor.herokuapp.com/](https://py-script-monitor.herokuapp.com/) - Example


