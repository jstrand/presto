import presto
import logging

# logging.basicConfig(filename="log.yml")
logging.basicConfig(level=logging.INFO)

bind_to = ''
port = 8000

presto.PrestoServer(bind_to, port).serve_forever()