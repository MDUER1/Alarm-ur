"""Konsolbaseret alarmur.

Programmet beder brugeren om et tidspunkt i formatet ``HH:MM`` og venter,
indtil tidspunktet nås. Når alarmen går i gang, afspilles et bip gentagne
gange, indtil brugeren trykker ``x``.

Bemærk:
- Programmet er designet til Windows, da det bruger ``winsound`` og ``msvcrt``.
"""

from __future__ import annotations

from datetime import datetime, timedelta
import time
import winsound
import msvcrt

# Saml centrale indstillinger som konstanter, så adfærd kan justeres ét sted.
CHECK_INTERVAL_SECONDS = 1.0
BEEP_FREQUENCY_HZ = 1000
BEEP_DURATION_MS = 150
STOP_KEY = "x"  # Brugeren stopper alarmen ved at trykke denne tast.


def parse_alarm_time(raw_value: str, now: datetime) -> datetime:
    """Konvertér brugerinput (HH:MM) til næste gyldige alarmtidspunkt.

    Hvis brugeren vælger et tidspunkt tidligere end nu, planlægges alarmen
    automatisk til næste dag.
    """
    candidate_time = datetime.strptime(raw_value.strip(), "%H:%M")
    alarm_time = candidate_time.replace(year=now.year, month=now.month, day=now.day)

    # Hvis tidspunktet allerede er passeret i dag, flyttes alarmen til i morgen.
    if alarm_time <= now:
        alarm_time += timedelta(days=1)

    return alarm_time


def ask_for_alarm_time() -> datetime:
    """Indhent tidspunkt fra brugeren med validering af inputformat."""
    while True:
        raw_value = input("Angiv tidspunkt for alarm (HH:MM): ")
        now = datetime.now()

        try:
            return parse_alarm_time(raw_value, now)
        except ValueError:
            # Giv tydelig fejlmeddelelse og prøv igen i stedet for at crashe.
            print("Ugyldigt format. Brug venligst HH:MM, fx 07:30.")


def wait_until_alarm(alarm_time: datetime) -> None:
    """Vent i loop, indtil alarmtidspunktet er nået."""
    while datetime.now() < alarm_time:
        time.sleep(CHECK_INTERVAL_SECONDS)


def play_alarm_until_stopped() -> None:
    """Afspil biplyde kontinuerligt, indtil brugeren trykker stop-tasten."""
    print(f"⏰ Alarmen ringer! Tryk '{STOP_KEY}' for at stoppe. ⏰")

    while True:
        winsound.Beep(BEEP_FREQUENCY_HZ, BEEP_DURATION_MS)

        # msvcrt.kbhit() gør det muligt at læse tastetryk uden Enter.
        if msvcrt.kbhit() and msvcrt.getwch().lower() == STOP_KEY:
            print("Alarmen er stoppet.")
            break


def main() -> None:
    """Entrypoint for alarmprogrammet."""
    alarm_time = ask_for_alarm_time()

    print(f"Alarm sat til: {alarm_time:%Y-%m-%d %H:%M}")
    wait_until_alarm(alarm_time)
    play_alarm_until_stopped()


if __name__ == "__main__":
    main()
