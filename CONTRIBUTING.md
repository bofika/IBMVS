# Contributing to IBM Video Streaming Manager

Thank you for your interest in contributing to the IBM Video Streaming Manager! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/IBMVS.git
   cd IBMVS
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/bofika/IBMVS.git
   ```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment tool (venv or virtualenv)

### Installation

1. Create and activate a virtual environment:
   ```bash
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your IBM Video Streaming API credentials
   ```

4. Run the application:
   ```bash
   python src/main.py
   ```

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug fixes**: Fix issues reported in the issue tracker
- **New features**: Implement new functionality
- **Documentation**: Improve or add documentation
- **Tests**: Add or improve test coverage
- **Code quality**: Refactoring, optimization, or cleanup

### Workflow

1. **Create a branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes** following the coding standards

3. **Commit your changes** with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: description of what you added"
   # or
   git commit -m "Fix: description of what you fixed"
   ```

4. **Keep your branch updated** with upstream:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use type hints for function parameters and return values
- Write docstrings for all public modules, functions, classes, and methods

### Code Organization

- Keep functions small and focused (single responsibility)
- Use meaningful variable and function names
- Add comments for complex logic
- Organize imports: standard library, third-party, local modules
- Use constants for magic numbers and strings

### Example

```python
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def process_channel_data(
    channel_id: str,
    settings: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Process channel data and apply settings.
    
    Args:
        channel_id: The unique identifier for the channel
        settings: Optional dictionary of channel settings
        
    Returns:
        Dictionary containing processed channel data
        
    Raises:
        ValueError: If channel_id is invalid
    """
    if not channel_id:
        raise ValueError("Channel ID cannot be empty")
    
    logger.info(f"Processing channel: {channel_id}")
    
    # Implementation here
    result = {"channel_id": channel_id}
    
    if settings:
        result.update(settings)
    
    return result
```

## Testing Guidelines

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/test_channels.py
```

### Writing Tests

- Write unit tests for all new functionality
- Use descriptive test names: `test_should_create_channel_with_valid_data`
- Follow AAA pattern: Arrange, Act, Assert
- Mock external API calls
- Aim for >80% code coverage

### Example Test

```python
import pytest
from src.api.channels import ChannelManager


def test_should_create_channel_with_valid_data():
    # Arrange
    manager = ChannelManager(api_key="test_key")
    channel_data = {
        "title": "Test Channel",
        "description": "Test Description"
    }
    
    # Act
    result = manager.create_channel(channel_data)
    
    # Assert
    assert result["title"] == "Test Channel"
    assert "id" in result
```

## Pull Request Process

### Before Submitting

- [ ] Code follows the project's style guidelines
- [ ] All tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated (if applicable)
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up to date with main

### PR Description Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Testing
Describe how you tested your changes

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
```

### Review Process

1. At least one maintainer must review and approve the PR
2. All CI checks must pass
3. Address any requested changes
4. Once approved, a maintainer will merge the PR

## Reporting Bugs

### Before Submitting a Bug Report

- Check the [issue tracker](https://github.com/OWNER/REPO/issues) for existing reports
- Verify the bug exists in the latest version
- Collect relevant information (OS, Python version, error messages)

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g., macOS 13.0, Windows 11]
- Python Version: [e.g., 3.10.5]
- Application Version: [e.g., 1.0.0]

**Additional context**
Any other relevant information.
```

## Suggesting Enhancements

### Enhancement Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Additional context**
Any other context, mockups, or examples.
```

## Questions?

If you have questions about contributing, feel free to:

- Open an issue with the "question" label at https://github.com/bofika/IBMVS/issues
- Check the [documentation](docs/USER_GUIDE.md)

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to IBM Video Streaming Manager! 🎉