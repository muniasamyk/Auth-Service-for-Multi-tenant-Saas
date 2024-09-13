from django.core.mail import send_mail

def send_invite_email(to_email, invite_link):
    send_mail(
        'You\'ve been invited!',
        f'Click here to join: {invite_link}',
        'your-email@example.com',
        [to_email]
    )

def send_password_update_alert(to_email):
    send_mail(
        'Password Updated',
        'Your password has been successfully updated.',
        'your-email@example.com',
        [to_email]
    )

def send_login_alert(to_email):
    send_mail(
        'Login Alert',
        'You have successfully logged in.',
        'your-email@example.com',
        [to_email]
    )
