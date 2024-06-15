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

        print(activities)
        """
            data = [
                (
                    id='ACTIVITY_ID' 
                    metadata=(
                        typename__='NetflixActivityMetadata', 
                        subject=[
                            (
                                typename__='Identifier', 
                                value='tt31473598', 
                                identifier_type=<IdentifierType.IMDB: 'IMDB'>
                            ), 
                            (   
                                typename__='Identifier', 
                                value='10296096', 
                                identifier_type=<IdentifierType.TVDB: 'TVDB'>
                            )
                        ], 
                        title="Judge Dee's Mystery: Season 1: Episode 3", 
                        last_played_at='01/01/2024'
                    ) 
                    typename__='Activity'
                ), ...
            ]
            limit=10 
            total=3409 
            page=1 
            typename__='ActivityResponse'
        """

    asyncio.run(main())
```

#### Lookup Activity

```python

    activity = await eye.lookup_activity(
        data_key="YOUR_DATA_KEY",
        activity_id="ACTIVITY_ID"
    )

    print(activity)
    """
        id='ACTIVITY_ID' 
        metadata=(
            typename__='NetflixActivityMetadata', 
            subject=[
                (
                    typename__='Identifier', 
                    value='tt31473598', 
                    identifier_type=<IdentifierType.IMDB: 'IMDB'>
                ), 
                (   
                    typename__='Identifier', 
                    value='10296096', 
                    identifier_type=<IdentifierType.TVDB: 'TVDB'>
                )
            ], 
            title="Judge Dee's Mystery: Season 1: Episode 3", 
            last_played_at='01/01/2024'
        ) 
        typename__='Activity'
    """
```

#### Get Traits

```python

    traits = await eye.get_traits(
        data_key="YOUR_DATA_KEY",
        source=Source.UBER,
        labels=[TraitLabel.RATING, TraitLabel.TRIP_COUNT, TraitLabel.ACCOUNT_CREATED_ON],
    )

    print(traits)
    """
        [ 
            (
                id='TRAIT_ID', 
                source=<Source.NETFLIX: 'NETFLIX'>, 
                label=<TraitLabel.PLAN: 'PLAN'>, value='premium', 
                timestamp='2024-06-11T11:41:00.552647Z', 
                typename__='Trait',
            ),
            ...
        ]
    """
```

#### Lookup Trait

```python

    trait = await eye.lookup_trait(
        data_key="YOUR_DATA_KEY",
        trait_id="TRAIT_ID"
    )

    print(trait)
    """
        id='TRAIT_ID' 
        source=<Source.NETFLIX: 'NETFLIX'> 
        label=<TraitLabel.PLAN: 'PLAN'> 
        value='premium' 
        timestamp='2024-06-11T11:41:00.552647Z' 
        typename__='Trait'
    """
```

## Contributing

Contributions are welcome, whether they're feature requests, bug fixes, or documentation improvements.
