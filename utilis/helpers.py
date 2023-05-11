def get_current_host(request):
    """
        get the current host name
    """
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol,host=host)
