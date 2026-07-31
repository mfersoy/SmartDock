import base64
import json
import logging
import httpx
from app.config import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, SYSTEM_PROMPT

logger = logging.getLogger("vision_service")

async def analyze_check_image(image_bytes: bytes, mime_type: str = "image/png") -> dict:
    """
    Sends the check image bytes to the Azure OpenAI gpt-5.1-ptu vision endpoint,
    requesting document key details in JSON format based on banking safety system prompts.
    """
    # 1. Convert image bytes to base64
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    
    # 2. Build headers
    headers = {
        "api-key": AZURE_OPENAI_KEY,
        "Content-Type": "application/json"
    }
    
    # 3. Build payload as specified by Azure OpenAI format
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
                        "text": "Lütfen bu çek görselini analiz et, tutarları karşılaştır ve sadece belirtilen JSON formatında yanıt dön."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "response_format": {"type": "json_object"},
        # Crucial Note: Using max_completion_tokens instead of max_tokens as requested by the user
        "max_completion_tokens": 2048,
        "temperature": 0.0
    }
    
    # 4. Perform async request using httpx
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            logger.info("Sending request to Azure OpenAI Vision API...")
            response = await client.post(AZURE_OPENAI_ENDPOINT, headers=headers, json=payload)
            response.raise_for_status()
            
            # Extract response payload
            result = response.json()
            logger.info("Response received successfully from Azure OpenAI.")
            
            # Extract messages content text
            logger.info(f"Raw API Response: {json.dumps(result, ensure_ascii=False)}")
            
            message = result["choices"][0]["message"]
            content_str = message.get("content")
            if content_str is None:
                raise Exception(f"No content in message. Full message: {message}")
            
            # Parse response string to dict
            analysis_data = json.loads(content_str)
            return analysis_data
            
        except httpx.HTTPStatusError as http_err:
            logger.error(f"HTTP error occurred: {http_err.response.status_code} - {http_err.response.text}")
            raise Exception(f"Vision API Çağrısı başarısız oldu: Sunucu kodu {http_err.response.status_code}")
        except json.JSONDecodeError as json_err:
            logger.error(f"JSON parsing error: {json_err} on content: {content_str if 'content_str' in locals() else 'None'}")
            raise Exception("Vision API'den gelen yanıt geçerli bir JSON formatında değil.")
        except Exception as e:
            logger.error(f"Unexpected error calling Vision service: {e}")
            raise Exception(f"Sistem hatası: {str(e)}")
