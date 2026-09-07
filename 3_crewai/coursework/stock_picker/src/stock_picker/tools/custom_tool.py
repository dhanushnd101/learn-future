from crewai.tools import tool
import os
import requests


# @tool("Send Push Notification")
# def send_push_notification(message: str) -> str:
#     """
#     Use this tool to send a push notification to the user.
#     Args:
#         message: The message to be sent as a push notification to the user.
#     Returns:
#         A string indicating the status of the push notification.
#     """
#     pushover_user = os.getenv("PUSHOVER_USER")
#     pushover_token = os.getenv("PUSHOVER_TOKEN")
#     pushover_url = "https://api.pushover.net/1/messages.json"
#     payload = {"user": pushover_user, "token": pushover_token, "message": message}
#     result = requests.post(pushover_url, data=payload).status_code
#     return f"Push notification sent with API response code: {result}"

from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage
load_dotenv(override=True)


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

@tool("Send Push Notification")
def send_push_notification(message: str) -> str:
    """
    Send a notification to the user about the chosen stock.
    Args:
        message: The notification text to send.
    Returns:
        A string indicating whether the notification was sent.
    """
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = "Stock Picker Notification"
    msg.set_content(message)

    with smtplib.SMTP(EMAIL_SMTP_SERVER, 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(msg)
    
    return "Notification sent successfully"