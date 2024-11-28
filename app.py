from flask import Flask, request, render_template, jsonify
import time
import re
from collections import defaultdict
import random
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Track bot and human request counts
bot_count = 0
human_count = 0

# Track different types of bot attacks
bot_attack_types = defaultdict(int)

# Store all request details, including bot and human requests
request_details = []

# To track request timestamps for each IP
ip_request_timestamps = defaultdict(list)

# List of common bot user-agents
bot_user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",  # Common bot
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",  # Google bot
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",  # Bing bot
    "Mozilla/5.0 (compatible; Slurp/3.0; Yahoo! Slurp)",  # Yahoo bot
    "curl/7.68.0",  # cURL bot
    "python-requests/2.24.0",  # Python requests bot
]

# Function to generate random string
def generate_random_string(length=10):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))

# Route to the registration page
@app.route('/')
def registration():
    return render_template('registration.html')

# Route to the dashboard page
@app.route('/dashboard')
def dashboard():
    global bot_count, human_count
    # Prepare pie chart for bot attack types
    pie_chart_url = generate_pie_chart()

    # Display the request details in the table on the dashboard
    return render_template('dashboard.html', bot_count=bot_count, human_count=human_count, request_details=request_details, pie_chart_url=pie_chart_url)

# Function to generate pie chart for bot attack types
def generate_pie_chart():
    global bot_attack_types
    labels = list(bot_attack_types.keys())
    sizes = list(bot_attack_types.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save pie chart to a BytesIO buffer and encode as base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close(fig)  # Close the plot to free up memory

    return f"data:image/png;base64,{img_base64}"

# Route for registration logic (handling POST requests)
@app.route('/register', methods=['POST'])
def register():
    global bot_count, human_count
    user_agent = request.headers.get('User-Agent', '')
    timestamp = time.time()
    client_ip = request.remote_addr

    # Check for bot using User-Agent
    is_bot = re.search(r'(bot|spider|crawl|curl|wget)', user_agent, re.IGNORECASE)
    attack_type = "Human"

    if is_bot:
        bot_count += 1
        attack_type = "Bot - User-Agent Spoofing"
        bot_attack_types[attack_type] += 1
        request_details.append({
            'ip': client_ip,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)),
            'type': 'Bot',
            'details': 'Bot detected by User-Agent spoofing'
        })
        return jsonify({"message": "Registration rejected. Bot detected."}), 400

    # Track requests and behavior for detecting bot-like patterns (rate-limiting flood)
    ip_request_timestamps[client_ip].append(timestamp)

    # Check if too many requests from the same IP in a short time frame (e.g., 5 requests in 10 seconds)
    recent_requests = [t for t in ip_request_timestamps[client_ip] if timestamp - t < 10]
    ip_request_timestamps[client_ip] = recent_requests

    if len(recent_requests) > 5:
        bot_count += 1
        attack_type = "Bot - Rate-Limiting Flood"
        bot_attack_types[attack_type] += 1
        request_details.append({
            'ip': client_ip,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)),
            'type': 'Bot',
            'details': 'Bot-like behavior detected (too many requests in short time frame)'
        })
        return jsonify({"message": "Registration rejected. Bot-like behavior detected (too many requests)."}), 400

    # Successfully handle human request
    human_count += 1
    request_details.append({
        'ip': client_ip,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)),
        'type': 'Human',
        'details': 'Registration successful. Welcome!!'
    })

    return render_template('success.html'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
