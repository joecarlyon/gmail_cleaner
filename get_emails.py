from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from get_attachments import get_attachments
import json

# Requires access to delete accounts. If you don't want that, instead use:
# https://www.googleapis.com/auth/gmail.readonly
SCOPES = 'https://mail.google.com/'


def download_attachments_from_messages(service, messages):
    messages_with_attachments = list()
    if not messages:
        print('No messages to handle.')
    else:
        print('Messages:')
        for message in messages:
            print(message['id'])
            msg_id = get_attachments(service, 'me', message['id'], "/Users/joecarlyon/Desktop/gmail_attachments/")
            if msg_id:
                messages_with_attachments.append(msg_id)

    return messages_with_attachments


def main():
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Find messages with attachments and download them
    response = service.users().messages().list(userId='me', q="has:attachment", maxResults=500).execute()
    messages = response['messages']
    messages_with_attachments = download_attachments_from_messages(service, messages)

    # Delete the messages
    print(f"{len(messages_with_attachments)} with attachments were downloaded.")
    service.users().messages().batchDelete(userId='me', body=json.dumps(messages_with_attachments)).execute()


if __name__ == '__main__':
    main()
