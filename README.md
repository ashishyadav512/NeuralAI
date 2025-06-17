
# AI Video & Image Generator

A powerful Flask-based web application that generates high-quality images and videos using advanced AI models. This application provides an intuitive interface for creating stunning visual content from text prompts.

## 🌟 Features

- **AI Image Generation**: Create high-resolution images from text descriptions
- **AI Video Generation**: Generate animated videos with motion effects and transitions
- **Multiple Generation Methods**: Utilizes various AI APIs and fallback methods
- **Gallery Management**: Browse, favorite, and manage your creations
- **Download Support**: Download individual images/videos or batch download
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Processing**: Live generation status and progress indicators

## 🛠 Technology Stack

### Backend Framework
- **Flask 3.1.1** - Lightweight WSGI web application framework
- **Flask-SQLAlchemy 3.1.1** - ORM for database operations
- **SQLAlchemy 2.0.41** - Database toolkit and ORM
- **Gunicorn 23.0.0** - Python WSGI HTTP Server for production

### AI & Machine Learning
- **OpenAI 1.86.0** - Integration with OpenAI's AI models
- **Pollinations API** - Free image generation service
- **Hugging Face Inference API** - Access to various AI models
- **Custom AI Pipeline** - Local image/video generation fallbacks

### Image & Video Processing
- **Pillow 11.2.1** - Python Imaging Library for image processing
- **OpenCV 4.11.0.86** - Computer vision and video processing
- **MoviePy 2.2.1** - Video editing and manipulation
- **NumPy 2.3.0** - Numerical computing for image arrays
- **SciPy 1.15.3** - Scientific computing for advanced effects

### Frontend Technologies
- **Bootstrap 5.3** - Responsive CSS framework
- **Font Awesome 6.4** - Icon library
- **Google Fonts** - Typography (Inter & Poppins)
- **Custom CSS** - Enhanced styling and animations
- **Vanilla JavaScript** - Interactive features and form handling

### Database
- **SQLite** - Development database (auto-configured)
- **PostgreSQL** - Production database support
- **psycopg2-binary 2.9.10** - PostgreSQL adapter

## 🚀 How It Works

### Image Generation Pipeline
1. **User Input**: User enters a descriptive text prompt
2. **API Prioritization**: System tries multiple AI services in order:
   - Pollinations API (free, no API key required)
   - Hugging Face Inference API (free tier)
   - Local procedural generation (fallback)
3. **Image Processing**: Generated images are processed and optimized
4. **Database Storage**: Metadata and file paths stored in SQLAlchemy database
5. **Gallery Display**: Images appear in responsive gallery with management options

### Video Generation Pipeline
1. **Prompt Analysis**: AI analyzes text for motion and visual elements
2. **Multi-Frame Generation**: Creates sequence of AI images for motion
3. **Advanced Animation**: Applies context-aware effects:
   - Motion blur for action scenes
   - Particle effects for magical content
   - Camera movements for dynamic feel
   - Smooth transitions between frames
4. **Post-Processing**: Adds cinematic effects, hooks, and background music
5. **Video Compilation**: Combines frames into MP4 using OpenCV and MoviePy

### Smart Content Recognition
The application uses intelligent prompt analysis to apply appropriate effects:

- **Action Scenes** (`cutting`, `fighting`, `running`) → Motion blur and impact effects
- **Nature Content** (`waterfall`, `forest`, `ocean`) → Particle effects and flowing motion
- **Dance/Party** (`dancing`, `celebration`) → Colorful effects and rhythm-based animation
- **Portrait/Character** (`person`, `face`) → Subtle breathing and enhancement effects
- **Fantasy/Magic** (`magic`, `spell`, `fantasy`) → Glowing effects and magical particles

## 📁 Project Structure

```
ai-video-generator/
├── app.py                 # Flask application initialization
├── main.py               # Application entry point
├── routes.py             # Web routes and request handlers
├── models.py             # Database models (SQLAlchemy)
├── utils.py              # Utility functions and validation
├── image_generator.py    # AI image generation pipeline
├── video_generator.py    # AI video generation pipeline
├── static/
│   ├── css/
│   │   └── style.css     # Custom styling and animations
│   ├── js/
│   │   └── main.js       # Frontend JavaScript functionality
│   ├── images/           # Generated images storage
│   └── videos/           # Generated videos storage
├── templates/
│   ├── base.html         # Base template with common elements
│   ├── index.html        # Main generation interface
│   ├── gallery.html      # Image gallery page
│   └── video_gallery.html # Video gallery page
├── instance/
│   └── aiimages.db       # SQLite database file
└── pyproject.toml        # Project dependencies
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.11 or higher
- Git for version control

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-video-generator.git
   cd ai-video-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Or if using uv:
   ```bash
   uv sync
   ```

3. **Set up environment variables** (optional)
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   export DATABASE_URL="sqlite:///aiimages.db"  # or PostgreSQL URL
   ```

