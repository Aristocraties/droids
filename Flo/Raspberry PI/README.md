> :warning: **This project is still under testing**: The installation instructions are yet to be verified on a fresh install. Please proceed with caution.

# Raspberry Pi Voice Assistant + ChatGPT

## Hardware Requirements

This project requires the following hardware:

- **Raspberry Pi 4B**: Currently, the project is designed to work with the Raspberry Pi 4B. Support for the Raspberry Pi 5 is in progress, but it's not officially supported by Picovoice yet. A workaround exists for all Picovoice libraries except PVRecorder. It's possible to use PyAudio as an alternative to PVRecorder, but this hasn't been tested yet. Note that the speech-to-text transcription may run a bit slow on the 4B, but it's expected to improve significantly on the 5 due to better disk and CPU performance.

- **USB Microphone**: A USB microphone is required for voice input. The one used in this project is available on [Amazon](https://www.amazon.com/gp/product/B075M7FHM1/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1).  The microphone you use will likely depend on your droid.  I found I needed to keep the cover on mine to prevents false wakes, but that also limits the voice range some.  Be sure to set this as your default input audio device in the OS.

- **USB Speaker**: A USB speaker is required for voice output. The one used in this project is available on [Amazon](https://www.amazon.com/gp/product/B08M37224H/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1).  This will be defined by the amount of speaker space you have.  This was one of the smallest I could find and it works fine.  It's not super loud and does not have volume controls on it.  I set the volume in the operating system (literally running it with keyboard, mouse, and monitor plugged in).  Be sure to set this as your default output audio device in the OS.


## Software Requirements

- **Debian 11 Bullseye**: I'm going to get it working on the Bookworm OS once the Pi 5 support exists for PicoVoice.  I used the 64-bit version of the Debian 11 Bullseye OS.  You install this with the Pi Imager like usual.  Here's an instructional link: https://www.raspberrypi.com/software/operating-systems/.

- **PicoVoice**: You'll need to create an account for [PicoVoice](https://console.picovoice.ai/login) so you can get the model files you need and the access keys. They have a development license that is pretty generous. At last look, it allowed for 25 hours of free Rhino and Leopard usage each month. Given how expensive it is to go from developer to actual customer, hopefully this suffices for most needs. They have a ton of documentation on their development website about how to create the model files you'll need.

  > Another option for higher usage levels is to just use PicoVoice for the wake word and use Open AI for the rest. You can implement intent recognition using Open AI's function calling. I'll likely create a version with that too. The downside of this approach is latency. Each step requires a call through the internet. I haven't tested whether the increased latency would be greater than the processing time of onboard speech to text.  Ideally, OpenAI would create an API endpoint that allowed one to pass audio in directly, transcribe, and return audio directly. That doesn't exist yet.  
  
  > It's also worth noting the AI response times are slow.  That'll likely improve in the future, but is reality now.  Don't expect it to feel like a conversation with another person.  I haven't tried to incorporate a streaming response yet.  

- **Open AI API**: You'll need to get a license key for [OpenAI's API](https://openai.com/blog/openai-api).  They have a wallet function you can use to add money for your usage.  I'm not sure how long it will work this way, but I added $50 to my wallet in November and they seem to give me an $18 credit that I never seem to use up.  Not sure how/why that works.  I've been using the GPT-4 model as it seems to have the best ability to follow my droid-based system prompt and incorporate creativity in the response best.  For the text-to-speech, they have six models you can choose from.  I'm using Nova for Flo, but you just change the model name in the main.py code.


## Software Installation
> :bulb: **Tip:** I did most of the installation, configuration, and testing with the Raspberry Pi connected to keyboard, mouse, and monitor.  You'll run out of USB ports when you want to add the eyes, so you could just comment those parts out in the main.py file until you're ready to run it headless. 

I found this guide to [Python Virtual Environments](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) helpful.

1. Start by creating a folder structure. Open a terminal and run the following command to create the directory path `/environments/florence` (replace florence with whatever you want to call your project):

   ```bash
   mkdir -p /environments/florence
   ```

2. Navigate to the newly created directory (change florence to whatever you called your project):

   ```bash
   cd /environments/florence
   ```

3. Create a Python 3 virtual environment named `florence` (replace florence with whatever you named your directory):

   ```bash
   python3 -m venv florence
   ```

4. Activate the virtual environment:

   ```bash
   source florence/bin/activate
   ```

    Note: The command to activate the virtual environment may vary depending on your shell. If you're using a shell other than bash, replace source with . (dot).

5. Check that the virtual environment is activated successfully:
    ```
    deactivate
    ```
6. Once the virtual environment is activated, install the necessary Python packages from the `requirements.txt` file. Make sure you're in the project directory where `requirements.txt` is located:

   ```bash
   pip install -r requirements.txt
   ```

    > :bulb: **Note:** Remember to deactivate the virtual environment when you're done by running deactivate.  This won't be necessary once we have it running as a service.
        ```
        deactivate
        ```
7.  Add your API keys to either a .env file (forthcoming) or edit main.py to add them.  Also add the path to your PicoVoice model files.
    ```
    LEOPARD = pvleopard.create(
            access_key='PICOVOICE_LEOPARD_ACCESS_KEY',
            model_path='/path/to/your leopard file.pv'
            )
    global RHINO
    RHINO = pvrhino.create(
            access_key='PICOVOICE_RHINO_ACCESS_KEY',
            context_path='/path/to/your rhino file.rhn'
            )
    global PORCUPINE
    PORCUPINE = pvporcupine.create(
            access_key='PICOVOICE_PORCUPINE_ACCESS_KEY',
            keyword_paths=['/path/to/your porcupine file.ppn']
            )

    with noalsaerr():
        global AUDIO
        AUDIO = pyaudio.PyAudio()

    print('testing')
    global CLIENT
    #recommend using a .env file to store your OpenAI API key
    CLIENT = OpenAI(api_key='OPENAI_API_KEY')
    ```

8. If you have commented out the arduino functions and activated your virtual environment, you should be able to run the main.py function to test it out.
    ```
    python main.py
    ```

## Run as a Service

I tried multiple ways to get this to run as a system service, but in the end, it was easiest to run as a user service.  That preserved all my user settings, particularly audio, and enabled it to work easiest.  User services don't start by default, though, so an additional command was required.

This [article](https://www.baeldung.com/linux/systemd-create-user-services) was very helpful. 

1. Edit and rename the florence.service as needed.  Note that the path to your virtual environment needs to be correct in the ExecStart.  I have two commands running here.  The first one starts the python virtual environment by calling python.  The second starts the main.py file.

2. Now, with the sudo privilege let’s copy the unit file to the /etc/systemd/user directory.
    ```
    cp florence.service /etc/system/user
    ```
