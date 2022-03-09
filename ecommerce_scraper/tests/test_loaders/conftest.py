import pytest
from scrapy.http import Request, HtmlResponse
import os

wiki_url = 'https://www.wiki.tn/pc-portables-gamer/pc-portable-asus-gaming-tuf-505dt-amd-r5-16go-512go-ssd-noir-35475.html'
file_name = 'Wiki_Asus_gaming_laptop.html'


@pytest.fixture(scope="session", params=[(wiki_url, file_name)])
def response_stub(request):
    url, file_name = request.param
    request = Request(url=url, meta={'dont_cache': True})

    if not file_name[0] == '/':
        responses_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(responses_dir, file_name)
    else:
        file_path = file_name

    with open(file_path, 'rb') as f:
        file_content = f.read()

    response = HtmlResponse(url=url, request=request, body=file_content)
    return response