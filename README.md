# AfyaChap [AfricasTalking May 2025 Hackathon]

This is powered by [AfricasTalking](https://www.africastalking.com/). So you will need to create an account and get your API key and username.

## Description

To be documented soon.

## Installation

Instructions are for UNIX-like systems. For Windows, the commands are similar but may require slight adjustments.

1. Clone the repository:

2. Create a virtual environment:

   ```bash
   python3.12 -m venv venv
   ```

3. Activate the virtual environment:

      ```bash
      source venv/bin/activate
      ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   Create a `.env` file in the root directory of the project and add your AfricasTalking credentials:

   ```plaintext
   AFRICASTALKING_USERNAME=your_username
   AFRICASTALKING_API_KEY=your_api_key
   GEMINI_API_KEY=your_gemini_api_key
   ```

6. Run the application:

   ```bash
    python main.py
    ```

    or

    ```bash
    uvicorn main:app
    ```
