# ArtBuddy - AI Art Generator & Gallery

A modern web application that allows users to generate stunning AI artwork using text prompts and share them in a community gallery.

## 🎨 Features

### AI Art Generation
- Generate unique artwork from text prompts using HuggingFace Inference API
- Customizable parameters (guidance scale, dimensions, negative prompts)
- Real-time generation progress tracking
- High-resolution image downloads

### Community Gallery
- Browse and discover artworks from the community
- Like, comment, and share functionality
- Featured artwork showcase
- Search and filter capabilities

### User Management
- User registration and authentication with JWT
- Personal gallery for each user
- Admin moderation capabilities
- Secure password handling

### Modern UI/UX
- Responsive design with Tailwind CSS
- Glass morphism effects and smooth animations
- Dark theme with gradient backgrounds
- Interactive components with Framer Motion

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- HuggingFace account and API token

### Local Development Setup

1. **Clone and navigate to the project:**
   ```bash
   cd c:\Ai_project\ArtBuddy
   ```

2. **Set up environment variables:**
   ```bash
   copy .env.example .env
   ```
   Edit `.env` and add your HuggingFace token:
   ```
   HF_TOKEN=your_huggingface_token_here
   ```

3. **Start the application:**
   ```bash
   .\start-artbuddy.ps1
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Docker Deployment

1. **Ensure Docker is running**

2. **Set up environment variables:**
   ```bash
   copy .env.example .env
   # Edit .env with your HuggingFace token
   ```

3. **Start with Docker:**
   ```bash
   .\start-docker.ps1
   ```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Lightweight database
- **HuggingFace Hub** - AI model inference
- **JWT** - Authentication tokens
- **Pillow** - Image processing

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Animations
- **Axios** - HTTP client
- **React Router** - Navigation

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Redis** - Caching and rate limiting

## 📁 Project Structure

```
ArtBuddy/
├── backend/
│   ├── models/          # Database models
│   ├── routes/          # API endpoints
│   ├── utils/           # Utility functions
│   ├── main.py          # FastAPI application
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   ├── context/     # React context
│   │   └── types/       # TypeScript types
│   └── package.json     # Node dependencies
├── static/              # Generated images storage
├── docker-compose.yml   # Docker configuration
└── README.md           # This file
```

## 🔧 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Artworks
- `POST /artworks/generate` - Generate new artwork
- `GET /artworks/gallery` - Get community gallery
- `GET /artworks/my-gallery` - Get user's artworks
- `POST /artworks/{id}/like` - Toggle artwork like
- `POST /artworks/{id}/comments` - Add comment
- `GET /artworks/{id}/comments` - Get comments

## 🎯 Usage Examples

### Generate Artwork
```python
# Example API request
{
  "title": "Sunset Landscape",
  "prompt": "A beautiful sunset over mountains with golden light",
  "guidance_scale": 7.5,
  "width": 512,
  "height": 512,
  "is_public": true
}
```

### Advanced Generation
```python
{
  "title": "Cyberpunk City",
  "prompt": "Futuristic cyberpunk cityscape with neon lights",
  "negative_prompt": "blurry, low quality, distorted",
  "guidance_scale": 10.0,
  "width": 768,
  "height": 768,
  "is_public": true
}
```

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Input validation and sanitization
- Rate limiting for API endpoints
- Environment variable configuration
- CORS protection

## 🚀 Deployment

### Production Deployment
1. Set production environment variables
2. Use Docker Compose for orchestration
3. Configure reverse proxy (nginx)
4. Set up SSL certificates
5. Configure persistent volumes

### Environment Variables
```bash
HF_TOKEN=your_production_token
SECRET_KEY=your_secure_secret_key
DATABASE_URL=sqlite:///./artbuddy.db
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the troubleshooting section below
- Open an issue on GitHub

## 🔧 Troubleshooting

### Common Issues

**HuggingFace API Errors:**
- Ensure your HF_TOKEN is valid and has API access
- Check your account quota and rate limits

**Database Issues:**
- Delete `artbuddy.db` to reset the database
- Ensure write permissions in the project directory

**Frontend Build Errors:**
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check Node.js version compatibility

**Docker Issues:**
- Ensure Docker Desktop is running
- Clear Docker cache: `docker system prune`

### Performance Tips
- Use appropriate image dimensions (512x512 for faster generation)
- Implement caching for frequently accessed artworks
- Monitor HuggingFace API usage and quotas

## 🎨 Example Prompts

Try these prompts to get started:
- "A majestic dragon soaring through a starlit sky"
- "Cyberpunk cityscape with neon lights and flying cars"
- "Peaceful zen garden with cherry blossoms"
- "Abstract geometric patterns in vibrant colors"
- "Steampunk mechanical butterfly with brass wings"# ArtBuddy
