"""
Test unitari per il file rate_limit.py
"""

import time
from unittest.mock import patch

import mainTool
from rate_limit import rate_minute


# Test della funzione rate_minute
# start_time < 60 secondi
# requests < 900
def test_rate_minute_below_limit():
    # Imposta il tempo in modo che sia trascorso meno di un minuto
    mainTool.start_time = time.time() - 30
    # Numero di richieste inferiori al limite
    mainTool.requests_count = 800

    rate_minute()

    # Verifica che il conteggio delle richieste e il tempo di inizio non siano stati modificati
    assert mainTool.requests_count == 800
    assert mainTool.start_time == mainTool.start_time

# Test della funzione rate_minute
# start_time < 60 secondi
# requests > 900
def test_rate_minute_above_limit():
    # Imposta il tempo in modo che sia trascorso meno di un minuto
    mainTool.start_time = time.time() - 30
    # Numero di richieste superiore al limite
    mainTool.requests_count = 950

    with patch('time.sleep') as mock_sleep:
        rate_minute()

    # Verifica che il conteggio delle richieste e il tempo di inizio
    # siano stati resettati dopo il superamento del limite
    assert mainTool.requests_count == 0
    assert mainTool.start_time == time.time()
    # Verifica che la funzione time.sleep è stata chiamata
    mock_sleep.assert_called()

# Test della funzione rate_minute
# start_time > 60 secondi
# requests < 900
def test_rate_minute_reset():
    # Imposta il tempo in modo che sia trascorso più di un minuto
    mainTool.start_time = time.time() - 85
    # Numero di richieste inferiori al limite
    mainTool.requests_count = 800
    print(f"Pre-Reset: {mainTool.requests_count} e {mainTool.start_time}")

    rate_minute()

    # Verifica che il conteggio delle richieste e il tempo di inizio siano stati modificati
    assert mainTool.requests_count == 0
    assert mainTool.start_time == mainTool.start_time
    print(f"Post-Reset: {mainTool.requests_count} e {mainTool.start_time}")
