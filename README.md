# 🌤️ Weather Dashboard

A real-time weather dashboard with data from OpenWeatherMap API. Built to learn Flask.
Live demo: https://flask-weather-app.stivluc.com
⚠️ It's a free web hosting instance, spinning down with inactivity, which can delay requests by 50 seconds or more.

## ✨ Features

- **Live Weather Data**: Real-time weather information from OpenWeatherMap
- **Smart City Search**: Autocomplete with city coordinates and deduplication
- **5-Day Forecast**: Extended weather predictions
- **Temperature Toggle**: Switch between Fahrenheit and Celsius
- **Responsive Design**: Professional UI with mobile support
- **Error Handling**: Graceful handling of API failures and invalid cities

## 🚀 Quick Start

### Local Development

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/weather-dashboard.git
cd weather-dashboard
```

2. **Create virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set API key**

```bash
export API_KEY=your_openweathermap_api_key_here
```

5. **Run the application**

```bash
python app.py
```

6. **Open browser** → http://127.0.0.1:5000

### Get OpenWeatherMap API Key

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Use it in the environment variable `API_KEY`

## 🌐 Live Demo

Deploy this app for free on multiple platforms:

- **Render** (Recommended): [render.com](https://render.com)
- **Railway**: [railway.app](https://railway.app)
- **PythonAnywhere**: [pythonanywhere.com](https://pythonanywhere.com)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 🏗️ Architecture

- **Backend**: Flask (Python)
- **Frontend**: Embedded HTML/CSS/JavaScript
- **API**: OpenWeatherMap for weather data and geocoding
- **Deployment**: Gunicorn WSGI server

## 📁 Project Structure

```
weather-dashboard/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Procfile           # Deployment configuration
├── render.yaml        # Render platform config
├── DEPLOYMENT.md      # Deployment guide
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

## 🔧 API Endpoints

- `GET /` - Main dashboard
- `GET /api/weather/{city}` - Get weather for a city
- `GET /api/forecast/{city}` - Get 5-day forecast
- `GET /api/autocomplete/{query}` - City autocomplete suggestions

## 🛡️ Security

- ✅ API keys properly externalized via environment variables
- ✅ No hardcoded secrets in repository
- ✅ Input validation and error handling
- ✅ Production-ready configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🎉 Demo Features in Action

1. **Search any city** → Real-time weather data appears
2. **Toggle units** → Switch between °F and °C instantly
3. **5-day forecast** → Extended weather predictions
4. **Smart autocomplete** → Find cities with coordinates
5. **Error handling** → Graceful handling of invalid cities

---
