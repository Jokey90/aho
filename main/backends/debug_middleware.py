def queries_stats(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        from django.db import connection

        response = get_response(request)

        msg = 'Query stats: \tcount:' + str(len(connection.queries)) + '\t' + 'time:' + str(
            round(sum([float(x['time']) for x in connection.queries]), 3)) + ' seconds'
        print(msg)

        return response

    return middleware
