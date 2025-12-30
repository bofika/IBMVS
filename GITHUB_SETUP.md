# GitHub Setup Guide

This guide will help you push the IBM Video Streaming Manager project to GitHub and set it up properly.

## Prerequisites

- Git installed on your system
- GitHub account created
- Repository created on GitHub (or ready to create one)

## Step 1: Initialize Git Repository

If you haven't already initialized git in your project directory:

```bash
git init
```

## Step 2: Configure Git (First Time Only)

Set your Git username and email if not already configured:

```bash
git config --global user.name "Bofika"
git config --global user.email "both.gergely@gmail.com"
```

## Step 3: Repository Already Created! ✅

Your repository is already live at: **https://github.com/bofika/IBMVS**

If you created a different repository name, update the remote URL:
```bash
git remote set-url origin https://github.com/bofika/IBMVS.git
```

## Step 4: Add All Files to Git

```bash
# Add all files to staging
git add .

# Check what will be committed
git status

# Commit with a meaningful message
git commit -m "Initial commit: IBM Video Streaming Manager v1.0.0

- Complete channel management functionality
- Video upload and management
- Player configuration
- Interactivity controls (chat, polls, Q&A)
- Real-time monitoring dashboard
- Analytics visualization
- Cross-platform support (macOS/Windows)
- Comprehensive documentation"
```

## Step 5: Connect to GitHub Repository

```bash
# Add remote repository (if not already added)
git remote add origin https://github.com/bofika/IBMVS.git

# Or update existing remote
git remote set-url origin https://github.com/bofika/IBMVS.git

# Verify remote
git remote -v
```

## Step 6: Push to GitHub

```bash
# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

If you're using SSH instead of HTTPS:
```bash
git remote set-url origin git@github.com:bofika/IBMVS.git
git push -u origin main
```

## Step 7: Verify Upload

1. Go to your repository on GitHub
2. Verify all files are present
3. Check that README.md displays correctly
4. Verify LICENSE file is recognized

## Step 8: Configure Repository Settings

### Enable Issues
1. Go to repository Settings → General
2. Under "Features", ensure "Issues" is checked

### Add Topics
1. Go to repository main page
2. Click the gear icon next to "About"
3. Add topics: `python`, `pyqt6`, `ibm`, `video-streaming`, `api-client`, `desktop-app`, `cross-platform`

### Set Up Branch Protection (Optional)
1. Go to Settings → Branches
2. Add rule for `main` branch
3. Enable:
   - Require pull request reviews before merging
   - Require status checks to pass before merging
   - Require branches to be up to date before merging

### Enable GitHub Actions
GitHub Actions should be automatically enabled. Verify:
1. Go to "Actions" tab
2. You should see the CI workflow

## Step 9: Create First Release

1. Go to repository main page
2. Click "Releases" → "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: `v1.0.0 - Initial Release`
5. Description:
   ```markdown
   ## 🎉 Initial Release
   
   First stable release of IBM Video Streaming Manager!
   
   ### Features
   - ✅ Complete channel management
   - ✅ Video upload and management
   - ✅ Player configuration
   - ✅ Interactivity controls
   - ✅ Real-time monitoring
   - ✅ Analytics dashboard
   - ✅ Cross-platform support (macOS/Windows)
   
   ### Installation
   See [README.md](README.md) for installation instructions.
   
   ### Documentation
   - [User Guide](docs/USER_GUIDE.md)
   - [API Reference](API_REFERENCE.md)
   - [Contributing Guidelines](CONTRIBUTING.md)
   ```
6. Click "Publish release"

## Step 10: Add Repository Badges

The README.md already has the correct badges. After your first release, you can add these additional badges:

```markdown
[![GitHub release](https://img.shields.io/github/release/bofika/IBMVS.svg)](https://github.com/bofika/IBMVS/releases)
[![GitHub issues](https://img.shields.io/github/issues/bofika/IBMVS.svg)](https://github.com/bofika/IBMVS/issues)
[![GitHub stars](https://img.shields.io/github/stars/bofika/IBMVS.svg)](https://github.com/bofika/IBMVS/stargazers)
```

## Step 11: Set Up Project Board (Optional)

1. Go to "Projects" tab
2. Click "New project"
3. Choose "Board" template
4. Name it "Development Roadmap"
5. Add columns: "To Do", "In Progress", "Done"
6. Add issues for pending tasks

## Troubleshooting

### Authentication Issues

If you get authentication errors:

**For HTTPS:**
```bash
# Use personal access token instead of password
# Generate token at: https://github.com/settings/tokens
```

**For SSH:**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "both.gergely@gmail.com"

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy output and add at: https://github.com/settings/keys
```

### Large Files

If you have large files (>100MB):
```bash
# Install Git LFS
brew install git-lfs  # macOS
# or download from: https://git-lfs.github.com/

# Initialize Git LFS
git lfs install

# Track large files
git lfs track "*.mp4"
git lfs track "*.mov"

# Commit .gitattributes
git add .gitattributes
git commit -m "Add Git LFS tracking"
```

### Undo Last Commit (Before Push)

```bash
# Undo commit but keep changes
git reset --soft HEAD~1

# Undo commit and discard changes
git reset --hard HEAD~1
```

## Next Steps

After pushing to GitHub:

1. ✅ Share repository link with collaborators
2. ✅ Set up continuous integration (already configured)
3. ✅ Create project documentation site (GitHub Pages)
4. ✅ Add screenshots to README
5. ✅ Create demo video
6. ✅ Announce on social media/forums
7. ✅ Submit to package indexes (PyPI)

## Useful Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Pull latest changes
git pull origin main

# View differences
git diff

# Stash changes
git stash
git stash pop

# Tag a version
git tag -a v1.0.1 -m "Bug fix release"
git push origin v1.0.1
```

## Resources

- [GitHub Docs](https://docs.github.com/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Semantic Versioning](https://semver.org/)

---

**Ready to push?** Follow the steps above and your project will be live on GitHub! 🚀