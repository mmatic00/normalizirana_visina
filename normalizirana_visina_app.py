import numpy as np
import streamlit as st

# Parametri modela
H_min = 182.88
gamma = 7
alpha = 8
beta = 4
delta = 0.02  # Manja penalizacija duga
k = 1.2
P_avg = 13.12
P_min = 13  # Negativni doprinos počinje za penis ispod 13 cm
min_height = 150  # Minimalna visina

# Funkcija za penis: s negativnim doprinosom ispod 13 cm, neutralan između 13 i 14, progresivan od 15 pa dalje
def penis_contribution(P):
    if P < P_min:
        # Negativan doprinos za penis manji od 13 cm
        return -2 * (P_min - P)  # Progresivno veći negativan doprinos s manjim penisom
    elif P <= 13:
        return 0  # Nema učinka za penis između 13 cm
    elif P <= 14:
        return 0  # Nema učinka za penis između 13 i 14 cm
    elif P <= 18:
        # Progresivni doprinos za penis od 15 cm do 18 cm
        return (P - 14) * 1.5  # Svaki cm iznad 14 cm daje progresivni doprinos
    else:
        # Za penis veći od 18 cm, doprinos raste dalje
        return (P - 14) * 2  # Svaki cm iznad 18 cm daje još veći doprinos

# Glavna funkcija za izračun normalizirane visine
def normalizirana_visina(H, N, D, P):
    # Logaritamski rast visine, smanjen doprinos za marginalne visine
    if H > H_min:
        height_contribution = gamma * np.log(H - H_min + 1) / 2  # Smanjen doprinos za visine blizu praga
    else:
        height_contribution = 0  # Za visine ispod praga
    
    # Logaritamski rast imovine, s manjim utjecajem za nisku imovinu
    wealth_contribution = alpha * np.log(np.log(N + 1) + 1) if N > 0 else 0
    
    # Doprinos penisa
    penis_contrib = penis_contribution(P)
    
    # Linearna penalizacija duga
    debt_penalty = delta * D
    
    # Izračun normalizirane visine
    NHM = H_min + height_contribution + wealth_contribution + penis_contrib - debt_penalty
    
    # Osiguranje da normalizirana visina ne padne ispod minimalne visine
    NHM = max(NHM, min_height)
    
    return NHM

# Streamlit UI
st.title('Teorija Kompenzacijske Visine')
st.write("Ovaj alat omogućuje izračun Normalizirane Visine Muškarca (NHM) temeljen na visini, imovini, penisu i dugovima.")

# Unos podataka
H = st.number_input("Visina (cm)", min_value=100, max_value=250, value=183)
N = st.number_input("Neto imovina (€)", min_value=0, value=0)
D = st.number_input("Dugovi (€)", min_value=0, value=0)
P = st.number_input("Penis (cm)", min_value=0, value=13)

# Izračun i ispis rezultata
NHM = normalizirana_visina(H, N, D, P)
st.write(f"Normalizirana visina muškarca je: {NHM:.2f} cm")

# Kategorija statusa
if NHM < 182.88:
    st.write("Status: Ispod praga muškosti")
elif NHM < 190:
    st.write("Status: Osnovna prihvatljivost")
elif NHM < 200:
    st.write("Status: Dobar status i pojava")
elif NHM < 215:
    st.write("Status: Visoko dominantno")
else:
    st.write("Status: Elita")




