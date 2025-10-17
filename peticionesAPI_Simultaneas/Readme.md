# 🚀 Test de Carga Asíncrono para API de Aspirantes

**Autor:** [Edwin De León](https://github.com/EdwinDLCx)  
**Lenguaje:** Python 3.10+  
**Licencia:** MIT  

---

## 📋 Descripción

Este script realiza **pruebas de carga asíncronas** sobre un endpoint REST de registro de aspirantes.  
Permite medir **tiempos de respuesta**, **tasa de éxito/fallo** y genera un **reporte detallado en CSV** con cada solicitud.  

Ideal para cuando quieres saber si tu API está lista para la guerra... o si se derrumba ante la primera ola de requests 🪖.

---

## ⚙️ Características Principales

✅ **Carga de payloads desde un archivo JSON.**  
✅ **Modos dinámicos de envío:**  
- `uuid` → agrega un identificador único y timestamp a cada request.  
- `cycle` → reenvía los payloads tal cual están.  
- `collision:<campo>` → simula colisiones intencionales (por ejemplo, mismo número de afiliado).  

✅ **Envió asíncrono con [aiohttp](https://docs.aiohttp.org/en/stable/)** para máxima velocidad.  
✅ **Dashboard en tiempo real** mostrando progreso, errores y latencias.  
✅ **Reporte final en CSV** con los resultados individuales de cada request.  

---

## 🧠 Flujo de Trabajo

1. Carga los **payloads base** desde un archivo JSON (`sample_payloads.json`).
2. Construye cada payload según el modo de ejecución.
3. Dispara todas las solicitudes en paralelo con `asyncio`.
4. Muestra estadísticas en vivo en la consola.
5. Exporta los resultados a `results_mass_test.csv`.

---

## 🚀 Uso

### 1️⃣ Instalar dependencias
```bash
pip install aiohttp
