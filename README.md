# Основная инструкция

## Зайти на сервер с помощью termius
Чтобы зайти в консоль сервера нужно:
- Выбрать "new host" <img width="509" alt="Screenshot 2024-08-11 at 17 35 02" src="https://github.com/user-attachments/assets/3429e4b7-d547-4597-9e3d-52de2d1aefc2">
- <img width="1248" alt="Screenshot 2024-08-11 at 17 37 26" src="https://github.com/user-attachments/assets/56293459-983b-4bb3-8504-31403336a1c2">
- <img width="1248" alt="Screenshot 2024-08-11 at 17 39 26" src="https://github.com/user-attachments/assets/9d38f364-de6f-47bd-91f9-dba335ec0d86">
- Ввести пароль


## Dynabot
Домен предоставлен на год, стоил 1.29$. Истекает 2025/07/01

## Где менять настройки алгоритма
- зайти в console сервера (см. в пунтке "Зайти на сервер с помощью termius")
- набрать команда "cd .." и Enter
- набрать команда "cd opt/RunBuddy" и Enter
- набрать команду "sudo nano .bot.env"
- меняем содержимое
- Если хотим сохранить и выйти, то нажимаем "ctrl + o" и Enter
- Если хотим просто выйти, то нажимаем "ctrl + x" и Enter

## Как менять текст для бота
Все тоже самое как и в настройках алгоритма, только 3 пункт команда будет такой "sudo nano .text.bot.env"

## Перевыпуск сертификата
- This certificate expires on 2025-01-13
- сертификат выдается на 3 месяца.
- Чтобы перевыпустить необходимо:
    - зайти в console сервера (см. в пунтке "Зайти на сервер с помощью termius") - Старт с 2024.07.14
    - набрать команда "cd .." и Enter
    - набрать команда "cd opt/RunBuddy" и Enter
    - выполнить команду "docker compose run --rm certbot renew"
 
## Как перезапустить бота
- зайти в console сервера (см. в пунтке "Зайти на сервер с помощью termius")
- набрать команда "cd .." и Enter
- набрать команда "cd opt/RunBuddy" и Enter
- набрать команду "docker compose stop"
- набрать команду "docker compose start"
