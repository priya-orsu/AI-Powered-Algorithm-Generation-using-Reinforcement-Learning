def algorithm_serializer(data):

    data["_id"] = str(data["_id"])

    return data


def algorithm_list_serializer(data):

    return [algorithm_serializer(item) for item in data]