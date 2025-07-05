# -*- coding: utf-8 -*-
from mcp.server.fastmcp import FastMCP
import requests
from typing import List, Dict, Any, Optional
import logging
import sys
from dotenv import load_dotenv
import os

logger = logging.getLogger('MapNavigator')

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

mcp = FastMCP("MapNavigator")

# 加载环境变量
load_dotenv()

# 获取高德地图API密钥
MAP_API_KEY = os.getenv("AMAP_API_KEY", "...your_api_key_here...")  # 替换为你的实际API密钥

@mcp.tool()
def geocode(address: str, city: str = "") -> dict:
    """Convert address to geographic coordinates using Amap API."""
    api_key = MAP_API_KEY
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "address": address,
        "city": city,
        "output": "json",
        "key": api_key
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        logger.info(f"Geocode API status: {data.get('status')}") 
        return data
    except Exception as e:
        logger.error(f"Error calling geocode API: {e}")
        return {"status": "0", "info": str(e)}
@mcp.tool()
def get_weather(city: str) -> dict:
    """Get weather information for a city using Amap API."""
    api_key = MAP_API_KEY
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        "city": city,
        "key": api_key,
        "output": "json"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        logger.info(f"Weather API status: {data.get('status')}")
        return data
    except Exception as e:
        logger.error(f"Error calling weather API: {e}")
        return {"status": "0", "info": str(e)}

@mcp.tool()
def plan_driving_route(origin: str, destination: str, waypoints: str = "", strategy: str = "0", 
                      extensions: str = "base", avoid_road: str = "") -> dict:
    """Plan a driving route between two points
    
    Parameters:
        origin: Starting coordinates, format "longitude,latitude", e.g. "116.481028,39.989643"
        destination: Ending coordinates, format "longitude,latitude", e.g. "116.434446,39.90816"
        waypoints: Optional waypoints, format "longitude1,latitude1;longitude2,latitude2"
        strategy: Route planning strategy, default is "0" (speed priority)
        extensions: Return basic information ("base") or all information ("all")
        avoid_road: Specify roads to avoid
        
    Returns:
        Route planning information, including distance, time, and detailed route segments
    """
    api_key = MAP_API_KEY
    url = "https://restapi.amap.com/v3/direction/driving"
    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key,
        "output": "json",
        "strategy": strategy,
        "extensions": extensions
    }
    
    if waypoints:
        params["waypoints"] = waypoints
        
    if avoid_road:
        params["avoidroad"] = avoid_road
    
    try:
        response = requests.get(url, params=params)
        response.encoding = 'utf-8'
        data = response.json()
        logger.info(f"Driving route planning API status: {data.get('status')}")
        return data
    except Exception as e:
        logger.error(f"Error calling driving route planning API: {e}")
        return {"status": "0", "info": str(e)}

@mcp.tool()
def input_tips(keywords: str, location: str = "", city: str = "", types: str = "", datatype: str = "all") -> dict:
    """Provide input suggestion service, returning matching POI information based on keywords
    
    Parameters:
        keywords: Query keyword, e.g. "McDonald's"
        location: Optional location coordinates, format "longitude,latitude", e.g. "113.914352,22.725713"
        city: Query city, e.g. "Guangming District, Shenzhen"
        types: Query POI type
        datatype: Type of data to return, default "all" (all types)
        
    Returns:
        List of matching location information
    """
    api_key = MAP_API_KEY
    url = "https://restapi.amap.com/v3/assistant/inputtips"
    params = {
        "keywords": keywords,
        "key": api_key,
        "output": "json",
        "datatype": datatype
    }
    
    if location:
        params["location"] = location
        
    if city:
        params["city"] = city
        
    if types:
        params["types"] = types
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        logger.info(f"Input tips API status: {data.get('status')}")
        return data
    except Exception as e:
        logger.error(f"Error calling input tips API: {e}")
        return {"status": "0", "info": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")