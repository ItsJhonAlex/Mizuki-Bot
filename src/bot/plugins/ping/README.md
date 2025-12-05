# 🏓 Ping Plugin

Check bot latency and response time with both slash and prefix commands.

## Features

- ⚡ **WebSocket Latency**: Shows the bot's connection latency to Discord
- 📡 **API Latency**: Shows the response time for API requests
- 🎨 **Color-coded**: Visual feedback based on latency (Green/Orange/Red)
- 🔀 **Dual Commands**: Works with both slash and prefix commands

## Commands

### Slash Command
```
/ping
```
- **Description**: Check bot latency
- **Permissions**: Everyone
- **Usage**: Simply type `/ping` and the bot will respond with latency information

### Prefix Command
```
!ping
```
(Replace `!` with your configured prefix)
- **Description**: Check bot latency
- **Permissions**: Everyone
- **Usage**: Type `!ping` (or your prefix + ping)

## Response

The bot will respond with an embed showing:

- **⚡ WebSocket Latency**: Connection latency to Discord (in ms)
- **📡 API Latency**: Time taken to send and receive messages (in ms)

### Latency Colors

- 🟢 **Green** (< 100ms): Excellent connection
- 🟠 **Orange** (100-200ms): Good connection
- 🟠 **Dark Orange** (200-300ms): Fair connection
- 🔴 **Red** (> 300ms): Poor connection

## Example Output

```
🏓 Pong!

⚡ WebSocket Latency: 45ms
📡 API Latency: 78ms

Requested by YourUsername
```

## Technical Details

- **Plugin Version**: 1.0.0
- **Author**: ItsJhonAlex
- **Dependencies**: None (uses built-in Discord.py)

## Code Structure

```python
PingPlugin
├── ping_slash()      # Slash command handler
├── ping_prefix()     # Prefix command handler
└── _get_latency_color()  # Helper to determine embed color
```

## Logs

The plugin logs each ping command usage with the format:
```
Ping command used by Username (WS: XXms, API: XXms)
```

## Troubleshooting

**High latency?**
- Check your server's internet connection
- Verify Discord API status: https://discordstatus.com/
- Consider your bot's hosting location (closer to Discord servers = lower latency)

**Command not working?**
- For slash commands: Make sure commands are synced (`/plugins` to verify)
- For prefix commands: Verify your bot's prefix in `.env`

