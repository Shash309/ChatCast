# ChatCast - A Chat Application with History and Bot Responses

## Overview
ChatCast is a chat application built using Python's `Tkinter` library, designed to provide a simple messaging interface where users can send and receive messages. The application also includes a chatbot that provides automated responses based on user input. Chat history is saved to a file and can be loaded again when the application is reopened.

### Key Features:
- **User Messaging:** Allows users to send and receive messages in a chat interface.
- **Bot Responses:** A chatbot (named "Matrix") responds to user messages with predefined replies.
- **Message History:** Chat messages are stored in a linked list and saved to a file (`chat_history.json`) for persistent chat history across sessions.
- **Clear Chat & Delete Last Message:** Users can clear the entire chat or delete the last message sent.
- **Save & Load History:** Chat history is saved in a JSON file and can be loaded again when reopening the app.

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Clone this repository to your local machine.
   ```bash
   git clone https://github.com/your-username/chatcast.git



## Usage

1. After running the app, the first prompt will ask you to enter your username.
2. You can send messages by typing in the message box and pressing Enter or using the "Send Message" button.
3. The chatbot "Matrix" will respond based on the predefined responses.
4. You can clear the chat, delete the last message, or save/load chat history using the corresponding buttons.
5. Chat history is saved automatically when the application is closed.

## Features Detail

* **Chat Interface:**
    * The user can interact with the chat interface, which displays messages from both the user and the bot.
    * The messages are shown in a scrollable window.

* **Chat History:**
    * Every message sent (either by the user or the bot) is saved along with a timestamp and the sender's username.
    * The history is stored in a linked list structure, which is saved to a `chat_history.json` file.

* **Bot Responses:**
    * The bot responds to common phrases such as "hello", "how are you", and "tell me a joke".
    * If the bot doesn't have a matching response, it will provide a random reply.

## Features to be Added

* **User Authentication:** Implement user login and registration.
* **Real-time messaging:** Add support for multiple users in a real-time chat environment.
* **File Sharing:** Implement file upload/download support.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

* This application uses `Tkinter` for the graphical user interface.
* Chatbot responses are predefined in the code, and future updates may allow dynamic learning.
### Running the Application
To run the application, simply execute the following command:
```bash
  python app.py




