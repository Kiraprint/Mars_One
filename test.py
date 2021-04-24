from requests import put, get, post, delete

url = 'http://127.0.0.1:5000/api/v2/jobs'

print(get(url).json())
print(post(url,
           json={'job': 'work', 'work_size': 20, 'collaborators': '1, 2, 3', 'team_leader': 2}).json())
print(get(url + '/2').json())
print(put(url + '/2',
          json={'job': 'work', 'work_size': 35, 'collaborators': '1, 3', 'team_leader': 2}).json())
print(get(url + '/2').json())
print(delete(url + '/2').json())
print(get(url + '/2').json())
