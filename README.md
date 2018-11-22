
# Visual GitHub

Инструкция по развертыванию python (необязательно, если уже имеется нужная версия и зависимости):
* `sudo apt-get update`  
* Установка python и pip:  
` sudo apt-get install python3.6 pip3`
* Создание виртуального окружения:  
`python3.6 -m venv /path/to/new/virtual/environment`
* Запуск виртуального окружения:  
`source /path/to/new/virtual/environment/bin/activate`

Установка необходимых библиотек для Python (необходим Python 3.6 или выше):  
```
pip3 install bottle github3.py websocket-server
```

Для запуска python backend необходимо запускать скрипт из папки src
```
python backend.py
```

Для linux
```
python3.6 backend.py
```

Для запуска приложения слежует перейти в папку src и запустить backend.py 
```
cd src || sudo python3.6 backend.py
```
