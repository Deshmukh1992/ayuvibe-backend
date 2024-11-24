

api_key = "AIzaSyDMExFclpvIclDr_mE3oMh_NcHN0s1Vu34"

import google.generativeai as genai

genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

chat = model.start_chat()

while True:
    message = input("You: ")
    if message.lower() == "bye":
        print("Chatbot: Goodbye!")
    res = chat.send_message(message)
    print("Chatbot:", res.text)




# response = model.generate_content("What is a good Ayurvedic treatment for cold?")
# print(response.text)
