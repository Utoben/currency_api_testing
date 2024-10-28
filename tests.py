import pytest
import requests
from config import *


BASE_URL = "https://api.apilayer.com/currency_data"

# успешное подключение к API
def test_api_connection():
    url = f"{BASE_URL}/live"
    headers = {"apikey": API_KEY}
    response = requests.get(url, headers=headers)
    
    # проверка статуса ответа 200 (успешно)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    print("Connection test passed.")


# проверка, что данные содержат основные элементы
def test_api_response_structure():
    url = f"{BASE_URL}/live"
    headers = {"apikey": API_KEY}
    response = requests.get(url, headers=headers)
    
    data = response.json()
    
    # проверка, что ответ содержит основные ключи
    assert "success" in data, "Missing 'success' in response"
    assert "quotes" in data, "Missing 'quotes' in response"
    assert "timestamp" in data, "Missing 'timestamp' in response"
    assert data["success"] is True, "API call was not successful"
    print("Response structure test passed.")


# проверка курса конкретной валюты
def test_specific_currency_quote():
    url = f"{BASE_URL}/live"
    headers = {"apikey": API_KEY}
    params = {"source": "USD", "currencies": "EUR"}
    response = requests.get(url, headers=headers, params=params)
    
    data = response.json()
    
    # проверка, что курс валюты USD к EUR присутствует
    assert "USDEUR" in data["quotes"], "USD to EUR quote missing in response"
    
    # проверка, что курс число и положительный
    usd_to_eur = data["quotes"]["USDEUR"]
    assert isinstance(usd_to_eur, float) and usd_to_eur > 0, "Invalid USD to EUR quote"
    print("Specific currency quote test passed.")


# проверка обработки некорректного ключа
def test_invalid_api_key():
    url = f"{BASE_URL}/live"
    headers = {"apikey": "INVALID_KEY"}
    response = requests.get(url, headers=headers)
    
    # проверка кода ошибки 401 или 403 (ошибка авторизации/unauthorized)
    assert response.status_code in [401, 403], f"Unexpected status code for invalid key: {response.status_code}"
    print("Invalid API key test passed.")
