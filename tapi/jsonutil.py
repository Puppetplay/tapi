
def name_to_json(cursor):
    row = [dict((cursor.description[i][0], value)
                for i, value in enumerate(row))
           for row in cursor.fetchall()]
    return row


def json_result(stat=None, data=None):
    result = {
        'status': stat,
        'data': data
    }
    return result

