import os
from dotenv import load_dotenv
from agentmail import AgentMail
from google import genai

#Load the API key from the .env file
api_key = "am_d1a18b8ad422d846a470d17728d76b2904238d7481e57b8250777d8abb9a83d3" #os.getenv("AGENTMAIL_API_KEY")

# Initialize the client
inbox = AgentMail(api_key=api_key)


# Create an inbox
# print("Creating inbox...")
# inbox = client.inboxes.create(
#     username="weekly_climate_change_email", 
#     domain="agentmail.to"
# )
# print("Inbox created successfully!")
# print(inbox)

# get ai_newsletter text from geminifrom google import genai
client = genai.Client(api_key="AIzaSyAilyy9UzUHJ93xHUl2GXpnD3c_Ozmoh8w") # The client gets the API key from the environment variable `GEMINI_API_KEY`.
response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Create the body for a news letter email about major events in climate change globally in the past week. \
    Some potential topics include: political policies, natural disasters, research studies, severe weather, general climate change data and statistics, and more."
)
ai_newsletter = response.text

# Sending Message
file = open('./mail/mail_list.txt','r')

for email in file:
    sent_message = inbox.inboxes.messages.send(
        inbox_id = 'weekly_climate_change_email@agentmail.to',
        to = email,
        labels=[
            "Weekly Email",
            "Climate Change Awareness"
        ],
        subject="Climate Change Awareness Weekly Email",
        text=ai_newsletter)

print(f"Message sent successfully with ID: {sent_message.message_id}")

