import base64
import json
import os
import requests
import getpass
import urllib.parse
from datetime import datetime

# Thanks to https://github.com/duckwc/ECAMpy for the code to token convertion

SDK_BUILD = 16650

API_KEY = "3_e5qn7USZK-QtsIso1wCelqUKAK_IVEsYshRIssQ-X-k55haiZXmKWDHDRul2e5Y2"
CLIENT_ID = "1S8q1WJEs-emOB43Z0-66WnL"
CLIENT_SECRET = "lmnceiD0B-4KPNN5ZS6WuWU70j9V5BCuSlz2OPsvHkyLryhMkJkPvKsivfTq3RfNYj8GpCELtOBvhaDIzKcBtg"
AUTHORIZATION_HEADER = (
    "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
)
APP_ID = "DeLonghiComfort2-mw-id"
APP_SECRET = "DeLonghiComfort2-Yg4miiqiNcf0Or-EhJwRh7ACfBY"

BROWSER_USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/79.0.3945.73 Mobile/15E148 Safari/604.1"
TOKEN_USER_AGENT = "DeLonghiComfort/3 CFNetwork/1568.300.101 Darwin/24.2.0"
API_USER_AGENT = "DeLonghiComfort/5.1.1 (iPhone; iOS 18.2; Scale/3.00)"

REFRESH_TOKEN_FILE = "refresh_token.txt"

LANGUAGES = {
    "en": "GB",
    "pt": "PT",
    "en-ca": "CA",
    "fr-ca": "CA",
    "es-mx": "MX",
    "es-co": "CO",
    "es-pe": "PE",
    "en-us": "US",
    "pt-br": "BR",
    "es-cl": "CL",
    "en-za": "ZA",
    "es": "ES",
    "fr": "FR",
    "lu": "LU",
    "nl": "NL",
    "my": "MY",
    "fr-be": "BE",
    "nl-inf": "BE",
    "de": "DE",
    "fr-ch": "CH",
    "de-inf": "CH",
    "it": "IT",
    "mt-mt": "MT",
    "en-mt": "MT",
    "hr": "HR",
    "sr": "RS",
    "sl": "SI",
    "br": "BG",
    "el": "GR",
    "ro": "RO",
    "tr": "TR",
    "cs": "CZ",
    "sk": "SK",
    "hu": "HU",
    "de-at": "AT",
    "uk": "UA",
    "sv": "SE",
    "fi": "FI",
    "no": "NO",
    "da": "DK",
    "pl": "PL",
    "et-ee": "EE",
    "lt-lt": "LT",
    "lv-lv": "LV",
    "en-ae": "AE",
    "ar-ae": "AE",
    "en-sg": "SG",
    "en-my": "MY",
    "en-au": "AU",
    "en-nz": "NZ",
    "ja": "JP",
    "ko": "KR",
    "en-kh": "KH",
    "en-hk": "HK",
    "en-bd": "BD",
    "en-th": "TH",
    "th": "TH",
    "es-ar": "AR",
    "ar-eg": "EG",
    "en-eg": "EG",
    "en-in": "IN",
    "en-ir": "IR",
    "fa": "IR",
    "en-il": "IL",
    "en-sa": "SA",
    "ar-sa": "SA",
    "en-ie": "IE",
    "en-id": "ID",
    "en-ph": "PH",
    "zh-tw": "TW",
    "en-om": "OM",
    "en-qa": "QA",
    "en-bh": "BH",
    "en-kw": "KW",
    "vi": "VN",
}

