import time
import logging 
from whatsapp_chatgpt_python import WhatsappGptBot, 
TextMessageHandler
# from whatsapp_chatgpt_python import 
# ImageMessageHandler # optional if using images 
# ====== Logging ======
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = 
logging.getLogger("whatsapp_chatgpt_python")
# ====== API KEYS / CONFIG ======
ID_INSTANCE = "your-instance-id" # Green API 
Instance ID API_TOKEN = "your-api-token" # Green 
API Token OPENAI_API_KEY = "your-openai-api-key" # 
OpenAI API Key
# ====== Initialize bot ======
bot = WhatsappGptBot( id_instance=ID_INSTANCE, 
    api_token_instance=API_TOKEN, 
    openai_api_key=OPENAI_API_KEY, model="gpt-4o", 
    system_message="You are a helpful assistant. Be concise and friendly in your replies. Always respond clearly.", max_history_length=15, 
    temperature=0.7, session_timeout=1800, 
    error_message="Sorry, your message could not be processed."
)
# ====== Enhanced Text Handler ======
class EnhancedTextHandler(TextMessageHandler): 
    async def process_message(self, notification, 
    *args, **kwargs):
        text = await 
        super().process_message(notification, 
        *args, **kwargs) if not text:
            return text lower_text = text.lower() 
        if any(term in lower_text for term in 
        ['code', 'function', 'script', 'program']):
            return f"🧑‍💻 CODE REQUEST: 
            {text}\n\n[Formatted code response]"
        elif text.endswith('?') or 
        text.lower().startswith(
                ('what', 'why', 'how', 'when', 
                'where', 'who', 'can', 'could')):
            return f"❓ QUESTION: {text}\n\n[Clear 
            and comprehensive answer]"
        return text 
bot.replace_handler(TextMessageHandler, 
EnhancedTextHandler())
# ====== Middleware for logging ======
def logging_middleware(notification, 
message_content, messages, session_data):
    user_id = notification.sender if 
    isinstance(message_content, str) and 
    len(message_content) > 100:
        content_display = message_content[:100] + 
        "..."
    else: content_display = message_content 
    logger.info(f"Message from {user_id}: 
    {content_display}") if "variables" not in 
    session_data.context:
        session_data.context["variables"] = {} 
    session_data.context["variables"].update({
        "last_interaction": int(time.time()), 
        "message_count": 
        session_data.context.get("variables", 
        {}).get("message_count", 0) + 1
    })
    return {"message_content": message_content, 
    "messages": messages}
bot.add_message_middleware(logging_middleware)
# ====== Middleware for formatting responses ======
def formatting_middleware(response, messages, 
session_data):
    formatted_response = response.strip() if 
    len(formatted_response) > 100 and not 
    formatted_response.endswith("_"):
        message_count = 
        session_data.context.get("variables", 
        {}).get("message_count", 0) 
        formatted_response += f"\n\n_Message 
        #{message_count} • Powered by GPT_"
    return {"response": formatted_response, 
    "messages": messages}
bot.add_response_middleware(formatting_middleware)
# ====== Commands ======
@bot.router.message(command="clear") def 
clear_history_handler(notification):
    chat_id = notification.chat session_data = 
    bot.get_session_data(chat_id) system_message = 
    next((msg for msg in session_data.messages if 
    msg.get("role") == "system"), None) 
    session_data.messages = [system_message] if 
    system_message else [] 
    bot.update_session_data(chat_id, session_data) 
    notification.answer("🗑️ Conversation history 
    cleared! Let's start fresh.")
@bot.router.message(command="help") def 
help_handler(notification):
    notification.answer( "🤖 *WhatsApp GPT Bot* 
        🤖\n\n" "Available commands:\n" "• */help* 
        - Show this help message\n" "• */clear* - 
        Clear conversation history\n" "• */info* - 
        Show bot information\n" "• */weather* - 
        Example handler that skips GPT\n\n" "Send 
        text, images, audio, and more. I'll respond 
        intelligently."
    ) @bot.router.message(command="info") def 
info_handler(notification):
    chat_id = notification.chat session_data = 
    bot.get_session_data(chat_id) message_count = 
    max(len(session_data.messages) - 1, 0) 
    vision_capable = "Yes" if bot.supports_images() 
    else "No" info_text = (
        "📊 *Bot Information* 📊\n\n" f"Model: 
        {bot.get_model()}\n" f"Vision capable: 
        {vision_capable}\n" f"Messages in current 
        session: {message_count}\n" f"Max history 
        length: {bot.max_history_length}\n" 
        f"Session timeout: {bot.session_timeout} 
        seconds\n\n" "To clear the conversation, 
        use */clear*"
    ) notification.answer(info_text) 
@bot.router.message(command="weather") def 
weather_handler(notification):
    notification.answer( "🌤️ This is a placeholder 
        weather response from a custom handler.\n" 
        "In a real bot, this would fetch actual 
        weather data from an API."
    )
