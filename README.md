# Alekhyaa

Alekhyaa is a text-to-video tool. Simply provide a script, and it will create a video with synchronized audio. If you provide video clips, Alekhyaa will adjust and concatenate them based on the audio content.

## Installation

### Prerequisites

- Python 3.10 or higher

### Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/alekhyaa.git
    cd alekhyaa
    ```

2. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    - Create a `.env` file in the root directory of the project.
    - Copy the contents of `env.template` into the `.env` file:
      ```plaintext
      GEMINI_API_KEY=gemini_key_here
      UNSPLASH_CLIENT_ID=unsplash_client_id_here // to get the images based on the script content if not videos are imported
      OPENAI_API_KEY=openai_api_key_here // if you want to use the GPT
      ```
    - Replace the placeholder with your actual API key.

## Usage

1. **Run the main script**:
    ```bash
    python main.py
    ```

This will open a webpage where you can upload an image or video and provide a script. Alekhyaa will process the inputs and generate the final video.
