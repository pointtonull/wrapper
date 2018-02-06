# Universal API Wrapper

This module creates a complete Python API Wrapper for any introspective API.

This will work as long as the root url returns a description of the API Available methods.

```javascript
{
  "service": "Example API",
  "endpoints": [
    {
      "url": "POST /auth",
      "description": "data is the complex thingy"
    },
    {
      "url": "GET /describe/{thingy}",
      "description": "Get info for given thingy"
    },
    {
      "url": "GET /",
      "description": "Self-documenting endpoint."
    }
  ]
}
```

