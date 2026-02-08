#!/usr/bin/env python3
"""
Tutorial PoC - HTTP API Test Client for TaskMatrix Visual ChatGPT

This script demonstrates how to interact with the Gradio-based Visual ChatGPT
service through its HTTP API endpoints.

Usage:
    python tutorial_poc.py

The Gradio app exposes several endpoints:
- /: Main Gradio interface (HTML)
- /queue/status: Queue status endpoint
- /api/: Public API endpoints for specific functions

Note: The internal Gradio app uses port 7861, mapped to host port 11220.
"""

import requests
import json
import argparse
import time
from typing import Optional, Dict, Any


class VisualChatGPTClient:
    """Client for interacting with TaskMatrix Visual ChatGPT via HTTP API."""

    def __init__(self, base_url: str = "http://localhost:11220"):
        """
        Initialize the client.

        Args:
            base_url: Base URL of the Gradio service (host:port)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def check_connection(self) -> bool:
        """Check if the service is running and accessible."""
        try:
            response = self.session.get(f"{self.base_url}/")
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Connection failed: {e}")
            return False

    def get_gradio_config(self) -> Optional[Dict[str, Any]]:
        """Get the Gradio app configuration (fingerprint and components)."""
        try:
            response = self.session.get(f"{self.base_url}/config")
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get config: {e}")
        return None

    def queue_status(self) -> Optional[Dict[str, Any]]:
        """Check the current queue status."""
        try:
            response = self.session.get(f"{self.base_url}/queue/status")
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to get queue status: {e}")
        return None

    def run_text(
        self,
        text: str,
        chat_history: Optional[list] = None,
        lang: str = "English"
    ) -> Dict[str, Any]:
        """
        Run a text-only query through the chat interface.

        Args:
            text: The input text query
            chat_history: Optional list of previous conversation messages
            lang: Language choice ('English' or 'Chinese')

        Returns:
            API response containing the chatbot's response
        """
        payload = {
            "data": [text, chat_history or [], lang],
            "fn_index": 1,  # fn_index for run_text in the Gradio app
            "event_data": None,
            "session_hash": str(int(time.time() * 1000))
        }

        try:
            response = self.session.post(
                f"{self.base_url}/run/text",
                json=payload,
                timeout=60
            )
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Text run failed: {e}")
        return {"error": "Request failed"}

    def run_image(
        self,
        image_path: str,
        text: str = "",
        chat_history: Optional[list] = None,
        lang: str = "English"
    ) -> Dict[str, Any]:
        """
        Run a query with an image upload.

        Args:
            image_path: Path to the image file
            text: Optional text query alongside the image
            chat_history: Optional list of previous conversation messages
            lang: Language choice ('English' or 'Chinese')

        Returns:
            API response containing the chatbot's response
        """
        # Read the image file
        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()
        except FileNotFoundError:
            return {"error": f"Image file not found: {image_path}"}
        except Exception as e:
            return {"error": f"Failed to read image: {e}"}

        # For image uploads, Gradio typically uses multipart/form-data
        # This is a simplified example - actual implementation may vary
        files = {
            "file": ("image.png", image_data, "image/png")
        }
        data = {
            "data": [text, chat_history or [], lang],
            "fn_index": 2,  # fn_index for run_image
            "session_hash": str(int(time.time() * 1000))
        }

        try:
            response = self.session.post(
                f"{self.base_url}/run/image",
                data=data,
                files=files,
                timeout=60
            )
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Image run failed: {e}")
        return {"error": "Request failed"}

    def clear_memory(self) -> Dict[str, Any]:
        """Clear the conversation memory."""
        payload = {
            "data": [],
            "fn_index": 3,  # Assuming clear memory is fn_index 3
            "session_hash": str(int(time.time() * 1000))
        }

        try:
            response = self.session.post(
                f"{self.base_url}/run/clear",
                json=payload,
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Clear memory failed: {e}")
        return {"error": "Request failed"}

    def detect_tools(self) -> list:
        """
        List available tools in the Visual ChatGPT system.

        Based on the code, the following tools are available:
        - ImageCaptioning: Generate captions for images
        - Text2Image: Generate images from text
        - Image2Pose: Detect poses in images
        - Pose2Image: Generate images from poses
        - Image2Seg: Generate segmentations from images
        - Seg2Image: Generate images from segmentations
        - Image2Depth: Estimate depth from images
        - Depth2Image: Generate images from depth maps
        - Image2Normal: Generate normal maps from images
        - Normal2Image: Generate images from normal maps
        - VisualQuestionAnswering: Answer questions about images
        """
        return [
            "ImageCaptioning",
            "Text2Image",
            "Image2Pose",
            "Pose2Image",
            "Image2Seg",
            "Seg2Image",
            "Image2Depth",
            "Depth2Image",
            "Image2Normal",
            "Normal2Image",
            "VisualQuestionAnswering"
        ]


def demo_interactive():
    """Run an interactive demo of the Visual ChatGPT client."""
    print("=" * 60)
    print("TaskMatrix Visual ChatGPT - Interactive Demo")
    print("=" * 60)
    print()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Visual ChatGPT Client")
    parser.add_argument("--url", default="http://localhost:11220",
                        help="Base URL of the Gradio service")
    args = parser.parse_args()

    # Initialize client
    client = VisualChatGPTClient(args.url)

    # Check connection
    print(f"Connecting to {client.base_url}...")
    if not client.check_connection():
        print("Failed to connect. Make sure the service is running.")
        print("\nTo start the service in Docker:")
        print("  cd /path/to/TaskMatrix")
        print("  ./invoke.sh")
        return

    print("Connected successfully!\n")

    # Display available tools
    print("Available tools:")
    for i, tool in enumerate(client.detect_tools(), 1):
        print(f"  {i}. {tool}")
    print()

    # Main interaction loop
    chat_history = []
    lang = "English"

    print("Type 'quit' to exit, 'clear' to clear history, 'lang' to switch language")
    print("-" * 40)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if not user_input:
            continue

        if user_input.lower() == 'quit':
            print("Goodbye!")
            break

        if user_input.lower() == 'clear':
            chat_history = []
            print("Conversation history cleared.")
            continue

        if user_input.lower() == 'lang':
            lang = "Chinese" if lang == "English" else "English"
            print(f"Language switched to: {lang}")
            continue

        # Send query
        print(f"\nAssistant ({lang}): ", end="", flush=True)

        result = client.run_text(user_input, chat_history, lang)

        if "error" in result:
            print(f"Error: {result['error']}")
            continue

        # Process response
        if "data" in result:
            response_data = result["data"]
            print(response_data.get("data", response_data))
        else:
            print(result)

        # Update chat history (simplified)
        chat_history.append((user_input, result))


def demo_simple():
    """Run a simple test of the client functionality."""
    print("TaskMatrix Visual ChatGPT - Simple Test")
    print("-" * 40)

    client = VisualChatGPTClient("http://localhost:11220")

    print("1. Checking connection...")
    if client.check_connection():
        print("   Connection: OK")
    else:
        print("   Connection: FAILED")
        print("\nMake sure the Docker container is running:")
        print("  ./invoke.sh")
        return

    print("\n2. Getting Gradio config...")
    config = client.get_gradio_config()
    if config:
        print("   Config retrieved successfully")
        print(f"   Fingerprint: {config.get('fingerprint', 'N/A')}")
    else:
        print("   Failed to get config")

    print("\n3. Checking queue status...")
    status = client.queue_status()
    if status:
        print(f"   Queue info: {json.dumps(status, indent=4)}")
    else:
        print("   Failed to get queue status")

    print("\n4. Available tools:")
    for tool in client.detect_tools():
        print(f"   - {tool}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_interactive()
    else:
        demo_simple()
