# 🚀 MCP Weather Dashboard - Deployment Guide

This guide shows you how to deploy your MCP Weather Dashboard for **FREE** on multiple platforms.

## 🌟 Best Free Options (Recommended)

### 1. 🔥 **Render** (Easiest & Most Reliable)
**Free Tier**: 512MB RAM, sleeps after 15min inactivity, custom domains

**Steps:**
1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click "New" → "Web Service"
4. Connect your GitHub repo
5. Use these settings:
   - **Name**: `mcp-weather-dashboard`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Environment Variables**: 
     - `API_KEY` = `your_openweathermap_api_key_here`
6. Deploy! 🎉

### 2. 🐍 **PythonAnywhere** (Python-Focused)
**Free Tier**: 512MB RAM, 1 web app, 3-month limit

**Steps:**
1. Sign up at [pythonanywhere.com](https://pythonanywhere.com)
2. Upload your files via Files tab
3. Go to Web tab → "Add a new web app"
4. Choose Flask and point to your `app.py`
5. Set environment variable `API_KEY` in WSGI config
6. Reload and done! 🎉

### 3. ⚡ **Railway** (Modern & Fast)
**Free Tier**: $5 monthly credits (generous)

**Steps:**
1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. "Deploy from GitHub repo"
4. Add environment variable: `API_KEY`
5. Auto-deploys! 🎉

---

## 🤔 **Can I use Vercel?**

**Short Answer**: Yes, but it's not ideal for Flask apps.

**Limitations**:
- Vercel is optimized for Next.js/static sites
- Flask runs as serverless functions (cold starts)
- 10-second execution limit per request
- More complex setup required

**If you want to try Vercel anyway**:
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in your project directory
3. Follow the prompts
4. Set `API_KEY` environment variable in Vercel dashboard

---

## 🛠️ **Files Included for Deployment**

- `app.py` - Production-ready Flask app with embedded HTML
- `requirements.txt` - Python dependencies
- `Procfile` - For Heroku/Render deployment
- `vercel.json` - Vercel configuration
- `render.yaml` - Render service configuration
- `railway.json` - Railway deployment config
- `runtime.txt` - Python version specification

---

## 🔧 **Environment Variables**

Set this environment variable on your chosen platform:

```
API_KEY=your_openweathermap_api_key_here
```

---

## 🎯 **Recommended Deployment Order**

1. **Try Render first** (most reliable for Flask)
2. **Railway as backup** (modern platform)
3. **PythonAnywhere for Python-specific needs**
4. **Vercel only if others don't work** (has limitations)

---

## 🌐 **After Deployment**

Your live MCP Weather Dashboard will have:
- ✅ Real-time weather data from OpenWeatherMap
- ✅ Smart city autocomplete with coordinates
- ✅ 5-day weather forecasts
- ✅ Temperature unit toggle (°F/°C)
- ✅ Professional UI with error handling
- ✅ Mobile-responsive design

---

## 🚨 **Important Notes**

- The API key included is for demo purposes
- For production, get your own OpenWeatherMap API key
- Free tiers may have usage limits
- Apps on free tiers may "sleep" when inactive

---

## 🎉 **You're Ready to Deploy!**

Choose your platform and follow the steps above. Your MCP Weather Dashboard will be live and accessible worldwide! 🌍