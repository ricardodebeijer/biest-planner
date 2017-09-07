import os
from shutil import copyfile

from biestplanner import settings


def save_planning(planning):
    base = settings.MEDIA_ROOT + '/plannings/'
    latest = base + 'planning.xls'
    storage = base + planning.name

    if not os.path.exists(base):
        os.mkdir(base)

    with open(storage, 'wb+') as destination:
        for chunk in planning.chunks():
            destination.write(chunk)

    if os.path.exists(latest):
        # print('latest exists, removing:')
        os.remove(latest)
    # print('copying uploaded to latest')
    copyfile(storage, latest)
    return
