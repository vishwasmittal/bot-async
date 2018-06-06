__all__ = ['message_parser']


async def message_parser(validated_data):
    """

    :param: validated_data: telegram.schema.Update Object for the incoming data in telegram webhook request
    """
    # pprint(UpdateSchema().dumps(validated_data))
    # await asyncio.sleep(3)
    # print("job sleep complete")


"""
Message parser:
validated data is received



"""
