# 🚀 Complete Hostinger Deployment Guide

## ⚠️ Important Note

**Hostinger shared hosting does NOT support Python applications.** Therefore:
- ✅ Deploy **Frontend** on Hostinger WordPress
- ✅ Deploy **Backend API** on free Python hosting (Render.com)

---

## Part 1: Deploy Backend API (Render.com - FREE)

### Step 1: Prepare Your Files

1. Create a GitHub account if you don't have one: https://github.com
2. Create a new repository called `ai-humanizer-api`

### Step 2: Upload to GitHub

Open Terminal and run:

```bash
cd ~/Downloads/ai-humanizer-wordpress

# Initialize git (if not already done)
git init

# Create .gitignore
cat > .gitignore << 'EOF'
venv/
__pycache__/
*.pyc
.DS_Store
*.log
EOF

# Add all files
git add .
git commit -m "Initial commit"

# Link to your GitHub repo (replace with YOUR username)
git remote add origin https://github.com/YOUR-USERNAME/ai-humanizer-api.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy to Render.com

1. **Sign up at Render.com**
   - Go to https://render.com
   - Click "Get Started for Free"
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub repository `ai-humanizer-api`

3. **Configure Service**
   - **Name:** `ai-humanizer-api`
   - **Environment:** `Python 3`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt && python -m spacy download en_core_web_sm && python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger_eng')"
     ```
   - **Start Command:**
     ```bash
     uvicorn api:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan:** Select "Free"

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Copy your API URL (e.g., `https://ai-humanizer-api.onrender.com`)

5. **Test Your API**
   - Visit: `https://your-api-url.onrender.com/health`
   - You should see: `{"status":"healthy"}`

✅ **Backend API is now live!**

---

## Part 2: Deploy Frontend on Hostinger WordPress

### Method A: WordPress Plugin (Recommended)

#### Step 1: Prepare Plugin Files

1. **Update API URL in index.html**

Open `~/Downloads/ai-humanizer-wordpress/index.html` and find line 271:

```html
value="http://localhost:8000"
```

Change to your Render API URL:
```html
value="https://your-api-url.onrender.com"
```

2. **Create Plugin ZIP**

```bash
cd ~/Downloads
zip -r ai-humanizer.zip ai-humanizer-wordpress/
```

#### Step 2: Upload to WordPress

1. **Login to WordPress Admin**
   - Go to `https://yoursite.com/wp-admin`

2. **Upload Plugin**
   - Go to: Plugins → Add New → Upload Plugin
   - Click "Choose File"
   - Select `ai-humanizer.zip`
   - Click "Install Now"
   - Click "Activate Plugin"

3. **Create a Page**
   - Go to: Pages → Add New
   - Title: "AI Text Humanizer"
   - Add a Paragraph block
   - Type: `[ai_humanizer api_url="https://your-api-url.onrender.com"]`
   - Click "Publish"

✅ **Done! Visit your page to see the tool**

---

### Method B: Direct HTML Embed (Alternative)

#### Step 1: Update API URL

Edit `index.html` line 271 to use your Render API URL (see Method A, Step 1)

#### Step 2: Upload via FTP

1. **Login to Hostinger Control Panel**
   - Go to https://hpanel.hostinger.com
   - Click on your hosting plan

2. **Open File Manager**
   - Find "File Manager" in the dashboard
   - Navigate to: `public_html/wp-content/uploads/`

3. **Create New Folder**
   - Click "New Folder"
   - Name: `ai-humanizer`

4. **Upload index.html**
   - Enter the `ai-humanizer` folder
   - Click "Upload Files"
   - Select `index.html` from your computer
   - Wait for upload to complete

#### Step 3: Embed in WordPress

1. **Create New Page**
   - Go to WordPress Admin → Pages → Add New
   - Title: "AI Text Humanizer"

2. **Add Custom HTML Block**
   - Click "+" to add block
   - Search for "Custom HTML"
   - Add this code:

```html
<iframe 
    src="/wp-content/uploads/ai-humanizer/index.html" 
    width="100%" 
    height="900px" 
    frameborder="0"
    style="border:none; display:block;"
></iframe>
```

3. **Publish the Page**

✅ **Done!**

---

