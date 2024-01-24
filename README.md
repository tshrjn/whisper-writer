# whisper-write

Video demo: https://www.youtube.com/watch?v=VnFtVR72jM4&feature=youtu.be

Simulate keyboard typing with voice commands on your computer. Use the power of OpenAI's Whisper.

Start the `wkey` listener. Keep a button pressed (by default: right `ctrl_l`) and speak. Your voice will be recoded locally. When the button is released, your command will be transcribed via Whisper and the text will be streamed to your keyboard.

You can use your voice to write anywhere. 

You will incur costs for Whisper API. Currently, it costs $0.36 for 1 hour of transcription.

## Setup

Install the package.

```shell
pip install -e .
```

You will need to set a few environment variables:

- WKEY: the keyboard key you want to use to start recording. By default, it is set to right ctrl. You can use any key. Note that Mac and Windows might have different key codes. You can run `fkey` to find the code of the key you want to use.

If you plan on using OPENAI's Whisper API instead of local model, you will also need to set:
- OPENAI_API_KEY: your personal OpenAI API key. You can get it by signing up here: https://platform.openai.com/


You can set the environment variables in your shell:

```shell
export OPENAI_API_KEY=<your key>
export WKEY=ctrl_l
```
## Usage

Run `wkey` in a terminal window to start listening. 
If you prefer to use the Whisper API instead of the local model, run `wkey --api` instead.

Run `fkey` to find the code of the key you want to use.

If there are issues, check the additional requirements.

## Planned features
CoreML build version of whisperCPP, [ref](https://github.com/SYSTRAN/faster-whisper/discussions/368)
- Build model guide [ref](https://github.com/ggerganov/whisper.cpp?tab=readme-ov-file#core-ml-support)
- WhisperCPP Direct API Binding to use such model [ref](https://github.com/aarnphm/whispercpp?tab=readme-ov-file#api)
  - Since WhisperCPP doesn't yet support directly loading CoreML build models.

## Additional requirements

Requirements differ depending on your OS.

### Ubuntu

You will need to install the portaudio library. 

```shell
sudo apt-get install portaudio19-dev 
```

### Mac
You will need to authorize your terminal to use the microphone and keyboard. Go to System Settings > Privacy and Security. Then: 
* Select Microphone and authorize your terminal.
* Select Accessibility and authorize your terminal.

Restart the terminal for the changes to take effect. 

Note that this might entail security risks.

### Windows
Haven't tested it on Windows yet. If you do, please let me know how it goes.

## Security risks

This script creates a recording with your microphone and sends the audio to the Whisper API. The Whisper API response will be automatically streamed to your keyboard and executed there. This might entail security risks. Use at your own risk. 