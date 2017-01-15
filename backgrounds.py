import json, requests, os, sys, math

# SETTINGS ======
# application ID - get from http://unsplash.com/api
APPLICATION_ID = 'ENTER APPLICATION_ID HERE'

# up to a maximum of 30 - per run
DOWNLOAD_COUNT = 30

# landscape, portrait, or squarish
PHOTO_ORIENTATION = 'landscape'

# relative to the directory the script is in
DOWNLOAD_LOCATION = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        'backgrounds'
    )
)
# ===============

# SETUP
if not os.path.exists(DOWNLOAD_LOCATION):
    os.makedirs(DOWNLOAD_LOCATION)

BATCHES = int(math.ceil(DOWNLOAD_COUNT / 30.0))

# DOWNLOAD
def get_backgrounds():
    for i in range(0, BATCHES):
        download_count = DOWNLOAD_COUNT - (i * 30)

        print("-> batch %d of %d (%d photo(s))" % ((i + 1), BATCHES, download_count))

        photos_json = requests.get('https://api.unsplash.com/photos/random', params={
            'client_id': APPLICATION_ID,
            'orientation': PHOTO_ORIENTATION,
            'count': download_count
        })

        for index, photo in enumerate(photos_json.json()):
            photo_id = photo['id']
            photo_url = photo['urls']['raw']

            print(" > downloading %s (%d of %d)" % (photo_id, (index + 1), DOWNLOAD_COUNT))
            photo_raw = download_with_progress(photo_url)
            destination_url = os.path.join(DOWNLOAD_LOCATION, '%s.jpeg' % photo_id)
            print("=> done, saving %s" % destination_url)

            with open(destination_url, 'w+') as destination:
                destination.write(photo_raw)

_PROGRESS_BAR_LENGTH = 50
_PROGRESS_BAR_PROGRESS_CHAR = '='
_PROGRESS_BAR_PAD_CHAR = ' '

def build_progress_bar(progress, total, units=''):
    _template = "\r=> [%s] %s";

    progress_percent = math.floor((progress * 100) / float(total))
    m_progress = int(progress * _PROGRESS_BAR_LENGTH / total)

    _progress_bar_body = _PROGRESS_BAR_PROGRESS_CHAR * m_progress
    _progress_bar_extra = ""

    if m_progress < _PROGRESS_BAR_LENGTH - 4: # show percent outside body
        _progress_bar_body = _progress_bar_body + \
            ' %02d%%' % progress_percent + \
            _PROGRESS_BAR_PAD_CHAR * (_PROGRESS_BAR_LENGTH - m_progress - 4)
    else:
        _progress_bar_body = _progress_bar_body + \
            _PROGRESS_BAR_PAD_CHAR * (_PROGRESS_BAR_LENGTH - m_progress)

        _progress_bar_extra = '%02d%% ' % progress_percent

    _progress_bar_extra = _progress_bar_extra + "[%02d%s / %02d%s]" % (progress, units, total, units)

    return _template % (_progress_bar_body, _progress_bar_extra)

def download_with_progress(url):
    response = requests.get(url, stream=True)
    content_length = response.headers.get('content-length')

    if content_length is None:
        print ("!> no content-length header, returning raw content")
        return response.content
    else:
        bytes_downloaded = 0
        content_length = int(content_length)
        _data = ""

        for data in response.iter_content(chunk_size=4096):
            bytes_downloaded = bytes_downloaded + len(data)
            _data = _data + data

            sys.stdout.write(build_progress_bar(bytes_downloaded/1000.0, content_length/1000.0, 'KB'))
            sys.stdout.flush()

        sys.stdout.write("\n")

        return _data

get_backgrounds()