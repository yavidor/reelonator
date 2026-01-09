import requests
import json
import sys
from urllib.parse import quote


def create_payload(shortcode):
    """Create payload with dynamic shortcode"""
    variables = json.dumps({"shortcode": shortcode})
    encoded_variables = quote(variables)

    return f'av=0&__d=www&__user=0&__a=1&__req=u&__hs=20371.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=GOOD&__rev=1028249517&__s=ywybjm%3Aq4co81%3Adplvd8&__hsi=7559456450740095677&__dyn=7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJw5ux609vCwjE1EE2Cw8G11wBz81s8hwGxu786a3a1YwBgao6C0Mo2swtUd8-U2zxe2GewGw9a361qw8Xxm16wa-0raazo7u3C2u2J0bS1LwTwKG0WE8oC1Iwqo5p0OwUQp1yU426V89F8uwm8jwhUaE4e1tyVrx60gm5oswFwtF85i5E&__csr=geIAaiFliZllsBav4trBuTJ-KJ5WhnQyAnxeEWpBCC-hJADG9AgG4qpQ8zat5BypWy9eaRgBaJ2Xx2p6WgymmGDzQjJo8JJ4iKi8xObCjx50FzLF4-8DiwxDyGqoydV-ESQ9DLAB_GdDzFEsyUSeG8xmF9oymWyqyVFF84q5ooHohwuE5a0CU01kUUb81CE12E5V08m0WFA0ei80n2bLwjp42TOw2J-0rq04tUKp06PwEhy1u1ig4Dgy9wdW0D8n80rl0UxGtw53hEx2E1yPUy7U1J9Q0JFvc0cXwpyG4B6B2US01IAw2Bo0K215w0YEwj8&__hsdp=gaQbh9gple4i4WuA2XCG7RVt5m8DxGU4K32awCF0GBcq1AyH40uWxe3AwboK5-0FE8UbkkU4-4o11XwQCyE9UswZweC4U6iq6UOewJyEhwBwjQ2259o1oE1E85u0km5Unw7Pwaau1CwMwkEeU1v82ew2rA0LoW0W8aO0Ewc6&__hblp=0nE20wpGx6vxy2i1ryE9Gg6q1hwkE9WwkocUso4O2vDyof98K7o4-48hDwyLBx61HwkGg8VoGqawDxCGBwQxG6S0I8jwywXBCxKczEqxaax62m1FDxim1nw4axq0oC362m0iu7ohBxu11wEwfm0AE421xDwhEvwxzEvG2-3K0nO0zE1MUK0DA1DwgEizEW0Qp-2Awa8nxyi1fwRBwFwau68bE&__comet_req=7&lsd=AdGtgRvhyjc&jazoest=21085&__spin_r=1028249517&__spin_b=trunk&__spin_t=1760073111&__crn=comet.igweb.PolarisLoggedOutDesktopPostRouteNext&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisPostRootQuery&server_timestamps=true&variables={encoded_variables}&doc_id=24368985919464652'


def scrape_instagram_reel(id):
    """Main function to scrape Instagram reel data with error handling"""
    try:
        shortcode = id
        payload = create_payload(shortcode)
        print(payload)

        headers = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
            'x-csrftoken': 'YuvV-QRvpR2Ggzgk0cTg1T',
            'x-ig-app-id': '936619743392459',
            'Cookie': 'csrftoken=YuvV-QRvpR2Ggzgk0cTg1T; mid=aOia4gALAAHSq3em2E34YEIFkMCC'
        }

        response = requests.post("https://www.instagram.com/graphql/query",
                                 headers=headers, data=payload, timeout=10)

        # Handle rate limiting
        if response.status_code == 429:
            return {
                "error": True,
                "status_code": 429,
                "message": "Rate limited. Please try again later."
            }

        # Handle not found
        if response.status_code == 404:
            return {
                "error": True,
                "status_code": 404,
                "message": "Reel not found or private."
            }

        # Handle other HTTP errors
        if response.status_code != 200:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": f"HTTP error: {response.status_code}"
            }

        data = response.json()

        # Check if reel data exists in response
        if not data.get('data', {}).get('xdt_api__v1__media__shortcode__web_info', {}).get('items'):
            return {
                "error": True,
                "status_code": 404,
                "message": "Reel data not found in response"
            }

        # Save successful response
        filename = f'{shortcode}_response.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return {
            "error": False,
            "status_code": 200,
            "message": "Success",
            "filename": filename,
            "data": data
        }

    except ValueError as e:
        return {
            "error": True,
            "status_code": 400,
            "message": f"Invalid URL: {str(e)}"
        }
    except requests.exceptions.Timeout:
        return {
            "error": True,
            "status_code": 408,
            "message": "Request timeout"
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": True,
            "status_code": 500,
            "message": f"Network error: {str(e)}"
        }
    except Exception as e:
        return {
            "error": True,
            "status_code": 500,
            "message": f"Unexpected error: {str(e)}"
        }


# Example usage
if __name__ == "__main__":
    reel_url = sys.argv[1]

    if not reel_url:
        print("No reel provided")
        exit(1)

    print(f"Scraping: {reel_url}")
    result = scrape_instagram_reel(reel_url)

    # Print result summary
    print(f"\nStatus: {'SUCCESS' if not result['error'] else 'FAILED'}")
    print(f"Message: {result['message']}")
    print(f"Status Code: {result['status_code']}")

    if not result['error']:
        print(f"File saved: {result['filename']}")
    else:
        print("Got error:")
        print(result['error'])
