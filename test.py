from dotenv import load_dotenv
import os
load_dotenv(".env")
import sendlk

SENDLK_TOKEN = os.environ.get("SENDLK_TOKEN")
SECRET = os.environ.get("SECRET")
SENDER_ID = os.environ.get("SENDER_ID")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER")

sendlk.initialize(SENDLK_TOKEN, SECRET)

from sendlk.responses import SmsResponse, ProfileResponse
from sendlk.exceptions import SendLKException
from sendlk.engine import SMS, Profile
from sendlk.options import SendLKVerifyOption, SendLKCodeTemplate

try:
    response: SmsResponse = SMS.send(PHONE_NUMBER, "Hello World!", SENDER_ID)
    print(response)
except SendLKException as e:
    print(e)

try:
    response: ProfileResponse = Profile.balance()
    print(response.remaining)
except SendLKException as e:
    print(e)

class CustomCodeTemplate(SendLKCodeTemplate):
    def __init__(self):
        super().__init__()
        
    def text(self, code: str) -> str:
        return f"{code} is the verification code for foo service."
    
options: SendLKVerifyOption = SendLKVerifyOption(
    code_length=6,
    expires_in=5,
    sender_id=SENDER_ID,
    subject="foo",
    code_template=CustomCodeTemplate()
)

try:
    response: SmsResponse = SMS.send_verify_code(PHONE_NUMBER, options)
    token = response.data.get("token", None)
    code = input("Enter the code: ")
    response: SmsResponse = SMS.validate_verify_code(code, token)
    print(response)
    print(response.data)
except SendLKException as e:
    print(e)