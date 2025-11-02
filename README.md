# Secure File Chat Application

A modern, immersive chat-like file sharing platform built with FastAPI, SQLAlchemy, and Jinja2 templates. Experience secure file sharing through an intuitive messaging interface where files appear as conversation bubbles with timestamps and sender information, all wrapped in a beautiful, centered, immersive UI design.

## 🚀 Features

### Core Functionality
- **User Registration & Authentication**: Secure user registration with email-based accounts and automatic credential generation
- **File Upload & Management**: Upload files with automatic secure storage and unique filename generation
- **Secure File Sharing**: Share files with recipients using unique access codes or direct username sharing
- **Chat-like Dashboard**: Modern messaging interface displaying files as conversation bubbles with chronological ordering
- **Unified File View**: See both sent and received files in a single, immersive chat timeline
- **Admin Panel**: Comprehensive administrative dashboard for system management and oversight
- **Real-time Notifications**: Instant feedback on file operations with smooth animations

### Security Features
- **Password Hashing**: SHA256-based password hashing for user credentials with secure key generation
- **Unique Access Codes**: 10-character alphanumeric codes for secure file access
- **Session Management**: Secure JWT-based authentication with configurable expiration
- **File Encryption**: Secure file storage with cryptographically secure unique filenames
- **Input Validation**: Comprehensive form validation and sanitization with Pydantic schemas
- **Database Migrations**: Alembic-powered database versioning for safe schema changes

### User Experience
- **Immersive Chat Interface**: Files appear as message bubbles with timestamps, sender info, and smooth animations
- **Centered Design**: Beautiful, immersive layout with glassmorphism effects and gradient backgrounds
- **Responsive Design**: Mobile-first interface that adapts seamlessly across all devices
- **Glassmorphism Effects**: Modern glass-like card designs with backdrop blur and transparency
- **Gradient Backgrounds**: Stunning visual experience with carefully crafted color schemes
- **Intuitive Navigation**: Clean, easy-to-use interface with contextual navigation
- **Real-time Feedback**: Instant success/error notifications with animated transitions
- **Smooth Animations**: Fade-in effects, hover states, and micro-interactions for enhanced UX

## 🛠️ Technology Stack

### Backend
- **FastAPI**: High-performance async web framework with automatic OpenAPI documentation
- **SQLAlchemy**: Powerful ORM for database operations with relationship management
- **SQLite**: Lightweight, file-based database for development with production-ready alternatives
- **Alembic**: Database migration tool for version control and schema management
- **Uvicorn**: Production-ready ASGI server with hot reload capabilities
- **Jinja2**: Flexible template engine for server-side rendering

### Frontend
- **Bootstrap 5**: Modern responsive CSS framework with utility classes
- **Custom CSS**: Hand-crafted glassmorphism and gradient effects with CSS variables
- **JavaScript**: Vanilla JS for interactive form handling and dynamic UI updates
- **Bootstrap Icons**: Comprehensive icon library for consistent visual language
- **Google Fonts**: Inter font family for modern, readable typography

### Security & Utilities
- **Passlib**: Robust password hashing utilities with multiple algorithm support
- **Python-JOSE**: Industry-standard JWT token handling and validation
- **Secrets**: Cryptographically secure random generation for codes and tokens
- **Hashlib**: SHA256 hashing implementation for password security
- **Pydantic**: Data validation and serialization with type hints
- **Email Validator**: Comprehensive email validation for user registration

## 📋 Prerequisites

- **Python**: 3.8 or higher (3.11 recommended for optimal performance)
- **pip**: Latest version of Python package manager
- **Virtual Environment**: Isolated Python environment (venv recommended)
- **Git**: Version control system for cloning and contribution

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd mini-project-is
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv myenv
myenv\Scripts\activate

# Linux/Mac
python -m venv myenv
source myenv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with the following settings:
```env
# Security Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL=sqlite:///./app.db

# File Storage Configuration
UPLOAD_DIR=uploaded_files
```

