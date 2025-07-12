# Raspberry Pi Web Soundboard

A simple, self-hosted web-based soundboard application designed to run on a Raspberry Pi. Trigger audio clips from any device on your network through a clean web interface.

![image](https://placehold.co/600x300/222/FFF?text=Raspberry+Soundboard)

## ✨ Features

- **Web Interface:** Easy-to-use interface accessible from any browser on your local network.
- **Customizable:** Configure buttons and corresponding audio files easily by editing a `buttons.json` file.
- **Lightweight:** Designed to be minimal and run efficiently on single-board computers like the Raspberry Pi.

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

- A Raspberry Pi (or any Linux-based machine)
- Python 3.x
- `git`

### Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/xSora/RaspberrySoundboard.git
    cd RaspberrySoundboard
    ```

2.  **Install dependencies** (assuming a `requirements.txt` file):
    ```sh
    pip install -r requirements.txt
    ```

3.  **Configure the application:**
    - Create a `.env` file in the root directory for your environment variables:
      ```
      APP_SECRET='your_super_secret_and_random_key'
      ```
    - Place your audio files (e.g., `.mp3`, `.wav`) in a `data/audio/` directory.
    - Edit the `data/buttons.json` file to define the buttons and link them to your audio files.

4.  **Run the application:**
    ```sh
    python app.py
    ```

5.  **Access the soundboard:**
    Open your web browser and navigate to `http://<your-pi-ip-address>:5000`.

## 🗺️ Project Roadmap

This project is under active development. Here is a look at what's planned:

- **[Deployment]** Convert the project to use Docker for consistent and easy deployment.
- **[Backend]** Refactor file storage to use a dedicated external data directory.
- **[Security]** Enhance security by generating the `APP_SECRET` dynamically and managing it in a configuration file.
- **[Frontend]** Implement enhanced audio player controls, including a visual indicator for playing audio, a progress bar, and a stop button.
- **[Bug Fix]** Investigate and fix the scrolling issue on Raspberry Pi touch displays.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📄 License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.