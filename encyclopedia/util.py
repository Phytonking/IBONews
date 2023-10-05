import re
from smtplib import SMTPAuthenticationError
from encyclopedia.models import *
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import datetime 
from django.core.mail import send_mail
from dotenv import dotenv_values

env = dotenv_values("encyclopedia/.env")

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def hasDarkMode(user):
    try:
        lk = Settings.objects.get(for_user=user)
        if lk.DarkMode == True:
            return True
        else:
            return False
    except TypeError:
        return False
    

def create_newsletter_email(subject, recipient, articles):
    # Create the HTML email body
    email_body = f"""<html>
    <head></head>
    <body>
        <p>Dear {recipient},</p>
        <p>We hope you're doing well! Here is the {subject}:</p>
    """

    # Iterate through the list of articles and add a section for each article
    for article in articles:
        email_body += f"""<div class="article">
            <h2>{article.title}</h2>
            <p>{article.description}</p>
            <p>Author: {article.author.name}</p>
        </div>
        """

    email_body += """<p>Best regards,<br>IBONews</p>
    </body>
    </html>
    """

    # Create the email subject and recipient email address (replace with actual values)
    recipient_email = recipient.email
    email_subject = subject

    # Here, you would typically use smtplib to send the email. This is a simplified example.
    print("Email Subject:", email_subject)
    print("Recipient:", recipient_email)
    print("Email Body (HTML):\n", email_body)
    try:
        send_mail(subject=subject, message=email_body, from_email=env["email"], recipient_list=[recipient_email], html_message=email_body)
    except SMTPAuthenticationError:
        print("Error: Authentication failed")
        return -1





