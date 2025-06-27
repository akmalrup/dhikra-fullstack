# Dhikra - Qur'an Memorization Assistant

A full-stack web application that helps users memorize the Qur'an by providing audio transcription and ayah matching capabilities using machine learning.

## 🚀 Features

- **Audio Recording**: Record Qur'anic recitations directly in the browser
- **Speech-to-Text**: Automatic transcription using OpenAI Whisper
- **Ayah Matching**: ML-powered matching of transcriptions to Qur'anic verses
- **User Authentication**: Firebase Google Sign-in integration
- **Progress Tracking**: Personal memorization statistics and history
- **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS

## 🏗️ Architecture

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python
- **Database**: PostgreSQL
- **Authentication**: Firebase Auth
- **ML Models**: OpenAI Whisper + Sentence Transformers + FAISS
- **Containerization**: Docker + Docker Compose

## 📋 Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- Firebase project with authentication enabled

## 🛠️ Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd dhikra-fullstack
```

### 2. Set Up Firebase

1. Create a Firebase project at [https://console.firebase.google.com/](https://console.firebase.google.com/)
2. Enable Google Authentication
3. Download the service account key JSON file
4. Place it as `backend/firebase-credentials.json`

### 3. Configure Environment Variables

**Backend Configuration:**
```bash
cp backend/env.example backend/.env
# Edit backend/.env with your Firebase credentials and database settings
```

**Frontend Configuration:**
```bash
cp frontend/env.example frontend/.env
# Edit frontend/.env with your Firebase web app configuration
```

### 4. Run with Docker Compose

```bash
# Start all services (database, backend, frontend)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📁 Project Structure

```
dhikra-fullstack/
├── backend/                 # FastAPI backend
│   ├── ml/                 # Machine learning components
│   │   ├── transcriber.py  # Whisper integration
│   │   └── ayah_matcher.py # Ayah matching logic
│   ├── scripts/            # ML preprocessing scripts
│   ├── data/              # Embeddings and metadata
│   ├── main.py            # FastAPI application
│   ├── database.py        # Database models
│   ├── auth.py            # Firebase authentication
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Backend container config
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── firebase.ts    # Firebase configuration
│   │   ├── api.ts         # API client
│   │   └── App.tsx        # Main application
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Frontend container config
├── docker-compose.yml      # Multi-service orchestration
├── init.sql               # Database initialization
└── README.md              # This file
```

## 🔧 Development Setup

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your configuration

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp env.example .env
# Edit .env with your Firebase configuration

# Start development server
npm start
```

### Database Setup (Local)

```bash
# Start PostgreSQL with Docker
docker run --name dhikra-postgres \
  -e POSTGRES_DB=dhikra_db \
  -e POSTGRES_USER=dhikra_user \
  -e POSTGRES_PASSWORD=dhikra_password \
  -p 5432:5432 \
  -d postgres:15
```

## 📊 ML Components

### Audio Transcription
- **Model**: OpenAI Whisper (medium)
- **Language**: Arabic speech with English translation output
- **Features**: Noise suppression, echo cancellation

### Ayah Matching
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Search**: FAISS for efficient similarity search
- **Similarity**: Cosine similarity scoring
- **Dataset**: Complete Qur'an with English translations

## 🚀 API Endpoints

### Authentication Required
All API endpoints require a valid Firebase ID token in the Authorization header:
```
Authorization: Bearer <firebase-id-token>
```

### Available Endpoints

- `POST /api/transcribe` - Transcribe audio file
- `POST /api/match_sentence` - Match text to ayah
- `GET /api/transcription_logs` - Get user's transcription history
- `GET /api/memorization_stats` - Get memorization statistics
- `GET /api/health` - Health check

## 🔐 Security

- Firebase Authentication for user management
- JWT token verification for API access
- CORS configuration for secure cross-origin requests
- Input validation and sanitization
- Database connection encryption

## 🌐 Deployment

### Production Deployment

1. Set up a cloud PostgreSQL database
2. Configure Firebase for production
3. Update environment variables
4. Build and deploy containers

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy to your cloud provider
# (Instructions vary by provider)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI Whisper for speech recognition
- Sentence Transformers for text embeddings
- Firebase for authentication services
- The open-source Qur'an translation datasets

## 📞 Support

For issues and questions:
1. Check the [Issues](issues) page
2. Review the API documentation at `/docs`
3. Ensure all environment variables are correctly configured 