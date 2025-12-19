# Módulo de Autenticación - Arquitectura Hexagonal

Este módulo implementa un sistema de autenticación siguiendo los principios de **Arquitectura Hexagonal** (Puertos y Adaptadores). El objetivo es aislar la lógica de negocio (Dominio) de los detalles técnicos (Infraestructura) y de los puntos de entrada (API).

## Estructura del Proyecto

```text
hexagonal/auth/
├── domain/                 # Núcleo de la lógica de negocio (Independiente)
│   ├── models/             # Entidades de dominio (User, Token)
│   ├── ports/              # Interfaces (Puertos de salida: Repositorios, Servicios Externos)
│   └── services/           # Lógica de dominio compleja
├── application/            # Casos de uso y orquestación
│   ├── use_cases/          # Implementación de acciones (Register, Login, etc.)
│   └── dtos/               # Objetos de transferencia de datos (Request/Response)
├── infrastructure/         # Detalles de implementación (Adaptadores)
│   ├── adapters/
│   │   ├── persistence/    # Implementación de base de datos (SQLAlchemy/SQLModel)
│   │   ├── external/       # Implementación de servicios externos (Google OAuth)
│   │   └── security/       # Implementación de JWT y Hashing
│   └── config/             # Configuración de entorno y base de datos
├── api/                    # Adaptador Primario (Punto de entrada)
│   ├── v1/
│   │   ├── endpoints/      # Definición de rutas FastAPI
│   │   └── dependencies.py # Inyección de dependencias
│   └── main.py             # Punto de entrada de la aplicación
└── README.md               # Documentación del módulo
```

## Endpoints a Implementar

| Método | Endpoint         | Descripción                                       | Seguridad             |
| :----- | :--------------- | :------------------------------------------------ | :-------------------- |
| `POST` | `/auth/register` | Registro de nuevos usuarios                       | Público               |
| `POST` | `/auth/login`    | Autenticación con email/password                  | Público               |
| `POST` | `/auth/refresh`  | Renovación de Access Token mediante Refresh Token | Público               |
| `GET`  | `/auth/google`   | Inicio de sesión/Registro con Google OAuth        | Público               |
| `GET`  | `/auth/me`       | Obtener información del usuario actual            | Protegido (JWT)       |
| `GET`  | `/users`         | Listar todos los usuarios registrados             | Protegido (Admin/JWT) |

## Flujo de Trabajo (Hexagonal)

1.  **API (Adaptador Primario):** Recibe la petición HTTP, valida el DTO de entrada y llama al **Caso de Uso** correspondiente.
2.  **Application (Casos de Uso):** Orquestan la lógica. Llaman al **Dominio** para reglas de negocio y usan los **Puertos** (interfaces) para interactuar con el mundo exterior.
3.  **Domain (Core):** Contiene las reglas esenciales. No conoce ni la base de datos ni FastAPI.
4.  **Infrastructure (Adaptadores Secundarios):** Implementan las interfaces definidas en los **Puertos**. Aquí reside el código de SQLModel, llamadas a Google API, etc.

## Ventajas de este enfoque

- **Testabilidad:** Se puede testear la lógica de negocio sin levantar una base de datos o un servidor web.
- **Mantenibilidad:** Cambiar de base de datos (ej. de SQLite a PostgreSQL) o de proveedor de OAuth solo afecta a la capa de `infrastructure`.
- **Desacoplamiento:** El dominio es puro y no tiene dependencias de frameworks externos.
