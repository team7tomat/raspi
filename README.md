# raspi

## Pin-konfiguration
Alla Raspberry PI:s har GPIO-pinnar för olika slags inputs och outputs. Vi använder model 3B+, som har inbyggt wifi.
Bilden under detaljerar GPIO-pinnarna: nummer (1-40) samt namn.

<img src="https://i.imgur.com/eZlqshD.png">

## Kamera
Installation:
På Raspberry:n finns det en lång port mellan ljud- och hdmi-porten, som kameran ska kopplas in i. 
Kameramodulens connector har en kopparfärgad ända som skall riktas från ethernet-porten.
Lyft försiktigt upp det svarta locket på porten, sätt ned connectorn tills den inte går ned längre, och stäng sedan locket.

## Ljussensor
Installation:
Ljussensorn har 4 hål i kretskortet, med en fastlödd sladd i varje. Det står ett namn för varje sladd på kretskortet.
Sensorns outputs kopplas in i såhär:

| Kretskorts-namn | Pin-namn | Pin-nummer |
| --- | --- | --- |
| VCC | 3V3 power | 1 |
| GND | GROUND | 6 |
| SCL | GPIO3 (SCL) | 4 |
| SDA | GPIO2 (SDA) | 3 |
| ADDR | Kopplas ej i | Ingen pin |

## Armatur
Installation:
På armaturen finns det sex stycken kopplingar. De fyra översta kontrollerar ljusstyrkan för de fyra färgerna. De två understa är ström (jord + 5V).
Sladdarna mellan armaturen och Raspberry PI:n kopplas in så här, uppifrån och ned:

| Armatur-namn | Pin-namn | Pin-nummer |
| --- | --- | --- |
| Far Red | GPIO12 (PWM0) | 32 |
| Hyper Red | GPIO13 (PWM1) | 33 |
| White | GPIO16 | 36 |
| Deep Blue | GPIO19 (PCM_FS) | 35 |
| GND | Ground | 34 |
| 5V | Tom (kopplas ej i) | Ingen pin |

## Programvara
De filer och scripts om Raspberry PI:n behöver laddas ned automatiskt från detta Github-repository.
Ifall fler Raspberry PI:s ska användas måste filen med namnet **setup** laddas ner och köras.
Filen är ett bash-script som laddar ned projektet, installerar nödvändiga filer samt ändrar så att **Startup**-filen startas automatiskt vid påslagning.
