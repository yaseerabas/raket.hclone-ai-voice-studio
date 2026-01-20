# Voice Cloning SaaS Platform

A comprehensive Text-to-Speech (TTS) platform with voice cloning capabilities built using Flask, MySQL, and modern web technologies.

## 🎯 Overview

This is a full-stack SaaS application that allows users to generate realistic voice recordings from text using various voice models, including cloned voices. The platform features subscription-based access control, admin management, and a responsive web interface.

## 🏗️ Architecture

### Backend (Python/Flask)
- **Framework**: Flask 3.1.2
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **API**: RESTful endpoints with proper error handling

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Mobile-first approach
- **Modern UI**: Clean, intuitive user interface
- **Real-time Updates**: Dynamic content loading
- **Cross-browser Compatibility**: Works on all modern browsers

## 🚀 Key Features

### 🔊 Core TTS Functionality
- **Text-to-Speech Generation**: Convert text to high-quality audio
- **Multiple Voice Models**: Male, female, and children voices
- **Voice Cloning**: Upload and clone custom voices
- **Language Support**: Multi-language TTS capabilities
- **Voice Styles**: Different speaking styles (neutral, cheerful, serious, calm)

### 👤 User Management
- **User Authentication**: Secure login/logout system
- **Role-based Access**: Admin and regular user roles
- **Profile Management**: User profile customization
- **Subscription Plans**: Tiered access based on character limits

### 💰 Subscription System
- **Plan Management**: Different tiers with varying character limits
- **Usage Tracking**: Real-time character usage monitoring
- **Token-based System**: Character-based consumption model
- **Usage Statistics**: Detailed analytics dashboard

### 🎛️ Admin Panel
- **User Management**: View and manage all users
- **Subscription Control**: Create/edit subscription plans
- **Content Moderation**: Monitor voice clones and generated content
- **System Analytics**: Usage statistics and performance metrics

### 📁 File Management
- **Audio Storage**: Organized file structure for generated audio
- **Voice Library**: Personal voice clone repository
- **Auto Cleanup**: Automatic deletion of expired audio files
- **Secure Downloads**: Authenticated file access

## 📁 Project Structure

```
.
├── app/                          # Backend Flask Application
│   ├── models/                   # Database Models
│   │   ├── user.py              # User model
│   │   ├── plan.py              # Subscription plans
│   │   ├── subscription.py      # User subscriptions
│   │   ├── usage.py             # Character usage tracking
│   │   ├── audio_file.py        # Generated audio files
│   │   ├── cloned_voice.py      # Voice clones
│   │   ├── contact_message.py   # Contact form messages
│   │   └── __init__.py
│   ├── routes/                   # API Endpoints
│   │   ├── auth_routes.py       # Authentication endpoints
│   │   ├── tts_routes.py        # TTS generation endpoints
│   │   ├── admin_routes.py      # Admin panel endpoints
│   │   ├── user_routes.py       # User management endpoints
│   │   ├── subscription_routes.py # Subscription management
│   │   ├── files_routes.py      # File upload/download
│   │   ├── contact_routes.py    # Contact form handling
│   │   ├── tokens_routes.py     # Token/usage endpoints
│   │   ├── translation_routes.py # Translation services
│   │   └── __init__.py
│   ├── schemas/                  # Data Serialization
│   │   └── [various schema files]
│   ├── utils/                    # Utility Functions
│   │   ├── file_utils.py        # File handling utilities
│   │   ├── helpers.py           # General helper functions
│   │   └── voice_utils.py       # Voice processing utilities
│   ├── config.py                # Application configuration
│   └── __init__.py              # Flask app factory
├── frontend/                     # Frontend Files
│   ├── css/                     # Stylesheets
│   │   ├── dashboard.css        # Main dashboard styles
│   │   ├── admin-dashboard.css  # Admin panel styles
│   │   ├── signin.css           # Authentication pages
│   │   ├── website.css          # Public website styles
│   │   ├── cloneslibrary.css    # Voice library styles
│   │   └── subscription-users.css # Subscription management
│   ├── js/                      # JavaScript Files
│   │   ├── dashboard.js         # Main dashboard functionality
│   │   ├── admin-dashboard.js   # Admin panel scripts
│   │   ├── api-config.js        # API configuration
│   │   ├── auth-check.js        # Authentication helpers
│   │   └── [other JS files]
│   ├── assests/                 # Static Assets
│   │   └── [images, logos, etc.]
│   ├── index.html               # Landing page
│   ├── dashboard.html           # User dashboard
│   ├── admin-dashboard.html     # Admin control panel
│   ├── signin.html              # Login page
│   ├── signup.html              # Registration page
│   ├── cloneslibrary.html       # Voice clone library
│   ├── contact.html             # Contact page
│   ├── pricing.html             # Pricing information
│   └── [other HTML files]
├── uploads/                      # Uploaded Files
│   ├── cloned_voices/           # Voice clone audio files
│   └── generated_audio/         # Generated TTS audio files
├── requirements.txt              # Python dependencies
├── run.py                       # Application entry point
├── init_plans.py                # Initialize subscription plans
├── create_test_data.py          # Test data generator
└── [documentation files]
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Node.js (for development tools)
- FFmpeg (for audio processing)

### Quick Setup

1. **Clone the Repository**
```bash
git clone <repository-url>
cd copy
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Database**
```sql
CREATE DATABASE tts_saas;
-- Update app/config.py with your database credentials
```

