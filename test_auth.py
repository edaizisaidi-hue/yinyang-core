from yinyang_dialectics.auth import SovereignAuthenticator
import os

def test_auth():
    print("[*] MEMULAKAN PROTOKOL UJIAN PENGESAHAN (EIP-8004)...")
    os.environ["OMEGA_MASTER_KEY"] = "TSA_ED_SECURE_KEY"
    auth_engine = SovereignAuthenticator()

    res_initiate = auth_engine.authenticate_request()
    assert res_initiate['tier']['name'] == "Initiate Protocol"

    res_omega = auth_engine.authenticate_request(api_key="TSA_ED_SECURE_KEY")
    assert res_omega['tier']['name'] == "Omega Prime (The Architect)"

if __name__ == "__main__":
    test_auth()
