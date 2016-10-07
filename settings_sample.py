# coding: utf-8
#
# Sample config file for whoisd
#
# Copy to settings.py and edit with your parameters
#

BIND_ADDRESS='0.0.0.0'
BIND_PORT=43

# Backend URL
# Queried domain is appended to this string.
# Expects an Ordered List in json
BACKEND_QUERY_URL='http://a.b.c.d:80/whois/'

# Maximum line length for a query.
MAX_LINE_LENGTH=100

# Regular expression used to validate queries
VALID_QUERY=r'^[a-zA-Z\d]{,63}(\.[a-zA-Z\d-]{,63})*.(ac|al|ap|am|ba|ce|df|es|go|ma|mt|ms|mg|pr|pb|pa|pe|pi|rj|rn|rs|ro|rr|sc|se|sp|to).leg.br\r?\n'

# Response header and footer
RESPONSE_HEADER="""whois server header
This text will be sent before each response
"""

RESPONSE_FOOTER="""whois server footer
Guess what. This will also be sent, but after each response
"""
