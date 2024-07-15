# Основная инструкция

## Digital ocean
Чтобы зайти в консоль сервера нужно:
- <img width="1423" alt="Screenshot 2024-07-15 at 22 41 47" src="https://github.com/user-attachments/assets/c9e0e139-0f6b-4085-9c37-7c88c39590cb">
- <img width="1423" alt="Screenshot 2024-07-15 at 22 42 25" src="https://github.com/user-attachments/assets/b32be756-c96a-4610-890f-fbfa4990e7ff">



## Dynabot
Домен предоставлен на год, стоил 1.29$. Истекает 2025/07/01

## Где менять настройки алгоритма
- зайти в console digital ocean (см. в пунтке digital ocean)
- набрать команда "cd RunBuddy" и Enter
- набрать команду "sudo nano .bot.env"
- меняем содержимое
- Если хотим сохранить и выйти, то нажимаем "ctrl + o" и Enter
- Если хотим просто выйти, то нажимаем "ctrl + x" и Enter

## Как менять текст для бота
Все тоже самое как и в настройках алгоритма, только 3 пункт команда будет такой "sudo nano .text.bot.env"

## Перевыпуск сертификата
- сертификат выдается на 3 месяца.
- Чтобы перевыпустить необходимо:
    - зайти в console digital ocean (см. в пунтке digital ocean) - Старт с 2024.07.14
    - набрать команда "cd RunBuddy" и Enter
    - выполнить команду "docker compose run --rm certbot renew"
