from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError, mail_managers

class ContactForm(forms.Form):
    FEEDBACK = 'F'
    CORRECTION = 'C'
    SUPPORT = 'S'
    REASON_CHOICES = (
        (FEEDBACK, 'Feedback'),
        (CORRECTION, 'Correction'),
        (SUPPORT, 'Support')
    )
    email = forms.EmailField(initial='Your Email Address')
    text = forms.CharField(widget=forms.Textarea)
    reason = forms.ChoiceField(
        choices = REASON_CHOICES,
        initial = FEEDBACK
    )

    def send_email(self):
        reason = self.cleaned_data.get('reason')
        reason_dict = dict(self.REASON_CHOICES)
        full_reason = reason_dict.get(reason)
        email = self.cleaned_data.get('email')
        text = self.cleaned_data.get('text')
        body = 'Message From: {}\n\n{}\n'.format(email, text)

        try:
            #shortcut for send_mail
            mail_managers(full_reason, body)
        except BadHeaderError:
            self.add_error(
                None,
                ValidationError(
                    'Could not Send Email.\n'
                    'Extra Headers not allowed '
                    'in email body. ',
                    code = 'badheader'
                )
            )
            return False
        else:
            return True