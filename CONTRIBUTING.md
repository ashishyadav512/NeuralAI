# Contributing to AI Video Generation Platform

Thank you for your interest in contributing to the AI Video Generation Platform! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites
- Python 3.11+
- FFmpeg
- Git
- Basic understanding of Flask and video processing

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/ai-video-generator.git
   cd ai-video-generator
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r dependencies.txt
   ```

5. Set environment variables:
   ```bash
   export DATABASE_URL="sqlite:///app.db"
   export SESSION_SECRET="your-secret-key"
   ```

6. Run the application:
   ```bash
   python main.py
   ```

## Code Style

### Python Code Standards
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and under 50 lines when possible

### Code Formatting
```bash
# Install formatting tools
pip install black isort flake8

# Format code
black .
isort .

# Check style
flake8 .
```

## Project Structure

```
ai-video-generator/
├── main.py                 # Application entry point
├── app.py                  # Flask configuration
├── routes.py               # API endpoints
├── models.py               # Database models
├── utils.py                # Utility functions
├── image_generator.py      # AI image generation
├── video_generator.py      # Video creation engine
├── static/                 # Frontend assets
└── templates/              # HTML templates
```

## Contributing Guidelines

### Types of Contributions

#### Bug Reports
- Use GitHub Issues with "bug" label
- Include steps to reproduce
- Provide error messages and logs
- Specify environment details

#### Feature Requests
- Use GitHub Issues with "enhancement" label
- Describe the feature clearly
- Explain the use case and benefits
- Consider implementation complexity

#### Code Contributions
- Focus on one feature or fix per pull request
- Write tests for new functionality
- Update documentation as needed
- Follow existing code patterns

### Pull Request Process

1. Create a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. Make your changes:
   - Write clean, well-documented code
   - Add tests for new functionality
   - Update documentation

3. Test your changes:
   ```bash
   python -m pytest tests/
   ```

4. Commit with clear messages:
   ```bash
   git commit -m "Add: Enhanced particle effects for nature scenes"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/amazing-feature
   ```

6. Open a Pull Request:
   - Use the provided template
   - Link related issues
   - Describe changes clearly

## Development Areas

### High Priority
- Performance optimizations
- Enhanced visual effects
- Audio generation improvements
- Mobile responsiveness

### Medium Priority
- Additional video formats
- Batch processing
- User preferences
- Analytics dashboard

### Low Priority
- Third-party integrations
- Advanced customization
- Export options

## Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_video_generator.py

# Run with coverage
python -m pytest --cov=.
```

### Writing Tests
- Test all new functions
- Use descriptive test names
- Test both success and error cases
- Mock external dependencies

Example test structure:
```python
def test_video_generation_success():
    """Test successful video generation with valid prompt"""
    generator = FreeVideoGenerator()
    result = generator.generate_video("dancing cat")
    assert result is not None
    assert result.endswith('.mp4')
```

## Architecture Guidelines

### Video Generation Pipeline
1. **Prompt Processing** - Enhance and validate user input
2. **AI Image Generation** - Create multiple motion frames
3. **Motion Interpolation** - Blend frames with smooth transitions
4. **Visual Effects** - Apply particles, lighting, and post-processing
5. **Hook Integration** - Add viral-ready text overlays
6. **Audio Synthesis** - Generate matching background music

### Performance Considerations
- Optimize image processing operations
- Use efficient data structures
- Minimize memory usage during video creation
- Implement proper error handling and fallbacks

### Security Guidelines
- Validate all user inputs
- Sanitize file uploads
- Use environment variables for secrets
- Implement rate limiting for API endpoints

## Documentation

### Code Documentation
- Add docstrings to all public functions
- Include parameter types and return values
- Provide usage examples for complex functions

### API Documentation
- Document all endpoints
- Include request/response examples
- Specify error codes and messages

### User Documentation
- Update README for new features
- Create tutorials for complex workflows
- Maintain changelog for releases

## Release Process

### Version Numbering
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number incremented
- [ ] Changelog updated
- [ ] Performance benchmarks run
- [ ] Security review completed

## Community Guidelines

### Communication
- Be respectful and inclusive
- Provide constructive feedback
- Help newcomers get started
- Share knowledge and resources

### Issue Management
- Respond to issues promptly
- Label issues appropriately
- Close resolved issues
- Link related discussions

## Getting Help

### Documentation
- Check the README first
- Review existing issues
- Read the code comments

### Support Channels
- GitHub Issues for bugs and features
- GitHub Discussions for questions
- Code reviews for implementation help

### Mentorship
- New contributors welcome
- Pair programming available
- Code review feedback provided

## Recognition

Contributors will be recognized in:
- README contributors section
- Release notes
- Project documentation

Thank you for contributing to making AI video generation accessible to everyone!