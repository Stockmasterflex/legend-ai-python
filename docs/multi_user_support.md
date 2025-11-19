# Multi-User Support System

## Overview

Complete multi-user support with JWT authentication, user-specific watchlists, API quotas, preferences, and admin dashboard.

## Features

- 🔐 **JWT Authentication** - Secure token-based authentication
- 👤 **User Registration/Login** - Self-service account creation
- 📊 **Per-User Watchlists** - Separate watchlists for each user
- ⚡ **API Quotas** - Rate limiting per user
- ⚙️ **User Preferences** - Customizable settings
- 📈 **Usage Analytics** - Track API usage per user
- 👨‍💼 **Admin Dashboard** - User management and system stats

## Quick Start

### Register New User

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "full_name": "John Doe"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_admin": false
  }
}
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

### Use Authenticated Endpoints

```bash
# Save token
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."

# Get user profile
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"

# Add to watchlist (user-specific)
curl -X POST http://localhost:8000/api/watchlist/add \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "reason": "VCP pattern"
  }'
```

## API Endpoints

### Authentication

#### POST /api/auth/register

Register a new user account.

**Request:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "telegram_user_id": "123456789"  // Optional
}
```

**Response:**
```json
{
  "access_token": "...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {...}
}
```

#### POST /api/auth/login

Login with username or email.

**Request:**
```json
{
  "username": "johndoe",  // or email
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "api_quota": 1000,
    "api_calls_today": 45
  }
}
```

#### GET /api/auth/me

Get current user profile (requires authentication).

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "telegram_user_id": "123456789",
  "is_admin": false,
  "api_quota_per_day": 1000,
  "api_calls_count": 45,
  "created_at": "2024-01-01T00:00:00",
  "last_login_at": "2024-01-15T10:00:00"
}
```

#### GET /api/auth/usage

Get API usage statistics.

**Response:**
```json
{
  "user_id": 1,
  "username": "johndoe",
  "api_quota_per_day": 1000,
  "api_calls_today": 45,
  "remaining_calls": 955,
  "percentage_used": 4.5,
  "last_api_call": "2024-01-15T10:30:00"
}
```

#### POST /api/auth/refresh

Refresh JWT token (extends expiration).

**Response:**
```json
{
  "access_token": "...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Admin Endpoints

**Note:** All admin endpoints require admin privileges.

#### GET /api/admin/users

List all users.

**Parameters:**
- `skip` (default: 0): Pagination offset
- `limit` (default: 100): Number of results

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "is_active": true,
      "is_admin": false,
      "api_quota": 1000,
      "api_calls": 45,
      "created_at": "2024-01-01T00:00:00",
      "last_login": "2024-01-15T10:00:00"
    }
  ],
  "count": 1
}
```

#### GET /api/admin/users/{user_id}

Get specific user details.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "johndoe",
    "statistics": {
      "watchlist_count": 15,
      "alerts_count": 42
    }
  }
}
```

#### PATCH /api/admin/users/{user_id}

Update user settings.

**Request:**
```json
{
  "is_active": true,
  "is_admin": false,
  "api_quota_per_day": 2000
}
```

#### DELETE /api/admin/users/{user_id}

Delete user account.

#### GET /api/admin/stats

Get system-wide statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "users": {
      "total": 150,
      "active": 142
    },
    "patterns": {
      "total": 5420
    },
    "watchlist": {
      "total_items": 1250
    },
    "alerts": {
      "total": 3890
    },
    "api": {
      "total_calls_today": 12450
    }
  }
}
```

## Authentication Flow

### Registration & Login Flow

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       │ POST /api/auth/register
       │ {username, email, password}
       ▼
┌─────────────────────┐
│   API Server        │
│  - Validate data    │
│  - Hash password    │
│  - Create user      │
│  - Generate JWT     │
└──────┬──────────────┘
       │
       │ {access_token, user}
       ▼
┌─────────────┐
│   Client    │
│ Store token │
└──────┬──────┘
       │
       │ GET /api/auth/me
       │ Authorization: Bearer <token>
       ▼
┌─────────────────────┐
│   API Server        │
│  - Verify JWT       │
│  - Get user         │
│  - Return profile   │
└──────┬──────────────┘
       │
       │ {user profile}
       ▼
┌─────────────┐
│   Client    │
└─────────────┘
```

### Authenticated Request Flow

```
Client Request → JWT Token → Verify Token → Get User → Check Quota → Process Request
```

## User Quotas

Each user has a daily API quota to prevent abuse.

### Default Quotas

| User Type | Daily Quota |
|-----------|-------------|
| Free | 1,000 calls/day |
| Premium | 10,000 calls/day |
| Admin | Unlimited |

### Quota Management

```python
# Check quota before API call
if not await auth_service.check_rate_limit(user.id):
    raise HTTPException(status_code=429, detail="API quota exceeded")

