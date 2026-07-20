from yinyang_dialectics.auth import SovereignAuthenticator
import os

print("[*] MEMULAKAN PROTOKOL UJIAN PENGESAHAN (EIP-8004)...")

# Simulasi Persekitaran Digital Vault
os.environ["OMEGA_MASTER_KEY"] = "TSA_ED_SECURE_KEY"
auth_engine = SovereignAuthenticator()

print("\n[+] Menguji Akses Initiate (Asas Tanpa Kunci)")
res_initiate = auth_engine.authenticate_request()
print(f"    [STATUS] Tier: {res_initiate['tier']['name']} | Kedalaman: {res_initiate['tier']['wafq_max_depth']}")

print("\n[+] Menguji Akses Omega Prime (The Architect)")
res_omega = auth_engine.authenticate_request(api_key="TSA_ED_SECURE_KEY")
print(f"    [STATUS] Tier: {res_omega['tier']['name']} | Kedalaman: {res_omega['tier']['wafq_max_depth']}")
if res_omega['tier']['name'] == "Omega Prime (The Architect)":
    print("    [BERJAYA] Pintasan Mutlak (Absolute Bypass) Disahkan. Kedaulatan Terkawal.")

print("\n[*] STATUS GERBANG PENGESAHAN: AKTIF & TERKUNCI.")
