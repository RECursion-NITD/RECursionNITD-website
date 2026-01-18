from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render

class APIModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Check if strict API mode is enabled
        if not getattr(settings, 'API_ONLY_MODE', False):
            return self.get_response(request)

        # 2. Check if the path is allowed
        path = request.path
        
        # Always allow these prefixes
        allowed_prefixes = [
            '/api/', 
            '/admin/', 
            '/static/', 
            '/media/', 
            '/oauth/',
        ]
        
        # Add whitelisted paths from settings
        whitelist = getattr(settings, 'API_MODE_WHITELIST', [])
        
        # Helper to check permissions
        is_allowed = False
        
        # Check standard prefixes
        for prefix in allowed_prefixes:
            if path.startswith(prefix):
                is_allowed = True
                break
        
        # Check whitelist (can be exact match or prefix)
        if not is_allowed:
            for item in whitelist:
                # If item ends with slash, treat as prefix? 
                # Ideally, simple startswith check is flexible enough
                if path.startswith(item):
                    is_allowed = True
                    break

        if is_allowed:
            return self.get_response(request)

        # 3. Block access
        # Return a simple unauthorized HTML page
        content = """
        <html>
            <head><title>Unauthorized</title></head>
            <body style="display:flex; justify-content:center; align-items:center; height:100vh; font-family:sans-serif; text-align:center;">
                <div>
                    <h1>APIs are routed through this! (●'◡'●)</h1>
                </div>
            </body>
        </html>
        """
        return HttpResponse(content, status=200) # Using 200 so it renders nicely in browser, or could use 403
