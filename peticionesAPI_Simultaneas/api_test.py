"""
===========================================================================
Test de Carga Asíncrono para API de Aspirantes
===========================================================================

Autor: Edwin De León
GitHub: https://github.com/EdwinDLCx
Descripción: 
    Este script permite realizar pruebas de carga sobre un endpoint REST 
    de registro de aspirantes, midiendo tiempos de respuesta, éxito/fallo 
    de las solicitudes y generando un reporte en CSV.

Características principales:
    1. Carga de payloads desde un archivo JSON.
    2. Generación de payloads dinámicos con diferentes modos:
       - uuid: agrega identificador único y timestamp.
       - cycle: envía payloads tal cual.
       - collision: simula colisiones en un campo específico.
    3. Envío asíncrono de solicitudes usando aiohttp.
    4. Dashboard en tiempo real de progreso, éxito/errores y latencias.
    5. Reporte final en CSV con detalle de cada request.

Instrucciones de uso:
    python mass_test.py
    - Espera START_IN_SECONDS antes de disparar las solicitudes.
    - Al finalizar, genera results_mass_test.csv con los resultados.
===========================================================================

Desarrollo realizado íntegramente por Edwin De León.
Consulta mi GitHub para más proyectos: https://github.com/EdwinDLCx
===========================================================================
"""
import asyncio
import aiohttp
import json
import time
import uuid
import csv
import sys
from typing import List, Dict, Any

API_URL = "https://tulinkaqui/test"
TIMEOUT = 30
PAYLOAD_FILE = "sample_payloads.json"
CSV_OUTPUT = "results_mass_test.csv"
MODE = "uuid"  # "uuid" | "cycle" | "collision:NumeroAFILIADO"
START_IN_SECONDS = 3.0  # Espera antes de disparar todas las requests

def load_payloads(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("El archivo JSON debe ser un arreglo de objetos.")
    return data

def build_payload(base: Dict[str, Any], mode: str, idx: int) -> Dict[str, Any]:
    p = dict(base)
    if mode == "uuid":
        p["_test_uuid"] = str(uuid.uuid4())
        p["_index"] = idx
        p["_ts"] = time.time()
    elif mode.startswith("collision:"):
        p["_index"] = idx
    elif mode == "cycle":
        pass
    else:
        raise ValueError("Modo desconocido")
    return p

async def send_one(session: aiohttp.ClientSession, payload: Dict[str, Any],
                   start_time: float, idx: int, results: List[Dict[str, Any]], stats: Dict[str, Any]):
    wait = start_time - time.time()
    if wait > 0:
        await asyncio.sleep(wait)

    t0 = time.perf_counter()
    try:
        async with session.post(API_URL, json=payload, timeout=TIMEOUT) as resp:
            text = await resp.text()
            latency = (time.perf_counter() - t0) * 1000
            results.append({
                "index": idx,
                "payload_afiliado": payload.get("afiliado"),
                "payload_correo": payload.get("correo"),
                "status": resp.status,
                "latency_ms": round(latency, 2),
                "error": None,
                "response": text
            })
            stats["sent"] += 1
            stats["latencies"].append(latency)
            if 200 <= resp.status < 300:
                stats["success"] += 1
            else:
                stats["errors"] += 1
    except Exception as e:
        latency = (time.perf_counter() - t0) * 1000
        results.append({
            "index": idx,
            "payload_afiliado": payload.get("afiliado"),
            "payload_correo": payload.get("correo"),
            "status": None,
            "latency_ms": round(latency, 2),
            "error": repr(e),
            "response": None
        })
        stats["sent"] += 1
        stats["errors"] += 1

async def dashboard(stats: Dict[str, Any], total_requests: int):
    while stats["sent"] < total_requests:
        latencies = stats["latencies"]
        min_lat = round(min(latencies), 2) if latencies else 0
        max_lat = round(max(latencies), 2) if latencies else 0
        avg_lat = round(sum(latencies) / len(latencies), 2) if latencies else 0
        sys.stdout.write(
            f"\rSent: {stats['sent']}/{total_requests} | Success: {stats['success']} | Errors: {stats['errors']} | Latency ms (min/avg/max): {min_lat}/{avg_lat}/{max_lat}"
        )
        sys.stdout.flush()
        await asyncio.sleep(0.3)
    print()

async def main():
    payloads = load_payloads(PAYLOAD_FILE)
    TOTAL_REQUESTS = len(payloads)  # Ajustar automáticamente al tamaño del JSON
    results: List[Dict[str, Any]] = []
    stats = {"sent": 0, "success": 0, "errors": 0, "latencies": []}

    connector = aiohttp.TCPConnector(limit=0, ssl=False)
    timeout_obj = aiohttp.ClientTimeout(total=None, sock_connect=TIMEOUT, sock_read=TIMEOUT)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout_obj) as session:
        tasks = []
        start_time = time.time() + START_IN_SECONDS
        print(f"Preparado. Lanzamiento en {START_IN_SECONDS} segundos (timestamp {start_time:.3f})")

        for i, base in enumerate(payloads):
            payload = build_payload(base, MODE, i)
            tasks.append(asyncio.create_task(send_one(session, payload, start_time, i, results, stats)))

        dash_task = asyncio.create_task(dashboard(stats, TOTAL_REQUESTS))
        await asyncio.gather(*tasks)
        await dash_task

    # Guardar CSV al final
    keys = ["index", "payload_afiliado", "payload_correo", "status", "latency_ms", "error", "response"]
    with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in results:
            writer.writerow({k: r.get(k) for k in keys})

    print(f"CSV guardado en: {CSV_OUTPUT}")

if __name__ == "__main__":
    asyncio.run(main())
