import time
from unittest.mock import patch

import mainTool
from rate_limit import rate_minute


# Test della funzione rate_minute
def test_rate_minute_below_limit():
    mainTool.start_time = time.time() - 30  # Imposta il tempo in modo che sia trascorso meno di un minuto
    mainTool.requests_count = 800  # Numero di richieste inferiori al limite

    rate_minute()

    assert mainTool.requests_count == 800  # Verifica che il conteggio delle richieste e il tempo di inizio non siano stati modificati
    assert mainTool.start_time == mainTool.start_time


def test_rate_minute_above_limit():
    mainTool.start_time = time.time() - 30  # Imposta il tempo in modo che sia trascorso meno di un minuto
    mainTool.requests_count = 950  # Numero di richieste superiore al limite

    with patch('time.sleep') as mock_sleep:
        rate_minute()

    # Verifica che il conteggio delle richieste e il tempo di inizio siano stati resettati dopo il superamento del limite
    assert mainTool.requests_count == 0
    assert mainTool.start_time == time.time()
    mock_sleep.assert_called()  # Verifica che la funzione time.sleep è stata chiamata 


def test_rate_minute_reset():
    mainTool.start_time = time.time() - 85  # Imposta il tempo in modo che sia trascorso più di un minuto
    mainTool.requests_count = 800  # Numero di richieste inferiori al limite
    print(f"Pre-Reset: {mainTool.requests_count} e {mainTool.start_time}")

    rate_minute()

    assert mainTool.requests_count == 0  # Verifica che il conteggio delle richieste e il tempo di inizio siano stati modificati
    assert mainTool.start_time == mainTool.start_time
    print(f"Post-Reset: {mainTool.requests_count} e {mainTool.start_time}")
