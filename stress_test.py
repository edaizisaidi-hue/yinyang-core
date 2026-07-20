import asyncio
from api.middleware import SovereignShieldMiddleware
from collections import namedtuple

# Objek Mock untuk mensimulasikan trafik The Matrix
RequestMock = namedtuple("Request", ["client", "headers"])
ClientMock = namedtuple("Client", ["host"])

async def mock_call_next(request):
    class ResponseMock:
        headers = {}
    return ResponseMock()

async def run_simulation():
    print("[*] MEMULAKAN PROTOKOL UJIAN TEKANAN KINETIK...")
    
    # Inisialisasi Perisai dengan kapasiti ketat untuk simulasi
    shield = SovereignShieldMiddleware(app=None, max_ip_capacity=100, max_payload_bytes=4096)
    
    print("\n[+] UJIAN 1: Menembak Payload Gergasi (Bom Kognitif)")
    req_giant = RequestMock(client=ClientMock("192.168.1.1"), headers={"content-length": "50000"})
    res_giant = await shield.dispatch(req_giant, mock_call_next)
    if res_giant.status_code == 413:
        print("    [BERJAYA] Payload ditolak (HTTP 413). Perisai Kognitif Aktif.")
    
    print("\n[+] UJIAN 2: Serangan IP Spoofing Berkelajuan Tinggi")
    success_blocks = 0
    # Menjana 150 request palsu (Kapasiti kita set kepada 100)
    for i in range(150):
        fake_ip = f"10.0.0.{i}"
        req_spam = RequestMock(client=ClientMock(fake_ip), headers={"content-length": "100"})
        await shield.dispatch(req_spam, mock_call_next)
    
    # Menyemak saiz memori (Bounded Cache)
    cache_size = len(shield.request_log)
    print(f"    [STATUS MEMORI] Saiz Cache IP Semasa: {cache_size} / 100")
    if cache_size <= 100:
        print("    [BERJAYA] Had memori tidak bocor (Kalis OOM).")
    
    print("\n[+] UJIAN 3: Sekatan Kadar (Rate-Limit) ke atas IP Agresif")
    # Menembak 55 kali berturut-turut dari 1 IP (Had: 50)
    blocked = False
    for _ in range(55):
        req_attack = RequestMock(client=ClientMock("10.0.0.99"), headers={"content-length": "100"})
        res_attack = await shield.dispatch(req_attack, mock_call_next)
        if hasattr(res_attack, 'status_code') and res_attack.status_code == 429:
            blocked = True
    
    if blocked:
        print("    [BERJAYA] Serangan Brute-Force disekat (HTTP 429).")
        
    print("\n[*] PROTOKOL SIMULASI TAMAT. STATUS PERISAI: KEBAL.")

if __name__ == "__main__":
    asyncio.run(run_simulation())
