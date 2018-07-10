# Publisher Framework

The publisher framework that is responsible for Spamming the user with
new content :stuck_out_tongue:.

This module Works on PUB-SUB Architecture

This Module, currently, consists of 4 parts.
- **manager**: Manager for the Publisher Framework. A singleton class.
- **publishers**: various publishers that will send the periodic data to the
users
- **Filters**: Filters for filtering the data before publishing
- **News Poller**: An pre-implemented RSS news fetcher.