4. **Initialize Database**
```bash
python -c "from app import create_app, db; app = create_app(); with app.app_context(): db.create_all()"
python init_plans.py
```

5. **Run the Application**
```bash
python run.py
```

The application will be available at `http://localhost:5000`

## 📊 Database Schema

### Core Tables

**Users Table**
- `id`: Primary key
- `email`: Unique user email
- `password`: Hashed password
- `user_type`: 'admin' or 'user'
- `plan_id`: Foreign key to subscription plans
- `created_at/updated_at`: Timestamps

**Plans Table**
- `id`: Primary key
- `name`: Plan name (Basic, Premium, etc.)
- `character_limit`: Maximum characters allowed
- `created_at/updated_at`: Timestamps

**Usage Table**
- `id`: Primary key
- `user_id`: Foreign key to users
- `characters_used`: Total characters consumed
- `characters_remaining`: Available characters
- `last_generated_at`: Last TTS generation timestamp

**Audio Files Table**
- `id`: Primary key
- `user_id`: Foreign key to users
- `file_path`: Path to generated audio file
- `characters_used`: Characters in generated text
- `expire_at`: Auto-deletion timestamp

**Cloned Voices Table**
- `id`: Primary key
- `user_id`: Foreign key to users
- `voice_file_path`: Path to voice sample
- `voice_name`: Custom voice name
- `created_at`: Creation timestamp

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update profile

### TTS Generation
- `POST /api/voice/generate` - Generate TTS audio
- `GET /api/voice/stream/<audio_id>` - Stream audio for preview
- `GET /api/voice/download/<audio_id>` - Download generated audio
- `GET /api/voice/languages` - Get supported languages
- `GET /api/voice/styles` - Get voice styles

### Voice Cloning
- `POST /api/voice/clone-voice` - Clone custom voice
- `GET /api/voice/voices` - List user's cloned voices
- `GET /api/voice/voices/<voice_id>/download` - Download voice clone
- `DELETE /api/voice/voices/<voice_id>` - Delete voice clone

### Admin Functions
- `GET /api/admin/users` - List all users
- `GET /api/admin/plans` - Manage subscription plans
- `GET /api/admin/analytics` - System analytics
- `GET /api/admin/audio-files` - Manage audio files

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt encryption for passwords
- **Input Validation**: Sanitized user inputs
- **File Upload Security**: Restricted file types and sizes
- **Rate Limiting**: API request limiting
- **CORS Protection**: Cross-origin resource sharing controls

## 📈 Performance Optimization

- **Database Indexing**: Optimized queries with proper indexing
- **Caching**: Strategic caching for frequently accessed data
- **File Streaming**: Efficient audio streaming for previews
- **Background Processing**: Async tasks for heavy operations
- **Connection Pooling**: Database connection optimization

## 🧪 Testing

### Automated Tests
```bash
# Run all tests
python -m pytest

# Run specific test modules
python -m pytest tests/test_auth.py
python -m pytest tests/test_tts.py
```

### Manual Testing
- Postman collection included for API testing
- Test data generation script available
- Browser-based UI testing

## 📚 Documentation

### Developer Guides
- `IMPLEMENTATION_GUIDE.md` - Technical implementation details
- `API_TESTING_GUIDE.md` - API endpoint testing procedures
- `QUICK_START.md` - Quick setup and deployment guide

### User Documentation
- In-app help system
- FAQ section
- Video tutorials (coming soon)

## 🚀 Deployment

### Production Checklist
- [ ] Set production database credentials
- [ ] Configure SSL certificates
- [ ] Set strong JWT secret key
- [ ] Configure file storage paths
- [ ] Set up monitoring and logging
- [ ] Configure backup procedures
- [ ] Set up CDN for static assets
- [ ] Configure load balancing

### Environment Variables
```bash
export DATABASE_URL=mysql+pymysql://user:pass@host/database
export JWT_SECRET=your-super-secret-key
export FLASK_ENV=production
```

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Coding Standards
- Follow PEP 8 for Python code
- Use meaningful variable names
- Write comprehensive docstrings
- Include unit tests for new features
- Maintain consistent code formatting

## 🐛 Troubleshooting

### Common Issues

**Database Connection Errors**
```bash
# Check MySQL service status
sudo systemctl status mysql

# Verify database credentials in config.py
```

**Audio Generation Failures**
```bash
# Ensure FFmpeg is installed
ffmpeg -version

# Check upload folder permissions
ls -la uploads/
```

**Authentication Issues**
```bash
# Verify JWT configuration
echo $JWT_SECRET

# Check token expiration settings
```

## 📞 Support

### Getting Help
- **Documentation**: Check the guides in `/docs`
- **Issues**: Submit GitHub issues for bugs
- **Feature Requests**: Use GitHub discussions
- **Community**: Join our Discord server

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Flask framework team for the excellent web framework
- PyDub library for audio processing capabilities
- All contributors who helped build this platform
- Open source community for various libraries and tools

---

**Built with ❤️ using Flask, MySQL, and modern web technologies**