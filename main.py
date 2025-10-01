from whatsapp_chatgpt_python import WhatsappGptBot
import os

bot = WhatsappGptBot(
    id_instance=os.environ["INSTANCE_ID"],
    api_token_instance=os.environ["INSTANCE_TOKEN"],
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model="gpt-4o",
    system_message="You are a helpful assistant."
)

if __name__ == "__main__"
