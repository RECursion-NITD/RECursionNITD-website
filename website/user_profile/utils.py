import threading
import six
from difflib import SequenceMatcher
from typing import List, Tuple, Union
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from rest_framework import serializers


class ProfileMatcher:
    """
    A ProfileMatcher object contains the query and ratio_threshold
    """

    def __init__(self, query: str, ratio_threshold=0.36):
        """
        :param query: The keyword to be searched (str)
        :param ratio_threshold: The threshold ratio (float)
        :type query: str
        :type ratio_threshold: float
        """
        self.query = str(query).lower()
        self.ratio_threshold = ratio_threshold

    def matcher(self, obj):
        score = max(
            SequenceMatcher(None, obj.name.lower(), self.query).ratio(),
            -1
        )
        if score >= self.ratio_threshold:
            return score
        return 0

    def __str__(self):
        return 'ProfileMatcher object with query="{}", ratio_threshold={} .'.format(self.query, self.ratio_threshold)


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


class LowerEmailField(serializers.EmailField):
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        if isinstance(data, bool) or not isinstance(data, (str, int, float,)):
            self.fail('invalid')
        value = str(data).lower()
        return value.strip() if self.trim_whitespace else value


class ThreadedMailing(threading.Thread):
    def __init__(self, emails: List[EmailMessage], fail_silently: bool = True, verbose: int = 0):
        self.email_msgs = emails
        self.fail_silently = fail_silently
        self.verbose = verbose
        threading.Thread.__init__(self)

    def run(self):
        if self.verbose > 0:
            print('Sending {} emails.'.format(len(self.email_msgs)))
        for email_number, email in enumerate(self.email_msgs, start=1):
            if self.verbose > 1:
                print('Sending email number:', email_number)
                print(email)
            email.send(fail_silently=self.fail_silently)


# needs change, UNFIT FOR USE
def send_verification_mail(domain, user, *args, **kwargs):
    if domain is None or user is None:
        raise ValidationError('Domain/User instance not provided')
    mail_subject = 'Activate your RECursion website account.'
    message = render_to_string('account_activation_email.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
    })
    to_email = settings.TRIAL_REC_MAIL
    mail = EmailMessage(
        mail_subject,
        message,
        to=[to_email, ]
    )

    # UNCOMMENT BELOW LINES TO SEND EMAIL
    threaded_mail = ThreadedMailing([mail, ])
    threaded_mail.start()

    return message
