from __future__ import print_function
import httplib2, os, pip, sys, io
from mimetypes import MimeTypes
try:
    from googleapiclient.errors import HttpError
    from apiclient import discovery
    import oauth2client
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
    from oauth2client import client
    from oauth2client import tools
    from apiclient import errors
except ImportError:
    print('goole-api-python-client is not installed. Try:')
    print('sudo pip install --upgrade google-api-python-client')
    sys.exit(1)
import sys

class Flag:
    auth_host_name = 'localhost'
    noauth_local_webserver = False
    auth_host_port = [8080, 8090]
    logging_level = 'ERROR'

# link = https://drive.google.com/open?id=1P92V7F5ibpK3spMkHxeJWhyyYWDjrugV
try:
    import argparse

    # flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    flags = Flag()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'GDrive'
FOLDER_TYPE = 'application/vnd.google-apps.folder'

def get_credentials():

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        # if flags:
        credentials = tools.run_flow(flow, store, flags)
        # else:  # Needed only for compatibility with Python 2.6
        #     credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def listfiles():
    print (ROOT_FOLDER_ID)
    results = service.files().list(fields="nextPageToken, files(id, name,mimeType)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        print('Filename (File ID)')
        for item in items:
            if item['id'] == ROOT_FOLDER_ID:
                print (item['name'].encode('utf-8'))
                print('{0} ({1}), ({2})'.format(item['name'].encode('utf-8'), item['id'], item['mimeType']))
        print('Total=', len(items))


def getlist(ds, q, **kwargs):
  import pdb; pdb.set_trace()
  result = None
  npt = ''
  while not npt is None:
    if npt != '': kwargs['pageToken'] = npt
    entries = ds.files().list(q=q, **kwargs).execute()
    if result is None: result = entries
    else: result['items'] += entries['items']
    npt = entries.get('nextPageToken')
  return result

def walk_to_directory(ds, folderId, folderName, outf, depth):
  spc = ' ' * depth
  outf.write('%s+%s\n%s  %s\n' % (spc, uenc(folderId), spc, uenc(folderName)))
  q = "'%s' in parents and mimeType='%s'" % (folderId, FOLDER_TYPE)
  entries = getlist(ds, q)
  if 'items' in entries:
      for folder in entries['items']:
        walk_to_directory(ds, folder['id'], folder['title'], outf, depth + 1)
      q = "'%s' in parents and mimeType!='%s'" % (folderId, FOLDER_TYPE)
      entries = getlist(ds, q)
      for f in entries['items']:
        outf.write('%s -%s\n%s   %s\n' % (spc, uenc(f['id']), spc, uenc(f['title'])))

def uenc(u):
  if isinstance(u, unicode): return u.encode('utf-8')
  else: return u

if __name__ == '__main__':
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    method = sys.argv[1]
    ROOT_FOLDER_ID =  sys.argv[2].split('?id=')[1]
    basedir = os.path.dirname(__file__)
    if method == 'list':
        f = open(os.path.join(basedir, 'hierarchy.txt'), 'wb')
        walk_to_directory(service, ROOT_FOLDER_ID, ROOT_FOLDER_ID , f, 0)
        f.close()
        # listfiles()
