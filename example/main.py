# import Eye from your eyeofsauron package path
from eyeofsauron.client import Eye
from eyeofsauron.enums import Source

import asyncio

async def main():
    eye = Eye("YOUR_PRIVATE_KEY")
    data_key = 'YOUR_DATA_KEY'
    source = Source.NETFLIX
    limit = 10
    page = 1

    activity = await eye.get_activity(
        data_key=data_key,
        source=source,
        limit=limit,
        page=page,
    )

    print(activity)

# Run the main function
asyncio.run(main())
