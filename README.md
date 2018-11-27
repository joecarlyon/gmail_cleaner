# Gmail Cleaner

My inbox is nearly full, and I have never cleaned it since my first beta invite.

I'm almost at max storage, and I suspect the reason is because my Grandpa emails me attachments of pictures instead of a link to an album.

The purpose of this script is to go through emails and detect if there are any attachments and to download them. It's certainly not fancy.

Ideally the emails should be deleted to clean up the space, but I'm running into an authorization issue at the moment.

# Requirements

* Python 3.6+

`pip3 install --upgrade google-api-python-client oauth2client`

Enable the Gmail Api through here: https://developers.google.com/gmail/api/quickstart/python

Download `credentials.json` and put them in the root of gmail_cleaner.

# Running

`python3 get_emails.py /path/to/save/directory`
