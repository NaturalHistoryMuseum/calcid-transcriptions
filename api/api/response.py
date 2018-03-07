import io
import csv

from apistar import http


def stream_csv(headers, rows):
    """
    Create CSV as StringIO and stream it as a file to be downloaded
    """
    output = io.StringIO()
    writer = csv.writer(output, delimiter=',')

    writer.writerow(headers)
    writer.writerows(rows)

    content = output.getvalue()
    headers = {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': 'attachment; filename="transcriptions.csv"',
    }
    return http.Response(content=content.encode('utf-8'), headers=headers, content_type='text/csv')
