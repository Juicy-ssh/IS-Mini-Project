# Secure File Chat Application - Comprehensive Flow & Architecture Documentation

## 📊 Application Architecture Overview

```mermaid
graph TB
    subgraph "Client Layer"
        A[Web Browser]
        B[Mobile Browser]
        C[API Clients]
    end

    subgraph "Presentation Layer"
        D[Jinja2 Templates]
        E[Bootstrap 5 UI]
        F[Custom CSS/JS]
    end

    subgraph "Application Layer"
        G[FastAPI Routes]
        H[Authentication Middleware]
        I[File Upload Handler]
        J[Admin Controllers]
    end

    subgraph "Business Logic Layer"
        K[User Management]
        L[File Operations]
        M[Security Services]
        N[CRUD Operations]
    end

    subgraph "Data Access Layer"
        O[SQLAlchemy ORM]
        P[Alembic Migrations]
        Q[SQLite/PostgreSQL]
    end

    subgraph "Infrastructure Layer"
        R[File Storage System]
        S[JWT Token Service]
        T[Email Service]
        U[Logging System]
    end

    A --> D
    B --> D
    C --> G

    D --> E
    E --> F

    F --> G
    G --> H
    G --> I
    G --> J

    H --> K
    I --> L
    J --> K
    J --> L

    K --> M
    L --> M
    M --> N

    N --> O
    O --> P
    P --> Q

    L --> R
    H --> S
    K --> T
    G --> U
```

## 🔄 Detailed Application Flow Diagrams

### 1. User Lifecycle Flow

```mermaid
stateDiagram-v2
    [*] --> VisitSite
    VisitSite --> Registration: New User
    VisitSite --> Login: Existing User

    Registration --> EmailValidation
    EmailValidation --> CredentialGeneration: Valid Email
    EmailValidation --> RegistrationError: Invalid Email

    CredentialGeneration --> DisplayCredentials
    DisplayCredentials --> Login

    Login --> CredentialValidation
    CredentialValidation --> Dashboard: Success
    CredentialValidation --> LoginError: Failure

    Dashboard --> FileOperations
    Dashboard --> AdminPanel: Admin User
    Dashboard --> Logout

    FileOperations --> Dashboard
    AdminPanel --> Dashboard
    Logout --> [*]

    RegistrationError --> Registration
    LoginError --> Login
```

### 2. File Upload & Sharing Flow

```mermaid
graph TD
    A[User Dashboard] --> B{Click Share File}
    B --> C[Expand Upload Form]

    C --> D[Select File]
    D --> E{File Selected?}
    E -->|No| C
    E -->|Yes| F[Optional: Enter Recipient]

    F --> G[Submit Upload]
    G --> H[Validate File]
    H --> I{Valid File?}
    I -->|No| J[Show Error]
    I -->|Yes| K[Generate Unique Filename]

    K --> L[Save File to Disk]
    L --> M{Create Database Record}
    M --> N{Recipient Specified?}
    N -->|Yes| O[Validate Recipient]
    N -->|No| P[Store as Private File]

    O --> Q{Recipient Exists?}
    Q -->|No| R[Show Error]
    Q -->|Yes| S[Create File Record with Recipient]

    S --> T[Create Chat Bubble]
    T --> U[Update Chat Timeline]
    U --> V[Show Success Message]
    V --> A

    P --> T
    J --> C
    R --> F
```

### 3. File Download Flow

```mermaid
graph TD
    A[Chat Dashboard/Received Page] --> B[Click Download Button]
    B --> C[Extract Saved Filename]

    C --> D[Query Database]
    D --> E{File Record Exists?}
    E -->|No| F[Show Error: File Not Found]
    E -->|Yes| G[Check Permissions]

    G --> H{User is Owner or Recipient?}
    H -->|No| I[Show Error: Access Denied]
    H -->|Yes| J[Check File on Disk]

    J --> K{File Exists on Disk?}
    K -->|No| L[Show Error: File Missing]
    K -->|Yes| M[Set Response Headers]

    M --> N[Stream File Content]
    N --> O[Log Download Event]
    O --> P[Complete Download]

    F --> A
    I --> A
    L --> A
```

### 4. Authentication & Authorization Flow

