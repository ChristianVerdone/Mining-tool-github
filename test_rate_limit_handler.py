from unittest.mock import patch
import time
from rate_limit_handler import wait_for_rate_limit_reset  

# Test quando il numero di richieste rimanenti è zero
# Esempio -> reset_time: 9:50  > nowTs: 9:00 
# Richieste rimanenti = 0 
# Sleep
def test_wait_for_rate_limit_reset_zero_remaining():
    remaining = 0
    reset_time = int(time.time()) + 3000  # Tempo di reset impostato 50 minuti nel futuro
    
    with patch('time.sleep') as mock_sleep:
        wait_for_rate_limit_reset(remaining, reset_time)

    #assert remaining == 5000
    #assert reset_time == time.time() #reset_time è uguale a tempo corrente 
    #print(f"Rimanenti: {remaining}")
    mock_sleep.assert_called()  # Verifica che la funzione time.sleep è stata chiamata       
    
    

# Test quando il numero di richieste rimanenti è diverso da zero
# Esempio -> reset_time: 9:50  > nowTs: 9:00 
# Richieste rimanenti = 50
# NO sleep
def test_wait_for_rate_limit_reset_non_zero_remaining():
    remaining = 50
    reset_time = int(time.time()) + 3000
    
    with patch('time.sleep') as mock_sleep:
        wait_for_rate_limit_reset(remaining, reset_time)

    assert remaining == 50
    mock_sleep.assert_not_called()  # Verifica che la funzione time.sleep non è stata chiamata   

# Ipotizzando che nowTs un'ora aventi
# Esempio -> reset_time: 8:50  < nowTs: 9:00 
# Richieste rimanenti = 100
# NO sleep
def test_wait_for_rate_limit_reset_negative_time():
    remaining = 100
    reset_time = int(time.time()) - 600  # Tempo di reset impostato 10 minuti nel passato
    
    with patch('time.sleep') as mock_sleep:
        wait_for_rate_limit_reset(remaining, reset_time)

    mock_sleep.assert_not_called()  # Verifica che la funzione time.sleep non è stata chiamata
        

# Esempio -> reset_time: 8:50  < nowTs: 9:00 
# Richieste rimanenti = 0
# No Sleep
def test_wait_for_rate_limit_reset_remaining():
    remaining = 0
    reset_time = int(time.time()) - 600
    
    with patch('time.sleep') as mock_sleep:
        wait_for_rate_limit_reset(remaining, reset_time)

    mock_sleep.assert_not_called()  # Verifica che la funzione time.sleep non è stata chiamata
   