import re
text = "0:efdc359a587e9d2677ca859a55507a3c46ba325b4ebd05ddf3738cbcb03b78f1"

print(re.match(r'^0:[0-9a-fA-F]+$', text))
