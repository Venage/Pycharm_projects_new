def interceptor(request):
    del request.headers['accept-language']
    request.headers['accept-language'] = 'en-GB,en-US;q=0.9,en;q=0.8'