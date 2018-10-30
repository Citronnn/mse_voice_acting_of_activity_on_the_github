
# Visual GitHub

Инструкция по развертыванию python (необязательно, если уже имеется нужная версия и зависимости):
* Установка python и pip:  
` sudo apt-get install python3.6 pip3`
* Создание виртуального окружения:  
`python3.6 -m venv /path/to/new/virtual/environment`
* Запуск виртуального окружения:  
`source /path/to/new/virtual/environment/bin/activate`

Установка необходимых библиотек для Python (необходим Python 3.6 или выше):  
```
pip install bottle github3.py websocket-server
```

Для запуска python backend необходимо запускать скрипт из папки src
```
python3 backend.py
```

Для linux
```
python3.6 backend.py
```

статическую HTML страницу `mse_voice_acting_of_activity_on_the_github/src/frontend.html` необходимо открыть с помощью браузера