### 5. Initialize Database with Migrations
```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration to create database tables
alembic upgrade head
```

## 🚀 Running the Application

### Development Mode
```bash
uvicorn main:app --reload --port 3000
```

### Production Mode
```bash
# Using environment variables
export SECRET_KEY="your-production-secret-key"
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Access the application at: `http://localhost:3000`

## 📖 Comprehensive Usage Guide

### User Registration Process
1. **Navigate to Registration**: Visit `/register` from the home page
2. **Enter Email**: Provide a valid email address for account creation
3. **Automatic Credential Generation**: System generates unique username and 10-character access code
4. **Credential Storage**: Save the displayed username and key securely for login

### User Authentication Flow
1. **Access Login Page**: Navigate to `/login`
2. **Enter Credentials**: Input generated username and access code
3. **Secure Authentication**: JWT token created and stored in HTTP-only cookie
4. **Dashboard Access**: Automatic redirect to personalized dashboard

### File Upload & Chat Interface
1. **Access Dashboard**: Navigate to `/dashboard` after authentication
2. **Expand Upload Form**: Click "Share File" button to reveal upload interface
3. **File Selection**: Choose file from local system with drag-and-drop support
4. **Optional Recipient**: Enter recipient username for direct sharing or leave empty
5. **Secure Upload**: File processed with unique filename generation and database storage
6. **Chat Bubble Creation**: File appears as animated message bubble in chat timeline

### Viewing File Conversations
- **Unified Timeline**: Dashboard displays all file interactions chronologically
  - **Blue Bubbles**: Files you've shared (sent messages)
  - **Green Bubbles**: Files shared with you (received messages)
  - **Timestamps**: Precise upload times with human-readable formatting
  - **Sender Information**: Clear identification of file originators
  - **Download Actions**: Direct download buttons within each bubble

### Advanced File Sharing Methods
1. **Direct Username Sharing**: Enter recipient username during upload for immediate sharing
2. **Access Code Sharing**: Copy generated codes for external sharing
3. **Public Access**: Recipients can access files via `/receive/{code}` endpoint
4. **Secure Downloads**: All downloads require authentication and proper permissions

### Received Files Management
- **Dedicated View**: Access `/received` for focused view of incoming files
- **Chat Format**: Consistent bubble interface for received files
- **Download Tracking**: Easy access to all files shared with you
- **Sender Context**: Clear visibility of who shared each file

### Administrative Functions
1. **Admin Access**: Navigate to `/admin` (admin users only)
2. **User Management**: View, monitor, and delete user accounts
3. **File Oversight**: Monitor all uploaded files and sharing activities
4. **System Statistics**: Comprehensive overview of platform usage
5. **Resource Management**: Delete inappropriate content or inactive accounts

## 🗄️ Database Schema & Architecture

### Users Table Structure
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Files Table Structure
```sql
CREATE TABLE files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename VARCHAR(255) NOT NULL,
    saved_filename VARCHAR(255) UNIQUE NOT NULL,
    owner_id INTEGER NOT NULL,
    recipient_id INTEGER,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES users(id) ON DELETE SET NULL
);
```

### Database Relationships
- **One-to-Many**: Users → Files (owner relationship)
- **One-to-Many**: Users → Files (recipient relationship)
- **Self-Referential**: Files can reference users as both owners and recipients

## 🔌 Complete API Reference

### Authentication Endpoints
- `GET /` - Landing page with immersive design
- `GET /register` - User registration form
- `POST /register` - Process registration with automatic credential generation
- `GET /login` - Authentication form with error handling
- `POST /login` - Process login with JWT token creation
- `POST /token` - API token endpoint for programmatic access
- `GET /logout` - Logout endpoint that clears authentication cookies

### File Management Endpoints
- `GET /dashboard` - Main chat interface with file timeline
- `POST /upload/` - Secure file upload with recipient specification
- `GET /download/{saved_filename}` - Authenticated file download
- `GET /received` - Dedicated received files view
- `GET /received-files/` - API endpoint for received files list

