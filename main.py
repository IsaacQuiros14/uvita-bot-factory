from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import os
from datetime import datetime

app = FastAPI(title="WhatsApp Bot Factory")

@app.get("/")
async def root():
    return {
        "status": "Bot Factory Online",
        "version": "1.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN", "test123")
    
    if mode == "subscribe" and token == verify_token:
        print(f"Webhook verificado correctamente")
        return PlainTextResponse(challenge)
    
    print(f"Verificación fallida - Token incorrecto")
    return PlainTextResponse("Error", status_code=403)

@app.post("/webhook")
async def receive_message(request: Request):
    try:
        data = await request.json()
        print(f"Mensaje recibido: {data}")
        
        return {"status": "received", "timestamp": datetime.now().isoformat()}
        
    except Exception as e:
        print(f"Error procesando mensaje: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

