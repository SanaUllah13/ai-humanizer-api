# 📋 Quick Deployment Checklist

Copy this checklist and mark off each step as you complete it!

---

## ⚡ STEP 1: GitHub Setup (5 minutes)

```bash
cd ~/Downloads/ai-humanizer-wordpress

# Setup Git
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub.com, then:
git remote add origin https://github.com/YOUR-USERNAME/ai-humanizer-api.git
git branch -M main
git push -u origin main
```

- [ ] GitHub account created
- [ ] New repo `ai-humanizer-api` created
- [ ] Code pushed successfully

---

## ⚡ STEP 2: Deploy Backend to Render.com (10 minutes)

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select your `ai-humanizer-api` repo
5. Configure:

```
Name: ai-humanizer-api
Environment: Python 3
Build Command:
pip install -r requirements.txt && python -m spacy download en_core_web_sm && python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger_eng')"

Start Command:
uvicorn api:app --host 0.0.0.0 --port $PORT

Plan: Free
```

6. Click "Create Web Service"
7. Wait 5-10 minutes

- [ ] Render.com account created
- [ ] Service deployed
- [ ] Got API URL: `https://______________.onrender.com`
- [ ] Tested: `https://your-url.onrender.com/health` shows `{"status":"healthy"}`

**SAVE YOUR API URL:** _________________________________

---

## ⚡ STEP 3: Update Frontend (2 minutes)

Open `index.html` in text editor and change line 271:

**Find:**
```html
value="http://localhost:8000"
```

**Replace with YOUR Render URL:**
```html
value="https://your-api-url.onrender.com"
```

- [ ] API URL updated in index.html
- [ ] File saved

---

## ⚡ STEP 4: Add to WordPress (5 minutes)

### Option A: Custom HTML (Easiest)

1. Login to WordPress Admin: `https://yoursite.com/wp-admin`
2. Go to: **Pages → Add New**
3. Title: "AI Text Humanizer"
4. Click **"+"** → Search "**Custom HTML**"
5. Copy entire `index.html` content and paste
6. Click **"Publish"**

- [ ] Page created
- [ ] HTML pasted
- [ ] Page published
- [ ] Visited page and tool works

### Option B: Upload via File Manager

1. Login to Hostinger: https://hpanel.hostinger.com
2. Open **File Manager**
3. Go to: `public_html/wp-content/uploads/`
4. Create folder: `ai-humanizer`
5. Upload `index.html`
6. In WordPress, create page with iframe:

```html
<iframe 
    src="/wp-content/uploads/ai-humanizer/index.html" 
    width="100%" 
    height="900px" 
    frameborder="0"
    style="border:none;"
></iframe>
```

- [ ] File uploaded
- [ ] Page created with iframe
- [ ] Tool works

---

## ✅ FINAL TEST

1. Visit your WordPress page
2. Enter some text: "I'll show you how it's done!"
3. Click "Transform to Academic Style"
4. Should get result: "I will show you how it is done!"

- [ ] Tool loads correctly
- [ ] Can enter text
- [ ] Transform button works
- [ ] Results display properly
- [ ] Can copy output

---

## 🎉 SUCCESS!

Your tool is live at: `https://yoursite.com/YOUR-PAGE-SLUG`

Share it with users! 🚀

---

## ⚠️ Common Issues

| Problem | Solution |
|---------|----------|
| "Failed to fetch" | Wait 30 seconds (API is waking up) |
| Blank page | Check browser console (F12) |
| API slow | Render free tier sleeps after 15 min |
| CORS error | Check API URL matches exactly |

---

## 📞 Support

Need help? Check:
1. **Render logs:** Dashboard → Your Service → Logs
2. **Browser console:** Right-click page → Inspect → Console
3. **API health:** Visit `https://your-api.onrender.com/health`
