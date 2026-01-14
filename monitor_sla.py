import subprocess
import json
import time
from datetime import datetime

# Configuration
SLA_FILE = "sla.txt"
SLA_TARGET = 99.5
CHECK_INTERVAL = 300  # 5 minutes en secondes (Mettez 5 pour tester rapidement !)

def get_openstack_instances():
    """Récupère la liste des serveurs via la commande MicroStack"""
    try:
        # On utilise la commande CLI formatée en JSON pour être précis
        cmd = "microstack.openstack server list --format json"
        result = subprocess.check_output(cmd, shell=True)
        return json.loads(result)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la connexion à OpenStack: {e}")
        return []

def calculate_availability(servers):
    """Calcule le % de disponibilité"""
    total = len(servers)
    if total == 0:
        return 0.0, 0
    
    active_count = 0
    for server in servers:
        # On vérifie si le statut est ACTIVE
        if server['Status'] == 'ACTIVE':
            active_count += 1
            
    availability = (active_count / total) * 100
    return availability, total

def update_sla_file(availability, total_vms):
    """Écrit le rapport dans le fichier texte"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "RESPECTÉ" if availability >= SLA_TARGET else "VIOLATION"
    
    report_line = (
        f"[{now}] Total VMs: {total_vms} | "
        f"Disponibilité: {availability:.2f}% | "
        f"Objectif: {SLA_TARGET}% -> {status}\n"
    )
    
    print(f"Rapport généré : {report_line.strip()}")
    
    with open(SLA_FILE, "a") as f:
        f.write(report_line)

def main():
    print("Démarrage de la surveillance SLA OpenStack...")
    print(f"Surveillance toutes les {CHECK_INTERVAL} secondes.")
    print("Appuyez sur CTRL+C pour arrêter.\n")

    try:
        while True:
            servers = get_openstack_instances()
            availability, total = calculate_availability(servers)
            update_sla_file(availability, total)
            
            # Attente avant la prochaine vérification
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\nArrêt de la surveillance.")

if __name__ == "__main__":
    main()
