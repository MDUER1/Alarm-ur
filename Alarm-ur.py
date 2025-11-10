# Marcus D. Duer
"""Dette er en simpel alarm, som vækker dig efter den tid  som du har sat den til"""

from datetime import datetime
import time
import winsound
import msvcrt  # giver adgang til tastetryk uden Enter

# variabler
nu = datetime.now()
angiv_sluttid = input("Angiv tidsafstanden til alarmen går af (HH:MM): ")

# Konverter tekst til tidspunkt (strp: string Parse)
aktuel_sluttid = datetime.strptime(angiv_sluttid, "%H:%M")

# Erstat dato til nuværende dato
aktuel_sluttid = aktuel_sluttid.replace(
    year=nu.year, month=nu.month, day=nu.day)

# Angiv tid til bruger
print(f"Du har nu sat sluttidspunktet til {aktuel_sluttid}")

# Kør alarmen - betingelse != er ikke gyldig, da tiden er for præcis med mikrosekunder
while datetime.now() < aktuel_sluttid:
    time.sleep(1)  # tjek tid -> pause 1 sekund -> repeat

# Loop hopper først videre her efter betingelsen ikke opfyldes
print("⏰Tiden er gået!⏰")

# afspil biplyd, indtil bruger stopper den

while True:
    winsound.Beep(1000, 100)
    time.sleep(0.1)

    if msvcrt.kbhit():  # tjekker om der er trykket en tast
        key = msvcrt.getwch()
        if key.lower() == "x":
            print("Du har stoppet alarmen nu.")
            break
        else:
            continue  # ignorer de andre taster
