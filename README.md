# MVP Для ФАУ "ГЛАВГОСЭКСПЕРТИЗА" России

Программа для поиска текста названия ОКС `PDF` документах,
выявления соответствия поисковой фразе и сохранения результатов в отдельные файлы.

## Установка зависимостей
Для работы программы необходимо установить следующие зависимости:
```
pip install -r requirements.txt
```
Так же нужно установить на персональный компьютер [Redis]('https://redis.io/download/')

## Использование
1. В терминале выполняем команду
```
redis-server
```
2. Далее выполняем команду
```
celery -A tasks worker --loglevel=info
```
3. Запускаем сервер Django
```
python manage.py runserver
```
4. Запустите программу перейдя по ссылке привязанного IP, чтобы выполнить поиск текста в PDF документах. 
5. Программа запросит у вас строку для поиска.
_Пример:_
_Введите строку для поиска: Капитальный ремонт автомобильной дороги Р-777 Сыктывкар - Китай
6. Выберите файлы документаций для обработки и нажмите кнопку Отправить

Программа выполнит поиск во всех `PDF` документах, 
отобразир их на странице results/ и сохранит результаты в отдельные файлы отчетов со ссылками на страницы. 
Каждый результат будет сохранён в формате `<имя_документа>_result.html`
и содержать информацию о страницах, на которых найдено совпадение текста и проценты сходства.

*Результаты будут сохранены в папку results, в которой находятся PDF документы.*


*Примечание:* Для работы программы необходимо наличие брокера сообщений `Redis`, 
работающего на localhost:6379. Убедитесь, что Redis установлен и запущен на вашей системе.

## Лицензия

Эта программа распространяется без лицензии.
