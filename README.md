
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
sudo pip3 install bottle github3.py websocket-server
```

Для запуска приложения следует перейти в директорию src и запустить backend.py 
```
cd src && sudo python3.6 backend.py
```

далее приложение в браузере будет доступно по адресу 
```
127.0.0.1:80
```