LANGUAGE_COMMS_KEYS = {
    "CA": "profiledCommunicationCA",
    "MX": "profiledCommunicationMXCO",
    "CO": "profiledCommunicationMXCO",
    "US": "profiledCommunicationUS",
    "BR": "profiledCommunicationBR",
    "CL": "profiledCommunicationCL",
    "AR": "profiledCommunicationCL",
    "PE": "profiledCommunicationCL",
    "ZA": "profiledCommunicationZA",
    "PT": "profiledCommunicationPT",
    "ES": "profiledCommunicationES",
    "GB": "profiledCommunicationGB",
    "IE": "profiledCommunicationGB",
    "FR": "profiledCommunicationFR",
    "NL": "profiledCommunicationNL",
    "BE": "profiledCommunicationBE",
    "LU": "profiledCommunicationBE",
    "DE": "profiledCommunicationDE",
    "CH": "profiledCommunicationCH",
    "IT": "profiledCommunicationIT",
    "MT": "profiledCommunicationHRRSSIBG",
    "HR": "profiledCommunicationHRRSSIBG",
    "RS": "profiledCommunicationHRRSSIBG",
    "SI": "profiledCommunicationHRRSSIBG",
    "BG": "profiledCommunicationHRRSSIBG",
    "GR": "profiledCommunicationGR",
    "RO": "profiledCommunicationRO",
    "TR": "profiledCommunicationTR",
    "CZ": "profiledCommunicationCZSKHU",
    "SK": "profiledCommunicationCZSKHU",
    "HU": "profiledCommunicationCZSKHU",
    "AT": "profiledCommunicationAT",
    "UA": "profiledCommunicationUA",
    "SE": "profiledCommunicationSEFINODK",
    "FI": "profiledCommunicationSEFINODK",
    "NO": "profiledCommunicationSEFINODK",
    "DK": "profiledCommunicationSEFINODK",
    "PL": "profiledCommunicationPLEELTLV",
    "EE": "profiledCommunicationPLEELTLV",
    "LT": "profiledCommunicationPLEELTLV",
    "LV": "profiledCommunicationPLEELTLV",
    "AE": "profiledCommunicationAE",
    "EG": "profiledCommunicationAE",
    "IN": "profiledCommunicationAE",
    "IR": "profiledCommunicationAE",
    "IL": "profiledCommunicationAE",
    "SA": "profiledCommunicationAE",
    "OM": "profiledCommunicationAE",
    "QA": "profiledCommunicationAE",
    "BH": "profiledCommunicationAE",
    "KW": "profiledCommunicationAE",
    "SG": "profiledCommunicationSG",
    "MY": "profiledCommunicationMY",
    "AU": "profiledCommunicationAU",
    "NZ": "profiledCommunicationNZ",
    "JP": "profiledCommunicationJP",
    "KR": "profiledCommunicationKR",
    "KH": "profiledCommunicationHKBDKHTH",
    "HK": "profiledCommunicationHKBDKHTH",
    "BD": "profiledCommunicationHKBDKHTH",
    "TH": "profiledCommunicationHKBDKHTH",
    "ID": "profiledCommunicationHKBDKHTH",
    "PH": "profiledCommunicationHKBDKHTH",
    "TW": "profiledCommunicationHKBDKHTH",
    "VN": "profiledCommunicationHKBDKHTH",
}

