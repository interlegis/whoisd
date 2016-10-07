# coding: utf-8

import asyncio
import collections
import json
import re
import requests
from requests_futures.sessions import FuturesSession

import settings

class WhoisServerClientProtocol(asyncio.Protocol):

    # asyncio.Protocol methods
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        #self.send_comment("Hi there. This is whois server")
        self.query_buffer = ''
        self.loop = self.transport._loop

    def data_received(self, data):

        self.query_buffer += data.decode()

        if len(self.query_buffer) > settings.MAX_LINE_LENGTH:
            self.send_error('ERROR: input line too long')

        # wait for more data in case query buffer doens't contain a line
        if re.match(r".*\n", self.query_buffer) == None:
            return

        if re.match(settings.VALID_QUERY, self.query_buffer, flags=re.IGNORECASE) == None:
            self.send_error('ERROR: invalid query')
            return # needed because of multithreading

        # query looks ok, schedule an answer
        self.query = self.query_buffer.strip()
        asyncio.ensure_future(self.process_query(self.query))

    def eof_received(self):
        """ Close connection. """
        # Multithreading mistery... why?
        asyncio.run_coroutine_threadsafe(self.close_connection(), self.loop)

    # auxiliary methods
    def send_line(self, string, meta=False):
        """ sends a line, if meta=True prepends line with % """
        if meta:
            string = '% ' + string
        string += '\r\n'
        self.transport.write(string.encode())

    def send_lines(self, lines_list, meta=False):
        """ send a list of lines """
        for line in lines_list:
            self.send_line(line, meta)

    def send_comment(self, comment_string):
        """ send a comment line """
        self.send_line(comment_string, meta=True)

    def send_error(self, error_string):
        """ sends an error message and closes connection """
        self.send_line(error_string, meta=True)
        self.eof_received()

    async def close_connection(self):
        """ coroutine used to close connection from another thread.

        example: 
        asyncio.run_coroutine_threadsafe(self.close_connection(), self.loop)
        """
        self.transport.close()

    # worker method
    async def process_query(self, query):

        #result = requests.get(settings.BACKEND_QUERY_URL+self.query)
        #class fut:
        #    def __init__(self, res):
        #        self.res = res
        #    def result(self):
        #        return self.res

        #future = fut(result)
        #self.send_query_result(future)
        #return

        session = FuturesSession()
        future = session.get(settings.BACKEND_QUERY_URL+query)
        future.add_done_callback(self.send_query_result)

    def send_query_result(self, future):

        self.send_line('')
        self.send_lines(settings.RESPONSE_HEADER.splitlines(), meta=True)
        self.send_line('')

        response = future.result()
        assert response.status_code == 200
        asdf=json.loads(response.text, object_pairs_hook=collections.OrderedDict)

        if len(asdf) == 0:
            self.send_comment('No match for: %s' % self.query)
        else:
            for (k,v) in asdf.items():
                if k[0] == '_':
                    send=self.send_comment
                else:
                    send=self.send_line
                send("%s: %s" % (k,v))
        
        self.send_line('')
        self.send_lines(settings.RESPONSE_FOOTER.splitlines(), meta=True)
        self.send_line('')

        self.eof_received()
        #asyncio.run_coroutine_threadsafe(self.close_connection(), self.loop)

loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(WhoisServerClientProtocol, settings.BIND_ADDRESS, settings.BIND_PORT)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    print('KeyboardInterrupt. Closing.')
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
