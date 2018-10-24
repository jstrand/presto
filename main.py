import presto
import logging
import config

logging.basicConfig(level=logging.INFO)

presto.PrestoServer(config.bind_to, config.port).serve_forever()
