import sys
import asyncio
from jsonrpcserver import async_dispatch, method, InvalidRequest
from .handlers import run_simulation

# decorate your handler so jsonrpcserver can find it by name:
method(name="runSimulation")(run_simulation)

class Server:
    async def _serve(self):
        """
        Read stdin line by line, dispatch each request through jsonrpcserver,
        write back the response (if any).
        """
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await asyncio.get_event_loop().connect_read_pipe(lambda: protocol, sys.stdin)

        while not reader.at_eof():
            line = await reader.readline()
            if not line:
                break
            text = line.decode().strip()
            if not text:
                continue

            # dispatch handles request/response and error formatting
            response = await async_dispatch(text)
            if response.wanted:
                # write response (notifications are not echoed)
                sys.stdout.write(str(response) + "\n")
                sys.stdout.flush()

    def run(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self._serve())
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()
