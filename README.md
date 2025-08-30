# NovelNest

Your ultimate reading companion. Track, discover, and never miss a chapter again. Built with FastAPI for speed and scalability. More exciting features coming soon.

## Features

### Authentication & Authorization
- JWT-based authentication system
- Role-based access control (Admin/User roles)
- Secure password hashing with bcrypt
- OAuth2 password bearer token authentication

### User Management
- User registration and login
- Admin user creation (admin-only)
- User profile management (view, update, delete)
- Permission-based operations (users can only modify their own data)

### Novel Pieces Management
- CRUD operations for novel pieces
- Search functionality by title
- Admin-only piece creation, update, and deletion
- Public read access with pagination

### Like System
- Toggle like/unlike functionality
- Like count tracking
- View personal likes
- View likes for specific pieces
- Real-time like count updates

### Database Integration
- PostgreSQL database with SQLAlchemy ORM
- Properly structured database models with relationships

## Technical Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT with passlib
- **Validation**: Pydantic
- **Password Hashing**: bcrypt
- **Python Version**: 3.13+

## API Endpoints

### Authentication
- `POST /login` - User login

### Users
- `GET /users/` - Get all users (paginated)
- `GET /users/{id}` - Get user by ID
- `POST /users/` - Create new user
- `POST /users/admin` - Create admin user (admin-only)
- `PUT /users/{id}` - Update user (self or admin)
- `DELETE /users/{id}` - Delete user (self or admin)

### Pieces
- `GET /pieces/` - Get all pieces (with search and pagination)
- `GET /pieces/{id}` - Get piece by ID
- `POST /pieces/` - Create piece (admin-only)
- `PUT /pieces/{id}` - Update piece (admin-only)
- `DELETE /pieces/{id}` - Delete piece (admin-only)

### Likes
- `POST /likes/` - Toggle like/unlike
- `GET /likes/count/{piece_id}` - Get like count for piece
- `GET /likes/my-likes` - Get current user's likes
- `GET /likes/{piece_id}` - Get all likes for a piece

## Installation

1. Clone the repository
2. Install dependencies with Poetry:
   ```bash
   poetry install
   ```
3. Set up environment variables in `.env` file:
   ```
   DB_HOSTNAME=localhost
   DB_PORT=5432
   DB_PASSWORD=your_password
   DB_NAME=novelnest
   DB_USERNAME=your_username
   SECRET_KEY=your_secret_key
   ALGO=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
4. Run the application:
   ```bash
   fastapi dev main.py
   ```

## Current Features

- **User Authentication System**: Complete JWT-based auth with role management
- **CRUD Operations**: Full Create, Read, Update, Delete for users and pieces
- **Like System**: Interactive like/unlike functionality with real-time counts
- **Role-Based Access**: Admin and user roles with appropriate permissions
- **Search & Pagination**: Efficient data retrieval with filtering
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Poetry Package Management**: Modern dependency management and virtual environment handling
- **Alembic Migrations**: Database migration management with Alembic

## Future Plans

- **Testing Suite**: Comprehensive unit and integration tests
- **Comments System**: Add commenting functionality for pieces
- **File Upload**: Support for cover images
- **Reading Progress**: Track user reading progress and bookmarks
- **User Statistics**: User statistics and reading analytics
- **Advanced Search**: Full-text search capabilities with filters by date, author, genre
- **Notifications**: Real-time notifications for likes, comments, and new content
- **External API Integration**: Fetch book data from MyAnimeList API or similar
- **Recommendation Engine**: Recommendation engine based on user preferences
- **Payment Integration**: Payment integration for premium features
- **Caching**: Redis integration for improved performance
- **API Rate Limiting**: Implement rate limiting for API endpoints
- **Deployment**: Production deployment with Docker and CI/CD pipelines