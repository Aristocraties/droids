> :warning: **This project is still under testing**: The installation instructions are yet to be verified on a fresh install. Please proceed with caution.

# Raspberry Pi Voice Assistant + ChatGPT

## Hardware Requirements

This project requires the following hardware:

- **Raspberry Pi 4B**: Currently, the project is designed to work with the Raspberry Pi 4B. Support for the Raspberry Pi 5 is in progress, but it's not officially supported by Picovoice yet. A workaround exists for all Picovoice libraries except PVRecorder. It's possible to use PyAudio as an alternative to PVRecorder, but this hasn't been tested yet. Note that the speech-to-text transcription may run a bit slow on the 4B, but it's expected to improve significantly on the 5 due to better disk and CPU performance.

- **USB Microphone**: A USB microphone is required for voice input. The one used in this project is available on [Amazon](https://www.amazon.com/gp/product/B075M7FHM1/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1).  The microphone you use will likely depend on your droid.  I found I needed to keep the cover on mine to prevents false wakes, but that also limits the voice range some.  

- **USB Speaker**: A USB speaker is required for voice output. The one used in this project is available on [Amazon](https://www.amazon.com/gp/product/B08M37224H/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1).  This will be defined by the amount of speaker space you have.  This was one of the smallest I could find and it works fine.  It's not super loud and does not have volume controls on it.  I set the volume in the operating system (literally running it with keyboard, mouse, and monitor plugged in).


## Software Requirements

- **Debian 11 Bullseye**: I'm going to get it working on the Bookworm OS once the Pi 5 support exists for PicoVoice.  I used the 64-bit version of the Debian 11 Bullseye OS.  You install this with the Pi Imager like usual.  Here's an instructional link: https://www.raspberrypi.com/software/operating-systems/.

- **PicoVoice**: You'll need to create an account for [PicoVoice](https://console.picovoice.ai/login) so you can get the model files you need and the access keys. They have a development license that is pretty generous. At last look, it allowed for 25 hours of free Rhino and Leopard usage each month. Given how expensive it is to go from developer to actual customer, hopefully this suffices for most needs. They have a ton of documentation on their development website about how to create the model files you'll need.

  > Another option for higher usage levels is to just use PicoVoice for the wake word and use Open AI for the rest. You can implement intent recognition using Open AI's function calling. I'll likely create a version with that too. The downside of this approach is latency. Each step requires a call through the internet. I haven't tested whether the increased latency would be greater than the processing time of onboard speech to text.  Ideally, OpenAI would create an API endpoint that allowed one to pass audio in directly, transcribe, and return audio directly. That doesn't exist yet.  
  
  > It's also worth noting the AI response times are slow.  That'll likely improve in the future, but is reality now.  Don't expect it to feel like a conversation with another person.  I haven't tried to incorporate a streaming response yet.  

- **Open AI API**: You'll need to get a license key for [OpenAI's API](https://openai.com/blog/openai-api).  They have a wallet function you can use to add money for your usage.  I'm not sure how long it will work this way, but I added $50 to my wallet in November and they seem to give me an $18 credit that I never seem to use up.  Not sure how/why that works.  I've been using the GPT-4 model as it seems to have the best ability to follow my droid-based system prompt and incorporate creativity in the response best.  For the text-to-speech, they have six models you can choose from.  I'm using Nova for Flo, but you just change the model name in the main.py code.


## Software Installation
> :bulb: **Tip:** I did most of the installation, configuration, and testing with the Raspberry Pi connected to keyboard, mouse, and monitor.  You'll run out of USB ports when you want to add the eyes, so you could just comment those parts out in the main.py file until you're ready to run it headless. 