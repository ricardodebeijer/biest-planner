import os
from shutil import copyfile

from biestplanner import settings


def save_planning(planning):
    latest = settings.MEDIA_ROOT + '/plannings/' + 'planning.xls'
    storage = settings.MEDIA_ROOT + '/plannings/' + planning.name

    with open(storage, 'wb+') as destination:
        for chunk in planning.chunks():
            destination.write(chunk)

    if os.path.exists(latest):
        #print('latest exists, removing:')
        os.remove(latest)
    #print('copying uploaded to latest')
    copyfile(storage, latest)
    return
