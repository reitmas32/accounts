from http import HTTPStatus

import requests

from core.settings import log

url = "http://127.0.0.1:7899/v1/users/"

token = """
    eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX21vdGhlcl9pZCI6IjZiMWFlMGYzLTc5YmUtNDY0OS05MzBhLTI4ZmEwZGE1ZTdjMiIsImV4cCI6MTcxMTkwNDI4OX0.schQ2WFCXNA-qm3sXkOj09tQHrJA3H9tcOOo-5LWhbWgg2kVR2RE_wUv55H5IPFrmkbWweSwtQ3IJ1buCkEL5KhVmn_LvpzW0rNqCft8y0qIcVxQBaSaQHxvKpy36GgbRtdcK6HhvqqRoj5VdNUTVTlVeTh-Qh2hLpymBNGFkqOGKtmM6stopo1X-CYxs7dLVqscE7e4ZbtnIloWGfLgXZbk1THpmFjlnLZhyHqQX7BFDC0nDEE4_d06WpEc18gqiEmN6ZWxgIyQw4Utq5cHi2vKol5mh1ZpxNRTSAKVqtTMC7pYbR-6E3SmPdGVb6ufnN97OUNk-sxkm82zA-1ahw
    """  # noqa: S105

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers, timeout=10)

if response.status_code == HTTPStatus.OK:
    data = response.json()
    log.info("Datos del usuario:", data)
else:
    log.error(f"Error: {response.status_code}", response.text)