```mermaid
graph TD
    A[Incoming Request] --> B{Requires Authentication?}
    B -->|No| C[Process Request]
    B -->|Yes| D[Check for Token]

    D --> E{Token in Cookie?}
    E -->|No| F[Check Authorization Header]
    E -->|Yes| G[Extract Token from Cookie]

    F --> H{Token in Header?}
    H -->|No| I[Return 401 Unauthorized]
    H -->|Yes| J[Extract Bearer Token]

    G --> K[Validate JWT Token]
    J --> K

    K --> L{Token Valid?}
    L -->|No| M[Return 401 Unauthorized]
    L -->|Yes| N[Extract User Info]

    N --> O[Query User from Database]
    O --> P{User Exists & Active?}
    P -->|No| Q[Return 401 Unauthorized]
    P -->|Yes| R[Attach User to Request]

    R --> S{Requires Admin?}
    S -->|No| T[Process Request]
    S -->|Yes| U{User is Admin?}
    U -->|No| V[Return 403 Forbidden]
    U -->|Yes| T

    C --> W[Return Response]
    T --> W
    I --> W
    M --> W
    Q --> W
    V --> W
```

## 🗂️ Database Schema & Relationships

### Complete Entity-Relationship Diagram

```mermaid
erDiagram
    User ||--o{ File : owns
    User ||--o{ File : receives
    User {
        integer id PK
        string username UK
        string email UK
        string hashed_password
        boolean is_active
        boolean is_admin
        datetime created_at
    }
    File {
        integer id PK
        string filename
        string saved_filename UK
        integer owner_id FK
        integer recipient_id FK
        datetime uploaded_at
    }
```

### Database Migration Strategy

```mermaid
graph TD
    A[Development] --> B[Create Migration]
    B --> C[alembic revision --autogenerate]
    C --> D[Review Migration File]
    D --> E[Apply to Dev DB]
    E --> F[alembic upgrade head]

    F --> G{Ready for Staging?}
    G -->|No| H[Modify Models]
    G -->|Yes| I[Deploy to Staging]

    I --> J[Test Migration]
    J --> K{Migration Successful?}
    K -->|No| L[Fix Issues]
    K -->|Yes| M[Deploy to Production]

    H --> B
    L --> I
```

## 🔐 Security Architecture

### Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as FastAPI
    participant J as JWT Service
    participant D as Database
    participant C as Cookie Store

    U->>F: POST /login (username, password)
    F->>D: Query user by username
    D-->>F: User data
    F->>F: Verify password hash
    F->>J: Generate JWT token
    J-->>F: Signed JWT token
    F->>C: Set HTTP-only cookie
    F-->>U: Redirect to dashboard

    Note over U,C: Subsequent requests include cookie
    U->>F: GET /dashboard (with cookie)
    F->>J: Validate JWT token
    J-->>F: Decoded user info
    F->>D: Verify user exists
    D-->>F: User confirmation
    F-->>U: Render dashboard
```

### File Security Flow

```mermaid
graph TD
    A[File Upload Request] --> B[Authenticate User]
    B --> C[Validate File Type/Size]
    C --> D[Generate UUID Filename]
    D --> E[Hash Filename + Salt]
    E --> F[Store File on Disk]
    F --> G[Create Database Record]
    G --> H[Set File Permissions]
    H --> I[Generate Access Code]
    I --> J[Return Success Response]

    J --> K[File Download Request]
    K --> L[Validate User Permissions]
    L --> M[Check File Exists]
    M --> N[Stream File Content]
    N --> O[Log Access Event]
```

## 🚀 Deployment & Infrastructure

### Production Architecture

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[Nginx/HAProxy]
    end

    subgraph "Application Servers"
        AS1[FastAPI App Server 1]
        AS2[FastAPI App Server 2]
        AS3[FastAPI App Server 3]
    end

    subgraph "Database Cluster"
        DB[(PostgreSQL Primary)]
        DB1[(PostgreSQL Replica 1)]
        DB2[(PostgreSQL Replica 2)]
    end

    subgraph "File Storage"
        FS[(MinIO/S3 Bucket)]
    end

    subgraph "Cache Layer"
        Redis[(Redis Cluster)]
    end

    subgraph "Monitoring"
        Mon[Prometheus + Grafana]
        Log[ELK Stack]
    end

    Client --> LB
    LB --> AS1
    LB --> AS2
    LB --> AS3

    AS1 --> DB
    AS2 --> DB
    AS3 --> DB

    DB --> DB1
    DB --> DB2

    AS1 --> FS
    AS2 --> FS
    AS3 --> FS

    AS1 --> Redis
    AS2 --> Redis
    AS3 --> Redis

    AS1 --> Mon
    AS2 --> Mon
    AS3 --> Mon

    AS1 --> Log
    AS2 --> Log
    AS3 --> Log
```

### CI/CD Pipeline

```mermaid
graph LR
    A[Developer Push] --> B[GitHub Actions]
    B --> C[Run Tests]
    C --> D{Lint & Format}
    D -->|Pass| E[Build Docker Image]
    D -->|Fail| F[Fix Code Quality]

    E --> G[Push to Registry]
    G --> H[Deploy to Staging]
    H --> I[Integration Tests]
    I --> J{Tests Pass?}
    J -->|Yes| K[Deploy to Production]
    J -->|No| L[Fix Issues]

    K --> M[Monitor & Alert]
    F --> A
    L --> A
```

