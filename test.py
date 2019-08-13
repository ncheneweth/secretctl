import json
test_val = [{"Key": "tag1", "Value": "value1"},{"Key": "tag2", "Value": "value2"}]


result = 'tg' in json.dumps(test_val)
print(result)
