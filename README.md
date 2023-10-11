# plugin.video.nhl66

<p align="center">
  <img src="/resources/media/icon.png" width="512">
</p>

## Features

- **Per-provider proxy selection.** User can switch from ESPN+ to NHL.TV streams without having to play with a VPN.
- **Direct streams.** Streams are fetch directly from ESPN+ and NHL.TV servers and played in original quality (up to 720p60).

## Installation

1. Add a source in the File Manager
   ```
   Settings > File manager > Add source
   ```
   Enter the following location:
   ```
   https://tekbec.github.io/repository.tekbec/
   ```
   Choose a source name, for exemple:
   ```
   tekbek
   ```
2. Install the repository
   ```
   Settings > Add-ons > Install from zip file > tekbec > repository.tekbec-1.0.0.zip
   ```
4. Install the addon
   ```
   Settings > Add-ons > Install from repository > tebec's Repository > Video add-ons > NHL66
   ```

## Troubleshooting

### Unable to start a stream

- If you are trying to play an ESPN+ stream, you must either be located in the US or specify a US proxy in the addon settings.
- If you are trying to play an NHL.TV stream, you must either be located in one of the [supported countries](https://nhl-support.zendesk.com/hc/en-us/articles/5584014279324-NHL-TV) or specify a proxy from one of them in the addon settings.

### ESPN streams stop after a few minutes

- If you are using a proxy for both ESPN and NHL66, try removing the proxy for NHL66 while keeping the ESPN one. Some proxy providers seem to block requests after too many reconnects.



