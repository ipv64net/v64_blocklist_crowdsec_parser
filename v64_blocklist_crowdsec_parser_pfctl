import re,json,requests
import subprocess
import ipaddress

# Get it From IPv64.net Website
v64_api_token="dein-api-key"
# Blocker Node ID
v64_blocker_node_id="deine-blocker-id"
# ipv64.net Api Endpoint
v64_url = "https://ipv64.net/api.php"

# Liste der Tabellennamen
table_names = ["crowdsec_blacklists", "crowdsec6_blacklists"]

# Funktion zur Extraktion und Validierung von IP-Adressen aus pfctl
def extract_ip_addresses(table_name):
    try:
        pfctl_output = subprocess.check_output(["pfctl", "-t", table_name, "-T", "show"], universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen des Befehls 'pfctl -t {table_name} -T show':", e)
        pfctl_output = ""

    ip_addresses = set()
    lines = pfctl_output.splitlines()
    for line in lines:
        try:
            addr = ipaddress.ip_address(line.strip())
            ip_addresses.add(addr)  # Hier verwenden wir das ipaddress-Objekt direkt
        except ValueError:
            pass
    return ip_addresses

# Erstelle leere Sets, um die IP-Adressen ohne Duplikate zu speichern
unique_ipv4_addresses = set()
unique_ipv6_addresses = set()

# Extrahiere und validiere IPv4- und IPv6-Adressen für jede Tabelle und füge sie den entsprechenden Sets hinzu
for table_name in table_names:
    table_ip_addresses = extract_ip_addresses(table_name)
    for ip_address in table_ip_addresses:
        if ip_address.version == 4:
            unique_ipv4_addresses.add(str(ip_address))
        elif ip_address.version == 6:
            unique_ipv6_addresses.add(str(ip_address))

# Kombiniere IPv4- und IPv6-Adressen in einer gemeinsamen Liste von JSON-Objekten
ip_list = [{"ip": ip_address} for ip_address in list(unique_ipv4_addresses) + list(unique_ipv6_addresses)]

# Erstelle ein JSON-Objekt mit der "ip_list"
ip_list_json = {"ip_list": ip_list}

# Konvertiere das JSON-Objekt in eine formatierte Zeichenfolge
ip_list = json.dumps(ip_list_json, indent=2)

#print(ip_list)

payload = {'blocker_id': v64_blocker_node_id,
    'report_ip_list': ip_list
}
headers = {
  'Authorization': f"Bearer {v64_api_token}"
}
response = requests.request("POST", v64_url, headers=headers, data=payload)
print(response.text)
