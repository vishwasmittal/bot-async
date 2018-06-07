def remove_null_fields(data):
    if type(data) == dict:
        corr_data = {}
        for key in data:
            temp = remove_null_fields(data[key])
            if temp is not None:
                print(key, temp)
                corr_data[key] = temp
        print("from QuerySchema.remove_null_fields\n", corr_data)
        return corr_data
    elif type(data) == list:
        corr_list = []
        for item in data:
            corr_list.append(remove_null_fields(item))
        return corr_list
    else:
        return data
