# Диаграмма 19. 4+1: представление уровня разработки

## Промпт
Создай development view для ASTROLL после реструктуризации. Покажи репозитории/пакеты сервисов: frontend, api-gateway, services/auth, services/characters, services/session, services/board, services/dice, services/social, services/admin, workers/board-worker, shared-contracts. В каждом backend-сервисе слои api, application/service, domain/models, repository, tests, Dockerfile, ci.yml. shared-contracts содержит DTO и события.

## PlantUML
```plantuml
@startuml
skinparam componentStyle rectangle
left to right direction

package "frontend\nReact" as Frontend
package "api-gateway\nNginx config" as Gateway

package "services/auth" as Auth {
  component api_auth as "api"
  component app_auth as "application"
  component domain_auth as "domain/models"
  component repo_auth as "repository"
}

package "services/session" as Session {
  component api_session as "api"
  component app_session as "application"
  component domain_session as "domain/models"
  component repo_session as "repository"
}

package "services/characters" as Characters
package "services/board" as Board
package "services/dice" as Dice
package "services/social" as Social
package "services/admin" as Admin
package "workers/board-worker" as Worker

package "shared-contracts" as Contracts {
  component DTOs
  component "Domain Events" as Events
  component "API Schemas" as Schemas
}

Frontend --> Contracts
Gateway --> Auth
Gateway --> Session
Gateway --> Characters
Gateway --> Board
Gateway --> Dice
Session --> Contracts
Characters --> Contracts
Board --> Contracts
Dice --> Contracts
Social --> Contracts
Admin --> Contracts
Worker --> Contracts
@enduml
```