4. **Initialize the database**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

5. **Run the application**
   ```bash
   python main.py
   ```
   Or for production:
   ```bash
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

The application will be available at `http://localhost:5000`

### Replit Deployment (Recommended)

This project is optimized for Replit deployment:

1. **Fork/Import** this repository to Replit
2. **Run** - Click the Run button (automatically configured)
3. **Deploy** - Use Replit's deployment feature for production

## 🎨 Features in Detail

### Image Generation
- **Multiple AI Models**: Fallback system ensures generation always succeeds
- **High Resolution**: 512x512 pixel output with quality optimization
- **Smart Prompting**: Enhanced prompts for better AI understanding
- **Instant Preview**: Real-time generation status and preview

### Video Generation
- **AI-Driven Animation**: Creates realistic motion from static concepts
- **Context-Aware Effects**: Different animations based on prompt content
- **Cinematic Quality**: Professional effects including:
  - Motion blur and camera movement
  - Particle systems and lighting effects
  - Color grading and film grain
  - Background music generation
- **Multiple Formats**: MP4 and GIF output support
- **Optimized Performance**: Efficient frame generation and compression

### Gallery Management
- **Organized Browsing**: Paginated galleries with search functionality
- **Favorites System**: Mark and filter favorite creations
- **Batch Operations**: Download multiple files at once
- **Metadata Tracking**: Generation time, prompts, and creation dates
- **Mobile Responsive**: Touch-friendly interface for mobile devices

## 📊 Database Schema

### GeneratedImage Model
```python
- id: Primary key
- prompt: Text description used for generation
- image_filename: Stored file name
- created_at: Timestamp of creation
- is_favorite: Boolean favorite status
- generation_time: Time taken to generate (seconds)
```

### GeneratedVideo Model
```python
- id: Primary key
- prompt: Text description used for generation
- video_filename: Stored file name
- created_at: Timestamp of creation
- is_favorite: Boolean favorite status
- generation_time: Time taken to generate (seconds)
- duration: Video length in seconds
```

## 🔒 Security Features

- **Input Validation**: Comprehensive prompt sanitization
- **XSS Protection**: HTML entity encoding and content filtering
- **File Security**: Secure file upload and storage handling
- **Rate Limiting**: Built-in protection against abuse
- **Environment Configuration**: Secure secret management

## 🌐 API Integration

### External Services
- **Pollinations.ai**: Primary image generation (free, unlimited)
- **Hugging Face**: Backup AI models and inference
- **Multiple Fallbacks**: Ensures 99%+ generation success rate

### Local Generation
- **Procedural Graphics**: PIL-based image creation
- **Smart Defaults**: Content-aware color schemes and layouts
- **Performance Optimized**: Fast generation for real-time feedback

## 📈 Performance Optimizations

- **Async Processing**: Non-blocking generation pipeline
- **Caching Strategy**: Intelligent file and database caching
- **Image Optimization**: Automatic compression and format selection
- **Lazy Loading**: Progressive gallery loading for better UX
- **Database Indexing**: Optimized queries for large datasets

## 🚀 Production Deployment

### Replit Deployment
1. Configure autoscale deployment
2. Set environment variables in Replit Secrets
3. Use provided `.replit` configuration
4. Deploy with one click

### Environment Variables
```bash
SESSION_SECRET=your-secure-session-key
DATABASE_URL=postgresql://user:pass@host:port/dbname  # for PostgreSQL
```

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** - For AI model integration
- **Pollinations.ai** - For free image generation API
- **Hugging Face** - For open-source AI model access
- **Flask Community** - For the excellent web framework
- **Bootstrap Team** - For responsive design components

## 📞 Support

For support, email ashishyadav.sde1@gmail.com or create an issue in this repository.

## 🔮 Future Enhancements

- [ ] User authentication and personal galleries
- [ ] Advanced video editing tools
- [ ] Real-time collaboration features
- [ ] API endpoints for external integration
- [ ] Advanced AI model fine-tuning
- [ ] Social sharing capabilities
- [ ] Custom style transfer options
- [ ] Batch processing improvements

---

**Built with ❤️ using Flask, AI, and creativity**
