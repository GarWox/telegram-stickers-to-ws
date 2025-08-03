# Telegram Stickers to WS

This is a Python script that allows you to export Telegram stickers to a `.wastickers` file. You can then use an app like **Sticker Maker** to import these stickers into WhatsApp.

## How to Use

1. **Create a Telegram Bot**:
   - Go to Telegram and search for **BotFather**.
   - Start a chat with BotFather and use the command `/newbot` to create a new bot.
   - Follow the instructions to get your bot token.

2. **Obtain API Credentials**:
   - You will need your bot token and the API ID and API Hash from the [Telegram API](https://my.telegram.org/apps).
   - Sign in and create a new application to get these credentials.

3. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   ```

2. Install the required dependencies.
  ```bash
    pip3 install -r requirements.txt
  ```
4. Run the script and send a sticker to your bot.

## Requirements
- Python 3.x
- Required libraries (see `requirements.txt`)

## License
This project is licensed under the MIT License.