LANGUAGE_COUNTRIES = {
    "en": "United Kingdom",
    "pt": "Portugal",
    "en-ca": "Canada",
    "fr-ca": "Canada",
    "es-mx": "Mexico",
    "es-co": "Colombia",
    "es-pe": "Peru",
    "en-us": "United States",
    "pt-br": "Brazil",
    "es-cl": "Chile",
    "en-za": "South Africa",
    "es": "Spain",
    "fr": "France",
    "lu": "Luxembourg",
    "nl": "Netherlands",
    "my": "Malaysia",
    "fr-be": "Belgium",
    "nl-inf": "Belgium",
    "de": "Germany",
    "fr-ch": "Switzerland",
    "de-inf": "Switzerland",
    "it": "Italy",
    "mt-mt": "Malta",
    "en-mt": "Malta",
    "hr": "Croatia",
    "sr": "Serbia",
    "sl": "Slovenia",
    "br": "Bulgaria",
    "el": "Greece",
    "ro": "Romania",
    "tr": "Turkey",
    "cs": "Czechia",
    "sk": "Slovakia",
    "hu": "Hungary",
    "de-at": "Austria",
    "uk": "Ukraine",
    "sv": "Sweden",
    "fi": "Finland",
    "no": "Norway",
    "da": "Denmark",
    "pl": "Poland",
    "et-ee": "Estonia",
    "lt-lt": "Lithuania",
    "lv-lv": "Latvia",
    "en-ae": "United Arab Emirates",
    "ar-ae": "United Arab Emirates",
    "en-sg": "Singapore",
    "en-my": "Malaysia",
    "en-au": "Australia",
    "en-nz": "New Zealand",
    "ja": "Japan",
    "ko": "South Korea",
    "en-kh": "Cambodia",
    "en-hk": "Hong Kong",
    "en-bd": "Bangladesh",
    "en-th": "Thailand",
    "th": "Thailand",
    "es-ar": "Argentina",
    "ar-eg": "Egypt",
    "en-eg": "Egypt",
    "en-in": "India",
    "en-ir": "Iran",
    "fa": "Iran",
    "en-il": "Israel",
    "en-sa": "Saudi Arabia",
    "ar-sa": "Saudi Arabia",
    "en-ie": "Ireland",
    "en-id": "Indonesia",
    "en-ph": "Philippines",
    "zh-tw": "Taiwan",
    "en-om": "Oman",
    "en-qa": "Qatar",
    "en-bh": "Bahrain",
    "en-kw": "Kuwait",
    "vi": "Vietnam",
}


def get_query_param(url, param):
    query = urllib.parse.urlparse(url).query
    params = urllib.parse.parse_qs(query)
    return params.get(param, [None])[0]


def url_encode(value):
    return urllib.parse.quote(value)


def get_refresh_token():
    if os.path.exists(REFRESH_TOKEN_FILE):
        with open(REFRESH_TOKEN_FILE, "r") as file:
            return file.read().strip()
    return None


def save_refresh_token(refresh_token):
    with open(REFRESH_TOKEN_FILE, "w") as file:
        file.write(refresh_token)


def input_boolean(prompt):
    value = input(f"{prompt} [Y]es/no: ").strip().lower()

    if value in ["yes", "y"]:
        return True
    elif value in ["no", "n"]:
        return False
    else:
        print(f"Invalid input '{value}'. Please enter one of [yes, y, no, n].")
        exit(1)


