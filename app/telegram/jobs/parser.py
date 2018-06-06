import asyncio

__all__ = ['message_parser']


async def message_parser(validated_data):
    """
    This will handle the message sent by telegram through webhook
    """
    print(validated_data)
    await asyncio.sleep(3)
    print("job sleep complete")
