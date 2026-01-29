/*=========================================================================== 
Proyecto: COUNTDOWN TIMER PARA APEX
Archivo: countdown_timer.js
Autor: Edwin De León
GitHub: https://github.com/EdwinDLCx/python-scripts-utilities/tree/master/Contador
Fecha de creación: 2025-10-21
Descripción:
    Contador regresivo para eventos en APEX.
Notas:
    - Asegurarse de que las fechas y horas estén en el formato correcto.
===============================================================================
*/

var apexCountdown = apexCountdown || {};

apexCountdown.iniciar = function (config) {
  const diaObjetivo = config.dia;
  const mesObjetivo = config.mes;
  const anioObjetivo = config.anio;
  const horaObjetivo = config.hora;
  const minutoObjetivo = config.minuto;
  const segundoObjetivo = config.segundo;
  const horaserverObjetivo = config.horaserver;

  console.log(horaserverObjetivo);
  let refreshEjecutado = false;
  let intervalId = null;
  let serverNow = null; // ⬅️ Hora del servidor

  function pad(n) {
    return n < 10 ? "0" + n : n;
  }

  function ejecutarRefresh() {
    if (refreshEjecutado) return;

    refreshEjecutado = true;

    // Evitar múltiples refresh globales
    if (window.__countdown_refresh_block) return;
    window.__countdown_refresh_block = true;

    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }

    document.getElementById("apex-countdown").textContent =
      "Tiempo restante: 00:00:00";
    document
      .getElementById("apex-countdown")
      .classList.add("apex-countdown-iniciado");

    console.log("⏳ Tiempo completado. Refrescando página...");

    setTimeout(() => {
      location.reload();
    }, 1000);
  }

  function actualizarCountdown() {
    if (refreshEjecutado || !serverNow) return;

    // ⏱️ Avanzar el reloj del servidor localmente (1 segundo)
    serverNow = new Date(serverNow.getTime() + 1000);

    const evento = new Date(
      anioObjetivo,
      mesObjetivo - 1,
      diaObjetivo,
      horaObjetivo,
      minutoObjetivo,
      segundoObjetivo,
    );

    const diff = evento - serverNow;
    const totalSegundos = Math.floor(diff / 1000);

    if (totalSegundos <= 0) {
      ejecutarRefresh();
      return;
    }

    const horasTotales = Math.floor(totalSegundos / 3600);
    const minutos = Math.floor((totalSegundos % 3600) / 60);
    const segundos = totalSegundos % 60;

    const countdownText = `${pad(horasTotales)}:${pad(minutos)}:${pad(segundos)}`;

    document.getElementById("apex-countdown").textContent =
      `El registro inicia en: ${countdownText}`;
  }

apex.server.process(
  "GET_SERVER_TIME",
  {},
  {
    dataType: "text", // 👈 CLAVE
    success: function (pData) {
      serverNow = new Date(pData.trim());
      console.log("Hora servidor:", serverNow);

      const evento = new Date(
        anioObjetivo,
        mesObjetivo - 1,
        diaObjetivo,
        horaObjetivo,
        minutoObjetivo,
        segundoObjetivo
      );

      if (serverNow < evento) {
        actualizarCountdown();

        if (!intervalId) {
          intervalId = setInterval(actualizarCountdown, 1000);
        }
      }
    },
    error: function (e) {
      console.error("GET_SERVER_TIME falló:", e);
    }
  }
);


  // Limpieza si APEX hace submit
  apex.jQuery(window).on("apexbeforepagesubmit", function () {
    if (intervalId) {
      clearInterval(intervalId);
      intervalId = null;
    }
  });
};
