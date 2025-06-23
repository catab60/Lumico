
<img src="https://github.com/catab60/Lumico/blob/main/assets/banner.gif?raw=true" width="800">


This is **Lumico**, an open-source animated wallpaper engine built entirely in **Python**, leveraging **Pygame** for the GUI and the **Windows API** for desktop integration. The project was a massive learning experience in understanding how Windows manages the desktop and how to manipulate it to render smooth, animated wallpapers that run seamlessly in the background.


## About the Project

**Lumico Version 1** provides a polished interface with four main tabs:

* **Home**
  Browse your **default**, **installed**, and **created** wallpapers in one place.
* **Browse**
  Discover and install **community-made** wallpapers directly from within the app.
* **Create**
  Upload your own **GIFs** and turn them into custom animated wallpapers.
* **Settings**
  • Enable **launch on startup** to have Lumico start with Windows

Under the hood, Lumico runs quietly in the system tray, keeping your desktop lively without impacting your workflow.

### Key Features

* **Animated wallpaper playback** truly integrated with the Windows desktop
* **System tray** control for quick access and pausing
* **Python + Pygame** GUI for cross-platform flexibility (Windows API calls for engine functionality)
* **Four intuitive tabs** for managing, browsing, creating, and configuring wallpapers
* **Open source** and extensible for community contributions

## Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/catab60/Lumico.git
   cd Lumico
   ```
2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
3. **Configure your Tenor API key:**
   Obtain a key from [Tenor Developers](https://tenor.com/gifapi) and place it at the top of `main.py`:

   ```python
   TENOR_API_KEY = "YOUR_API_KEY_HERE"
   ```
4. **Run Lumico:**

   ```bash
   python main.py
   ```

> **Note:** A Tenor API key is required to fetch GIFs for the **Create** tab. You’ll need to sign up at [https://tenor.com/developer](https://tenor.com/developer) and insert your key into `main.py`.

## Learning Experience

Building Lumico taught me:

* The inner workings of the **Windows desktop** and how to render custom content beneath desktop icons
* How to combine **Pygame** with low-level **Windows API** calls for a smooth user experience
* Best practices for managing long-running background processes and system tray integration

## Future Plans

* **Video to wallpaper** support (MP4, AVI, etc.)
* **Interactive wallpapers** powered by mini-games and custom IDE interface for developers

## Contributions

Lumico is completely open source, and community contributions are very welcome! Feel free to:

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Submit a pull request

Whether it’s optimizing performance, adding new wallpaper formats, or improving the UI, your help is appreciated!

















