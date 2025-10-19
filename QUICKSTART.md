# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Setup Backend (3 minutes)

```bash
cd ~/Downloads/ai-humanizer-wordpress

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLP models
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger_eng')"

# Run the API
python api.py
```

✅ Backend running at: `http://localhost:8000`

---

## Step 2: Test Frontend (1 minute)

Open a new terminal:

```bash
cd ~/Downloads/ai-humanizer-wordpress
python -m http.server 8080
```

✅ Open browser: `http://localhost:8080`

---

## Step 3: Add to WordPress (1 minute)

### Option A: Iframe (Easiest)

1. Create a new WordPress page
2. Add "Custom HTML" block
3. Paste this code:

```html
<iframe 
    src="http://localhost:8080/index.html" 
    width="100%" 
    height="800" 
    frameborder="0"
    style="border:none;"
></iframe>
```

### Option B: Embed Directly

1. Create a new WordPress page
2. Add "Custom HTML" block
3. Copy entire contents of `index.html` and paste

---

## Step 4: Production Deployment

### Backend (Choose one):

- **Railway.app** - Free, auto-deploy from GitHub
- **Render.com** - Free tier available
- **Your VPS** - Use gunicorn

### Frontend:

- **Netlify** - Drag and drop `index.html`
- **WordPress uploads** - Upload to `/wp-content/uploads/`

---

## WordPress Plugin Method

1. Copy entire `ai-humanizer-wordpress` folder to:
   ```
   /wp-content/plugins/ai-humanizer/
   ```

2. Activate plugin in WordPress admin

3. Use shortcode in any page:
   ```
   [ai_humanizer api_url="https://your-api.com"]
   ```

---

## 🎉 That's it!

You now have a WordPress-integrated AI Text Humanizer!

See `README.md` for detailed documentation.
