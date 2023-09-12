import re,json,requests
import subprocess

# Get it From IPv64.net Website
v64_api_token="kcnY9WJRVvmz7qZwhrb3BPF5sSOy2Ddj"
# Blocker Node ID
v64_blocker_node_id="Xrzhjy78I4QwTZKEcWRAMmpVedN3nvqt"
# ipv64.net Api Endpoint
v64_url = "https://ipv64.net/api.php"

# Fuehre den Befehl 'ipset list' aus und lies die Ausgabe ein
try:
    ipset_output = subprocess.check_output(["ipset", "list"], universal_newlines=True)
except subprocess.CalledProcessError as e:
    print("Fehler beim Aussdfghren des Befehls 'ipset list':", e)
    ipset_output = ""

# Regular expression pattern for matching IPv4 and IPv6 addresses
#ip_pattern = r'\b(?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|(?:[0-9A-Fa-f]{1,4}:){7}[0-9A-Fa-f]{1,4})\b'
ipv4_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
ipv6_pattern = r'((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*))'
#ipv6_pattern = r'\b([a-f0-9:]+:+)+[a-f0-9]+\b'

# Find all IPv4 addresses in the input string
ipv4_addresses = re.findall(ipv4_pattern, ipset_output)
# Find all IPv6 addresses in the input string
ipv6_addresses = re.findall(ipv6_pattern, ipset_output)

# Filter out duplicate IPv4 and IPv6 addresses (if any)
unique_ipv4_addresses = list(set(ipv4_addresses))
unique_ipv6_addresses = list(set(ipv6_addresses))

# Erstelle separate Listen von JSON-Objekten für IPv4 und IPv6
ipv4_json_objects = [{"ip": ipv4_address} for ipv4_address in unique_ipv4_addresses]
ipv6_json_objects = [{"ip": ipv6_address} for ipv6_address in unique_ipv6_addresses]

ip_list = ipv4_json_objects + ipv6_json_objects

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
