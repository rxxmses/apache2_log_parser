from bs4 import BeautifulSoup
import requests
import re

url = "https://telegra.ph/Sample-log-01-27"
headers = {'Accept': "*/*", 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
response = requests.get(url, headers=headers)
parse_text = response.text

soup = BeautifulSoup(parse_text, "html.parser")
p_logs = soup.find_all('article', class_='tl_article_content')[0].find_all('p')

pattern = r'(\S+) (\S+) (\S+) (\S+) (\d+) \[(.*?)\] "(.*?)" "(.*?)" (\d+) (\S+) "(.*?)" "(.*?)" (\d+) (\d+) (\d+)'

dict_of_ip = {}
dict_of_requests = {}

for p in p_logs:
    text = p.text
    result = re.match(pattern, text)

    if result:
        ip_address = result.group(1)
        if ip_address in dict_of_ip:
            dict_of_ip[ip_address] += 1
        else:
            dict_of_ip[ip_address] = 1

        remote_host = result.group(2)
        user_identity = result.group(3)
        user_auth = result.group(4)
        port = result.group(5)
        timestamp = result.group(6)
        request = result.group(7)
        if request in dict_of_requests:
            dict_of_requests[request] += 1
        else:
            dict_of_requests[request] = 1

        referrer = result.group(8)
        status_code = result.group(9)
        response_size = result.group(10)
        user_agent = result.group(11)
        duration = result.group(12)
        request_size = result.group(13)
        offset = result.group(14)

        print("IP Address:", ip_address)
        print("Remote Host:", remote_host)
        print("User Identity:", user_identity)
        print("User Authentication:", user_auth)
        print("Port:", port)
        print("Timestamp:", timestamp)
        print("Request:", request)
        print("Referrer:", referrer)
        print("Status Code:", status_code)
        print("Response Size:", response_size)
        print("User Agent:", user_agent)
        print("Duration:", duration)
        print("Request Size:", request_size)
        print("Offset:", offset, "\n\n")
    else:
        print("Строка не соответствует формату.")

print("ТОП IP:")
sorted_ip = dict(sorted(dict_of_ip.items(), key=lambda x: x[1], reverse=True))
for key, value in sorted_ip.items():
    print(f"{key}: {value} раз")

print("\n\nТОП запросов:")
sorted_requests = dict(sorted(dict_of_requests.items(), key=lambda x: x[1], reverse=True))
for key, value in sorted_requests.items():
    print(f"{key}: {value} раз")