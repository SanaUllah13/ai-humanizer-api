# 🧔🏻‍♂️ AI Text Humanizer for WordPress 🤖

A FastAPI backend + standalone HTML/CSS/JS frontend that transforms AI-generated text into natural, academic writing. **Easily embeddable in WordPress!**

## ✨ Features

- ✅ Expands contractions (don't → do not)
- ✅ Adds academic transitions (Moreover, Therefore, etc.)
- ✅ Optional passive voice conversion
- ✅ Optional synonym replacement for formal tone
- ✅ Word and sentence statistics
- ✅ Clean, responsive UI
- ✅ **WordPress-ready with multiple integration options**

---

## 📋 Requirements

- Python 3.8+
- Node.js (optional, for local testing)
- WordPress site (for integration)

---

## 🚀 Installation & Setup

### 1️⃣ Clone or Download

```bash
cd ~/Downloads/ai-humanizer-wordpress
```

### 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Download NLP Models

```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger_eng')"
```

### 5️⃣ Run the Backend API

```bash
python api.py
```

The API will run at `http://localhost:8000`

---

## 🧪 Test Locally

Open `index.html` in your browser or use a local server:

```bash
# Option 1: Python server
python -m http.server 8080

# Option 2: PHP server
php -S localhost:8080

# Then open: http://localhost:8080
```

Make sure the backend API is running at `http://localhost:8000`

---

## 🌐 WordPress Integration

### **Method 1: Iframe Embed (Easiest)**

1. **Host your frontend** (upload `index.html` to your server or use a service like Netlify/Vercel)
2. **Deploy your backend API** (see deployment section below)
3. **Update API URL** in `index.html` (line 271) to your backend URL
4. **Add to WordPress** using HTML block:

```html
<iframe 
    src="https://your-domain.com/index.html" 
    width="100%" 
    height="800" 
    frameborder="0"
></iframe>
```

---

### **Method 2: Custom HTML Block**

1. In WordPress, create a new page/post
2. Add a "Custom HTML" block
3. Copy and paste the **entire contents** of `index.html`
4. Update the API URL in the JavaScript section (around line 271)
5. Publish!

---

### **Method 3: WordPress Plugin (Advanced)**

Create a simple WordPress plugin:

1. Create folder `wp-content/plugins/ai-humanizer/`
2. Create `ai-humanizer.php`:

```php
<?php
/**
 * Plugin Name: AI Text Humanizer
 * Description: Transforms AI text into academic writing
 * Version: 1.0.0
 */

function ai_humanizer_shortcode() {
    // Read the HTML file
    $html = file_get_contents(plugin_dir_path(__FILE__) . 'index.html');
    return $html;
}

add_shortcode('ai_humanizer', 'ai_humanizer_shortcode');
```

3. Copy `index.html` to the plugin folder
4. Activate plugin in WordPress
5. Use shortcode `[ai_humanizer]` anywhere

---

## ☁️ Deployment

### **Backend Deployment Options**

#### **Option 1: Railway.app (Free)**
1. Create account at [railway.app](https://railway.app)
2. Create new project from GitHub
3. Add environment variables if needed
4. Railway will auto-detect FastAPI and deploy

#### **Option 2: Render.com (Free)**
1. Create account at [render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repo
4. Build command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
5. Start command: `python api.py`

#### **Option 3: DigitalOcean App Platform**
1. Create account at [digitalocean.com](https://digitalocean.com)
2. Create new app from GitHub
3. Follow deployment wizard

#### **Option 4: Your Own VPS**

```bash
# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run with production server
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app --bind 0.0.0.0:8000
```

---

### **Frontend Deployment Options**

#### **Option 1: Netlify (Free, Easiest)**
1. Drag and drop `index.html` to [netlify.com](https://netlify.com)
2. Update API URL in the deployed file
3. Use the Netlify URL in WordPress iframe

#### **Option 2: Vercel**
1. Create account at [vercel.com](https://vercel.com)
2. Upload `index.html`
3. Get deployment URL

#### **Option 3: Your WordPress Site**
Upload `index.html` to:
```
/wp-content/uploads/ai-humanizer/index.html
```

Then use in iframe:
```html
<iframe src="<?php echo site_url('/wp-content/uploads/ai-humanizer/index.html'); ?>"></iframe>
```

---

## 🔧 Configuration

### Update API URL

In `index.html`, find line ~271 and update:

```javascript
value="https://your-backend-api.com"  // Replace with your API URL
```

### CORS Settings

For production, update `api.py` line 22:

```python
allow_origins=["https://your-wordpress-site.com"],  # Replace * with your domain
```

---

## 📁 Project Structure

```
ai-humanizer-wordpress/
├── api.py                 # FastAPI backend
├── index.html            # Frontend (WordPress-ready)
├── requirements.txt      # Python dependencies
├── transformer/          # Text transformation logic
│   ├── __init__.py
│   └── app.py
└── README.md            # This file
```

---

## 🧪 API Endpoints

### `POST /humanize`

**Request:**
```json
{
  "text": "Your text here",
  "use_passive": false,
  "use_synonyms": false
}
```

**Response:**
```json
{
  "original_text": "...",
  "humanized_text": "...",
  "input_word_count": 50,
  "input_sentence_count": 3,
  "output_word_count": 55,
  "output_sentence_count": 3
}
```

### `GET /health`
Health check endpoint

---

## 🐛 Troubleshooting

### CORS Errors
- Make sure backend CORS allows your WordPress domain
- Check browser console for specific errors

### API Not Loading
- Verify backend is running
- Check API URL is correct in frontend
- Test API directly: `http://your-api.com/health`

### WordPress Embed Issues
- Try iframe method first (easiest)
- Check if WordPress allows iframe embeds
- Some themes may strip custom HTML

---

## 📝 License

MIT License - feel free to use and modify!

---

## 🙏 Credits

Based on the original AI Text Humanizer by [@DadaNanjesha](https://github.com/DadaNanjesha)

---

## 📞 Support

For issues or questions, please open an issue on GitHub.

---

**🎉 Enjoy transforming AI text into human-like academic writing on WordPress!**
