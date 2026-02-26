# 🚀 AI Resume Analyzer - Global Deployment Guide

Make your AI Resume Analyzer accessible globally from any system!

---

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Local Installation](#local-installation)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Network Access](#network-access)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Option 1: Direct Run (Fastest)
```bash
# Clone/navigate to project
cd AI-Resume-Stimulator

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run ai_resume_analyzer_global.py
```

**Access:** `http://localhost:8501`

---

## Local Installation

### Requirements
- Python 3.8+
- pip (Python package manager)
- 2GB RAM minimum
- Modern web browser

### Installation Steps

1. **Clone the Repository**
```bash
git clone https://github.com/samadrita01/AI-Resume-Stimulator.git
cd AI-Resume-Stimulator
```

2. **Create Virtual Environment (Recommended)**
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the Application**
```bash
streamlit run ai_resume_analyzer_global.py
```

5. **Access the Application**
Open your browser and go to: `http://localhost:8501`

### Network Access (Same Network)
To access from another computer on the same network:

```bash
streamlit run ai_resume_analyzer_global.py --server.address=0.0.0.0
```

Find your IP address:
- **Windows:** `ipconfig` (look for IPv4 Address)
- **macOS/Linux:** `ifconfig` (look for inet)

Access from other machines: `http://<YOUR_IP>:8501`

---

## Docker Deployment

### Requirements
- Docker installed
- Docker Compose (optional but recommended)

### Using Docker Compose (Recommended)

1. **Build and Run**
```bash
docker-compose up -d
```

2. **Check Status**
```bash
docker-compose ps
```

3. **View Logs**
```bash
docker-compose logs -f
```

4. **Stop Service**
```bash
docker-compose down
```

**Access:** `http://localhost:8501` or `http://<HOST_IP>:8501`

### Using Docker CLI Only

1. **Build Image**
```bash
docker build -t ai-resume-analyzer .
```

2. **Run Container**
```bash
docker run -d \
  -p 8501:8501 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/data:/app/data \
  --name resume-analyzer \
  ai-resume-analyzer
```

3. **Stop Container**
```bash
docker stop resume-analyzer
docker rm resume-analyzer
```

---

## Cloud Deployment

### Option 1: Streamlit Cloud (Free)

1. **Push to GitHub**
```bash
git push origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to: https://streamlit.io/cloud
   - Click "New app"
   - Select your GitHub repo and file
   - Deploy!

**Your public URL:** `https://<repo-name>-<random-id>.streamlit.app`

### Option 2: Heroku Deployment

1. **Create `Procfile`**
```
web: streamlit run ai_resume_analyzer_global.py --server.port=$PORT --server.address=0.0.0.0
```

2. **Create `.gitignore`**
```
venv/
__pycache__/
*.pyc
.DS_Store
data/
uploads/
```

3. **Deploy**
```bash
heroku login
heroku create your-app-name
git push heroku main
```

**Your public URL:** `https://your-app-name.herokuapp.com`

### Option 3: AWS/Azure/Google Cloud

#### Using AWS EC2:
```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv
git clone <your-repo>
cd AI-Resume-Stimulator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install and run
pip install -r requirements.txt
streamlit run ai_resume_analyzer_global.py --server.address=0.0.0.0
```

#### Using Docker on AWS:
```bash
# Push to ECR and deploy to ECS
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker build -t ai-resume-analyzer .
docker tag ai-resume-analyzer:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-resume-analyzer:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-resume-analyzer:latest
```

### Option 4: DigitalOcean App Platform

1. Connect GitHub repository
2. Select `ai_resume_analyzer_global.py` as entry point
3. Configure environment:
   - Port: 8501
   - HTTP Routes: `/`
4. Click Deploy!

---

## Network Access

### Local Network (Same WiFi/Ethernet)

1. **Start with network binding**
```bash
streamlit run ai_resume_analyzer_global.py --server.address=0.0.0.0
```

2. **Find your IP**
   - Windows: `ipconfig`
   - Mac/Linux: `ifconfig` or `hostname -I`

3. **Share URL:** `http://<YOUR_IP>:8501`

### Secure Remote Access

Using SSH Tunnel:
```bash
# On remote server
streamlit run ai_resume_analyzer_global.py --server.address=localhost

# On your machine
ssh -L 8501:localhost:8501 user@server-ip
```

Then access: `http://localhost:8501`

### Using Ngrok (Public URL)

```bash
# Install ngrok
pip install pyngrok

# Or download from: https://ngrok.com

# Run in terminal
ngrok http 8501
```

**Your public URL appears in terminal** (e.g., `https://xxxx-xx-xxx-xxx-xx.ngrok.io`)

---

## Performance Optimization

### For Multiple Users

1. **Increase Memory Limit:**
```bash
streamlit run ai_resume_analyzer_global.py \
  --logger.level=warning \
  --client.maxMessageSize=200 \
  --server.maxUploadSize=200
```

2. **Use Nginx as Reverse Proxy:**
```nginx
upstream streamlit {
    server localhost:8501;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://streamlit;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

3. **Use PM2 for Process Management:**
```bash
npm install -g pm2
pm2 start "streamlit run ai_resume_analyzer_global.py" --name resume-analyzer
pm2 startup
pm2 save
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8501
lsof -i :8501  # Mac/Linux
netstat -ano | findstr :8501  # Windows

# Kill process and try different port
streamlit run ai_resume_analyzer_global.py --server.port=8502
```

### Dependencies Not Found
```bash
# Ensure virtual environment is activated
# Then reinstall
pip install --upgrade -r requirements.txt
```

### CPU/Memory Issues
```bash
# Reduce number of questions/optimize
streamlit run ai_resume_analyzer_global.py --logger.level=error
```

### CORS Issues
Update `.streamlit/config.toml`:
```toml
[server]
enableCORS = true
```

### Connection Refused
```bash
# Check if app is running
lsof -i :8501

# Check firewall
sudo ufw status
sudo ufw allow 8501/tcp
```

---

## 📊 Accessing from Other Systems

### Same Local Network
```
http://<server-ip>:8501
Example: http://192.168.1.100:8501
```

### From Internet (Secure)
- Use Streamlit Cloud (recommended)
- Use Heroku with SSL
- Use AWS with Security Groups
- Use Ngrok with authentication

### Mobile Access
- Same URL as above in mobile browser
- Works on iOS Safari, Android Chrome
- Responsive design included

---

## Security Considerations

1. **Never expose on public internet without authentication**
2. **Use HTTPS in production**
3. **Implement rate limiting**
4. **Validate all file uploads**
5. **Use environment variables for sensitive data**

Example with authentication:
```python
# Add to ai_resume_analyzer_global.py
import streamlit as st

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Enter password:", type="password")
    if password == "your-secret-password":
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.stop()
```

---

## Monitoring

### Docker Container
```bash
docker stats resume-analyzer
docker logs resume-analyzer
```

### System Resources
```bash
# Linux
top
htop

# Mac
top -l 1

# Windows
tasklist | findstr python
```

---

## Support & Issues

For issues or questions:
1. Check this guide
2. Review [Streamlit Documentation](https://docs.streamlit.io)
3. Create GitHub issue: https://github.com/samadrita01/AI-Resume-Stimulator/issues

---

**Happy Deploying! 🚀**
