# Development Guide

This document provides guidelines and instructions for setting up and contributing to the AI Chief of Staff project.

## Development Environment Setup

### Prerequisites

- Node.js (v16+)
- Python (3.9+)
- Git
- A Supabase account
- A Pinecone account
- An OpenAI API key

### Backend Setup

1. Clone the repository and navigate to the backend directory:
   ```bash
   git clone https://github.com/yourusername/ai-chief-of-staff.git
   cd ai-chief-of-staff/backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and add your configuration values.

5. Run the development server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file based on `.env.example` and add your configuration values.

4. Run the development server:
   ```bash
   npm run dev
   ```

## Development Workflow

### Branch Naming Convention

- Feature: `feature/short-description`
- Bug fix: `fix/short-description`
- Documentation: `docs/short-description`
- Refactoring: `refactor/short-description`

### Commit Message Format

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Types include:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or correcting tests
- `chore`: Changes to the build process or auxiliary tools

Example:
```
feat(auth): implement JWT authentication

Added JWT token generation and validation for API endpoints.

Closes #123
```

### Pull Request Process

1. Create a new branch for your feature or bug fix.
2. Make your changes with appropriate tests.
3. Ensure all tests and linting pass.
4. Submit a pull request against the `main` branch.
5. Fill out the pull request template completely.
6. Request a review from at least one team member.
7. Address any feedback from reviewers.
8. Once approved, your PR will be merged by a maintainer.

## Testing

### Backend Testing

Run backend tests:
```bash
cd backend
pytest
```

For coverage report:
```bash
pytest --cov=. --cov-report=term
```

### Frontend Testing

Run frontend tests:
```bash
cd frontend
npm test
```

## Code Style

### Backend

- We use Black for code formatting with a line length of 88 characters.
- We use Flake8 for linting.
- Run formatting:
  ```bash
  black .
  ```

### Frontend

- We use ESLint and Prettier for JavaScript/TypeScript.
- Run linting:
  ```bash
  npm run lint
  ```
- Run formatting:
  ```bash
  npm run format
  ```

## Deployment

### CI/CD Pipeline

We use GitHub Actions for continuous integration and deployment:

1. Every push to a branch triggers linting and testing.
2. Pull requests undergo full test suites before they can be merged.
3. Merges to `main` trigger automatic deployment to the development environment.
4. Tagged releases trigger deployment to production.

### Environment Variables

- Development: Set in GitHub repository secrets for CI/CD.
- Production: Set in the production environment (Vercel/Heroku).

## Documentation

- API documentation is generated using FastAPI's built-in Swagger UI.
- Component documentation should be maintained alongside the code.
- Update this guide when introducing significant changes to the development workflow. 