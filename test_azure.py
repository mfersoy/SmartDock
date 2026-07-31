import asyncio
import base64
import json
import httpx
from app.config import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, SYSTEM_PROMPT

async def test_vision():
    headers = {
        "api-key": AZURE_OPENAI_KEY,
        "Content-Type": "application/json"
    }
    
    # Read sample image
    with open("/Users/mini/Desktop/örnek dökümanlar/finans çek.jpg", "rb") as f:
        image_bytes = f.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Lütfen bu çek görselini analiz et."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "response_format": {"type": "json_object"},
        "max_completion_tokens": 2048,
        "temperature": 0.0
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        print("Sending request with image...")
        response = await client.post(AZURE_OPENAI_ENDPOINT, headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    asyncio.run(test_vision())
