# gandalf-python-sdk

gandalf-python-sdk is a command-line tool designed to generate the necessary files that makes it super easy to interact with the Sauron API. It completely abstracts away the complexity of authentication and interacting with the GraphQL APIs.

## Features

- Generate necessary files required for interacting with the Sauron API
- Automatically install required dependencies

## Installation

### Prerequisites

- [Python](https://www.python.org/downloads/) - version 3.10 or higher

### Installing eyeofsauron

```bash

pip install git+https://github.com/gandalf-network/gandalf-sdk-python.git

```

## Usage

```bash

eyeofsauron generate

```

### Flags

- --folder [folder]: Set the destination folder for the generated files

### Using the Generated Files

Once you have successfully generated the necessary files and installed the required dependencies using eyeofsauron, you can proceed to use these files to interact with the API.

#### Initialization

```python

# Change eyeofsauron to suit the path you specified for the SDK generation
from eyeofsauron.client import Eye
from eyeofsauron.enums import Source
from eyeofsauron.enums import TraitLabel

eye = Eye("YOUR_PRIVATE_KEY")
```

#### Get Activity

```python
    import asyncio

    async def main():
        activities = await eye.get_activity(
            data_key = 'YOUR_DATA_KEY',
            source = Source.NETFLIX,
            limit = 10,
            page = 1,
        )

        print(activities.data)

    asyncio.run(main())
```

#### Lookup Activity

```python

    activity = await eye.lookup_activity(
        data_key="YOUR_DATA_KEY",
        activity_id="ACTIVITY_ID"
    )

    print(activity)
```

#### Get Traits

```python

    traits = await eye.get_traits(
        data_key="YOUR_DATA_KEY",
        source=Source.UBER,
        labels=[TraitLabel.RATING, TraitLabel.TRIP_COUNT, TraitLabel.ACCOUNT_CREATED_ON],
    )

    print(traits)
```

#### Lookup Trait

```python

    trait = await eye.lookup_trait(
        data_key="YOUR_DATA_KEY",
        trait_id="TRAIT_ID"
    )

    print(trait)
```

## Contributing

Contributions are welcome, whether they're feature requests, bug fixes, or documentation improvements.
