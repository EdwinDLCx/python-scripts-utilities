DECLARE
    v_html   CLOB;
    v_dia    NUMBER;
    v_mes    NUMBER;
    v_anio   NUMBER;
    v_hora   NUMBER;
    v_minuto NUMBER;
    v_segundo NUMBER;
BEGIN
    -- Obtener datos
    SELECT 
        EXTRACT(DAY FROM ASA_FECINI),
        EXTRACT(MONTH FROM ASA_FECINI),
        EXTRACT(YEAR FROM ASA_FECINI),
        EXTRACT(HOUR FROM CAST(ASA_FECINI AS TIMESTAMP)),
        EXTRACT(MINUTE FROM CAST(ASA_FECINI AS TIMESTAMP)),
        ROUND(EXTRACT(SECOND FROM CAST(ASA_FECINI AS TIMESTAMP)))
    INTO 
        v_dia, v_mes, v_anio, v_hora, v_minuto, v_segundo
    FROM ASATIPEVE_VW
    WHERE ASA_TIPO = :P20_TIPO_COUNTER;

   /* v_html := q'[
    <div id="apex-countdown-container">
        <h1>El evento inicia el:</h1>
        <div id="apex-fechaEvento">]';

    v_html := v_html || LPAD(v_dia,2,'0')||'/'||LPAD(v_mes,2,'0')||'/'||v_anio;

    v_html := v_html || q'[
        </div>
        <h1>A las:</h1>
        <div id="apex-horaEvento">]';

    v_html := v_html || 
        LPAD(v_hora,2,'0')||':'||LPAD(v_minuto,2,'0')||':'||LPAD(v_segundo,2,'0');

    v_html := v_html || q'[
        </div>
        <div id="apex-countdown">Calculando...</div>
    </div>

    <script>
    setTimeout(function(){
        if (typeof apexCountdown !== "undefined" && apexCountdown.iniciar) {
            apexCountdown.iniciar({
    ]';

    v_html := v_html ||
        'dia:'||v_dia||','||
        'mes:'||v_mes||','||
        'anio:'||v_anio||','||
        'hora:'||v_hora||','||
        'minuto:'||v_minuto||','||
        'segundo:'||v_segundo;

    v_html := v_html || q'[
            });
        } else {
            console.error("apexCountdown no se ha cargado.");
        }
    }, 300);
    </script>
    ]';*/


v_html := q'[
    <div id="apex-countdown-container">
        <h1>El evento inicia en:</h1>
        <div id="apex-fechaEvento"></div>

        <div id="apex-horaEvento"></div>

        <div id="apex-countdown">Calculando...</div>
    </div>

    <script>
    setTimeout(function(){
        if (typeof apexCountdown !== "undefined" && apexCountdown.iniciar) {
            apexCountdown.iniciar({
]';

v_html := v_html ||
    'dia:'||v_dia||','||
    'mes:'||v_mes||','||
    'anio:'||v_anio||','||
    'hora:'||v_hora||','||
    'minuto:'||v_minuto||','||
    'segundo:'||v_segundo;

v_html := v_html || q'[
            });
        } else {
            console.error("apexCountdown no se ha cargado.");
        }
    }, 300);
    </script>
]';


    RETURN v_html;

EXCEPTION 
    WHEN NO_DATA_FOUND THEN
        RETURN '<div>No se encontró el evento.</div>';
END;
