import requests

url = "http://127.0.0.1:8000/api/update-profile/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyNDI2MjMzLCJpYXQiOjE3NDI0MjU5MzMsImp0aSI6ImVlYThiYThkMjAxYzQyMTc4NzVjNTJjMDVhMmE2YzdkIiwidXNlcl9pZCI6MX0.ta8sJXTiQ1o7uYw1nfqKotCP-5UsPxKO2dSRY34GMts",
    "Content-Type": "application/json"
}
data = {
    "name": "moreen",
    "email": "moreenvictor@gmail.com"
}

response = requests.patch(url, json=data, headers=headers)
print(response.json())
