from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from get_attachments import get_attachments
import json

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API
    response = service.users().messages().list(userId='me', q="has:attachment", maxResults=500).execute()
    messages = response['messages']
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

    print(f"{len(messages_with_attachments)} with attachments were downloaded.")

    response = service.users().messages().batchDelete(userId='me', body=json.dumps(messages_with_attachments)).execute()
    response


if __name__ == '__main__':
    main()
