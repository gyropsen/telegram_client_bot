<h1 align="center">Telegram_client_bot</h1>

<h3>Приложение предназначено для быстрого управления ботнетом telegram-аккаунтов для подписки на telegram-каналы</h3>

><h3 align="center">ВНИМАНИЕ!!!</h3>
>
>**Для корректной работы в PyCharm, необходимо включить эмуляцию терминала!!! Для этого необходимо открыть файл 
main.py, вызвать контекстное меню нажатием правой кнопки мыши и перейти в пункт "Modify Run Configuration...". Нажать на 
"Modify Options" и установить галочку на "Emulate terminal in out console"**
>
*Для рыботы с приложеним, нужно в корне проекта создать файл .env и записать туда следйющие данные:*
```
api_id='your_data'
api_hash='your_data'
proxy_type='your_data'
proxy_addr='your_data'
proxy_port='your_data'
proxy_username='your_data'
proxy_password='your_data'
```
***
<h3 align="center">1 Основной функционал</h3>
* Управление одним или несколькими аккаунтами
* Добавление новых номеров в базу данных
* Подписка на telegram-каналы
* Отписка от telegram-каналов
* Проверка наличия премиума
***

<h3 align="center">2 Запуск приложения</h3>

Для запуска необходимо настроить виртуальное окружение poetry в корневой директории проекта:
```bash
poetry install
poetry shell
```
Запуск приложения:
```bash
python3 main.py
```
***

<h3 align="center">3 Работа с приложением</h3>
<h4 align="center">3.1 telegram-канал</h4>

После успешного запуска приложения, необходимо выбрать telegram-канал:
```
Enter the link to the format channel <https://t.me/wewantyoutodothejob>: 
```
***
<h4 align="center">3.2 Библиотека</h4>

Дальше необходимо указать библиотеку, с которой будет происходить работа:
```
Enter the library to work with:
1. Pyrogram
2. Telethon
```
***
<h4 align="center">3.3 Главное меню</h4>

После появится главное меню:
```
  Main Menu.                                                                                                                                                                                                                
  Press Q or Esc to quit.                                                                                                                                                                                                   
                                                                                                                                                                                                                            
> Manage accounts                                                                                                                                                                                                           
  Manage account                                                                                                                                                                                                            
  Add accounts                                                                                                                                                                                                              
  Quit                                                                                                                                                                                                                      
```
1. Управление всеми аккаунтами
2. Управление одним аккаунтом
3. Добавление в базу данных новых аккаунтов
4. Выход из приложения



