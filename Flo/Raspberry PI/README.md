> :warning: **This project is still under testing**: The installation instructions are yet to be verified on a fresh install. Please proceed with caution.

# Raspberry Pi Voice Assistant + ChatGPT

## Hardware Requirements

This project requires the following hardware:

- **Raspberry Pi 4B**: Currently, the project is designed to work with the Raspberry Pi 4B. Support for the Raspberry Pi 5 is in progress, but it's not officially supported by Picovoice yet. A workaround exists for all Picovoice libraries except PVRecorder. It's possible to use PyAudio as an alternative to PVRecorder, but this hasn't been tested yet. Note that the speech-to-text transcription may run a bit slow on the 4B, but it's expected to improve significantly on the 5 due to better disk and CPU performance.

- **USB Microphone**: A USB microphone is required for voice input. The one used in this project is available on [Amazon](https://www.amazon.com/gp/product/B075M7FHM1/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&th=1).  The microphone you use will likely depend on your droid.  I found I needed to keep the cover on mine to prevents false wakes, but that also limits the voice range some.  

- **USB Speaker**: A USB speaker is required for voice output. The one used in this project is available on [Amazon](https://www.amazon.com/gp/product/B08M37224H/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1).  This will be defined by the amount of speaker space you have.  This was one of the smallest I could find and it works fine.  It's not super loud and does not have volume controls on it.  I set the volume in the operating system (literally running it with keyboard, mouse, and monitor plugged in).


## Software Requirements
