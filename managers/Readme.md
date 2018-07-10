# Managers

This module consists of manager classes that perform various functions.

- **ActionManager**: Defined in [actions.py](actions.py). Responsible for
managing and resolving actions for services.
- **Interaction Manager**: Defined in [interaction.py](interaction.py).
Responsible for the interaction and services via Interaction layer.

    `ActionManager` can be considered a part of `InteractionManager`. Later
    uses the former for resolution of actions and handles all other operations
    by itself.

- **BaseServiceManager**: Defined in [service_manager.py](service_manager.py).
Base class for manager of a Bot service. Derive a new class from this class
and override the `incoming_action_callback()` to define what to do when
an action from this service was chosen. All the Children of this class, i.e.
the managers of different services should be `Singleton Classes`.

- **StorageManager**: Defined in [storage.py](storage.py). Class that defines
methods for storing and retrieving data from database.