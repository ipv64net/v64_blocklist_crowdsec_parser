import re,json,requests
import subprocess

# Get it From IPv64.net Website
v64_api_token="dein-api-key"
# Blocker Node ID
v64_blocker_node_id="dein-blocker-id"
# ipv64.net Api Endpoint
v64_url = "https://ipv64.net/api.php"

# Führe den Befehl 'pfctl -t tabelle -T show' aus und lies die Ausgabe ein
try:
    pfctl_output = subprocess.check_output(["pfctl", "-t", "crowdsec_blacklists", "-T", "show"], universal_newlines=True)
except subprocess.CalledProcessError as e:
    print("Fehler beim Ausführen des Befehls 'pfctl -t crowdsec_blacklists -T show':", e)
    pfctl_output = ""

# Regular expression pattern for matching IPv4 addresses
ipv4_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

# Find all IPv4 addresses in the input string
ipv4_addresses = re.findall(ipv4_pattern, pfctl_output)

# Filter out duplicate IPv4 addresses (if any)
unique_ipv4_addresses = list(set(ipv4_addresses))

# Erstelle separate Listen von JSON-Objekten für IPv4
ipv4_json_objects = [{"ip": ipv4_address} for ipv4_address in unique_ipv4_addresses]

ip_list = ipv4_json_objects 

ip_list = {"ip_list": ip_list}

ip_list = json.dumps(ip_list, indent=2)

# Drucke den JSON-String
#print(ip_list)

payload = {'blocker_id': v64_blocker_node_id,
    'report_ip_list': ip_list
}
headers = {
  'Authorization': f"Bearer {v64_api_token}"
}
response = requests.request("POST", v64_url, headers=headers, data=payload)
print(response.text)
