#!/usr/bin/env python3
import threading, time, random, json, requests

DASHBOARD_URL = "http://localhost:5008"  # Dashboard
API_BASE = "http://localhost:5007/api"   # Sua API (opcional)

RFIDS = [
    "ECAAAAAAAAAAAAAAAAAAAAAAMOTTU20293",
    "EC04ABC10000",
    "string",
    "E200001161072C05",
    "A1B2C3D4E5F6G7H8"
]

BASE_POS = [
    (-23.561414, -46.655881),
    (-23.562000, -46.656500),
    (-23.560800, -46.656200)
]

def now_ms():
    return int(time.time() * 1000)

def post_dashboard(payload):
    try:
        requests.post(f"{DASHBOARD_URL}/new_reading", json=payload, timeout=2)
    except:
        pass

class Device(threading.Thread):
    def __init__(self, moto_id, rfid, base_pos, interval=3, max_reads=None):
        super().__init__(daemon=True)
        self.moto_id = moto_id
        self.rfid = rfid
        self.base_pos = base_pos
        self.interval = interval
        self.max_reads = max_reads
        self.count = 0
        self.running = True

    def rand_gps(self):
        lat = self.base_pos[0] + random.uniform(-0.0006, 0.0006)
        lon = self.base_pos[1] + random.uniform(-0.0006, 0.0006)
        return {"latitude": round(lat,6), "longitude": round(lon,6)}

    def rand_mov(self):
        moving = random.random() < 0.4
        intensity = random.randint(1,10) if moving else 0
        return {"moving": moving, "intensity": intensity}

    def send(self, sensor, value):
        payload = {
            "motoId": self.moto_id,
            "sensor": sensor,
            "value": value,
            "timestamp": now_ms(),
            "ok": True
        }
        post_dashboard(payload)

    def run_cycle(self):
        self.send("rfid", {"rfid": self.rfid})
        time.sleep(0.2)
        self.send("gps", self.rand_gps())
        time.sleep(0.2)
        self.send("movimento", self.rand_mov())

    def run(self):
        while self.running:
            self.run_cycle()
            self.count += 1
            if self.max_reads and self.count >= self.max_reads:
                break
            time.sleep(self.interval)

# Inicializa múltiplos devices
devices = []
for i, rfid in enumerate(RFIDS[:3]):  # Ajuste a quantidade de devices
    dev = Device(moto_id=f"MOTO{i+1}", rfid=rfid, base_pos=BASE_POS[i])
    dev.start()
    devices.append(dev)

# Mantém o script rodando
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Parando devices...")
    for d in devices:
        d.running = False
