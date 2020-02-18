f = open("saljivo.txt", "r")
data = []
totals = {}
counts = {}
for line in f.readlines():
    i = line.index('[')
    predictions = list(map( lambda x: float(x.split(':')[1][:-1]), line[i+1:-2].split(',')))
    actual = line.split()[1]
    if not actual in totals:
        totals[actual] = predictions
    else:
        totals[actual] = [sum(pair) for pair in zip(totals[actual], predictions)]
    if not actual in counts:
        counts[actual] = 0
    else:
        counts[actual] += 1
format_string = "{:20}|{:10}|{:12}|{:16}|{:16}|{:16}|{:16}|{:15}|{:12}|{:13}|{:14}|{:14}|{:15}"
print(format_string.format('POZA', 'BEZ_POZE', 'DIGNUTA_RUKA', 'ISPRUZENA_RUKA_1', 'ISPRUZENA_RUKA_2', 'ISPRUZENA_RUKA_3',
               'ISPRUZENA_RUKA_4', 'POVECAJ_BRZINU', 'PRIDJI_BLIZE', 'SMANJI_BRZINU', 'STAJACA_POZA_1',
               'STAJACA_POZA_2', 'ZAUSTAVI_VOZILO'))
for key, value in totals.items():
    print(format_string.format(key, *[round(x / counts[key], 7) for x in value]))