# Диаграмма 1. UML вариантов использования: Игрок

## Промпт
Создай UML use case диаграмму для веб-системы ASTROLL, роли "Игрок". Покажи границу системы "ASTROLL". Актор "Игрок" должен выполнять регистрацию и вход, управление профилем, поиск и добавление друзей, создание/редактирование/удаление персонажей, импорт и экспорт листа персонажа, подключение к комнате по ссылке, просмотр и редактирование доски при наличии прав, бросок кубов от имени персонажа, просмотр истории бросков и выход из комнаты. Для редактирования доски добавь расширения: добавление изображения, текста, фигур, рисование, перемещение токена персонажа. Стиль: аккуратная учебная UML-диаграмма на русском языке.

## PlantUML
```plantuml
@startuml
left to right direction
actor "Игрок" as Player
rectangle "ASTROLL" {
  usecase "Зарегистрироваться" as UC_Register
  usecase "Войти в систему" as UC_Login
  usecase "Управлять профилем" as UC_Profile
  usecase "Найти пользователя" as UC_Search
  usecase "Добавить/удалить друга" as UC_Friend
  usecase "Управлять персонажами" as UC_Characters
  usecase "Создать персонажа" as UC_CreateCharacter
  usecase "Редактировать лист персонажа" as UC_EditSheet
  usecase "Импортировать лист JSON" as UC_Import
  usecase "Экспортировать лист JSON" as UC_Export
  usecase "Удалить персонажа" as UC_DeleteCharacter
  usecase "Подключиться к комнате" as UC_JoinRoom
  usecase "Просматривать доску" as UC_ViewBoard
  usecase "Редактировать доску" as UC_EditBoard
  usecase "Добавить изображение" as UC_AddImage
  usecase "Добавить текст" as UC_AddText
  usecase "Добавить фигуру" as UC_AddShape
  usecase "Рисовать на доске" as UC_Draw
  usecase "Переместить токен персонажа" as UC_MoveToken
  usecase "Сделать бросок кубов" as UC_RollDice
  usecase "Просмотреть историю бросков" as UC_RollHistory
  usecase "Выйти из комнаты" as UC_LeaveRoom
}

Player --> UC_Register
Player --> UC_Login
Player --> UC_Profile
Player --> UC_Search
Player --> UC_Friend
Player --> UC_Characters
Player --> UC_JoinRoom
Player --> UC_ViewBoard
Player --> UC_EditBoard
Player --> UC_RollDice
Player --> UC_RollHistory
Player --> UC_LeaveRoom

UC_Characters <|-- UC_CreateCharacter
UC_Characters <|-- UC_EditSheet
UC_Characters <|-- UC_Import
UC_Characters <|-- UC_Export
UC_Characters <|-- UC_DeleteCharacter

UC_EditBoard <.. UC_AddImage : <<extend>>
UC_EditBoard <.. UC_AddText : <<extend>>
UC_EditBoard <.. UC_AddShape : <<extend>>
UC_EditBoard <.. UC_Draw : <<extend>>
UC_EditBoard <.. UC_MoveToken : <<extend>>
UC_RollDice ..> UC_EditSheet : <<include>>
@enduml
```