def get_new_refresh_token():
    has_account = input_boolean("Do you have a De'Longhi account")
    print("")
    print("Please enter your De'Longhi account credentials.")
    language = None
    while True:
        print(f"Choose one of the following languages : {', '.join(LANGUAGES.keys())}")
        language = input("Language: ").strip()
        if language in LANGUAGES.keys():
            print(f"You selected: {LANGUAGES[language]}")
            break
        else:
            print(f"Invalid choice '{language}'. Please try again.")
    email = input("Email: ").strip()
    password = getpass.getpass(prompt="Password: ", stream=None)

    if not has_account:
        new_account(language, email, password)

    try:
        # Step 1: Start authentication process
        response = requests.get(
            f"https://fidm.eu1.gigya.com/oidc/op/v1.0/{API_KEY}/authorize",
            headers={"User-Agent": BROWSER_USER_AGENT},
            params={
                "client_id": CLIENT_ID,
                "response_type": "code",
                "redirect_uri": "https://google.it",
                "scope": "openid email profile UID comfort en alexa",
                "nonce": str(int(datetime.now().timestamp())),
            },
            allow_redirects=False,
        )
        context = get_query_param(response.headers["Location"], "context")

        # Step 2: Fetch Gigya session data
        response = requests.get(
            f"https://socialize.eu1.gigya.com/socialize.getIDs",
            headers={"User-Agent": BROWSER_USER_AGENT},
            params={
                "APIKey": API_KEY,
                "includeTicket": True,
                "pageURL": "https://aylaopenid.delonghigroup.com/",
                "sdk": "js_latest",
                "sdkBuild": SDK_BUILD,
                "format": "json",
            },
        ).json()

        ucid = response["ucid"]
        gmid = response["gmid"]
        gmid_ticket = response["gmidTicket"]

        # Step 3: Login
        risk_context_json = json.dumps(
            {
                "b0": 4494,
                "b1": [0, 2, 2, 0],
                "b2": 2,
                "b3": [],
                "b4": 2,
                "b5": 1,
                "b6": BROWSER_USER_AGENT,
                "b7": [
                    {
                        "name": "PDF Viewer",
                        "filename": "internal-pdf-viewer",
                        "length": 2,
                    },
                    {
                        "name": "Chrome PDF Viewer",
                        "filename": "internal-pdf-viewer",
                        "length": 2,
                    },
                    {
                        "name": "Chromium PDF Viewer",
                        "filename": "internal-pdf-viewer",
                        "length": 2,
                    },
                    {
                        "name": "Microsoft Edge PDF Viewer",
                        "filename": "internal-pdf-viewer",
                        "length": 2,
                    },
                    {
                        "name": "WebKit built-in PDF",
                        "filename": "internal-pdf-viewer",
                        "length": 2,
                    },
                ],
                "b8": datetime.now().strftime("%H:%M:%S"),
                "b9": 0,
                "b10": {"state": "denied"},
                "b11": False,
                "b13": [5, "440|956|24", False, True],
            }
        )

        response = requests.post(
            "https://accounts.eu1.gigya.com/accounts.login",
            headers={"User-Agent": BROWSER_USER_AGENT},
            data={
                "loginID": email,
                "password": password,
                "sessionExpiration": 7884009,
                "targetEnv": "jssdk",
                "include": "profile,data,emails,subscriptions,preferences",
                "includeUserInfo": True,
                "loginMode": "standard",
                "lang": language,
                "riskContext": url_encode(risk_context_json),
                "APIKey": API_KEY,
                "source": "showScreenSet",
                "sdk": "js_latest",
                "authMode": "cookie",
                "pageURL": "https://aylaopenid.delonghigroup.com/",
                "gmid": gmid,
                "ucid": ucid,
                "sdkBuild": SDK_BUILD,
                "format": "json",
            },
        ).json()

        login_token = response["sessionInfo"]["login_token"]

        # Step 4: Get user info
        response = requests.post(
            "https://socialize.eu1.gigya.com/socialize.getUserInfo",
            headers={"User-Agent": BROWSER_USER_AGENT},
            data={
                "enabledProviders": "*",
                "APIKey": API_KEY,
                "sdk": "js_latest",
                "login_token": login_token,
                "authMode": "cookie",
                "pageURL": "https://aylaopenid.delonghigroup.com/",
                "gmid": gmid,
                "ucid": ucid,
                "sdkBuild": SDK_BUILD,
                "format": "json",
            },
        ).json()

        user_uid = response["UID"]
        user_uid_signature = response["UIDSignature"]
        user_signature_timestamp = response["signatureTimestamp"]

        # Step 5: Consent
        response = requests.get(
            f"https://aylaopenid.delonghigroup.com/OIDCConsentPage.php",
            headers={"User-Agent": BROWSER_USER_AGENT},
            params={
                "lang": language,
                "context": context,
                "clientID": CLIENT_ID,
                "scope": "openid+email+profile+UID+comfort+en+alexa",
                "UID": user_uid,
                "UIDSignature": user_uid_signature,
                "signatureTimestamp": user_signature_timestamp,
            },
        ).text

        signature = response.split("const consentObj2Sig = '")[1].split("';")[0]

        # Step 6: Authorization
        response = requests.get(
            f"https://fidm.eu1.gigya.com/oidc/op/v1.0/{API_KEY}/authorize/continue",
            headers={"User-Agent": BROWSER_USER_AGENT},
            params={
                "context": context,
                "login_token": login_token,
                "consent": json.dumps(
                    {
                        "scope": "openid email profile UID comfort en alexa",
                        "clientID": CLIENT_ID,
                        "context": context,
                        "UID": user_uid,
                        "consent": True,
                    },
                    separators=(",", ":"),
                ),
                "sig": signature,
                "gmidTicket": gmid_ticket,
            },
            allow_redirects=False,
        )
        code = get_query_param(response.headers["Location"], "code")

        # Step 7: Get IDP access token
        response = requests.post(
            f"https://fidm.eu1.gigya.com/oidc/op/v1.0/{API_KEY}/token",
            headers={
                "User-Agent": TOKEN_USER_AGENT,
                "Authorization": AUTHORIZATION_HEADER,
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": "https://google.it",
            },
        ).json()

        idp_token = response["access_token"]

        # Step 8: Exchange IDP token for Ayla token
        response = requests.post(
            "https://user-field-eu.aylanetworks.com/api/v1/token_sign_in",
            headers={"User-Agent": TOKEN_USER_AGENT},
            data={
                "app_id": APP_ID,
                "app_secret": APP_SECRET,
                "token": idp_token,
            },
        ).json()

        refresh_token = response["refresh_token"]
        save_refresh_token(refresh_token)

        return response["access_token"]

    except Exception as e:
        print(f"Failed retrieving refresh token with response: {response}")
        exit(1)


