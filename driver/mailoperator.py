import imaplib
import email
from email.header import decode_header
from newsdriver.secrets import MAIL_SERVER, MAIL_LOGIN, \
    MAIL_PASSWORD, NEWS_MAIL


def imap_get_inbox_connection():
    imap = imaplib.IMAP4_SSL(MAIL_SERVER)
    imap.login(MAIL_LOGIN, MAIL_PASSWORD)
    imap.select('INBOX')
    return imap


def get_str_from_header(msg, header_name):
    parts = []
    for bts, encoding in decode_header(msg[header_name]):
        if not encoding:
            part = bts.decode()
        else:
            part = bts.decode(encoding)
        parts.append(part)
    return ' '.join(parts)


def get_new_novospas_mails(imap):
    result, data = imap.search(None, f'(FROM "{NEWS_MAIL}" UNSEEN)' )
    new_mails_headers = []
    if not data[0]:
        return []
    for mail_id in data[0].split(b' ')[::-1]:
        typ, header = imap.fetch(mail_id, '(BODY.PEEK[HEADER])')
        msg = email.message_from_bytes(header[0][1])
        mail_date = msg['Date']
        mail_from = get_str_from_header(msg, 'From')
        mail_subject = get_str_from_header(msg, 'Subject')
        new_mails_headers.append((int(mail_id), mail_date, mail_from, mail_subject))
    return new_mails_headers


def get_new_mails():
    imap = imap_get_inbox_connection()
    new_mails = get_new_novospas_mails(imap)
    imap.logout()
    return new_mails