# Track API usage
await auth_service.update_api_usage(user.id, "/api/analyze")
```

### Quota Reset

- Quotas reset daily at midnight UTC
- Counter resets automatically on first API call of new day

## User Preferences

Store user-specific preferences in JSON format.

### Example Preferences

```json
{
  "theme": "dark",
  "default_interval": "1d",
  "alert_preferences": {
    "email_enabled": true,
    "telegram_enabled": true,
    "frequency": "daily"
  },
  "watchlist_settings": {
    "auto_alerts": true,
    "confidence_threshold": 0.7
  }
}
```

### Update Preferences

```python
# In user API
user.preferences = json.dumps({
    "theme": "dark",
    "default_interval": "1d"
})
```

## User-Specific Watchlists

Each user has their own separate watchlist.

### Implementation

```python
# Watchlist model has user_id field
class Watchlist(Base):
    user_id = Column(String(100), index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"))
    ...

# Query user-specific watchlist
watchlist = await session.execute(
    select(Watchlist).where(Watchlist.user_id == user.id)
)
```

## Integration with Telegram

Link Telegram account to user profile.

### Link Telegram

```python
# During registration
user = await auth_service.create_user(
    username="johndoe",
    email="john@example.com",
    password="password",
    telegram_user_id="123456789"  # From Telegram
)

# Or update existing user
user.telegram_user_id = "123456789"
```

### Telegram Bot Integration

```python
# In Telegram bot handler
@bot.command("/start")
async def start(chat_id):
    # Get user by Telegram ID
    user = await auth_service.get_user_by_telegram_id(str(chat_id))

    if not user:
        # Prompt to register
        await send_message(chat_id, "Please register first")
    else:
        # Show user dashboard
        await show_dashboard(chat_id, user)
```

## Security Best Practices

### Password Security

- Passwords hashed with bcrypt
- Minimum 8 characters
- Never stored in plain text

### JWT Tokens

- Expire after 60 minutes (configurable)
- Include user ID and username
- Signed with secret key
- Can be refreshed before expiration

### API Keys (Optional)

- Alternative to JWT for programmatic access
- One key per user
- Can be revoked anytime

### Rate Limiting

- Per-user API quotas
- IP-based rate limiting (60 req/min)
- Prevents abuse

## Migration from Single User

### Existing Data Migration

```sql
-- Update existing watchlist items to default user
UPDATE watchlists SET user_id = 'default' WHERE user_id IS NULL;

-- Update existing alerts to default user
UPDATE alert_logs SET user_id = 'default' WHERE user_id IS NULL;
```

### Backward Compatibility

- Default user ID: "default"
- Existing endpoints work without auth (uses default user)
- Gradual migration path

## Admin Tasks

### Create Admin User

```python
# Via Python script
user = await auth_service.create_user(
    username="admin",
    email="admin@example.com",
    password="secure_admin_password"
)

# Make admin
async with db_service.get_session() as session:
    result = await session.execute(
        select(User).where(User.username == "admin")
    )
    admin = result.scalar_one()
    admin.is_admin = True
    await session.commit()
```

### Manage Users

```bash
# List users
curl http://localhost:8000/api/admin/users \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Update user quota
curl -X PATCH http://localhost:8000/api/admin/users/123 \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"api_quota_per_day": 5000}'

# Deactivate user
curl -X PATCH http://localhost:8000/api/admin/users/123 \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}'
```

## Testing

### Test Registration

```python
import requests

# Register
response = requests.post("http://localhost:8000/api/auth/register", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
})

token = response.json()["access_token"]

# Use token
response = requests.get(
    "http://localhost:8000/api/auth/me",
    headers={"Authorization": f"Bearer {token}"}
)

print(response.json())
```

## Troubleshooting

### "Invalid authentication credentials"

- Token expired (refresh token)
- Invalid token format
- User deactivated

### "API quota exceeded"

- User hit daily limit
- Wait until midnight UTC for reset
- Admin can increase quota

### "Not enough permissions"

- Endpoint requires admin privileges
- User is not admin

## Best Practices

1. **Secure Passwords** - Enforce strong password policy
2. **Token Refresh** - Refresh tokens before expiration
3. **Logout** - Clear tokens on client side
4. **HTTPS Only** - Never send tokens over HTTP
5. **Rate Limiting** - Respect API quotas
6. **Monitor Usage** - Track API usage regularly
7. **Admin Access** - Limit admin privileges
8. **Audit Logs** - Track admin actions

## Related Documentation

- [Authentication API](./api/auth.md)
- [Admin API](./api/admin.md)
- [Deployment Guide](../deploy/README.md)
- [Security Guide](./security.md)
