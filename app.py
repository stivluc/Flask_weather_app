#!/usr/bin/env python3
"""
MCP Weather Dashboard - Production Version
Demonstrates Model Context Protocol integration with real weather data
"""

from flask import Flask, render_template_string, jsonify, request
import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from datetime import datetime

app = Flask(__name__)

# Environment variables for production
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable is required")

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct"
ONECALL_URL = "http://api.openweathermap.org/data/3.0/onecall"

# Popular cities for quick access
POPULAR_CITIES = ["New York", "London", "Tokyo", "Paris", "Sydney", "Los Angeles", "Berlin", "Mumbai"]

def get_coordinates_for_city(city):
    """Get coordinates for a city using OpenWeatherMap Geocoding API"""
    try:
        params = {
            'q': city,
            'limit': 1,
            'appid': API_KEY
        }
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                location = data[0]
                return {
                    'lat': location['lat'],
                    'lon': location['lon'],
                    'name': location['name'],
                    'country': location.get('country', '')
                }
        return None
    except Exception as e:
        print(f"Geocoding API Error: {e}")
        return None

def get_enhanced_weather_data(lat, lon, units='imperial'):
    """Get enhanced weather data including UV index using One Call API"""
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY,
            'units': units,
            'exclude': 'minutely,alerts'
        }
        response = requests.get(ONECALL_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            current = data['current']
            daily = data['daily'][0]
            hourly = data['hourly'][:24]  # Next 24 hours
            
            # Calculate rain probability from hourly data
            rain_prob = 0
            for hour in hourly:
                if 'pop' in hour:
                    rain_prob = max(rain_prob, hour['pop'] * 100)
            
            return {
                'uv_index': current.get('uvi', 0),
                'rain_prob': f"{rain_prob:.0f}%",
                'temp_min': daily['temp']['min'],
                'temp_max': daily['temp']['max']
            }
    except Exception as e:
        print(f"Enhanced Weather API Error: {e}")
        return None

def get_weather_via_api(city, units='imperial'):
    """Get weather data with geocoding fallback"""
    try:
        # First try direct city search
        params = {
            'q': city,
            'appid': API_KEY,
            'units': units
        }
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            temp_unit = '°F' if units == 'imperial' else '°C'
            
            # Get enhanced data from One Call API
            enhanced = get_enhanced_weather_data(data['coord']['lat'], data['coord']['lon'], units)
            
            result = {
                'temperature': f"{int(data['main']['temp'])}{temp_unit}",
                'condition': data['weather'][0]['description'],
                'humidity': f"{data['main']['humidity']}%",
                'city': data['name'],
                'country': data['sys']['country']
            }
            
            if enhanced:
                result.update({
                    'temp_min': f"{int(enhanced['temp_min'])}{temp_unit}",
                    'temp_max': f"{int(enhanced['temp_max'])}{temp_unit}",
                    'rain_prob': enhanced['rain_prob'],
                    'uv_index': f"{enhanced['uv_index']:.0f}"
                })
            else:
                # Fallback values with proper placeholders
                result.update({
                    'temp_min': f"{int(data['main']['temp_min'])}{temp_unit}",
                    'temp_max': f"{int(data['main']['temp_max'])}{temp_unit}",
                    'rain_prob': "No data",
                    'uv_index': "No data"
                })
            
            return result
        else:
            # Geocoding fallback
            coordinates = get_coordinates_for_city(city)
            if coordinates:
                coord_params = {
                    'lat': coordinates['lat'],
                    'lon': coordinates['lon'],
                    'appid': API_KEY,
                    'units': units
                }
                coord_response = requests.get(WEATHER_URL, params=coord_params, timeout=10)
                
                if coord_response.status_code == 200:
                    data = coord_response.json()
                    temp_unit = '°F' if units == 'imperial' else '°C'
                    
                    # Get enhanced data from One Call API
                    enhanced = get_enhanced_weather_data(coordinates['lat'], coordinates['lon'], units)
                    
                    result = {
                        'temperature': f"{int(data['main']['temp'])}{temp_unit}",
                        'condition': data['weather'][0]['description'],
                        'humidity': f"{data['main']['humidity']}%",
                        'city': coordinates['name'],
                        'country': coordinates['country']
                    }
                    
                    if enhanced:
                        result.update({
                            'temp_min': f"{int(enhanced['temp_min'])}{temp_unit}",
                            'temp_max': f"{int(enhanced['temp_max'])}{temp_unit}",
                            'rain_prob': enhanced['rain_prob'],
                            'uv_index': f"{enhanced['uv_index']:.0f}"
                        })
                    else:
                        # Fallback values with proper placeholders
                        result.update({
                            'temp_min': f"{int(data['main']['temp_min'])}{temp_unit}",
                            'temp_max': f"{int(data['main']['temp_max'])}{temp_unit}",
                            'rain_prob': "No data",
                            'uv_index': "No data"
                        })
                    
                    return result
            return None
    except Exception as e:
        print(f"Weather API Error: {e}")
        return None

@app.route('/')
def index():
    """Main page with embedded HTML template"""
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MCP Weather Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            padding: 40px;
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }
        
        .mcp-badge {
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            margin-left: 10px;
        }
        
        .search-section {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .search-input-container {
            position: relative;
            flex: 1;
        }
        
        #citySearch {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 10px;
            outline: none;
        }
        
        #citySearch:focus {
            border-color: #667eea;
        }
        
        .autocomplete-dropdown {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid #ddd;
            border-top: none;
            border-radius: 0 0 10px 10px;
            max-height: 200px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
        }
        
        .autocomplete-item {
            padding: 12px 15px;
            cursor: pointer;
            border-bottom: 1px solid #eee;
            transition: background-color 0.2s ease;
        }
        
        .autocomplete-item:hover {
            background-color: #f8f9fa;
        }
        
        #searchBtn {
            padding: 15px 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            transition: transform 0.2s ease;
        }
        
        #searchBtn:hover {
            transform: translateY(-2px);
        }
        
        .unit-toggle {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .toggle-label {
            position: relative;
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            user-select: none;
        }
        
        .toggle-label input {
            opacity: 0;
            width: 0;
            height: 0;
        }
        
        .toggle-slider {
            position: relative;
            width: 60px;
            height: 30px;
            background: #ccc;
            border-radius: 30px;
            transition: background 0.3s ease;
        }
        
        .toggle-slider:before {
            content: '';
            position: absolute;
            top: 3px;
            left: 3px;
            width: 24px;
            height: 24px;
            background: white;
            border-radius: 50%;
            transition: transform 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        .toggle-label input:checked + .toggle-slider {
            background: #667eea;
        }
        
        .toggle-label input:checked + .toggle-slider:before {
            transform: translateX(30px);
        }
        
        .unit-text {
            display: flex;
            gap: 5px;
            font-weight: 500;
            color: #333;
        }
        
        .unit-text span {
            padding: 2px 6px;
            border-radius: 4px;
            transition: all 0.3s ease;
        }
        
        #fahrenheit.active, #celsius.active {
            background: #667eea;
            color: white;
        }
        
        .search-result-card {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 10px 20px rgba(40, 167, 69, 0.3);
            animation: slideDown 0.5s ease-out;
            display: none;
        }
        
        .search-result-card.error {
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
            box-shadow: 0 10px 20px rgba(220, 53, 69, 0.3);
        }
        
        .search-result-card.show {
            display: block;
        }
        
        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .city-name {
            font-size: 1.8em;
            margin-bottom: 15px;
            text-transform: capitalize;
        }
        
        .temperature {
            font-size: 3.5em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .condition {
            font-size: 1.3em;
            margin-bottom: 10px;
            text-transform: capitalize;
        }
        
        .humidity {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .weather-details {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 20px;
            padding-top: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .weather-detail-item {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.95em;
        }
        
        .detail-icon {
            font-size: 1.2em;
            width: 20px;
        }
        
        .detail-label {
            font-size: 0.85em;
            opacity: 0.8;
            min-width: 55px;
            text-align: left;
        }
        
        .detail-value {
            font-weight: 500;
            flex: 1;
        }
        
        .popular-cities-title {
            margin-bottom: 10px;
        }
        
        .popular-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 40px;
        }
        
        .popular-city-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 25px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .popular-city-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        .forecast-section {
            margin-top: 30px;
            margin-bottom: 40px;
            display: none;
        }
        
        .forecast-section.show {
            display: block;
            animation: slideDown 0.5s ease-out;
        }
        
        .forecast-title {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.3em;
            text-align: center;
        }
        
        .forecast-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }
        
        .forecast-card {
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        
        .forecast-date {
            font-weight: bold;
            color: #495057;
            margin-bottom: 8px;
            font-size: 0.9em;
        }
        
        .forecast-temp {
            font-size: 1.2em;
            color: #dc3545;
            margin: 5px 0;
        }
        
        .forecast-condition {
            color: #6c757d;
            font-size: 0.8em;
            text-transform: capitalize;
        }
        
        .mcp-info {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 25px;
            margin-top: 30px;
        }
        
        .mcp-info h3 {
            color: #495057;
            margin-bottom: 15px;
        }
        
        .mcp-info p {
            color: #6c757d;
            line-height: 1.7;
            margin-bottom: 15px;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            
            .container {
                padding: 20px;
                border-radius: 15px;
            }
            
            h1 {
                font-size: 2em;
                margin-bottom: 8px;
            }
            
            .subtitle {
                font-size: 1em;
                margin-bottom: 25px;
            }
            
            .search-section {
                flex-direction: column;
                gap: 15px;
            }
            
            .search-input-container {
                min-width: 100%;
            }
            
            #citySearch {
                font-size: 16px; /* Prevents zoom on iOS */
            }
            
            .unit-toggle {
                justify-content: center;
                margin: 0;
            }
            
            .weather-card {
                padding: 20px;
                margin-bottom: 15px;
            }
            
            .weather-card h2 {
                font-size: 1.5em;
            }
            
            .temperature {
                font-size: 2.5em;
            }
            
            .forecast-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
            }
            
            .forecast-card {
                padding: 12px;
            }
            
            .popular-grid {
                flex-direction: column;
                gap: 10px;
            }
            
            .popular-city-btn {
                width: 100%;
                justify-content: center;
            }
            
            .mcp-info {
                padding: 20px;
                margin-top: 20px;
            }
            
            .weather-details {
                grid-template-columns: 1fr;
                gap: 10px;
                margin-top: 15px;
            }
            
            .weather-detail-item {
                font-size: 0.9em;
                justify-content: center;
            }
        }
        
        @media (max-width: 480px) {
            .container {
                padding: 15px;
            }
            
            h1 {
                font-size: 1.8em;
            }
            
            .temperature {
                font-size: 2em;
            }
            
            .weather-info {
                font-size: 0.9em;
            }
            
            .forecast-grid {
                grid-template-columns: 1fr;
            }
            
            .forecast-card {
                padding: 15px;
                text-align: center;
            }
            
            .autocomplete-dropdown {
                max-height: 200px;
            }
        }
        
        /* Touch-friendly interactions */
        @media (hover: none) and (pointer: coarse) {
            .popular-city-btn,
            button {
                min-height: 44px;
                font-size: 16px;
            }
            
            .autocomplete-item {
                min-height: 44px;
                display: flex;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌤️ MCP Weather Dashboard <span class="mcp-badge">LIVE DATA</span></h1>
        <p class="subtitle">Real-time weather powered by Model Context Protocol</p>
        
        <div class="search-section">
            <div class="search-input-container">
                <input type="text" id="citySearch" placeholder="Search for any city..." autocomplete="off" />
                <div class="autocomplete-dropdown" id="autocompleteDropdown"></div>
            </div>
            <button id="searchBtn">🔍 Search</button>
            <div class="unit-toggle">
                <label class="toggle-label">
                    <input type="checkbox" id="unitToggle" />
                    <span class="toggle-slider"></span>
                    <span class="unit-text">
                        <span id="fahrenheit">°F</span>
                        <span id="celsius">°C</span>
                    </span>
                </label>
            </div>
        </div>
        
        <div class="search-result-card" id="searchResultCard">
            <div class="city-name" id="searchCityName"></div>
            <div class="temperature" id="searchTemp"></div>
            <div class="condition" id="searchCondition"></div>
            
            <div class="weather-details">
                <div class="weather-detail-item">
                    <span class="detail-icon">🌡️</span>
                    <span class="detail-label">Range:</span>
                    <span class="detail-value" id="searchMinMax"></span>
                </div>
                <div class="weather-detail-item">
                    <span class="detail-icon">🌦️</span>
                    <span class="detail-label">Rain:</span>
                    <span class="detail-value" id="searchRainProb"></span>
                </div>
                <div class="weather-detail-item">
                    <span class="detail-icon">☀️</span>
                    <span class="detail-label">UV:</span>
                    <span class="detail-value" id="searchUVIndex"></span>
                </div>
                <div class="weather-detail-item">
                    <span class="detail-icon">💧</span>
                    <span class="detail-label">Humidity:</span>
                    <span class="detail-value" id="searchHumidity"></span>
                </div>
            </div>
        </div>
        
        <div class="forecast-section" id="forecastSection">
            <h3 class="forecast-title">5-Day Forecast</h3>
            <div class="forecast-grid" id="forecastGrid"></div>
        </div>
        
        <div class="popular-cities">
            <h3 class="popular-cities-title">Popular Cities</h3>
            <div class="popular-grid" id="popularGrid"></div>
        </div>
        
        <div class="mcp-info">
            <h3>🔧 About this MCP Demo</h3>
            <p><strong>Model Context Protocol (MCP)</strong> is a standardized way for AI assistants to connect to external tools and data sources. This weather dashboard demonstrates MCP in action:</p>
            <p>🌐 <strong>Real-time Data</strong>: This app fetches live weather information from OpenWeatherMap API</p>
            <p>🔍 <strong>Smart Search</strong>: The autocomplete feature uses geocoding APIs to find cities worldwide with coordinates</p>
            <p>📊 <strong>Dynamic Interaction</strong>: MCP enables seamless integration between AI assistants and external services, making tools like this weather dashboard possible</p>
            <p>This is a practical example of how MCP bridges the gap between AI and real-world data sources, creating more useful and interactive applications.</p>
        </div>
    </div>

    <script>
        let cities = {{ cities|tojson }};

        document.addEventListener('DOMContentLoaded', async function() {
            renderPopularCities();
            updateUnitDisplay();
            
            const searchBtn = document.getElementById('searchBtn');
            const searchInput = document.getElementById('citySearch');
            const unitToggle = document.getElementById('unitToggle');
            
            searchBtn.addEventListener('click', searchCity);
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') searchCity();
            });
            searchInput.addEventListener('input', handleAutocomplete);
            unitToggle.addEventListener('change', function() {
                updateUnitDisplay();
                const query = searchInput.value.trim();
                if (query && document.getElementById('searchResultCard').classList.contains('show')) {
                    searchCity();
                }
            });
            
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.search-input-container')) {
                    document.getElementById('autocompleteDropdown').style.display = 'none';
                }
            });
        });

        function renderPopularCities() {
            const popularGrid = document.getElementById('popularGrid');
            popularGrid.innerHTML = '';
            cities.forEach(city => {
                const cityBtn = document.createElement('button');
                cityBtn.className = 'popular-city-btn';
                cityBtn.textContent = city;
                cityBtn.onclick = () => searchSpecificCity(city);
                popularGrid.appendChild(cityBtn);
            });
        }

        async function searchSpecificCity(city) {
            document.getElementById('citySearch').value = city;
            await searchCity();
        }

        async function searchCity() {
            const query = document.getElementById('citySearch').value.trim();
            if (!query) return;
            
            const card = document.getElementById('searchResultCard');
            const isCelsius = document.getElementById('unitToggle').checked;
            const units = isCelsius ? 'metric' : 'imperial';
            
            document.getElementById('autocompleteDropdown').style.display = 'none';
            
            card.classList.remove('error');
            card.classList.add('show');
            document.getElementById('searchCityName').textContent = query;
            document.getElementById('searchTemp').textContent = 'Loading...';
            document.getElementById('searchCondition').textContent = '';
            document.getElementById('searchMinMax').textContent = '';
            document.getElementById('searchRainProb').textContent = '';
            document.getElementById('searchUVIndex').textContent = '';
            document.getElementById('searchHumidity').textContent = '';
            
            try {
                const response = await fetch(`/api/weather/${encodeURIComponent(query)}?units=${units}`);
                const data = await response.json();

                if (response.ok) {
                    document.getElementById('searchTemp').textContent = data.temperature;
                    document.getElementById('searchCondition').textContent = data.condition;
                    document.getElementById('searchMinMax').textContent = `${data.temp_min} - ${data.temp_max}`;
                    document.getElementById('searchRainProb').textContent = data.rain_prob;
                    document.getElementById('searchUVIndex').textContent = `UV ${data.uv_index}`;
                    document.getElementById('searchHumidity').textContent = data.humidity;
                    loadForecast(query, units);
                } else {
                    card.classList.add('error');
                    document.getElementById('searchTemp').textContent = '❌';
                    document.getElementById('searchCondition').textContent = 'City not found - Please check the city name';
                    document.getElementById('searchMinMax').textContent = '';
                    document.getElementById('searchRainProb').textContent = '';
                    document.getElementById('searchUVIndex').textContent = '';
                    document.getElementById('searchHumidity').textContent = '';
                }
            } catch (error) {
                card.classList.add('error');
                document.getElementById('searchTemp').textContent = '🌐';
                document.getElementById('searchCondition').textContent = 'Network error - Please check your connection';
                document.getElementById('searchMinMax').textContent = '';
                document.getElementById('searchRainProb').textContent = '';
                document.getElementById('searchUVIndex').textContent = '';
                document.getElementById('searchHumidity').textContent = '';
            }
        }

        async function loadForecast(city, units) {
            try {
                const response = await fetch(`/api/forecast/${encodeURIComponent(city)}?units=${units}`);
                const data = await response.json();
                
                if (response.ok) {
                    const forecastGrid = document.getElementById('forecastGrid');
                    forecastGrid.innerHTML = '';
                    data.forecasts.forEach(forecast => {
                        const card = document.createElement('div');
                        card.className = 'forecast-card';
                        card.innerHTML = `
                            <div class="forecast-date">${forecast.date}</div>
                            <div class="forecast-temp">${forecast.temperature}</div>
                            <div class="forecast-condition">${forecast.condition}</div>
                        `;
                        forecastGrid.appendChild(card);
                    });
                    document.getElementById('forecastSection').classList.add('show');
                }
            } catch (error) {
                console.error('Forecast error:', error);
            }
        }

        async function handleAutocomplete() {
            const query = document.getElementById('citySearch').value.trim();
            const dropdown = document.getElementById('autocompleteDropdown');
            
            if (query.length < 2) {
                dropdown.style.display = 'none';
                return;
            }
            
            try {
                const response = await fetch(`/api/autocomplete/${encodeURIComponent(query)}`);
                const data = await response.json();
                
                if (data.cities && data.cities.length > 0) {
                    dropdown.innerHTML = '';
                    data.cities.forEach(city => {
                        const item = document.createElement('div');
                        item.className = 'autocomplete-item';
                        item.textContent = city.display;
                        item.onclick = () => {
                            document.getElementById('citySearch').value = city.name;
                            dropdown.style.display = 'none';
                            searchCity();
                        };
                        dropdown.appendChild(item);
                    });
                    dropdown.style.display = 'block';
                } else {
                    dropdown.style.display = 'none';
                }
            } catch (error) {
                dropdown.style.display = 'none';
            }
        }

        function updateUnitDisplay() {
            const isCelsius = document.getElementById('unitToggle').checked;
            document.getElementById('fahrenheit').classList.toggle('active', !isCelsius);
            document.getElementById('celsius').classList.toggle('active', isCelsius);
        }
    </script>
