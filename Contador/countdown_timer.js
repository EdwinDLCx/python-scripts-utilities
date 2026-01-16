/*=========================================================================== 
Proyecto: COUNTDOWN TIMER PARA APEX
Archivo: countdown_timer.js
Autor: Edwin De León
GitHub: https://github.com/EdwinDLCx
Fecha de creación: 2025-10-21
Descripción:
    Contador regresivo para eventos en APEX.
Notas:
    - Asegurarse de que las fechas y horas estén en el formato correcto.
===============================================================================
*/

var apexCountdown = apexCountdown || {};

apexCountdown.iniciar = function(config) {
    const diaObjetivo = config.dia;
    const mesObjetivo = config.mes;
    const anioObjetivo = config.anio;
    const horaObjetivo = config.hora;
    const minutoObjetivo = config.minuto;
    const segundoObjetivo = config.segundo;

    let refreshEjecutado = false;
    let intervalId = null;

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

    document.getElementById('apex-countdown').textContent =
        "Tiempo restante: 00:00:00";
    document.getElementById('apex-countdown').classList.add('apex-countdown-iniciado');

    console.log("⏳ Tiempo completado. Refrescando página...");

    setTimeout(() => {
        location.reload();
    }, 1000);
}


    function actualizarCountdown() {
        if (refreshEjecutado) return;

        const ahora = new Date();
        const evento = new Date(anioObjetivo, mesObjetivo - 1, diaObjetivo, horaObjetivo, minutoObjetivo, segundoObjetivo);

        const diff = evento - ahora;
        const totalSegundos = Math.floor(diff / 1000);

        if (totalSegundos <= 0) {
            ejecutarRefresh();
            return;
        }

        // Formato HH:MM:SS
        const horasTotales = Math.floor(totalSegundos / 3600);
        const minutos = Math.floor((totalSegundos % 3600) / 60);
        const segundos = totalSegundos % 60;

        const countdownText = `${pad(horasTotales)}:${pad(minutos)}:${pad(segundos)}`;

        // ✔ Tu texto favorito intacto
        document.getElementById('apex-countdown').textContent =
            `Tiempo restante: ${countdownText}`;
    }

    // Inicio del contador
    const ahora = new Date();
    const evento = new Date(anioObjetivo, mesObjetivo - 1, diaObjetivo, horaObjetivo, minutoObjetivo, segundoObjetivo);

    if (ahora < evento) {
        actualizarCountdown();
        intervalId = setInterval(actualizarCountdown, 1000);
    }

    // Limpieza por si hay submit manual de APEX
    apex.jQuery(window).on('apexbeforepagesubmit', function() {
        if (intervalId) {
            clearInterval(intervalId);
            intervalId = null;
        }
    });
};
