import requests
from bs4 import BeautifulSoup
from time import sleep

class CoupangParser:
    def __init__(self):
        self.headers = {}

        self.headers['authority'] = 'www.coupang.com'
        self.headers['method'] = 'GET'
        self.headers['path'] = '/'
        self.headers['scheme'] = 'https'

        self.headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        self.headers['accept-encoding'] = 'gzip, deflate, br, zstd'
        self.headers['accept-language'] = 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'

        self.headers['cache-control'] = 'max-age=0'
        self.headers['cookie'] = 'PCID=11254535146241151225774; _fbp=fb.1.1690118144338.282170310; gd1=Y; ILOGIN=Y; sid=e26a571188604543bc8d39382e65e149357a5315; MARKETID=11254535146241151225774; x-coupang-accept-language=ko-KR; x-coupang-target-market=KR; trac_src=0; trac_spec=0; trac_addtag=0; trac_ctag=""; trac_lptag=""; trac_itime=""; trac_sid=""; trac_appver=""; ak_bmsc=D7AE4C72C9B646E1BF499DDF93E4A4F2~000000000000000000000000000000~YAAQb3XTF/efPJaPAQAATq+LoBcr4NlX3+nDx2I624CTGSzz68+0E9v/pjcbRDx9vIYyyROww6OaWbEcbzSltvQzyIM3JuvPyIX1hjGprmevpXnPoaRL9pf3e+nQEy2iUHQfCN8yyNn05D3oXUHEJ3L2F5oPmGV5xjUU+RrzVEBZu+jme0/Xp3jOLIcdOUJbxHakjrSK2xMQvjBJWOUNd+UB+u639ut4L1qM40B1NwaULKoxxDRV1Ag5WlyJIMy/PVUTS1F2aS0bL7M23MTLUIe6ljVaJB6cEYdoJ+51it6faEytvenpjDAJSJI0XQXcMFcKKbeov8Msft8xZaNxF/6PWKx9HlAkq/GEy8VNX8TElGDBPxqsOWTwMd6SPM+wUM/Db1FfALChC5XhKI0/IwJQL5dE8ctaR049EVlFRgD0W57EAnVco/ixJp0sG5c8BfJMieilwKa8TkfNvbss; delivery_toggle=false; CSID=; CUPT=; baby-isWide=small; bm_sv=CCE88017BA6912DC67148EBE0B667DC9~YAAQZAI1F16TOJiPAQAAlN7GoBe7NuhguwOX0s/pc2cTn8kb1uIpY2B8QYXjqbb7i6Bb6BGUcjZukAAAIryTdyRWWQ/ymvHfEi1hEa7Pt4l/y03sHcyizpMOsonMOzN4HH31BI7jKywzwRu9Gysl18tE9Ztj6ursxDhL7hu4vE+Ia8Q7TkMoiDFnbBvYhx8iuQNp6FcWjOyx2Q5fCLhRwPlbM0Obv4iiif20WXOnD2wNZwzqggxOG+HY4TD86zAg8Rc=~1; bm_sz=6E5F2113AE8D07DD0CF41E51C699B96D~YAAQZAI1F1+TOJiPAQAAlN7GoBdlGEqLp4Milg/6dknSLAN7f92rVhq5QWEmV/exklM4G0pv/fx/Pt8ll+gG+slMFVwMahoN5vomCoc95AF0ZNBsJN2KpXhUdX4J8iD1sla1yuf9oxmrSHuVt9tHrEkbdaUgIn6jskQheP8ZHq/Fi9jH7/us5+It1AGwIAnzF315dN50YYBqQb839X7w766QO0L53jod/4TG39/q5TKAuJJgb+VzYCkXdpxuQKlf2bgW6oBqUc9ocWa7i85jdIZW32uX0qt65Aqa+o23+AvMSygq9Q7dV7w/vNdueszS8PwHNxozkUI2OjGIZpmvSAloPGTcdCdjAcvSuGQRULNid09byShXRbwA/gcfIgc6jM85HeT5yMDVQlOTa/qOOZkkt0jtqoGb72fQg5k96UFpobNQg+yAPs6LJjd8gTTJEkmKnCougANvYyiqpqaDfjpBUF/l+TBUysPSyTIu4FM1DF5B0NO29VFQ2CGHkZjJcz2NEOX3evChzzm7Gj3VL60Da9pkuC+kFBxAIabu~4338241~4276792; _abck=B3C2825744BA0F8DF373A6526B484B40~0~YAAQZAI1FySUOJiPAQAA8+LGoAurkAHJRXTUBIbQ5s1UvOXQIWylPQXkviIZOiBLgVhfNSuAurqy7v5AS6Y9If2bqroz+yL1iNX8K2Ql4ZnCRjZVI2pbRQu9nA3l+3U522ZHE2d9Ih4BFLyX+9RyFgIz0aFQU4VKobm2hXwzTl+DUWeTQLl0GQT/9biS9u8ISWS1e3HIbvbpjIx6HKNKtRHla3D24FjHAuSCPPT/0UkCmA/MXmGojDFch2puE0c/n66UWSTRfiIDGIbWOUs4mQOAB6IZlvOzka49F8Zu2yU519M75g84Xw08l179J93PZ28OiKrP/+IAo2u57A4+/vzaytU+fJEe77i7jiC6c2l0aGWT2H3OVsIb0/surDHyRW/MV6EFmYlkAfIRRCuADKYUAhyMWck20EW/KsZIHSukfHx5jNxp~-1~-1~1716392939'

        self.headers['priority'] = 'u=0,i'
        self.headers['sec-ch-a']= '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"'
        self.headers['sec-ch-ua-mobile'] = '?0'
        self.headers['sec-ch-ua-platform'] = '"Windows"'

        self.headers['sec-fetch-dest'] = 'document'
        self.headers['sec-fetch-mode'] = 'navigate'
        self.headers['sec-fetch-site'] = 'same-origin'

        self.headers['sec-fetch-user'] = '?1'
        self.headers['upgrade-insecure-requests'] = '1'
        self.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

        self.referrer = None

    def fetch_url(self, url: str) -> str:
        if self.referrer != None:
            self.headers['referrer'] = self.referrer

        self.headers['path'] = url

        request_url = f'https://www.coupang.com{url}'
        session = requests.Session()
        response = session.get(url=request_url, headers=self.headers, timeout=5)

        if response.status_code != 200:
            raise Exception(f'Coupang responded with a status code {response.status_code}')
        
        self.referrer = request_url
        document = str(response.content, encoding='UTF-8')
        return document

    def get_item(self, product_id, item_id, vendor_item_id, oms_page_id):
        url = f'/vp/products/{product_id}?itemId={item_id}&vendorItemId={vendor_item_id}&omsPageId={oms_page_id}&omsPageUrl={oms_page_id}&isAddedCart='
        
        self.headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        self.headers['priority'] = 'u=0,i'

        self.headers['sec-fetch-dest'] = 'document'
        self.headers['sec-fetch-mode'] = 'navigate'
        
        return self.fetch_url(url)
    
    def get_reviews(self, product_id):
        url = f'/vp/product/reviews?productId={product_id}&page=1&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=3&ratingSummary=true'
        
        self.headers['accept'] = '*/*'
        self.headers['priority'] = 'u=1,i'

        self.headers['cookie'] = 'PCID=11254535146241151225774; _fbp=fb.1.1690118144338.282170310; gd1=Y; ILOGIN=Y; sid=e26a571188604543bc8d39382e65e149357a5315; MARKETID=11254535146241151225774; x-coupang-accept-language=ko-KR; x-coupang-target-market=KR; trac_src=0; trac_spec=0; trac_addtag=0; trac_ctag=""; trac_lptag=""; trac_itime=""; trac_sid=""; trac_appver=""; ak_bmsc=D7AE4C72C9B646E1BF499DDF93E4A4F2~000000000000000000000000000000~YAAQb3XTF/efPJaPAQAATq+LoBcr4NlX3+nDx2I624CTGSzz68+0E9v/pjcbRDx9vIYyyROww6OaWbEcbzSltvQzyIM3JuvPyIX1hjGprmevpXnPoaRL9pf3e+nQEy2iUHQfCN8yyNn05D3oXUHEJ3L2F5oPmGV5xjUU+RrzVEBZu+jme0/Xp3jOLIcdOUJbxHakjrSK2xMQvjBJWOUNd+UB+u639ut4L1qM40B1NwaULKoxxDRV1Ag5WlyJIMy/PVUTS1F2aS0bL7M23MTLUIe6ljVaJB6cEYdoJ+51it6faEytvenpjDAJSJI0XQXcMFcKKbeov8Msft8xZaNxF/6PWKx9HlAkq/GEy8VNX8TElGDBPxqsOWTwMd6SPM+wUM/Db1FfALChC5XhKI0/IwJQL5dE8ctaR049EVlFRgD0W57EAnVco/ixJp0sG5c8BfJMieilwKa8TkfNvbss; delivery_toggle=false; CSID=; CUPT=; overrideAbTestGroup=%5B%5D; authCodeVerifier=IOV190fp7b49-97t0wX3weQO8i9iKsXPVM5ENytryeE; authLoginChallenge=001b26ad71c44bcaaf94d87872da2329; CT_LSID=tVPzFHl0nqtEPJmZtlSDQFD6Mepfv3Dd-DuQoto71c4; _abck=B3C2825744BA0F8DF373A6526B484B40~0~YAAQf2HKF6wbRYWPAQAA+JPtoAuQ+a8KLR/0wPl5oqEaAw3h9KlMiolAH/sjxdsoJvY6gvF/8vUeJsy4fJ8XWCVTiMg/lNOtoKN+AwL2C15wQn8RaECHC2RTEPhQXWl+fB87rHDjhEMHR8V2Dmq1ZN7ltl/Rda1LQk/HvHxzL+hVvAuQJ/id4xRXZG5Lo8rDy7iTQ/yYnffTWeGSnvWORD+grXV/249WOJZbCVrZu11+cDDhFQ8V3ntFFu/QeW2RvjU2sIak6GZ/Lgfyl9Y0QrjzG5qX9z3zNWZojNQEVhL/zLYSheA2AoFo5v2qT23pOeco5aRU/pH4KoChdS2ZG6oI1sLAcVQf64RvjEQw2cywPZl7uJKADDdVS+m024ed+M9YJ8CW8XiLCtsWUT478ZDrgFs1qbf1chYp9ibQ2XwaAdyicUwh~-1~-1~1716395475; bm_sz=6E5F2113AE8D07DD0CF41E51C699B96D~YAAQBg3VFySFGHqPAQAAV5ntoBcD2wFs7hAZ7wsiQ7c2pRfTgpXYAfS3U7rAz0tEdHnJL8EA8e9dtAUZq0pge3tf+WXEZ5vmcQJmXL3vSBaorTx45w+SA4dzURWgoFZ22sg+4Pe3flMil6X0RuI3rtoyoPq0Ejt/BG7J/qSBxSZ7mhj4pZzhfkGLbiPStwgObbXWXxxBaV8XOtcly2ZdPLVH3gEEMnEv03qX/cw1/Mo6nYForpyXhwHIEkysQnLV8QoHcZHM8iwqqDxIl/O3nD8SRkmYW+D0YivH89GqvpT17j4X6E5fAVMTxuZAeyIL/2DZf33mY4rkwZxr4cPvPxDxtToDVXxq2Jdpu9U94dsi011oWjjk0c7aaEg68Qneglt4nFufwX5kl69vwVayMJcJtv777Rg66+doRwyxScbPzSs79uuBVVPhE3gZ1ou1UiujSYdBo2v4TyIgIpmvrK9csIU9hEyIKW2gNroB0Eu+gQAxp/epYfz9tDehGjzhUpnaPlfUdCXqIwO1F5MztJJzz62IES0r8aB79QP58KY=~4338241~4276792; baby-isWide=small; bm_sv=CCE88017BA6912DC67148EBE0B667DC9~YAAQBg3VF6SFGHqPAQAATaLtoBcwoaWyXPopIQZ/M4vNYrZvOLGTmKq9FU7bbT2iGI6lFsUl1WHUlbm8V5oWuMtyV7cQFaSP+Y+IUkB1oQ30Xr3Ein2ze07TzMbpfXszLeiScVY2MigNPHaD6dxNcGYv8nC6IogoQWZHfpC+n2Q9/x3QZZgG+fhJhEcUPDzRdxooz9lBDzyA3EFofAuQddN5lybotUyWINnQYNVE1eAWuk+XPLQbz2k08BGr6dX7M/XK~1'

        self.headers['sec-fetch-dest'] = 'empty'
        self.headers['sec-fetch-mode'] = 'cors'

        return self.fetch_url(url)
    
if __name__ == '__main__':
    crawler = CoupangParser()
    document = crawler.get_item('8017082199', '22392172082', '89392917330', 's278388')
    print(document)
    sleep(3)
    print(crawler.fetch_url('/vp/products/review-details'))
    sleep(3)
    document = crawler.get_reviews('8017082199')

    bs = BeautifulSoup(document, 'html.parser')

    reviews = bs.find('li', name='review')

    for review in reviews:
        print(review)