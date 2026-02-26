# 📊 AI Resume Analyzer - Global Platform

A comprehensive AI-powered resume analysis platform with skill analysis, mock interviews, aptitude testing, and job recommendations. **Now accessible globally from any system!**

## ✨ Features

- 📄 **Resume Upload** - Upload PDF or DOCX resumes for instant analysis
- 🔍 **Skill Analysis** - AI-powered skill detection and career path recommendations
- 🎯 **Mock Interview** - Real-time interview simulation with instant scoring and feedback
- 🧠 **Aptitude Test** - Logic, quantitative, and verbal reasoning tests with explanations
- 💼 **Job Recommendations** - AI-matched job opportunities based on your skills
- 📊 **Performance Dashboard** - Comprehensive performance analytics and improvement suggestions

## 🚀 Quick Start (Choose One)

### 1️⃣ Automatic Setup (Recommended) - 2 Minutes

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
streamlit run ai_resume_analyzer_global.py
```

**Windows:**
```bash
setup.bat
```

### 2️⃣ Docker (Instant Setup - No Installation)

```bash
docker-compose up -d
```
Access: `http://localhost:8501`

### 3️⃣ Manual Installation

```bash
# Create and activate virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run ai_resume_analyzer_global.py
```

## 🌍 Make It Globally Accessible

### Option 1: Same Network/Local Network
```bash
streamlit run ai_resume_analyzer_global.py --server.address=0.0.0.0
```
Share URL: `http://<YOUR_IP>:8501`

### Option 2: Free Public Access (Streamlit Cloud)
1. Push code to GitHub
2. Visit https://streamlit.io/cloud
3. Deploy with one click
4. Get public URL instantly!

### Option 3: Ngrok Tunneling (Quick)
```bash
pip install pyngrok
ngrok http 8501
```
Share the public HTTPS URL!

### Option 4: Production Deployment
- **Heroku:** `git push heroku main`
- **AWS/Azure/Google Cloud:** See [DEPLOYMENT.md](DEPLOYMENT.md)
- **DigitalOcean:** Connect GitHub and deploy

## 📱 Access Points

| Method | URL | Access |
|--------|-----|--------|
| Local | `http://localhost:8501` | This computer only |
| Network | `http://<YOUR_IP>:8501` | Same WiFi/Network |
| Streamlit Cloud | `https://<app-name>.streamlit.app` | Public internet |
| Ngrok | `https://xxxx-xx-xxx.ngrok.io` | Public internet |
| Production | `https://yourdomain.com` | Production |

## 📦 System Requirements

- **Python:** 3.8+
- **RAM:** 2GB minimum
- **Storage:** 500MB
- **Browser:** Any modern browser (Chrome, Firefox, Safari, Edge)
- **OS:** Windows, macOS, or Linux

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [QUICK_START.md](QUICK_START.md) | Get started in 5 minutes |
| [DEPLOYMENT.md](DEPLOYMENT.md) | All deployment options & configurations |
| [requirements.txt](requirements.txt) | Python dependencies |

## 🛠 Configuration

Customize the app by editing `.streamlit/config.toml`:
- Theme colors and styling
- Port number (default: 8501)
- Upload file size limits
- Logging levels

## 🔧 Common Commands

```bash
# Run with custom port
streamlit run ai_resume_analyzer_global.py --server.port=8502

# Run for network access
streamlit run ai_resume_analyzer_global.py --server.address=0.0.0.0

# View logs and debug
streamlit run ai_resume_analyzer_global.py --logger.level=debug

# Run with Docker
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8501 in use | `streamlit run ai_resume_analyzer_global.py --server.port=8502` |
| Dependencies fail | `pip install --upgrade -r requirements.txt` |
| Can't access from other PCs | `streamlit run ai_resume_analyzer_global.py --server.address=0.0.0.0` |
| Docker issues | `docker-compose down && docker-compose up -d` |
| Virtual env problems | Delete `venv` folder and run `setup.sh` or `setup.bat` again |

## 📊 Performance Tips

- Use Docker for consistent performance
- Increase memory for multiple concurrent users
- Deploy on cloud for better uptime
- Use reverse proxy (Nginx) for load balancing

## 🔒 Security Considerations

For production deployments:
- Use HTTPS/SSL certificates
- Implement user authentication
- Validate all file uploads
- Use environment variables for secrets
- Enable CORS carefully
- Set up rate limiting

## 📞 Support & Issues

- 📖 Read [DEPLOYMENT.md](DEPLOYMENT.md) for detailed help
- 🔗 Check [Streamlit Docs](https://docs.streamlit.io)
- 🐛 Report issues on [GitHub](https://github.com/samadrita01/AI-Resume-Stimulator/issues)
- 💬 Join Streamlit community

## 📄 License

MIT License - Free to use and modify

## 👨‍💻 Author

**Samadrita** (@samadrita01)  
AI Resume Analyzer - Global Platform

---

**🎉 Start analyzing resumes and get job recommendations now!**

Made with ❤️ using [Streamlit](https://streamlit.io) | Deployed globally 🌍