def get_access_token():
    refresh_token = get_refresh_token()
    if not refresh_token:
        # If no refresh token is available, perform login and token acquisition
        return get_new_refresh_token()

    # Attempt to use the refresh token to get a new access token
    try:
        response = requests.post(
            "https://user-field-eu.aylanetworks.com/users/refresh_token.json",
            headers={
                "User-Agent": TOKEN_USER_AGENT,
                "Content-Type": "application/json",
            },
            json={"user": {"refresh_token": refresh_token}},
        )

        if response.status_code == 200:
            data = response.json()
            new_access_token = data["access_token"]
            new_refresh_token = data.get("refresh_token")

            # Save the new refresh token if provided
            if new_refresh_token:
                save_refresh_token(new_refresh_token)

            return new_access_token
        else:
            print(f"Failed retrieving new access token with response: {response}")
            print("Falling back to login...")
            return get_new_refresh_token()

    except Exception as e:
        print(f"Failed retrieving new access token with response: {response}")
        print("Falling back to login...")
        return get_new_refresh_token()


def new_account(language, email, password):
    response = requests.get(
        f"https://socialize.eu1.gigya.com/socialize.getIDs",
        headers={"User-Agent": BROWSER_USER_AGENT},
        params={
            "APIKey": API_KEY,
            "includeTicket": True,
            "pageURL": "https://aylaopenid.delonghigroup.com/",
            "sdk": "js_latest",
            "sdkBuild": SDK_BUILD,
            "format": "json",
        },
    ).json()

    ucid = response["ucid"]
    gmid = response["gmid"]

    response = requests.post(
        "https://accounts.eu1.gigya.com/accounts.initRegistration",
        headers={
            "User-Agent": TOKEN_USER_AGENT,
            "Apikey": API_KEY,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "apikey": API_KEY,
            "format": "json",
            "gmid": gmid,
            "ucid": ucid,
            "httpStatusCodes": False,
            "nonce": str(int(datetime.now().timestamp())),
            "sdk": "ios_swift_1.5.8",
            "targetEnv": "mobile",
        },
    ).json()

    response = requests.post(
        "https://accounts.eu1.gigya.com/accounts.register",
        headers={
            "User-Agent": TOKEN_USER_AGENT,
            "Apikey": API_KEY,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "apikey": API_KEY,
            "format": "json",
            "gmid": gmid,
            "ucid": ucid,
            "httpStatusCodes": False,
            "nonce": str(int(datetime.now().timestamp())),
            "finalizeRegistration": True,
            "lang": language,
            "sdk": "ios_swift_1.5.8",
            "targetEnv": "mobile",
            "regToken": response["regToken"],
            "data": json.dumps(
                {"origin": "ARIA-DRY-APP", "brands": {"delonghi": True}},
                separators=(",", ":"),
            ),
            "email": email,
            "password": password,
            "preferences": json.dumps(
                {LANGUAGE_COMMS_KEYS[LANGUAGES[language]]: {"isConsentGranted": False}},
                separators=(",", ":"),
            ),
            "profile": json.dumps(
                {
                    "email": email,
                    "locale": language,
                    "country": LANGUAGE_COUNTRIES[language],
                },
                separators=(",", ":"),
            ),
        },
    ).json()

    if response["statusCode"] == 206:
        print("Account created successfully.")
        print("")
    else:
        print("Account creation failed with response: ", response)
        exit(1)


