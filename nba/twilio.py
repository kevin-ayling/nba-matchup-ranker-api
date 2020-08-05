from twilio.rest import Client
import logging



client = Client(account_sid, auth_token)


def send_sms(message):
    for number in numbers:
        message = client.messages \
            .create(
            messaging_service_sid=message_service_id,
            body=message,
            to=number
        )
        logging.info('successful message sent: {}'.format(message.sid))


def send_alert(message):
    message = client.messages \
        .create(
        messaging_service_sid=message_service_id,
        body=message,
        to=alert_num
    )
    logging.info('successful alert sent: {}'.format(message.sid))
