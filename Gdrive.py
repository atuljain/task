##############################################################################################################
############################################ Import packages #################################################
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
###############################################################################################################
# Set flag for host and port
class Flag:
    auth_host_name = 'localhost'
    noauth_local_webserver = False
    auth_host_port = [8080, 8090]
    logging_level = 'ERROR'

# demo drive root folder link https://drive.google.com/open?id=1P92V7F5ibpK3spMkHxeJWhyyYWDjrugV
try:
    import argparse
    flags = Flag()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'GDrive'
FOLDER_TYPE = 'application/vnd.google-apps.folder'

################################################################################################################
#
# Function for getting credentials 
#
################################################################################################################
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
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

################################################################################################################
#
# Function for getting list of all files
# NOTE: This is Test Function  
#
################################################################################################################

def list_files():
    results = service.files().list(fields="nextPageToken, files(id, name,mimeType)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        print('Filename (File ID)')
        for item in items:
            if item['id'] == ROOT_FOLDER_ID:
                print_files_in_folder(service, ROOT_FOLDER_ID)
                print('{0} ({1}), ({2})'.format(item['name'].encode('utf-8'), item['id'], item['mimeType']))
        print('Total=', len(items))

################################################################################################################
#
# Function for getting list of all files
#
################################################################################################################


def getlist(ds, q, **kwargs):
  result = None
  npt = ''
  while not npt is None:
    if npt != '': kwargs['pageToken'] = npt
    entries = ds.files().list(q=q, **kwargs).execute()
    if result is None: result = entries
    else: result['items'] += entries['items']
    npt = entries.get('nextPageToken')
  return result

################################################################################################################
#
# Recursive Function for getting into folder's Folder
#
################################################################################################################


def walk_to_directory(ds, folderId, folderName, outf, depth):
  spc = ' ' * depth
  outf.write('%s+%s\n%s  %s\n' % (spc, uenc(folderId), spc, uenc(folderName)))
  json_drive['name'] = uenc(folderName)
  json_drive['id'] = uenc(folderId)
  json_drive['children'] = []
  q = "'%s' in parents and mimeType='%s'" % (folderId, FOLDER_TYPE)
  entries = getlist(ds, q)
  if 'items' in entries:
      for folder in entries['items']:
        walk_to_directory(ds, folder['id'], folder['title'], outf, depth + 1)
      q = "'%s' in parents and mimeType!='%s'" % (folderId, FOLDER_TYPE)
      entries = getlist(ds, q)
      for f in entries['items']:
        json_drive['name'] = uenc(f['title'])
        json_drive['id'] = uenc(f['id'])
        json_drive['children'] = []
        outf.write('%s -%s\n%s   %s\n' % (spc, uenc(f['id']), spc, uenc(f['title'])))


################################################################################################################
#
# Unicode 
#
################################################################################################################


def uenc(u):
  if isinstance(u, unicode): return u.encode('utf-8')
  else: return u

################################################################################################################
#
# Test Function For getting list of child into Folders 
#
################################################################################################################

def print_files_in_folder(service, folder_id):
  """Print files belonging to a folder.

  Args:
    service: Drive API service instance.
    folder_id: ID of the folder to print files from.
  """
  page_token = None
  while True:
    try:
      param = {}
      if page_token:
        param['pageToken'] = page_token
      children = service.children().list(
          folderId=folder_id, **param).execute()

      for child in children.get('items', []):
        print ('File Id: %s' % child['id'])
      page_token = children.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print ('An error occurred: %s' % error)
      break
################################################################################################################
#
# Make JSON 
#
################################################################################################################
def drive_json():
    data = {
	'name':'<folder_name>',
	'type': '<type_of_items>'	
	}
    if type == 'folder':
	data['children'] = []
	for i in len('folder'):
	   data = {
		'name':'<folder_name>',
		'type': '<type_of_items>'	
		}   
if __name__ == '__main__':
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)
    method = sys.argv[1]
    ROOT_FOLDER_ID =  sys.argv[2].split('?id=')[1]
    json_drive = {}
    basedir = os.path.dirname(__file__)
    if method == 'list':
        # f = open(os.path.join(basedir, 'hierarchy.txt'), 'wb')
        # walk_to_directory(service, ROOT_FOLDER_ID, 'root' , f, 0)
        # f.close()
        list_files()
