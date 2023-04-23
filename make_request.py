import requests
import json

url = 'http://localhost:6543/benford'

file = {'file': open('sample_data3.csv', 'rb')}
response = requests.post(url, files=file)

if response.status_code == 200:
    print("CSV file uploaded successfully!")
    res = json.loads(response.text)
    if bool(res['follows']):
        print('Given data follows benford\'s law with p_value = ', res['P_value'])
    else:
        print('Given data doesnot follow benford\'s law with p_value = ', res['P_value'])
else:
    print("Error uploading CSV file:", response.text)

