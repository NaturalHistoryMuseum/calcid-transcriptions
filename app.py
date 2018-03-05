from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
# from apistar.handlers import docs_urls, static_urls


# def welcome(name=None):
#     if name is None:
#         return {'message': 'Welcome to API Star!'}
#     return {'message': 'Welcome to API Star, %s!' % name}


def get_transcription():
    pass
    # if name is None:


def create_transcription():
    pass
    # if name is None:


def edit_transcription(transcription_id):
    pass
    # if name is None:
    #     return {'message': 'Welcome to API Star!'}
    # return {'message': 'Welcome to API Star, %s!' % name}

transcription_routes = [
    Route('/', 'GET', get_transcription),
    Route('/', 'POST', create_transcription),
    Route('/{transcription_id}', 'PUT', edit_transcription)
]


routes = [
    Include('/transcriptions', transcription_routes)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