### Administrative Endpoints
- `GET /admin` - Administrative dashboard (admin only)
- `GET /admin/users/` - List all users (admin only)
- `GET /admin/files/` - List all files (admin only)
- `DELETE /admin/users/{user_id}` - Delete user account (admin only)
- `DELETE /admin/files/{file_id}` - Delete file record (admin only)

## 🔐 Advanced Security Implementation

### Password Security Architecture
- **SHA256 Hashing**: Industry-standard cryptographic hashing for passwords
- **Salt Integration**: Automatic salt generation for enhanced security
- **Key Generation**: 10-character alphanumeric access codes using cryptographically secure methods
- **Token Expiration**: Configurable JWT token lifetimes with automatic cleanup

### File Security Measures
- **Unique Filename Generation**: UUID-based filenames prevent enumeration attacks
- **Secure Storage**: Files stored outside web root with restricted access
- **Permission Validation**: Multi-layer authorization checks for file access
- **Metadata Protection**: File information secured in database with proper relationships

### Input Validation & Sanitization
- **Pydantic Schemas**: Comprehensive data validation with type hints
- **Email Validation**: RFC-compliant email address verification
- **SQL Injection Prevention**: Parameterized queries with SQLAlchemy ORM
- **XSS Protection**: Template escaping and content sanitization
- **File Type Validation**: Extension and MIME type checking

### Session Management
- **HTTP-Only Cookies**: Secure token storage preventing JavaScript access
- **JWT Implementation**: Stateless authentication with cryptographic signing
- **Expiration Handling**: Automatic token invalidation and re-authentication
- **Cross-Site Request Forgery**: Built-in CSRF protection with FastAPI

## 🧪 Testing & Quality Assurance

### Manual Testing Checklist
- [ ] User registration with valid/invalid email formats
- [ ] Login authentication with correct/incorrect credentials
- [ ] File upload functionality with various file types and sizes
- [ ] Direct file sharing with existing/non-existing usernames
- [ ] Chat bubble creation and chronological ordering
- [ ] File download functionality from chat bubbles
- [ ] Timestamp display and formatting accuracy
- [ ] Admin panel access and permission restrictions
- [ ] Responsive design across mobile/tablet/desktop
- [ ] Animation performance and smooth transitions
- [ ] Error handling for network issues and invalid operations

### API Testing Examples
```bash
# User Registration
curl -X POST "http://localhost:3000/create-user/" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# API Authentication
curl -X POST "http://localhost:3000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user123&password=ABC123DEF4"

# File Upload (requires authentication)
curl -X POST "http://localhost:3000/upload/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@document.pdf" \
  -F "recipient_username=friend456"

# List Received Files
curl -X GET "http://localhost:3000/received-files/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Automated Testing Structure
```python
# Example test structure
def test_user_registration():
    # Test successful registration
    # Test duplicate email handling
    # Test invalid email formats

def test_file_upload():
    # Test successful upload
    # Test large file handling
    # Test unauthorized access

def test_chat_interface():
    # Test bubble rendering
    # Test chronological ordering
    # Test download functionality
```

## 🚀 Deployment & Production

### Docker Containerization
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create upload directory
RUN mkdir -p uploaded_files

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Environment Setup
```bash
# Environment variables for production
export SECRET_KEY="your-production-secret-key-here"
DATABASE_URL="postgresql://user:password@host:port/database"
ACCESS_TOKEN_EXPIRE_MINUTES=60
UPLOAD_DIR="/var/app/uploads"

# Using Gunicorn for production serving
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Nginx Reverse Proxy Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/your/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 🤝 Development & Contribution

### Development Setup
1. **Fork Repository**: Create your own fork of the project
2. **Create Feature Branch**: `git checkout -b feature/your-feature-name`
3. **Install Development Dependencies**: `pip install -r requirements-dev.txt`
4. **Run Tests**: `pytest` or `python -m pytest`
5. **Code Formatting**: `black .` and `isort .`
6. **Type Checking**: `mypy .`

