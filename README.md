# FastAPI Expense Tracker API 💰

A production-ready **FastAPI-based Expense Tracking API** with comprehensive CRUD operations, database integration, and robust testing.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.118+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLModel](https://img.shields.io/badge/SQLModel-latest-orange.svg)](https://sqlmodel.tiangolo.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

---

## 🚀 Features

### Core Functionality
- 💰 **Expense Management** - Full CRUD operations for expenses
- 💱 **Currency Support** - Multi-currency expense tracking
- 👤 **User Management** - User-based expense organization
- 🔍 **Advanced Filtering** - Category-based expense filtering
- 📊 **Data Validation** - Comprehensive input validation with Pydantic

### Production Features
- 🗄️ **Database Integration** - SQLModel with SQLite (PostgreSQL ready)
- 🔧 **Configuration Management** - Environment-based settings
- 📝 **Structured Logging** - Centralized logging configuration
- 🧪 **Comprehensive Testing** - Unit tests with pytest
- 📋 **Code Quality** - Linting, formatting, and type checking
- 📚 **API Documentation** - Interactive Swagger UI and ReDoc
- 🐳 **CI/CD Ready** - GitHub Actions workflow included

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- pip or poetry

### Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd fastapi_project

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Development Setup

```bash
# Install development dependencies
make install

# Run code quality checks
make lint
make typecheck
make format

# Run tests
make test

# Run all checks
make all
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=sqlite:///./expense_tracker.db
# For PostgreSQL: postgresql://user:password@localhost/dbname

# Application Settings
LOG_LEVEL=INFO
```

### Database Setup

The application automatically creates database tables on startup. For production:

```bash
# Use PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/expense_tracker
```

---

## ▶️ Running the Application

### Development

```bash
PYTHONPATH=. uvicorn app.main:app --reload
```

### Production

```bash
# Using Gunicorn (recommended)
PYTHONPATH=. gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Or with Uvicorn
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**API Documentation:**
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 API Usage Examples

### Currencies

```bash
# List all currencies
curl -X GET "http://localhost:8000/currencies/"

# Create a new currency
curl -X POST "http://localhost:8000/currencies/" \
  -H "Content-Type: application/json" \
  -d '{
    "currency_id": "USD",
    "name": "US Dollar",
    "is_active": true
  }'
```

### Expenses

```bash
# Get all expenses
curl -X GET "http://localhost:8000/expenses/"

# Create an expense
curl -X POST "http://localhost:8000/expenses/" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 25.50,
    "category": "food",
    "vendor": "Restaurant ABC",
    "user_id": "user123",
    "currency_id": "USD"
  }'

# Update an expense
curl -X PUT "http://localhost:8000/expenses/{expense_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 30.00,
    "category": "food",
    "vendor": "Restaurant XYZ",
    "user_id": "user123",
    "currency_id": "USD"
  }'

# Delete an expense
curl -X DELETE "http://localhost:8000/expenses/{expense_id}"
```

---

## 📂 Project Structure

```
fastapi_project/
├── app/
│   ├── main.py                  # Application entry point
│   ├── core/
│   │   ├── config.py            # Configuration management
│   │   └── logging.py           # Logging setup
│   ├── db/
│   │   ├── engine.py            # Database engine & sessions
│   │   └── lifespan.py          # Application lifecycle
│   ├── models/
│   │   ├── currency.py          # Currency database model
│   │   ├── expense.py           # Expense database model
│   │   └── user.py              # User database model
│   ├── schemas/
│   │   ├── currency.py          # Currency API schemas
│   │   └── expense.py           # Expense API schemas
│   └── routers/
│       ├── currencies.py        # Currency endpoints
│       └── expenses.py          # Expense endpoints
├── tests/
│   └── test_main.py            # API tests
├── requirements.txt            # Production dependencies
├── Makefile                   # Development commands
├── pyproject.toml            # Tool configurations
└── README.md                 # This file
```

---

## 🛠️ Technology Stack

### Core Framework
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework
- **[SQLModel](https://sqlmodel.tiangolo.com/)** - SQL databases with Python types
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation and settings
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI server implementation

### Development Tools
- **[Pytest](https://pytest.org/)** - Testing framework
- **[Black](https://black.readthedocs.io/)** - Code formatter
- **[Ruff](https://docs.astral.sh/ruff/)** - Fast Python linter
- **[MyPy](https://mypy.readthedocs.io/)** - Static type checker
- **[isort](https://pycqa.github.io/isort/)** - Import sorter

---

## 📋 API Endpoints

### Expenses
- `GET /expenses/` - List all expenses
- `POST /expenses/` - Create new expense
- `GET /expenses/{expense_id}` - Get expense by ID
- `PUT /expenses/{expense_id}` - Update expense
- `DELETE /expenses/{expense_id}` - Delete expense

### Currencies
- `GET /currencies/` - List all active currencies
- `POST /currencies/` - Create new currency

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_main.py -v
```

### Test Coverage

The test suite covers:
- API endpoint functionality
- Database operations
- Error handling
- Data validation

---

## 🚀 Deployment

### Docker Deployment

```dockerfile
# Dockerfile example
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup

```bash
# Production environment variables
export DATABASE_URL="postgresql://user:password@db:5432/expense_tracker"
export LOG_LEVEL="WARNING"
```

---

## 🔧 Development

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Type checking
make typecheck

# Run all quality checks
make all
```

### Adding New Features

1. Create database models in `app/models/`
2. Define API schemas in `app/schemas/`
3. Implement endpoints in `app/routers/`
4. Add tests in `tests/`
5. Update documentation

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write tests for new features
- Update documentation as needed
- Ensure all quality checks pass

---

## 📞 Support

For support and questions:

- 📧 Email: [devspace0201@gmail.com]
- 🐛 Issues: [GitHub Issues](https://github.com/utkarsh-0201/fastapi_project/issues)
- 📖 Documentation: [API Docs](http://localhost:8000/docs)

---

**Built with ❤️ using FastAPI and modern Python practices**