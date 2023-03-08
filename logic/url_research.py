from urllib.parse import urlparse
from OpenSSL.SSL import Connection, Context, SSLv3_METHOD, TLSv1_2_METHOD
from datetime import datetime
import OpenSSL
import socket
import httpx
import asyncio
import whois


async def country_host(url: str):
    domain_name = urlparse(url).hostname
    ip = socket.gethostbyname(domain_name)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'http://ipinfo.io/{ip}/json')
            response = response.json()
        return {"result": f'{response["country"]}, {response["city"]}'}
    except Exception as ex:
        return {"result": "error"}


async def country_domain(url: str):
    domain_name = urlparse(url).hostname
    loop = asyncio.get_running_loop()
    country = await loop.run_in_executor(None, whois.whois, domain_name)
    try:
        return {"result": f'{country["country"]}, {country["state"]}'} if country["country"] else {"result": "error"}
    except KeyError:
        return {"result": f'{country["registrar"]}'} if country["registrar"] else {"result": "error"}


async def date_create_domain(url: str):
    domain_name = urlparse(url).hostname
    loop = asyncio.get_running_loop()
    date = await loop.run_in_executor(None, whois.whois, domain_name)
    date = date['creation_date']
    if type(date) == list:
        return {"result": datetime.strptime(str(date[0]), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")} if date else {
            "result": "error"}
    else:
        return {"result": datetime.strptime(str(date), "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y")} if date else {
            "result": "error"}


async def check_protocol(url: str):
    domain_name = urlparse(url).hostname
    if 'www.' in domain_name:
        domain = domain_name.split('www.')[1]
    else:
        domain = domain_name
    try:
        cert_info = dict()
        try:
            ssl_connection_setting = Context(SSLv3_METHOD)
        except ValueError:
            ssl_connection_setting = Context(TLSv1_2_METHOD)
        ssl_connection_setting.set_timeout(3)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            loop = asyncio.get_running_loop()
            await loop.sock_connect(s, (domain, 443))
            c = Connection(ssl_connection_setting, s)
            c.set_tlsext_host_name(str.encode(domain))
            c.set_connect_state()
            await loop.run_in_executor(None, c.do_handshake)

            cert = c.get_peer_certificate()

            sub_list = cert.get_subject().get_components()

            for item in sub_list:
                if item[0].decode('utf-8') == 'CN':
                    cert_info['toWhomIssued'] = item[1].decode('utf-8')

            if cert_info['toWhomIssued'][2:] == domain or cert_info['toWhomIssued'][1:] in domain:
                cert_info['domainMatch'] = True
            else:
                cert_info['domainMatch'] = False

            if not cert.has_expired():
                cert_info['valid'] = True
                cert_info['validUntil'] = str(
                    datetime.strptime(str(cert.get_notAfter().decode('utf-8')), "%Y%m%d%H%M%SZ").strftime(
                        "%d-%m-%Y"))
            else:
                cert_info['valid'] = False
                cert_info['expired'] = str(
                    datetime.strptime(str(cert.get_notAfter().decode('utf-8')), "%Y%m%d%H%M%SZ").strftime(
                        "%H:%M:%S %d-%m-%Y"))
            return {"result": cert_info}

    except (TypeError, ConnectionRefusedError, socket.gaierror, OSError, OpenSSL.SSL.Error):
        return {"result": 'Detailed information about the certificate is missing.'}


async def main(url: str):
    country = asyncio.create_task(country_host(url))
    ssl = asyncio.create_task(check_protocol(url))

    domain = asyncio.create_task(country_domain(url))
    date = asyncio.create_task(date_create_domain(url))

    results = await asyncio.gather(country, domain, ssl, date, return_exceptions=True)

    return {
        "countryHost": results[0],
        "countryDomain": results[1],
        "certSSL": results[2],
        "domainCreationDate": results[3]
    }
