import pandas as pd              # Voor data inlezen en verwerken (DataFrame)
import matplotlib.pyplot as plt  # Voor het maken van grafieken
import numpy as np               # Voor numerieke berekeningen, hier voor trendlijn

# Lees het CSV-bestand in een DataFrame
df = pd.read_csv('werkloosheid_wereld.csv')

# Zet de kolom 'TIME' om naar numeriek (jaar), en zet ongeldige waarden om in NaN
df['TIME'] = pd.to_numeric(df['TIME'], errors='coerce')

# Landen die we willen analyseren: Nederland, België, Duitsland (ISO-landcodes)
landen = ['NLD', 'BEL', 'DEU']

# Focus op totale groep (niet specifiek mannen/vrouwen)
groep = 'TOT'

# Maak een nieuw figuur aan met een bepaalde grootte (breedte x hoogte in inches)
plt.figure(figsize=(10,6))

# Loop door elk land in de lijst
for land in landen:
    # Filter de DataFrame op het huidige land, de totale groep, juiste meeteenheid, jaarlijkse frequentie en vanaf 2010
    df_land = df[
        (df['LOCATION'] == land) &
        (df['SUBJECT'] == groep) &
        (df['MEASURE'] == 'PC_LF') &     # percentage van de beroepsbevolking
        (df['FREQUENCY'] == 'A') &      # jaarlijkse data (Annual)
        (df['TIME'] >= 2010)            # vanaf jaar 2010
    ]
    
    # Sorteer de data op jaar (oplopend)
    df_land = df_land.sort_values(by='TIME')
    
    # Plot de werkloosheidspercentages per jaar voor dit land (zachte lijn)
    plt.plot(df_land['TIME'], df_land['Value'], label=f'{land} werkloosheid')
    
    # Bereken de trendlijn met lineaire regressie (polyfit met graad 1)
    x = df_land['TIME']
    y = df_land['Value']
    coeffs = np.polyfit(x, y, deg=1)  # coeffs bevat [helling, intercept]
    trendline = np.poly1d(coeffs)      # functie die bij elk x een y-waarde berekent
    
    # Plot de trendlijn als een gestippelde lijn
    plt.plot(x, trendline(x), linestyle='--', label=f'{land} trend')

# Geef de grafiek een titel
plt.title('Werkloosheidstrend Nederland, België en Duitsland (2010-nu)')

# Label de x-as en y-as
plt.xlabel('Jaar')
plt.ylabel('Werkloosheidspercentage')

# Toon een legenda om te zien welke lijn bij welk land hoort
plt.legend()

# Voeg een raster toe voor betere leesbaarheid
plt.grid(True)

# Laat de grafiek zien
plt.show()
