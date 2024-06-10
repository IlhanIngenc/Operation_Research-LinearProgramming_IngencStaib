import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog


# Funktion zur Lösung des Optimierungsproblems der Möbelfabrik
def lp_möbelfabrik():
    # Zielfunktion: Negative Werte, da die Funktion linprog standardmäßig minimiert
    c_lp = [-25, -15]  # -25€ pro Tisch und -15€ pro Stuhl (Deckungsbeitrag)

    # Nebenbedingungen: Ressourcenverbrauch pro Tisch und Stuhl, dargestellt als ein 2D-Array
    A_lp = [[5, 3],  # Holzverbrauch: 5 Kg pro Tisch, 3 Kg pro Stuhl
            [5, 2],  # Arbeitsstunden: 5 Stunden pro Tisch, 2 Stunden pro Stuhl
            [3, 2]]  # Maschinenstunden: 3 Stunden pro Tisch, 2 Stunden pro Stuhl

    # Verfügbare Ressourcen, dargestellt als ein 1D-Array
    b_lp = [600, 450, 300]  # Maximale Kapazitäten: 600 Kg Holz, 450 Arbeitsstunden, 300 Maschinenstunden

    # Produktionsmengen können nicht negativ sein - Nicht-Negativitäts-Bedingung
    bounds_lp = [(0, None), (0, None)]

    # Lösung des linearen Optimierungsproblems mit der Simplex-Methode
    res_lp = linprog(c_lp, A_ub=A_lp, b_ub=b_lp, bounds=bounds_lp, method='simplex')

    # Rückgabe der optimalen Produktionsmengen und des maximalen Gewinns
    return res_lp.x, res_lp.fun


# Ausführen der Funktion und Speichern der Ergebnisse
lp_ergebnisse, lp_gewinn = lp_möbelfabrik()


# Funktion zur Visualisierung der Lösung
def visualize_lp_solution(ergebnisse, gewinn):
    # Berechnung der maximalen Anzahl von Tischen und Stühlen für die Darstellung
    tische_max = int(600 / 5) + 10  # Obergrenze für die Anzahl der Tische
    stuehle_max = int(600 / 3) + 10  # Obergrenze für die Anzahl der Stühle

    # Wertebereich für die Anzahl der Tische
    tische = np.linspace(0, tische_max, 500)

    # Berechnung der maximal möglichen Anzahl von Stühlen basierend auf den Ressourcen
    stuehle1 = (600 - 5 * tische) / 3  # Basierend auf Holzressourcen
    stuehle2 = (450 - 5 * tische) / 2  # Basierend auf Arbeitsstunden
    stuehle3 = (300 - 3 * tische) / 2  # Basierend auf Maschinenstunden

    # Darstellung der Zielfunktion für den maximalen Gewinn
    gewinn_linie = (gewinn - 25 * tische) / 15  # Umformung der Zielfunktion: Gewinn = 25*T + 15*S

    # Erstellen des Plots
    plt.figure(figsize=(10, 8))
    plt.plot(tische, stuehle1, label='Holzressourcen (5T + 3S ≤ 600)')
    plt.plot(tische, stuehle2, label='Arbeitsstunden (5T + 2S ≤ 450)')
    plt.plot(tische, stuehle3, label='Maschinenstunden (3T + 2S ≤ 300)')
    plt.plot(tische, gewinn_linie, 'm--', label=f'Zielfunktion für Gewinn = {gewinn} Euro')

    # Darstellung der zulässigen Lösungsmenge
    plt.fill_between(tische, 0, np.minimum(np.minimum(stuehle1, stuehle2), stuehle3), color='gray', alpha=0.5)
    plt.plot(ergebnisse[0], ergebnisse[1], 'ro', markersize=10, label='Optimale Lösung')

    # Hilfslinien zur Verdeutlichung der optimalen Lösung
    plt.plot([ergebnisse[0], ergebnisse[0]], [0, ergebnisse[1]], 'r--')
    plt.plot([0, ergebnisse[0]], [ergebnisse[1], ergebnisse[1]], 'r--')

    # Achsenbegrenzungen und Beschriftungen
    plt.xlim(0, tische_max)
    plt.ylim(0, stuehle_max)
    plt.xlabel('Anzahl der Tische')
    plt.ylabel('Anzahl der Stühle')
    plt.legend()
    plt.title('Visualisierung der LP-Lösung für die Möbelfabrik')
    plt.grid(False)
    plt.show()


# Visualisieren der optimalen Lösung
visualize_lp_solution(lp_ergebnisse, -lp_gewinn)

# Konsolenausgabe der berechneten Werte aus der linearen Optimierung
print('[Console] Das optimale Ergebnis liegt bei: ' + str(lp_ergebnisse))
print('[Console] Mit einem potenziellen Gewinn in Höhe von ' + str(-lp_gewinn) + '€ !')


# Keine halben Stühle/Tische, daher -> Überprüfung der Machbarkeit des Aufrundens
# Ergebnisse werden aus dem Array('lp_ergebnisse') geholt.
anzahl_tische = lp_ergebnisse[0]
anzahl_stuehle = np.ceil(lp_ergebnisse[1])  # Aufrunden auf die nächste ganze Zahl

# Überprüfung der Ressourcennutzung
holznutzung = 5 * anzahl_tische + 3 * anzahl_stuehle
arbeitsnutzung = 5 * anzahl_tische + 2 * anzahl_stuehle
maschinennutzung = 3 * anzahl_tische + 2 * anzahl_stuehle

# Abfrage - Werden die Ressourcenbeschränkungen überschritten, wenn man aufrundet?
# Wenn Ja -> Setze neues, optimales Ergebnis
if holznutzung <= 600 and arbeitsnutzung <= 450 and maschinennutzung <= 300:
    print(f"[Console] Aufgerundete Ergebnisse: Tische = {anzahl_tische}, Stühle = {anzahl_stuehle}")
    print("[Console] Ressourcennutzung ist innerhalb der Grenzen.")
else:
# Wenn Nein -> Behalte das vorherige Ergebnis
    print("[Console] Aufrunden nicht möglich, da es die Ressourcenbeschränkungen überschreiten würde.")
