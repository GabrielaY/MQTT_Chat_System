# Message represents the Ditto's Envelope specification. As a Ditto's message consists of an envelope along
# with a Ditto-compliant payload, the structure is to be used as a ready to use Ditto message.

class Message:
	def __init__(self, topic, headers, path, value, fields, extra, status, revision, timestamp):
		self.topic = topic
		self.headers = headers
		self.path = path
		self.value = value
		self.fields = fields
		self.extra = extra
		self.status = status
		self.revision = revision
		self.timestamp = timestamp
