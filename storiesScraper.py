import requests
import json
import sys
from urllib.parse import quote


def create_payload(user_id: str):
    """Create payload with dynamic user_id"""

    variables = json.dumps({"reel_ids_arr":[user_id],"__relay_internal__pv__PolarisCommunityNoteStoriesLabelEnabledrelayprovider":True})

    encoded_variables = quote(variables)

    return f'av=0&__d=www&__user=0&__a=1&__req=q&__hs=20718.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=EXCELLENT&__rev=1048159918&__s=zkak6z%3At7hnq5%3Az992cx&__hsi=7688463637682775812&__dyn=7xeUjG1mxu1syaxG4Vp41twpUnwgU7SbzEdF8vyUco2qwJyEiw50x609vCwjE1EEc87m0yE462mcw5Mx62G5UswoEcE7O2l0Fwqo5W1yw9O1lwxwQzXwae4UaEW2G0AEco5G0zK5o4q0HU1wEbUGdwtUeo9UaQ0Lo6-bwHwKG6Ufk0zU8oC1IwjUpwlAcwBwUQp1yU426V8aUuwm8jxK0-8KmUhw4rwXyFEaVE4616wAwj83KwRyrg5e&__csr=gQw8YcTqtgx55lrWYFay7XL-4bklFROlfF46E_BiliWnWR-j_apABWZqF6-mVVXKaGGExZjWtfBd7aOita9NRKqykHALQhbARKihA8CuAFaYWVmiJk9CKlaKCmui52qykTF6hEHBBzazHxmVlVXBl7x6ayFk5oCp1ebxucDUoxivyUgghgOXBm9KWmbKaDxWHGdZ5AG58KlU-uWUkKF9GxachF8KquibGfxvy88F84q1gAwcJ3bw5Zw08H-00Yp8cU4W07H8Qo9kawODu0ftws930Ro0hmw16q9yk0IE4ml0vQ5ozw2pUBpxM128xo1lE1zUO0TaiJ4yQ2G17xK1jwqEbQmVixm05MEvAy401JOw0BMUow3QS06EU3Sw3eo&__hsdp=g4d9Yj1AxbapbSdanklsHteLeyuPlc8wEB1yWKN0gJ1irq2o8F860x84e4i0Gxi1WglwkUoxtFAlJ0Ag9N0jwBxe4E5S1fw-BDwp69wn83swLx61mxiu1uwTxe16wgUgxK16wmFUsyoW2O0PVU0EO0Vo0xS0wo0zC0RUe86W07g84-3u0AO1e3O3m481PE3RwIw4rU6G0oe1vwcm09Sw2-UfE5O0Ulu8wqo2jo&__hblp=1y2CU5u3e3u7UkG8F9u8yUsxG6HwYwQzohDy-bAG54FoC1oCy8nwwwyzbo5qi1jGq2eqpdd0yQi2xrXDwyG9yoiwRwDDDwQyEfFpU62S9w_xCK6U-2-1swxwLzrCxe2Si8yUyu78463u4UeEK13Dy9UjwhEG2i2Gu6qy6dwwyU3fDw2eodosxSaz8W10wnU4Zo1A8eo21wdm7U1gU3nwUwrE0ZC081w8K3W1bwjo4-m36umcxW1p8iuq3O48623609DwIwbC1xU526oK0nu1vwsU5609Swa2ew8O16weq1kyEc8fEb8bU2BwXlUy1Eg2jo&__sjsp=g4dnYj5Mj9OIFAEjanklsHteLeyuOtswy2ya1aq2F1i01VAw&__comet_req=7&fb_dtsg=NAfzX6M8BkQ51T92E4tYI8L8KR3-ADsqsTa2QafU7bDemhKN896gT0w%3A17855905060073950%3A1785084411&jazoest=25831&lsd=tBGz0iqJiIOV4XEWSKFuHP&__spin_r=1048159918&__spin_b=trunk&__spin_t=1790109937&__crn=comet.igweb.PolarisProfilePostsTabRoute&qpl_active_flow_ids=767108973&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisStoriesV3ReelPageStandaloneQuery&server_timestamps=true&variables={encoded_variables}&doc_id=29184890191114309&fb_api_analytics_tags=%5B%22qpl_active_flow_ids%3D767108973%22%5D'

    # return f'av=0&__d=www&__user=0&__a=1&__req=u&__hs=20371.HYP%3Ainstagram_web_pkg.2.1...0&dpr=1&__ccg=GOOD&__rev=1028249517&__s=ywybjm%3Aq4co81%3Adplvd8&__hsi=7559456450740095677&__dyn=7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJw5ux609vCwjE1EE2Cw8G11wBz81s8hwGxu786a3a1YwBgao6C0Mo2swtUd8-U2zxe2GewGw9a361qw8Xxm16wa-0raazo7u3C2u2J0bS1LwTwKG0WE8oC1Iwqo5p0OwUQp1yU426V89F8uwm8jwhUaE4e1tyVrx60gm5oswFwtF85i5E&__csr=geIAaiFliZllsBav4trBuTJ-KJ5WhnQyAnxeEWpBCC-hJADG9AgG4qpQ8zat5BypWy9eaRgBaJ2Xx2p6WgymmGDzQjJo8JJ4iKi8xObCjx50FzLF4-8DiwxDyGqoydV-ESQ9DLAB_GdDzFEsyUSeG8xmF9oymWyqyVFF84q5ooHohwuE5a0CU01kUUb81CE12E5V08m0WFA0ei80n2bLwjp42TOw2J-0rq04tUKp06PwEhy1u1ig4Dgy9wdW0D8n80rl0UxGtw53hEx2E1yPUy7U1J9Q0JFvc0cXwpyG4B6B2US01IAw2Bo0K215w0YEwj8&__hsdp=gaQbh9gple4i4WuA2XCG7RVt5m8DxGU4K32awCF0GBcq1AyH40uWxe3AwboK5-0FE8UbkkU4-4o11XwQCyE9UswZweC4U6iq6UOewJyEhwBwjQ2259o1oE1E85u0km5Unw7Pwaau1CwMwkEeU1v82ew2rA0LoW0W8aO0Ewc6&__hblp=0nE20wpGx6vxy2i1ryE9Gg6q1hwkE9WwkocUso4O2vDyof98K7o4-48hDwyLBx61HwkGg8VoGqawDxCGBwQxG6S0I8jwywXBCxKczEqxaax62m1FDxim1nw4axq0oC362m0iu7ohBxu11wEwfm0AE421xDwhEvwxzEvG2-3K0nO0zE1MUK0DA1DwgEizEW0Qp-2Awa8nxyi1fwRBwFwau68bE&__comet_req=7&lsd=AdGtgRvhyjc&jazoest=21085&__spin_r=1028249517&__spin_b=trunk&__spin_t=1760073111&__crn=comet.igweb.PolarisLoggedOutDesktopPostRouteNext&fb_api_caller_class=RelayModern&fb_api_req_friendly_name=PolarisPostRootQuery&server_timestamps=true&variables={encoded_variables}&doc_id=24368985919464652'


def scrape_instagram_reel(user_id: str):
    """Main function to scrape Instagram reel data with error handling"""
    try:
        payload = create_payload(user_id)
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
