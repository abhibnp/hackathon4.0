import requests
import random
import time
import string

# URL of the registration page
url = 'http://127.0.0.1:5000/register'

# List of common bot user-agents
bot_user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",  # Common bot
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",  # Google bot
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",  # Bing bot
    "Mozilla/5.0 (compatible; Slurp/3.0; Yahoo! Slurp)",  # Yahoo bot
    "curl/7.68.0",  # cURL bot
    "python-requests/2.24.0",  # Python requests bot
]

# Random data generators for different types of bot attacks
def generate_random_string(length=10):
    """Generate a random string of letters and digits."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_email():
    """Generate a random email."""
    return generate_random_string(8) + "@example.com"

# Function to simulate bot registration request with User-Agent Spoofing
def send_bot_request(user_agent=None):
    if not user_agent:
        user_agent = random.choice(bot_user_agents)  # Use a random user agent

    headers = {'User-Agent': user_agent}

    try:
        response = requests.post(url, headers=headers)
        print(f"Response Code: {response.status_code}, Message: {response.json().get('message')}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

# Function to simulate Rate-Limiting Flood Attack (Too many requests in short time)
def rate_limiting_attack():
    for _ in range(10):  # Sending 10 requests quickly
        send_bot_request()
        time.sleep(random.uniform(0.1, 0.5))  # Random delay between requests

# Function to simulate CAPTCHA Bypass Attempt (Conceptual)
def captcha_bypass_attack():
    # Simulating an attack that attempts to bypass CAPTCHA (this will not actually bypass CAPTCHA)
    for _ in range(5):
        headers = {
            'User-Agent': random.choice(bot_user_agents),
            'X-BYPASS-CAPTCHA': 'true',  # Hypothetical header to bypass CAPTCHA
        }
        try:
            response = requests.post(url, headers=headers)
            print(f"Captcha Bypass Attempt: {response.status_code}, Message: {response.json().get('message')}")
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")

# Function to simulate Request Flood (Multiple requests from different IPs)
def request_flood():
    # Simulating requests with different IPs by using proxy or spoofed IP
    proxies = {
        "http": "http://127.0.0.1:8080",  # Use a proxy server if available
        "https": "http://127.0.0.1:8080",  # This could be any proxy
    }
    for _ in range(15):
        send_bot_request(user_agent=random.choice(bot_user_agents))
        time.sleep(random.uniform(0.1, 0.3))  # Random delay

# Function to simulate Form Field Flooding (Filling out forms with random data)
def form_field_flooding():
    data = {
        'username': generate_random_string(),
        'password': generate_random_string(),
        'email': generate_random_email(),
    }
    headers = {
        'User-Agent': random.choice(bot_user_agents),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(url, data=data, headers=headers)
        print(f"Form Flood Attempt: {response.status_code}, Message: {response.json().get('message')}")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

# Main function to initiate various bot attack types
def run_multiple_attacks():
    while True:
        # Randomly choose an attack type to run
        attack_type = random.choice([
            rate_limiting_attack,
            captcha_bypass_attack,
            request_flood,
            form_field_flooding
        ])

        print(f"Executing {attack_type.__name__}...")
        attack_type()  # Execute the chosen attack type

        print("---- End of attack cycle ----\n")
        time.sleep(random.uniform(1, 3))  # Random wait time between attack cycles

if __name__ == "__main__":
    run_multiple_attacks()