### Code Quality Standards
- **PEP 8 Compliance**: Follow Python style guidelines
- **Type Hints**: Use comprehensive type annotations
- **Docstrings**: Document all functions and classes
- **Testing**: Maintain >80% test coverage
- **Security**: Regular security audits and updates

### Commit Message Guidelines
```
feat: add user profile customization
fix: resolve file upload timeout issue
docs: update API documentation
style: format code with black
refactor: simplify authentication logic
test: add integration tests for file sharing
```

### Pull Request Process
1. **Update Documentation**: Ensure README and docstrings are current
2. **Add Tests**: Include tests for new functionality
3. **Code Review**: Request review from maintainers
4. **Merge**: Squash and merge after approval

## 📊 Monitoring & Analytics

### Application Metrics
- **User Registration**: Track signup conversion rates
- **File Upload Statistics**: Monitor upload frequency and sizes
- **Authentication Success**: Track login success/failure rates
- **Performance Metrics**: Response times and error rates

### Logging Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Error Tracking
- **Sentry Integration**: Real-time error monitoring and alerting
- **Log Aggregation**: Centralized logging with ELK stack
- **Performance Monitoring**: APM tools for bottleneck identification

## 🆘 Troubleshooting Guide

### Common Issues & Solutions

**Database Connection Errors**
```bash
# Check database file permissions
ls -la app.db

# Reinitialize database
rm app.db
alembic upgrade head
```

**File Upload Failures**
```bash
# Check upload directory permissions
ls -la uploaded_files/

# Verify directory creation
mkdir -p uploaded_files
chmod 755 uploaded_files
```

**Authentication Problems**
```bash
# Verify JWT secret key
echo $SECRET_KEY

# Check token expiration
# Default: 30 minutes
```

**Performance Issues**
```bash
# Profile application performance
python -m cProfile main.py

# Check database query performance
# Enable SQLAlchemy echo=True in config
```

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug mode
uvicorn main:app --reload --log-level debug
```

## 📈 Future Roadmap

### Phase 1: Enhanced User Experience
- [ ] Email notifications for file sharing events
- [ ] File expiration and automatic cleanup system
- [ ] Advanced search and filtering in chat interface
- [ ] File preview functionality for images/documents

### Phase 2: Advanced Features
- [ ] Real-time notifications with WebSocket support
- [ ] File versioning and history tracking
- [ ] Advanced user roles and permission management
- [ ] Integration with cloud storage providers (AWS S3, Google Cloud)

### Phase 3: Enterprise Features
- [ ] Two-factor authentication (2FA) implementation
- [ ] API rate limiting and abuse prevention
- [ ] Comprehensive audit logging and compliance reporting
- [ ] Multi-tenant architecture for enterprise deployments

### Phase 4: Mobile & Ecosystem
- [ ] Progressive Web App (PWA) for mobile experience
- [ ] Native mobile applications (React Native/Flutter)
- [ ] REST API expansion for third-party integrations
- [ ] Plugin system for extensibility

### Technical Improvements
- [ ] GraphQL API implementation
- [ ] Microservices architecture consideration
- [ ] Container orchestration with Kubernetes
- [ ] CI/CD pipeline with automated testing and deployment

## 📄 License & Legal

### MIT License
```
Copyright (c) 2024 Secure File Chat Application

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Security Considerations
- Regular security audits and dependency updates
- Responsible disclosure policy for security vulnerabilities
- GDPR compliance for data protection and privacy
- Secure coding practices and OWASP guidelines adherence

### Support & Community
- **GitHub Issues**: Bug reports and feature requests
- **Documentation Wiki**: Community-contributed guides and tutorials
- **Discord Community**: Real-time support and discussion
- **Professional Support**: Enterprise support options available

---

**Built with ❤️ for secure, beautiful, and immersive file sharing experiences**
