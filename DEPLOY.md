# Quick Deploy Guide

## Option 1: DigitalOcean (Your current server)

See detailed instructions in `deploy_guide.md`

**Quick steps:**
1. SSH to server: `ssh root@your_ip`
2. Run automated script (see deploy_guide.md)
3. Access at: `http://your_ip`

**Time:** 15-20 minutes

---

## Option 2: Render.com (Easiest, Free)

1. Push code to GitHub
2. Go to https://render.com
3. Create new "Web Service"
4. Connect GitHub repository
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `gunicorn main:app`
7. Click "Deploy"

**Time:** 5 minutes  
**Result:** `https://your-app.onrender.com`

---

## Option 3: Heroku (Simple)

```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Login
heroku login

# Create app
heroku create estate-catalog

# Add Procfile
echo "web: gunicorn main:app" > Procfile

# Deploy
git push heroku main

# Open
heroku open
```

**Time:** 10 minutes

---

## Which to choose?

- **DigitalOcean**: Full control, best performance, you already have it ✅
- **Render**: Easiest, free tier, auto-deploy from GitHub
- **Heroku**: Simple, good for prototypes

**Recommendation:** Use your DigitalOcean server - you already paid for it!
