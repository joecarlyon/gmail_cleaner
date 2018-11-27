"""Retrieve an attachment from a Message in Gmail.
"""

import base64
from apiclient import errors


def get_data_from_part(service, user_id, msg_id, part):
    if 'data' in part['body']:
        return part['body']['data']
    else:
        att_id = part['body']['attachmentId']
        att = service.users().messages().attachments().get(userId=user_id, messageId=msg_id, id=att_id).execute()
        return att['data']


def write_file_to_location(data, path):
    with open(path, 'wb') as f:
        f.write(data)
    print("Attachment downloaded.")


def sanitize_string(dirty_string):
    clean_string = dirty_string.replace(':', '').replace('/', '').replace(' ', '_').replace('.', '+')
    return clean_string


def get_attachments(service, user_id, msg_id, save_path):
    """Get and store attachment from Message with given id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
    save_path: The directory used to store attachments.
  """
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        if 'parts' not in message['payload']:
            if message['payload']['body']['size'] > 0:
                print("Downloading single-part attachment...")
                file_data = base64.urlsafe_b64decode(message['payload']['body']['data'].encode('UTF-8'))
                path = ''.join([save_path, sanitize_string(message['snippet'][0:70])])
                write_file_to_location(file_data, path)
        elif 'parts' in message['payload']:
            for part in message['payload']['parts']:
                print("Downloading multi-part attachment...")
                if part['filename']:
                    data = get_data_from_part(service, user_id, msg_id, part)
                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    path = ''.join([save_path, part['filename']])
                    write_file_to_location(file_data, path)
        # Nothing to download
        else:
            return None

    except errors.HttpError as error:
        print(f"An error occurred: {error}")

    return msg_id
