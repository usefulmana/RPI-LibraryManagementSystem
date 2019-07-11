import base64

print('before')
string = 'OWZ1bzhxa2RrcWZvNGR1MTAyaTk0cmVyNm8gbmxiYXNuaTIwMTBAbQ'
lens = len(string)
lenx = lens - (lens % 4 if lens % 4 else 4)
decoded_string = base64.b64decode(string[:lenx])
print(decoded_string)
print('after')
event_id = str(decoded_string).split(' ')[0][2:].strip()
print(event_id)