### Method C: Direct Code Embed (Most Flexible)

#### Step 1: Update API URL in index.html
(Same as Method A, Step 1)

#### Step 2: Copy HTML Content

1. Open `index.html` in a text editor
2. Copy ALL content (Ctrl+A, Ctrl+C)

#### Step 3: Paste in WordPress

1. **Create New Page**
   - WordPress Admin → Pages → Add New
   - Title: "AI Text Humanizer"

2. **Add Custom HTML Block**
   - Click "+" → Search "Custom HTML"
   - Paste the entire HTML content
   - Update the API URL in line 271 if not done

3. **Publish**

✅ **Done!**

---

## Part 3: Configure CORS (Security)

After deployment, update backend security:

### Step 1: Update api.py

Edit `api.py` line 22:

**Before:**
```python
allow_origins=["*"],  # Allow all domains
```

**After:**
```python
allow_origins=["https://yoursite.com"],  # Replace with your WordPress URL
```

### Step 2: Push Update to GitHub

```bash
cd ~/Downloads/ai-humanizer-wordpress
git add api.py
git commit -m "Update CORS to allow only my domain"
git push
```

Render.com will automatically redeploy with the new settings.

---

## 🎯 Complete Setup Checklist

### Backend (Render.com)
- [ ] GitHub account created
- [ ] Code pushed to GitHub
- [ ] Render.com account created
- [ ] Web service deployed
- [ ] API URL copied
- [ ] Health check working: `https://your-api.onrender.com/health`

### Frontend (Hostinger)
- [ ] API URL updated in index.html
- [ ] WordPress site accessible
- [ ] Plugin uploaded OR iframe added OR direct HTML added
- [ ] Page published
- [ ] Tool working on WordPress

---

## 🐛 Troubleshooting

### Problem: "Failed to fetch" error

**Solution:**
1. Check if API is running: Visit `https://your-api.onrender.com/health`
2. Check API URL in frontend matches exactly
3. Wait 30 seconds (Render free tier sleeps after inactivity)

### Problem: API is slow first time

**Solution:**
- Render free tier sleeps after 15 minutes of inactivity
- First request wakes it up (takes 30-60 seconds)
- Keep API active or upgrade to paid plan

### Problem: WordPress strips HTML

**Solution:**
- Use iframe method instead
- Or install "Code Snippets" plugin to allow HTML

### Problem: CORS error in browser console

**Solution:**
1. Check `api.py` CORS settings
2. Make sure your WordPress domain is allowed
3. Clear browser cache

---

## 💰 Cost Breakdown

| Service | Cost |
|---------|------|
| Render.com (Backend) | **FREE** (750 hours/month) |
| Hostinger (Frontend) | **Your existing plan** |
| **Total Additional Cost** | **$0** |

---

## 🚀 Alternative Backend Hosting (if Render doesn't work)

### Option 1: PythonAnywhere (Free)
- Visit: https://www.pythonanywhere.com
- Free tier: 512MB, 1 web app
- Good for testing

### Option 2: Railway.app (Free $5 credit)
- Visit: https://railway.app
- Very easy deployment from GitHub
- Free $5 credit monthly

### Option 3: Hostinger VPS (Paid)
- If you have Hostinger VPS (not shared hosting)
- Follow VPS deployment guide

---

## 📝 Next Steps After Deployment

1. **Test thoroughly** - Try different text inputs
2. **Monitor API** - Check Render.com dashboard for errors
3. **Share with users** - Get the WordPress page URL
4. **Add to menu** - Add page to WordPress navigation menu

---

## 🎉 You're Done!

Your AI Text Humanizer is now:
- ✅ Backend running on Render.com (free, reliable)
- ✅ Frontend integrated with WordPress on Hostinger
- ✅ Accessible to anyone visiting your WordPress site

**Your tool URL:** `https://yoursite.com/ai-text-humanizer` (or whatever page slug you chose)

---

## 📞 Need Help?

If you encounter issues:
1. Check Render.com logs: Dashboard → Your Service → Logs
2. Check WordPress console: Right-click → Inspect → Console tab
3. Verify API URL is correct in frontend
4. Test API directly in browser: `https://your-api.onrender.com/health`

Good luck! 🚀