# API Docs: https://docs.aylanetworks.com/reference


def get_request(path, access_token):
    url = f"https://ads-eu.aylanetworks.com/{path}"
    headers = {
        "User-Agent": API_USER_AGENT,
        "Authorization": f"auth_token {access_token}",
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers)
    return response.json()


def post_request(path, body, access_token):
    url = f"https://ads-eu.aylanetworks.com/{path}"
    headers = {
        "User-Agent": API_USER_AGENT,
        "Authorization": f"auth_token {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()


def main():
    access_token = get_access_token()
    devices = get_request("apiv1/devices.json", access_token=access_token)
    print("Devices: ", devices)

    # dsn = devices[0]["device"]["dsn"]
    # device_id = devices[0]["device"]["key"]

    # print(f"DSN: {dsn}")
    # print(f"Device ID: {device_id}")

    # device = get_request(f"apiv1/devices/{device_id}.json", access_token=access_token)
    # device = get_request(f"apiv1/dsns/{dsn}.json", access_token=access_token)
    # print("Device: ", device)
    # properties = get_request(f"apiv1/devices/{device_id}/properties.json", access_token=access_token)
    # properties = get_request(f"apiv1/dsns/{dsn}/properties.json", access_token=access_token)
    # print("Properties: ", properties)

    # device_data = get_request(f"apiv1/dsns/{dsn}/data.json", access_token=access_token)
    # print("Device data: ", device_data)

    # humidity = get_request(f"apiv1/dsns/{dsn}/properties/humidity_setpoint/datapoints.json", access_token=access_token)
    # print("Humidity: ", humidity)

    # room_temp = get_request(
    #     f"apiv1/dsns/{dsn}/properties/room_temp/datapoints.json",
    #     access_token=access_token,
    # )
    # print("Value: ", room_temp)

    # Status
    # 1 ON
    # 2 OFF
    # post_request(
    #     f"apiv1/dsns/{dsn}/properties/set_status/datapoints.json",
    #     {"datapoint": {"value": 2}},
    #     access_token=access_token,
    # )

    # Humidity
    # [0, 100] % (percentage)
    # post_request(
    #   f"apiv1/dsns/{dsn}/properties/humidity_setpoint/datapoints.json",
    #   {"datapoint":{"value": 60}},
    #   access_token=access_token
    # )

    # Mode
    # 1 Dehuimidify
    # 2 Dry Clothes
    # 3 Air purifier
    # post_request(
    #   f"apiv1/dsns/{dsn}/properties/device_mode/datapoints.json",
    #   {"datapoint":{"value": 1}},
    #   access_token=access_token
    # )

    # Activate Real Feel Mode
    # post_request(
    #   f"apiv1/dsns/{dsn}/properties/activate_realfeel/datapoints.json",
    #   {"datapoint":{"value": "AQIDChIXHEY8Mig="}},
    #   access_token=access_token
    # )

    # Swing
    # 0 Off
    # 1 On
    # post_request(
    #   f"apiv1/dsns/{dsn}/properties/set_eco/datapoints.json",
    #   {"datapoint":{"value": 1}},
    #   access_token=access_token
    # )

    # Eco
    # 0 Off
    # 1 On
    # post_request(
    #   f"apiv1/dsns/{dsn}/properties/set_eco/datapoints.json",
    #   {"datapoint":{"value": 1}},
    #   access_token=access_token
    # )


# This block ensures that the main function runs only when the script is executed directly
if __name__ == "__main__":
    main()
