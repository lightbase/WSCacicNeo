import csv
import json
from pyramid.response import Response
from pyramid.response import FileResponse
import uuid
import os

def json2csv(request):

    json_data = request.params['json_data']
    filename = request.params['filename']

    json_data = json.loads(json_data)

    columns = list(json_data[0].keys())

    file_path = '/tmp/' + str(uuid.uuid4()) + '.csv'

    csvfile = open(file_path, 'w')

    spamwriter = csv.writer(csvfile, delimiter=';',
        quotechar='|', quoting=csv.QUOTE_MINIMAL)

    spamwriter.writerow(columns)

    for row in json_data:
        spamwriter.writerow(list(row.values()))

    csvfile.close()

    app_iter = open(file_path).read()
    os.remove(file_path)
    content_type=[
        'text/csv',
        'charset=UTF-8',
    ]
    content_disposition=[
        'attachment',
        'filename=' + filename,
    ]
    return Response(app_iter=app_iter,
        content_type='; '.join(content_type),
        content_disposition='; '.join(content_disposition))

