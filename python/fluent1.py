import msgpack
from io import BytesIO

def overflow_handler(pendings):
    unpacker = msgpack.Unpacker(BytesIO(pendings))
    for unpacked in unpacker:
        print(unpacked)

import logging.config
import yaml

with open('logging.yaml') as fd:
    conf = yaml.load(fd, Loader=yaml.SafeLoader)

logging.config.dictConfig(conf['logging'])

import logging
from fluent import handler

custom_format = {
  'host': '%(hostname)s',
  'where': '%(module)s.%(funcName)s',
  'type': '%(levelname)s',
  'stack_trace': '%(exc_text)s'
}

logging.basicConfig(level=logging.INFO)
l = logging.getLogger('fluent.test')
h = handler.FluentHandler('app.follow', host='host', port=24224, buffer_overflow_handler=overflow_handler)
formatter = handler.FluentRecordFormatter(custom_format)
h.setFormatter(formatter)
l.addHandler(h)
l.info({
  'from': 'userA',
  'to': 'userB'
})
l.info('{"from": "userC", "to": "userD"}')
l.info("This log entry will be logged with the additional key: 'message'.")
