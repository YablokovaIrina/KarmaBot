# KarmaBot

## Бот для discord 
KarmaBot - экономический discord-бот. Валютой являются очки кармы. Настроены пермишены (изменять количество кормы может только определенная роль). Лидерборд - топ50 по количеству кармы (выполнен с пагинацией и с использованием эмбедов). В БД заносится только определенная роль.

Бот упакован в docker-контейнера.

### Пример наполнения env файла
```
TOKEN='ваш токен бота'
ADMIN='id роли , которая может менять очки кармы'
GUILD_ID='id сервера'
UR='id роли, которая заносится в БД'

```

### Authors
Яблокова Ирина
