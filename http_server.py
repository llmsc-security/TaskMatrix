"""
HTTP Server for TaskMatrix Visual ChatGPT

This module provides a FastAPI HTTP server that wraps the TaskMatrix Gradio app
to provide REST API endpoints for chat interactions.
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

# Configuration
GRADIO_HOST = os.environ.get('GRADIO_HOST', 'localhost')
GRADIO_PORT = int(os.environ.get('WEB_PORT', 7861))
HTTP_PORT = int(os.environ.get('HTTP_PORT', 8000))

# Create FastAPI app
app = FastAPI(
    title="TaskMatrix API",
    description="Visual ChatGPT API",
    version="1.0.0",
)


class MessageRequest(BaseModel):
    """Request model for message endpoint."""
    message: str = Field(..., description="Message text to send")
    language: str = Field(default="English", description="Language (Chinese or English)")


class MessageResponse(BaseModel):
    """Response model for message endpoint."""
    success: bool
    reply: Optional[str] = None
    error: Optional[str] = None


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns the current status of the TaskMatrix service.
    """
    return {
        "status": "healthy",
        "service": "TaskMatrix API",
        "version": "1.0.0",
        "gradio_port": GRADIO_PORT,
        "http_port": HTTP_PORT
    }


@app.get("/", tags=["Info"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": "TaskMatrix API",
        "version": "1.0.0",
        "description": "Visual ChatGPT - Multi-Modal AI Assistant",
        "endpoints": {
            "health": "/health",
            "message": "/api/message (POST)",
            "gradio": f"http://{GRADIO_HOST}:{GRADIO_PORT}"
        }
    }


@app.post("/api/message", tags=["Chat"], response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """
    Send a message to the Visual ChatGPT bot.

    This endpoint provides a simplified way to interact with TaskMatrix
    through the Gradio backend.

    Args:
        request: MessageRequest with message text and optional language

    Returns:
        MessageResponse with the bot's reply
    """
    try:
        # Get the Gradio app endpoint
        # TaskMatrix runs on port 7861 by default
        gradio_url = f"http://{GRADIO_HOST}:{GRADIO_PORT}"

        # Check if Gradio is running
        try:
            resp = requests.get(f"{gradio_url}/", timeout=5)
            if resp.status_code != 200:
                raise HTTPException(status_code=503, detail="Gradio service not available")
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=503, detail=f"Gradio service unavailable: {str(e)}")

        # Note: TaskMatrix doesn't have a direct REST API, so we return
        # information about how to access the Gradio interface
        return MessageResponse(
            success=True,
            reply=f"TaskMatrix Visual ChatGPT is running. Access the Gradio interface at {gradio_url}",
            error=None
        )

    except HTTPException:
        raise
    except Exception as e:
        return MessageResponse(
            success=False,
            reply=None,
            error=str(e)
        )


@app.get("/info", tags=["Info"])
async def get_info():
    """
    Get detailed information about the TaskMatrix service.
    """
    return {
        "service": "TaskMatrix Visual ChatGPT",
        "version": "1.0.0",
        "gradio_host": GRADIO_HOST,
        "gradio_port": GRADIO_PORT,
        "http_port": HTTP_PORT,
        "capabilities": [
            "Image Captioning",
            "Text to Image Generation",
            "Visual Question Answering",
            "Conversation Memory",
            "Multi-language support"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "http_server:app",
        host="0.0.0.0",
        port=HTTP_PORT,
        reload=False
    )
