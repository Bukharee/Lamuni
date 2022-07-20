from email import message
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
    

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.v2.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])


def send(phone):
    verify.verifications.create(to=phone, channel='sms')

def check(phone, code):
    # try:
    result = verify.verification_checks.create(to=f'{phone}', code=f'{code}')
    print(result.status)
    # except TwilioRestException:
        # print(TwilioRestException)
        # print('no')
        # return False
    return result.status == 'approved'

def sms_reset(phone, code):
         message = client.messages.create(
                                        body=f'Hi, here is your reset password code {code}.\
                                        Don\'nt share this code with anyone; our employees will \
                                            never ask for it.',
                                        from_='+2349155425705',
                                        to=f'{phone}'
                                    )
         return message
