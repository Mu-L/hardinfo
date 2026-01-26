#!/usr/bin/python

import sys
import json

vendors = {}

for arg in sys.argv[1:]:
  with open(arg, "r") as f:
    contents = f.read().split("\n\n")
    for content in contents:
      vendor = {
        'match_string_case': set(),
        'match_string': set(),
        'match_string_exact': set(),
        'match_string_num_prefix': set(),
        'match_string_num_prefix_case': set(),
        'match_string_prefix': set(),
        'url': set(),
        'url_support': set(),
      }
      for field in (field.strip() for field in content.split("\n")):
        if not field:
          continue
        if field.startswith('#'):
          continue

        key, value = field.split(' ', 1)
        if key.startswith('url'):
          value = value.replace('http://', '')
          value = value.replace('https://', '')
          vendor[key].add(value)
        elif key.startswith('match_'):
          vendor[key].add(value)
        else:
          vendor[key] = value
      
      if not 'name' in vendor:
        continue
      
      if not vendor['name'] in vendors:
        vendors[vendor['name']] = vendor
        continue

      for k, v in vendor.items():
        if k.startswith(('match_', 'url')):
          vendors[vendor['name']][k] |= v

for vendor_name, vendor in sorted(vendors.items()):
  print(f'name {vendor_name}')
  for k, v in vendor.items():
    if k.startswith(('match_', 'url')):
      for elem in v:
        print(f'    {k} {elem}')
    else:
      print(f'    {k} {v}')
  print()

          