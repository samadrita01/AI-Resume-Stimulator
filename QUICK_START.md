# 🚀 Quick Start Guide

Get the AI Resume Analyzer up and running in minutes!

## 1️⃣ Choose Your Installation Method

### Method A: Automatic Setup (Easiest)

#### On Linux/macOS:
```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
streamlit run ai_resume_analyzer_global.py
```

#### On Windows:
```bash
setup.bat
```

Then in the opened terminal:
```bash
streamlit run ai_resume_analyzer_global.py
```

---

### Method B: Manual Installation

```bash
# 1. Clone repository
git clone https://github.com/samadrita01/AI-Resume-Stimulator.git
cd AI-Resume-Stimulator

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run application
streamlit run ai_resume_analyzer_global.py
```

---

### Method C: Docker (No installation needed!)

```bash
# Make sure Docker is installed, then:
docker-compose up -d

# That's it! Your app is running.
```

---

## 2️⃣ Access the Application

Once running, open your browser:
- **Local access:** `http://localhost:8501`
- **Network access:** `http://<YOUR_IP>:8501`

To find your IP:
- Windows: `ipconfig`
- macOS/Linux: `ifconfig` or `hostname -I`

---

## 3️⃣ Features

✅ Resume Upload (PDF/DOCX)  
✅ Skill Analysis  
✅ Mock Interview  
✅ Aptitude Test  
✅ Job Recommendations  
✅ Performance Dashboard  

---

## 4️⃣ Share with Others

### Same Network
```bash
streamlit run ai_resume_analyzer_global.py --server.address=0.0.0.0
```
Share URL: `http://<YOUR_IP>:8501`

### Internet (Free)
Use Streamlit Cloud:
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect and deploy!

---

## ⚙️ Configuration

Edit `.streamlit/config.toml` to customize:
- Colors and theme
- Port number
- Upload limits
- Logging level

---

## 🆘 Troubleshooting

**Port 8501 already in use?**
```bash
streamlit run ai_resume_analyzer_global.py --server.port=8502
```

**Dependencies not installing?**
```bash
pip install --upgrade -r requirements.txt
```

**Virtual environment issues?**
```bash
# Delete and recreate
rm -rf venv  # or rmdir venv on Windows
python -m venv venv
```

---

## 📚 More Help

- [Full Deployment Guide](DEPLOYMENT.md)
- [Streamlit Docs](https://docs.streamlit.io)
- [GitHub Issues](https://github.com/samadrita01/AI-Resume-Stimulator/issues)

---

**Happy analyzing! 📊**
