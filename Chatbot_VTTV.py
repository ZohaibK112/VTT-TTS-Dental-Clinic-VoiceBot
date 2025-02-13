from urllib import response
import assemblyai as aai
import google.generativeai as genai
from elevenlabs import play
from elevenlabs.client import ElevenLabs


class AI_assistant:
    def __init__(self):
        aai.settings.api_key='assemblyai_KEY'
        self.google_api_key = "Gemini_API"
        genai.configure(api_key=self.google_api_key)
        self.elevenlabs_api_key = "elevenlabs_key"

        self.transcriber = None

        #prompt

        self.full_transcript = [
            {"role":"system", "content":"You are a receptionist at a dental clinic. Be resourceful and efficient."}
        ]

        #Real Time Transcription with assemblyAI

    def start_transcription(self):
        self.transcriber = aai.RealtimeTranscriber(
                sample_rate = 16000,
                on_data = self.on_data,
                on_error=self.on_error,
                on_open=self.on_open,
                on_close=self.on_close,
                end_utterance_silence_threshold=1000

            )

        self.transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
        self.transcriber.stream(microphone_stream)

    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None


    def on_open(self,session_opened: aai.RealtimeSessionOpened):
       #print("Session ID:", session_opened.session_id)
       return

    def on_data(self, transcript: aai.RealtimeTranscript):
     if not transcript.text:
        print("No text transcribed yet...")
        return

     print(f"Transcribed Text: {transcript.text}")

     if isinstance(transcript, aai.RealtimeFinalTranscript):
        self.generate_ai_response(transcript.text)




    def on_error(self, error: aai.RealtimeError):
     print(f"An error occurred: {error}")




    def on_close(self):
     #print("Closing Session")
     return

# Real_time trascript to Gemini 

    def generate_ai_response(self, transcript):
        self.stop_transcription()
        self.full_transcript.append({"role":"user:", "content":transcript.text})
        print(f"\nPatient: {transcript.text}", end="\r\n")
    
        response = genai.chat(
        model="gemini-1.5-pro",
        messages=self.full_transcript,
)

    
        ai_response = response.choices[0].message.content

        self.generate_audio(ai_response)
    
        self.start_transcription()
      
    #Generate Audio with Elevanlabs
    def generate_audio(self, text):
       self.full_transcript.append({"role":"assistant", "content":text})
       print(f"\nAI Receptionist:{text}")
      
       client = ElevenLabs(api_key=self.elevenlabs_api_key)
    
       audio = client.generate(
          text = text,
          voice="Brian",
          model="eleven_multilingual_v2"

       )
       play(audio)
    


if __name__ == "__main__":
    greeting = "Thank you for calling Vancouver Dental Clinic. My name is Sandy. How may I assist you?"
    ai_assistant = AI_assistant()
    ai_assistant.generate_audio(greeting)
    ai_assistant.start_transcription()


    



    

       


