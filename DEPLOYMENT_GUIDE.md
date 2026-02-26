# 🚀 AI Resume Analyzer - Complete Deployment Guide

This guide covers deploying your AI Resume Analyzer to multiple platforms globally.

## Table of Contents

1. [Quick Start - Streamlit Cloud](#quick-start---streamlit-cloud)
2. [Docker Deployment](#docker-deployment)
3. [Platform-Specific Guides](#platform-specific-guides)
4. [Production Setup](#production-setup)
5. [Troubleshooting](#troubleshooting)

---

## Quick Start - Streamlit Cloud

### ⭐ **EASIEST & FREE** - Recommended for Everyone

Streamlit Cloud is the fastest way to deploy globally. It's completely free and takes 2 minutes.

### Step 1: Prepare Your Repository

```bash
# Initialize git
git init
git add .
git commit -m "🚀 AI Resume Analyzer - Global Deployment"

# Create GitHub repository at https://github.com/new
# Then push:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-resume-analyzer.git
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to **https://share.streamlit.io**
2. Click **"New app"**
3. Select:
   - Repository: `ai-resume-analyzer`
   - Branch: `main`
   - Main file path: `ai_resume_analyzer_global.py`
4. Click **"Deploy"**

### Step 3: Share Your App

Your app will be live at:
```
https://yourusername-ai-resume-analyzer.streamlit.app
```

**Features:**
- ✅ Free hosting
- ✅ SSL/HTTPS included
- ✅ Global CDN
- ✅ Auto-scaling
- ✅ Custom domain support
- ✅ Real-time updates (push to GitHub = auto-deploy)

---

## Docker Deployment

### Local Docker Setup

#### Linux/macOS:
```bash
chmod +x deploy.sh
./deploy.sh
```

#### Windows:
```bash
deploy.bat
```

Or manually:
```bash
docker-compose up -d
```

Your app will be at: `http://localhost:8501`

### Deploy Docker to Cloud

Using Docker with cloud providers:

#### AWS EC2:
```bash
# SSH into your EC2 instance
ssh -i your-key.pem ubuntu@your-instance.com

# Clone repository
git clone https://github.com/YOUR_USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer

# Run Docker
docker-compose up -d
```

Access at: `http://your-server-ip:8501`

#### Google Cloud Run:
```bash
# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy ai-resume-analyzer \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

#### Azure Container Instances:
```bash
az container create \
    --resource-group myResourceGroup \
    --name ai-resume-analyzer \
    --image YOUR_REGISTRY/ai-resume-analyzer:latest \
    --ports 8501 \
    --environment-variables STREAMLIT_SERVER_PORT=8501
```

---

## Platform-Specific Guides

### 1. Railway.sh ($5/month - Professional)

**Pros:** Custom domain, professional, good performance

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

Your URL: `https://your-app-production.up.railway.app`

---

### 2. Heroku (Paused - Use Railway Instead)

Heroku's free tier ended, but the setup still works if you have a paid plan:

```bash
# Install Heroku CLI
brew tap heroku/brew && brew install heroku

# Login
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

---

### 3. Render.com (Free tier available)

1. Go to **https://render.com**
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run ai_resume_analyzer_global.py`
5. Deploy

Your URL: `https://your-app.onrender.com`

---

### 4. Google App Engine

```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Deploy
gcloud app deploy

# View logs
gcloud app logs read
```

Your URL: `https://your-project.appspot.com`

---

### 5. DigitalOcean App Platform

1. Go to **https://cloud.digitalocean.com**
2. Click **"Create"** → **"Apps"**
3. Connect GitHub repository
4. Select Python runtime
5. Set environment:
   - Build: `pip install -r requirements.txt`
   - Run: `streamlit run ai_resume_analyzer_global.py --server.port 8080`
6. Deploy

---

### 6. AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init

# Create environment
eb create ai-resume-analyzer-env

# Deploy updates
git add .
git commit -m "Update"
eb deploy

# View logs
eb logs
```

---

## Production Setup

### Using Nginx as Reverse Proxy

Edit `nginx.conf` with your domain and use:

```bash
# Install Nginx
sudo apt-get install nginx

# Copy config
sudo cp nginx.conf /etc/nginx/sites-available/ai-resume-analyzer

# Enable site
sudo ln -s /etc/nginx/sites-available/ai-resume-analyzer \
    /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### SSL Certificate with Let's Encrypt

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d your-domain.com

# Auto-renew
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## Scale for Multiple Users

### Using PM2 Process Manager

```bash
# Install PM2
npm install -g pm2

# Start app
pm2 start "streamlit run ai_resume_analyzer_global.py" --name resume-analyzer

# Auto-restart on reboot
pm2 startup
pm2 save

# Monitor
pm2 monit
```

### Load Balancing with Nginx

```nginx
upstream streamlit_cluster {
    server localhost:8501;
    server localhost:8502;
    server localhost:8503;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://streamlit_cluster;
    }
}
```

---

## Custom Domain Setup

### For Streamlit Cloud:

1. Go to app settings
2. Click **"Custom domain"**
3. Add your domain
4. Update DNS CNAME records as instructed

### For Other Platforms:

Typically involves:
1. Buying domain (GoDaddy, Namecheap, etc.)
2. Setting DNS records to point to your hosting
3. Setting up SSL certificate

---

## Environment Variables

### Streamlit Cloud:
1. Go to app settings
2. Click **"Secrets"**
3. Add environment variables

### Docker:
Add to `docker-compose.yml`:
```yaml
environment:
  - API_KEY=your_key
  - DATABASE_URL=your_url
```

### Heroku/Railway:
```bash
# Heroku
heroku config:set API_KEY=your_key

# Railway
railway variables set API_KEY=your_key
```

---

## Monitoring & Logs

### Streamlit Cloud:
- Automatic analytics in Settings
- View logs in "Develop" tab

### Docker:
```bash
docker-compose logs -f
docker stats
```

### Cloud Platforms:
Each has their own logging/monitoring:
- Google Cloud: Cloud Logging
- AWS: CloudWatch
- Azure: Application Insights
- Railway: In-built logs

---

## Security Best Practices

### 1. Environment Variables
Never commit secrets to git:
```python
import os
api_key = os.getenv("API_KEY")
```

### 2. Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

### 3. HTTPS/SSL
Always use HTTPS in production (included in most platforms)

### 4. Input Validation
Validate all file uploads:
```python
if uploaded_file.size > MAX_FILE_SIZE:
    st.error("File too large")
```

### 5. CORS Configuration
For API endpoints:
```python
# .streamlit/config.toml
[server]
enableCORS = true
```

---

## Cost Comparison

| Platform | Free Tier | Paid Starting | Best For |
|----------|-----------|---------------|----------|
| **Streamlit Cloud** | ✅ Yes | $10/month | Everyone |
| **Railway** | ❌ No | $5/month | Small projects |
| **Render** | ✅ Yes | $7/month | Hobby projects |
| **Google Cloud** | ✅ Yes (free tier) | Pay-as-you-go | Scalable apps |
| **AWS** | ✅ Yes (free tier) | Pay-as-you-go | Enterprise |
| **DigitalOcean** | ❌ No | $5/month | Developers |
| **Vercel** | ✅ Yes | $20/month | APIs only |

---

## Troubleshooting

### Build Fails
1. Check Python version: `python --version` (3.8+)
2. Verify requirements.txt syntax
3. Test locally: `pip install -r requirements.txt`

### App Won't Start
1. Check if main file exists
2. Verify imports work locally
3. Check logs for errors

### Port Issues
```bash
# Find process using port 8501
lsof -i :8501

# Use different port
streamlit run app.py --server.port 8502
```

### Slow Performance
1. Optimize file upload handling
2. Cache expensive operations
3. Use CDN for large files
4. Scale horizontally

### SSL Certificate Issues
1. Wait 24-48 hours for DNS propagation
2. Clear browser cache
3. Use https in all URLs
4. Check certificate validity

---

## Next Steps

1. **Choose a platform** - Start with Streamlit Cloud (easiest)
2. **Deploy your app** - Follow the guide above
3. **Test thoroughly** - Try all features
4. **Share with world** - Get your URL and share!
5. **Monitor usage** - Track user engagement
6. **Get feedback** - Improve based on usage

---

## Support & Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Docker Docs**: https://docs.docker.com
- **Nginx Guide**: https://nginx.org/en/docs/
- **Railway Docs**: https://docs.railway.app
- **Google Cloud**: https://cloud.google.com/docs

---

**Your AI Resume Analyzer is ready to deploy globally! Choose your platform and launch! 🚀**
