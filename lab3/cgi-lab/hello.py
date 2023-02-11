#!/usr/bin/env python3

import os
import json

print("Content-Type: application/json")
print()

print(json.dumps(dict(os.environ), indent=2))
#Q2 QUERY_STRING

#Q3 HTTP_USER_AGENT


