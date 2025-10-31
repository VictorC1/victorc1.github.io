# OAuth configuration for GitHub Pages domain
GGG_REDIRECT_URI = "https://victorc1.github.io/poe-oauth-callback"  # Public GitHub Pages
GGG_CLIENT_ID = "your_ggg_client_id"  # From GGG Developer Portal
GGG_CLIENT_SECRET = "your_ggg_secret"  # From GGG Developer Portal

@app.route('/api/ggg/auth')
def start_ggg_oauth():
    """Start OAuth flow - redirects to GGG with GitHub Pages as callback"""
    auth_url = (
        "https://www.pathofexile.com/oauth/authorize?"
        f"client_id={GGG_CLIENT_ID}&"
        "response_type=code&"
        f"state={secrets.token_urlsafe(16)}&"
        f"redirect_uri={GGG_REDIRECT_URI}&"
        "scope=service:currency_exchange&"
        "prompt=consent"
    )
    return jsonify({"auth_url": auth_url})

@app.route('/api/ggg/handle-callback')
def handle_ggg_callback():
    """Your private endpoint that receives the forwarded OAuth code"""
    code = request.args.get('code')
    state = request.args.get('state')
    
    if not code:
        return jsonify({"error": "No authorization code received"}), 400
    
    try:
        # Exchange code for token (using your private backend)
        token_data = exchange_code_for_token(code)
        
        # Store token securely in your database
        store_ggg_token(token_data)
        
        return jsonify({
            "status": "success", 
            "message": "GGG OAuth completed successfully"
        })
        
    except Exception as e:
        logging.error(f"OAuth token exchange failed: {e}")
        return jsonify({"error": str(e)}), 500

def exchange_code_for_token(authorization_code):
    """Exchange OAuth code for access token"""
    token_url = "https://www.pathofexile.com/oauth/token"
    
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': GGG_REDIRECT_URI,
        'client_id': GGG_CLIENT_ID,
        'client_secret': GGG_CLIENT_SECRET
    }
    
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    return response.json()
