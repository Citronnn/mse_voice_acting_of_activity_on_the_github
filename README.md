
# Visual GitHub

Данный репозиторий является проектом, реализованным в рамках курса "Введение в ПИ".

Участники:  
1) Туров Владимир - лидер, работа над backend приложения
2) Иванов Владимир - разработчик, работа над frontend
3) Пискунов Ярослав - разработчик, работа над frontend
4) Зыль Сергей - разработчик, работа над frontend
5) Матюшина Марина - работа со звуками

## О проекте

![](https://pp.userapi.com/c851524/v851524553/6f6b9/Ve9IcBWJxGQ.jpg)

Результатом проекта является веб-приложение, состоящее из единственной страницы, а также веб-сервер, организующий достп к этой странице и собирающий данные с GitHub.com. Для информации по развёртыванию приложения следует обратиться к TECHNICAL.md.

Приложение собирает события, происходящие на всех репозиториях GitHub.com и предсталяет их в удобном виде. Все события приходят как в текстовом виде, так и отображаются в виде цветной геометрической фигуры, при клике мышкой на которую в новой вкладке открывается соответствующее событие на GitHub.com. События можно фильтровать как по типу события (поддерживается 9 типов событий), как и по владельцу и названию репозитория. При отрисовке фигуры также проигрывается случайный звук из выбранного набора звуков.

Функциональные особенности приложения:

1. Фильтрация по владельцам и репозиториям поддерживает синтаксис регулярных выражений, совместимый с python 3.6.
2. Поддерживаются две темы - тёмная и светлая.
3. Поддерживается автосохранение всех выбранных фильтров, а также фильтров по владельцам и репозиториям, выбранной темы, громкости звуков.
4. Поддерживается возможность создания нескольких наборов звуков - при проигрывании будут браться звуки только в рамках одного набора.
5. Поддерживается добавление новых звуков в проект без вмешательства в исходный код приложения - все звуки должны быть в формате `src/audio/<название набора>/<любое название звука>.mp3`.
6. Поддрерживается автоматическое отключение анимации в случае большого потока событий и неспособности браузера анимировать каждый из них по отдельности.
