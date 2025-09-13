# Domain Blacklist Feature

## Overview

The Domain Blacklist feature allows you to exclude specific device domains from being included in the prompt sent to the LLM. This is useful when you have many devices of a certain type that you don't want to be accessible through voice commands or when you want to reduce the prompt size by excluding less important device types.

## Configuration

To use the Domain Blacklist feature:

1. Navigate to your Home Assistant instance
2. Go to **Settings** > **Devices & Services**
3. Find the **WebSocket Model Context Protocol Server** integration and click on it
4. Click on **Configure**
5. In the configuration form, you'll find a text field for **domain_blacklist**
6. Enter the domains you want to blacklist, separated by commas (e.g., `switch,light,sensor`). Use a simple text format without special formatting.
7. Click **Submit** to save your configuration

## How It Works

When the integration processes the prompt to be sent to the LLM:

1. It checks if any domain blacklist is configured
2. If a blacklist exists, it parses the Static Context section of the prompt
3. Any device with a domain matching an entry in the blacklist will be removed from the prompt
4. The filtered prompt is then sent to the LLM

## Example

If your original prompt contains:

```
Static Context: An overview of the areas and the devices in this smart home:
- names: Living Room Light
  domain: light
  areas: Living Room
- names: Kitchen Switch
  domain: switch
  areas: Kitchen
- names: Bedroom Thermostat
  domain: climate
  areas: Bedroom
```

And you've blacklisted `switch,light`, the filtered prompt will contain:

```
Static Context: An overview of the areas and the devices in this smart home:
- names: Bedroom Thermostat
  domain: climate
  areas: Bedroom
```

## Logging

The integration logs information about the domain blacklist processing:

- When a domain blacklist is enabled
- Which devices are filtered out
- The final prompt after filtering

You can check these logs in your Home Assistant logs with the filter `custom_components.ws_mcp_server`.

## Notes

- The domain blacklist only affects the Static Context section of the prompt
- It does not prevent devices from being controlled through other means
- Changes to the blacklist require a restart of Home Assistant to take effect