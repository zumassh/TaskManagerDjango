# TaskManagerDjango
Репозиторий курсовой работы дисциплины "Бэкенд-разработка" (6 семестр)
Для запуска сервера небоходимо перейти в папку taskmanager и в терминалах выполнить следующие команды:
1. python manage.py runserver
2. celery -A taskmanager worker --loglevel=info --pool=solo
3. celery -A taskmanager beat --loglevel=info  
