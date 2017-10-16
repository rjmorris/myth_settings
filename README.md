This repo provides utilities for querying the MythTV database to inspect and edit frontend settings. The primary use case is assigning the settings on a new frontend, because working through the frontend menu system to change all the settings can be tedious. It also helps ensure that different frontends share the same settings.

**WARNING:** The utilities access the database directly, which is frowned upon by the MythTV developers. Use at your own risk. Be sure you have a working database backup in case anything goes wrong.

Settings from 3 database tables are currently supported:

- `settings`: Most of the general frontend settings.
- `keybindings`: Keybindings for actions associated with specific contexts, such as "TV Playback" or "Main Menu".
- `jumppoints`: Keybindings for global actions that jump to different parts of the MythTV interface, such as the Recordings screen or Live TV.

See [sample.py] for an example usage session.
