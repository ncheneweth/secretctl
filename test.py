import json
# fixtures = [
#     {"path": "app/dev/secret1", "value": "111", "description": "secret1 description", "tags": "team=one"},
#     {"path": "app/dev/secret2", "value": "222", "description": "secret2 description", "tags": "team=two"},
#     {"path": "app/dev/secret3", "value": "333", "description": "secret3 description", "tags": "team=three"}
# ]
#
# for secret in fixtures:
#     print(secret['path'])
test = [{'secret1': '111'}]

print(next(test[0].values()))
