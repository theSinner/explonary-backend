from django.conf import settings
from django.template.loader import render_to_string

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib

from celery.task import task

import hashlib

import requests

import os


def contains_non_ascii_characters(str):
    return not all(ord(c) < 128 for c in str)


@task(name='send_sms')
def send_sms(phone_number, code, template, locale_prefix=""):
    print("phone_number:", phone_number)
    print("code:", code)
    print("template:", template)
    message = settings.SMS_TEMPLATE[locale_prefix + template].format(code=code)
    print("sms template is: ", settings.SMS_TEMPLATE[
        locale_prefix + template].format(code=code))
    SMS_HOST = settings.SMS_HOST
    SMS_URL_FOR_HASH = settings.SMS_URL_FOR_HASH
    SMS_URL_FOR_SENDING = settings.SMS_URL_FOR_SENDING
    to_hash = SMS_URL_FOR_HASH.format(
        message=message, mobile=phone_number
    ).encode('utf-8')
    hashed_part = hashlib.sha1(to_hash)
    url = SMS_URL_FOR_SENDING.format(
        host=SMS_HOST,
        mobile=phone_number,
        message=message,
        hash=hashed_part.hexdigest()
    )
    requests.get(url)


@task(name='send_email')
def send_email(email, code, template, locale_prefix):
    message = render_to_string(
        "user/{}.html".format(locale_prefix + template),
        {
            "header": settings.EMAIL_TEMPLATE[
                locale_prefix + template]["header"],
            "content": settings.EMAIL_TEMPLATE[
                locale_prefix + template]["content"],
            "code": code,
            "icon": settings.EMAIL_TEMPLATE[locale_prefix + template]["icon"],
            "logo_url": os.environ["BASE_URL"] + "/public/icons/logo2.png",
            "facebook_link_url": os.environ[
                "BASE_URL"] + "/public/icons/facebook.png",
            "instagram_link_url": os.environ[
                "BASE_URL"] + "/public/icons/instagram.png",
            "twitter_link_url": os.environ[
                "BASE_URL"] + "/public/icons/twitter.png",
            "linkedin_link_url": os.environ[
                "BASE_URL"] + "/public/icons/linkedin.png",
            "aparat_link_url": os.environ[
                "BASE_URL"] + "/public/icons/aparat.png",

        }
    )
    msg = MIMEMultipart()
    msg['From'] = "info@sabavision.com"
    msg['To'] = email
    msg['Subject'] = "Email Verification"

    msg.attach(MIMEText(message, 'html'))

    server = smtplib.SMTP('mailer1.saba-e.com')

    a = server.sendmail(msg['From'], msg['To'], msg.as_string())
    print("RESPONSE IS: ", a)
    print(type(a))

    server.quit()
    return "sending email process reached to end"