## 📈 Performance & Scalability

### Performance Monitoring Dashboard

```mermaid
graph TD
    A[Application Metrics] --> B[Response Times]
    A --> C[Error Rates]
    A --> D[Throughput]

    B --> E[API Endpoints]
    B --> F[Database Queries]
    B --> G[File Operations]

    C --> H[4xx Errors]
    C --> I[5xx Errors]

    D --> J[Requests per Second]
    D --> K[Concurrent Users]

    L[Infrastructure Metrics] --> M[CPU Usage]
    L --> N[Memory Usage]
    L --> O[Disk I/O]

    P[Business Metrics] --> Q[User Registrations]
    P --> R[File Uploads]
    P --> S[Storage Usage]
```

### Caching Strategy

```mermaid
graph TD
    A[User Request] --> B{Cache Hit?}
    B -->|Yes| C[Return Cached Response]
    B -->|No| D[Process Request]

    D --> E{Static Content?}
    E -->|Yes| F[Cache in CDN]
    E -->|No| G{Dynamic Content?}

    G -->|Yes| H{Cacheable?}
    H -->|Yes| I[Cache in Redis]
    H -->|No| J[Process Normally]

    I --> C
    F --> C
    J --> C
```

## 🔧 Maintenance & Operations

### Backup & Recovery Flow

```mermaid
graph TD
    A[Scheduled Backup] --> B[Database Dump]
    B --> C[File System Backup]
    C --> D[Encrypt Backups]
    D --> E[Upload to S3]
    E --> F[Update Backup Index]

    G[Recovery Needed] --> H[Select Backup Point]
    H --> I[Download from S3]
    I --> J[Decrypt Backup]
    J --> K[Restore Database]
    K --> L[Restore Files]
    L --> M[Verify Integrity]
    M --> N{Recovery Successful?}
    N -->|Yes| O[Resume Operations]
    N -->|No| P[Escalate to Team]
```

### Incident Response Flow

```mermaid
graph TD
    A[Alert Triggered] --> B[Assess Severity]
    B --> C{Production Impact?}
    C -->|High| D[Page On-Call Engineer]
    C -->|Low| E[Create Ticket]

    D --> F[Investigate Issue]
    E --> F

    F --> G{Identified Root Cause?}
    G -->|No| H[Gather More Data]
    G -->|Yes| I[Implement Fix]

    I --> J[Test Fix]
    J --> K{Fix Successful?}
    K -->|Yes| L[Deploy Fix]
    K -->|No| M[Revert Changes]

    L --> N[Monitor System]
    N --> O{Stable?}
    O -->|Yes| P[Post-Mortem]
    O -->|No| Q[Escalate]

    H --> F
    M --> I
    P --> A
    Q --> D
```

## 🎯 Future Enhancement Roadmap

### Phase 1: Enhanced User Experience (Q1 2024)

```mermaid
graph TD
    A[Phase 1 Goals] --> B[Email Notifications]
    A --> C[File Expiration]
    A --> D[Advanced Search]
    A --> E[File Previews]

    B --> F[SMTP Integration]
    C --> G[Cleanup Jobs]
    D --> H[Elasticsearch]
    E --> I[Thumbnail Generation]
```

### Phase 2: Advanced Features (Q2 2024)

```mermaid
graph TD
    A[Phase 2 Goals] --> B[Real-time Notifications]
    A --> C[File Versioning]
    A --> D[Role Management]
    A --> E[Cloud Storage]

    B --> F[WebSocket Support]
    C --> G[Version History]
    D --> H[RBAC System]
    E --> I[AWS S3 Integration]
```

### Phase 3: Enterprise Features (Q3 2024)

```mermaid
graph TD
    A[Phase 3 Goals] --> B[Two-Factor Auth]
    A --> C[API Rate Limiting]
    A --> D[Audit Logging]
    A --> E[Multi-tenancy]

    B --> F[TOTP Implementation]
    C --> G[Redis Rate Limiter]
    D --> H[Compliance Logs]
    E --> I[Tenant Isolation]
```

### Phase 4: Ecosystem Expansion (Q4 2024)

```mermaid
graph TD
    A[Phase 4 Goals] --> B[PWA Support]
    A --> C[Mobile Apps]
    A --> D[API Expansion]
    A --> E[Plugin System]

    B --> F[Service Worker]
    C --> G[React Native]
    D --> H[GraphQL API]
    E --> I[Plugin Architecture]
```

This comprehensive documentation provides detailed insights into the application's architecture, flows, security measures, and future development plans. The diagrams and explanations serve as a complete reference for understanding, maintaining, and extending the Secure File Chat Application.
