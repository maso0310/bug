import requests

file = {'uploadFile': open('C:/bug/397892.jpg', 'rb')}
print(file)
r = requests.post('http://pythonscraping.com/pages/files/processing2.php', files=file)
print(r.text)

# The file image.png has been uploaded.