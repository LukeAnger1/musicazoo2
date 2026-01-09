# Musicazoo Systemd Service Installation

This guide explains how to set up Musicazoo to run automatically on system startup using systemd.

## Prerequisites

1. Ensure all Python dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Install supervisord if not already installed:
   ```bash
   pip install supervisor
   ```

3. Verify the service works manually:
   ```bash
   source init.sh
   ./run_musicazoo.sh settings.json
   ```

## Installation Steps

### 1. Customize the service file

Edit `musicazoo.service` and replace the following placeholders with your actual values:

- **USER_PLACEHOLDER**: Replace both instances with your username (e.g., `user`, not `root`)
- **WorkingDirectory**: Update to the full path of your musicazoo2 repository
- **SHMOOZE_SETTINGS**: Update to the full path of your settings.json file
- **DISPLAY**: Update if your X display is different from `:0`

Example customization:
```bash
# Find your username
whoami

# Get the full repository path
pwd

# Edit the service file
nano musicazoo.service
```

### 2. Copy the service file to systemd directory

```bash
sudo cp musicazoo.service /etc/systemd/system/
```

### 3. Reload systemd daemon

```bash
sudo systemctl daemon-reload
```

### 4. Enable the service to start on boot

```bash
sudo systemctl enable musicazoo.service
```

### 5. Start the service

```bash
sudo systemctl start musicazoo.service
```

## Managing the Service

### Check service status
```bash
sudo systemctl status musicazoo.service
```

### View logs
```bash
sudo journalctl -u musicazoo.service -f
```

### Stop the service
```bash
sudo systemctl stop musicazoo.service
```

### Restart the service
```bash
sudo systemctl restart musicazoo.service
```

### Disable auto-start on boot
```bash
sudo systemctl disable musicazoo.service
```

## Troubleshooting

### Service fails to start

1. Check the service status and logs:
   ```bash
   sudo systemctl status musicazoo.service
   sudo journalctl -u musicazoo.service -n 50
   ```

2. Verify paths in the service file are correct

3. Ensure the user has permissions to access the repository directory

4. Check that supervisord is installed and in PATH:
   ```bash
   which supervisord
   ```

### Permission issues

If the service fails due to permission errors:

1. Make sure the User/Group in the service file matches the owner of the repository
2. Verify file permissions:
   ```bash
   ls -la /home/user/musicazoo2/
   ```

### Display issues

If you get X display errors, ensure:
- X server is running
- The DISPLAY environment variable is correct
- The user has permission to access the display (run `xhost +local:` if needed)

## Advanced Configuration

### Custom settings file

To use a different settings file, modify the `SHMOOZE_SETTINGS` environment variable in the service file:

```ini
Environment="SHMOOZE_SETTINGS=/path/to/your/custom/settings.json"
```

### Running without display (headless)

If running on a headless server, you may need to set up a virtual display using xvfb:

```bash
sudo apt-get install xvfb
```

Then modify the service file to use xvfb-run:
```ini
ExecStart=/usr/bin/xvfb-run -a /usr/bin/supervisord -c /home/user/musicazoo2/supervisord.conf
```
