def invalid_params_response():
    '''
    defines the response sent out if the params are not valid
    '''

    response = {
        'status_code': 400,
        'data': 'Bad Request',
    }

    return response


def unauthorized_response():
    '''
    defines the response sent out if the request is unauthorized
    '''

    response = {
        'status_code': 401,
        'data': 'Unauthorized. User credentials incorrect.',
    }

    return response