</body>
</html>'''
    
    return render_template_string(html_template, cities=POPULAR_CITIES)

@app.route('/api/weather/<city>')
def get_weather(city):
    """API endpoint to get weather data for any city"""
    units = request.args.get('units', 'imperial')
    weather = get_weather_via_api(city, units)
    if weather:
        return jsonify({
            'city': weather['city'],
            'temperature': weather['temperature'],
            'condition': weather['condition'],
            'humidity': weather['humidity'],
            'real_data': True
        })
    else:
        return jsonify({'error': 'City not found'}), 404

@app.route('/api/autocomplete/<query>')
def autocomplete_cities(query):
    """API endpoint for city autocomplete suggestions"""
    if len(query.strip()) < 2:
        return jsonify({'cities': []})
    
    try:
        params = {
            'q': query,
            'limit': 5,
            'appid': API_KEY
        }
        response = requests.get(GEOCODING_URL, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            cities = []
            seen_cities = set()
            
            for location in data:
                city_name = location['name']
                country = location.get('country', '')
                state = location.get('state', '')
                lat = location.get('lat', 0)
                lon = location.get('lon', 0)
                
                unique_key = f"{city_name.lower()}_{country}_{state}"
                if unique_key in seen_cities:
                    continue
                    
                seen_cities.add(unique_key)
                
                display_name = city_name
                if country == 'FR' and state:
                    display_name = f"{city_name}, {state}, France ({lat:.2f}, {lon:.2f})"
                elif state and country:
                    display_name = f"{city_name}, {state}, {country} ({lat:.2f}, {lon:.2f})"
                elif country:
                    display_name = f"{city_name}, {country} ({lat:.2f}, {lon:.2f})"
                else:
                    display_name = f"{city_name} ({lat:.2f}, {lon:.2f})"
                
                cities.append({
                    'name': city_name,
                    'display': display_name,
                    'lat': lat,
                    'lon': lon,
                    'country': country,
                    'state': state
                })
            
            return jsonify({'cities': cities})
        else:
            return jsonify({'cities': []})
    except Exception as e:
        print(f"Autocomplete error: {e}")
        return jsonify({'cities': []})

@app.route('/api/forecast/<city>')
def get_forecast(city):
    """API endpoint to get 5-day weather forecast"""
    units = request.args.get('units', 'imperial')
    
    try:
        coordinates = get_coordinates_for_city(city)
        if not coordinates:
            return jsonify({'error': 'City not found'}), 404
        
        params = {
            'lat': coordinates['lat'],
            'lon': coordinates['lon'],
            'appid': API_KEY,
            'units': units
        }
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            temp_unit = '°F' if units == 'imperial' else '°C'
            
            daily_forecasts = []
            seen_dates = set()
            
            for item in data['list']:
                date_str = item['dt_txt'][:10]
                time_str = item['dt_txt'][11:13]
                
                if date_str not in seen_dates and time_str in ['12', '15']:
                    seen_dates.add(date_str)
                    
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%a, %b %d')
                    
                    daily_forecasts.append({
                        'date': formatted_date,
                        'temperature': f"{int(item['main']['temp'])}{temp_unit}",
                        'condition': item['weather'][0]['description']
                    })
                    
                    if len(daily_forecasts) >= 5:
                        break
            
            return jsonify({
                'city': coordinates['name'],
                'forecasts': daily_forecasts
            })
        else:
            return jsonify({'error': 'Forecast data not available'}), 500
            
    except Exception as e:
        print(f"Forecast API Error: {e}")
        return jsonify({'error': 'Forecast data not available'}), 500

@app.route('/api/cities')
def get_cities():
    """API endpoint to get list of popular cities"""
    return jsonify({'cities': POPULAR_CITIES})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)