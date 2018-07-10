# Actions

Fundamental unit of User-Bot interaction (commands/data sent by user to
the bot).

There can be three `kinds` of such interactions:
- `Command`: Slash commands that specify specific action eg `/start`.
- `Message`: Fixed message that need not be represented as slash command.
- `Input`: Request random keyboard input from the user.


Each `Action` has following basic attributes:
- `Trigger`: Keyword that can activate the command. (Doesn't contain
preceding `/` in case of slash commands
- `Kind`:
    - `C`: for slash command
    - `M`: for some fixed message
    - `I`: for input action
- `callback function`: function to be called when this action is invoked.
