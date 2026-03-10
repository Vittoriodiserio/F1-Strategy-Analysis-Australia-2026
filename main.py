import fastf1
from fastf1 import plotting
import matplotlib.pyplot as plt
import numpy as np
import os

# --- 1. CONFIGURAZIONE SISTEMA ---
if not os.path.exists('cache'): os.makedirs('cache')
fastf1.Cache.enable_cache('cache')
plotting.setup_mpl()

# Caricamento sessione globale
session = fastf1.get_session(2026, 'Australia', 'R')
session.load()

laps_lec = session.laps.pick_driver('LEC')
laps_rus = session.laps.pick_driver('RUS')

# --- 2. ANALISI STRATEGICA (GRAFICO 1) ---
def plot_strategic_analysis():
    laps_lec['TimeCumulative'] = laps_lec['LapTime'].dt.total_seconds().cumsum()
    laps_rus['TimeCumulative'] = laps_rus['LapTime'].dt.total_seconds().cumsum()
    
    delta = laps_lec.set_index('LapNumber')['TimeCumulative'] - laps_rus.set_index('LapNumber')['TimeCumulative']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(delta.index, delta, color='red', label='Leclerc vs Russell (Delta)')
    ax.axvline(x=11, color='blue', linestyle='--', label='VSC (Ritiro Hadjar)')
    ax.axvline(x=25, color='black', linestyle=':', label='Pit Stop Leclerc')
    ax.set_title("Analisi Strategica Australia 2026: L'impatto della VSC")
    ax.set_xlabel('Giro')
    ax.set_ylabel('Distacco (secondi)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

# --- 3. ANALISI DEGRADO (GRAFICO 2) ---
def plot_tyre_degradation():
    # Pulizia dati per isolare il degrado puro
    stint1_lec = laps_lec.loc[(laps_lec['LapNumber'] > 1) & (laps_lec['LapNumber'] < 25)]
    stint1_lec = stint1_lec.loc[stint1_lec['LapTime'].dt.total_seconds() < 100]
    
    stint2_rus = laps_rus.loc[(laps_rus['LapNumber'] > 11) & (laps_rus['LapNumber'] < 25)]
    stint2_rus = stint2_rus.loc[stint2_rus['LapTime'].dt.total_seconds() < 100]

    lec_times = stint1_lec['LapTime'].dt.total_seconds()
    rus_times = stint2_rus['LapTime'].dt.total_seconds()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(stint1_lec['LapNumber'], lec_times, color='#EF1A2D', label='Leclerc (Medium Usate)', s=40)
    ax.scatter(stint2_rus['LapNumber'], rus_times, color='#00A19C', label='Russell (Hard Nuove)', s=40)

    # Regressioni lineari
    z_lec = np.polyfit(stint1_lec['LapNumber'], lec_times, 1)
    p_lec = np.poly1d(z_lec)
    ax.plot(stint1_lec['LapNumber'], p_lec(stint1_lec['LapNumber']), color='#EF1A2D', linestyle='--')

    z_rus = np.polyfit(stint2_rus['LapNumber'], rus_times, 1)
    p_rus = np.poly1d(z_rus)
    ax.plot(stint2_rus['LapNumber'], p_rus(stint2_rus['LapNumber']), color='#00A19C', linestyle='--')

    ax.set_title('Analisi Degradamento Pneumatici (Filtered): Australia 2026')
    ax.set_xlabel('Giro')
    ax.set_ylabel('Tempo sul Giro (s)')
    ax.legend()
    plt.show()
    
    # Output numerici per il report [cite: 37, 42, 45]
    print(f"Degrado Leclerc: {z_lec[0]:.4f} s/giro")
    print(f"Degrado Russell: {z_rus[0]:.4f} s/giro")
    print(f"Pace Delta Medio: {lec_times.mean() - rus_times.mean():.3f}s")

# --- 4. SIMULAZIONE VITTORIA (GRAFICO 3) ---
def plot_victory_simulation():
    pace_delta_medio = 0.601 # [cite: 45]
    vsc_gain_time = 10.7    # [cite: 25]
    
    rus_cum_time = laps_rus['LapTime'].dt.total_seconds().cumsum().values
    sim_lec_times = []

    for i, row in laps_lec.iterrows():
        lap = row['LapNumber']
        real_time = row['LapTime'].total_seconds()
        
        if lap < 11:
            sim_lec_times.append(real_time)
        elif lap == 11:
            sim_lec_times.append(real_time - vsc_gain_time)
        elif 11 < lap <= 25:
            # Recupero performance con Hard nuove al passo di Russell
            sim_lec_times.append(laps_rus.loc[laps_rus['LapNumber'] == lap, 'LapTime'].dt.total_seconds().iloc[0])
        else:
            sim_lec_times.append(real_time)

    sim_lec_cum_time = np.cumsum(sim_lec_times)
    diff = rus_cum_time - sim_lec_cum_time

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(laps_lec['LapNumber'], diff, color='gold', linewidth=3, label='Leclerc Simulato (VSC Pit)')
    ax.axhline(0, color='blue', linestyle='--', alpha=0.5, label='Russell (P1 Reale)')
    ax.fill_between(laps_lec['LapNumber'], diff, 0, where=(diff > 0), color='gold', alpha=0.1)
    ax.set_title('CAPITOLO 5: SIMULAZIONE VITTORIA VIRTUALE')
    ax.set_xlabel('Giro')
    ax.set_ylabel('Vantaggio su Russell (secondi)')
    ax.legend()
    plt.show()
    print(f"Margine di Vittoria Simulato: {diff[-1]:.2f} secondi") # [cite: 55]

# --- ESECUZIONE ---
if __name__ == "__main__":
    plot_strategic_analysis()
    plot_tyre_degradation()
    plot_victory_simulation()