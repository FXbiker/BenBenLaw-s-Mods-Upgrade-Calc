from itertools import combinations, product

'''
MADE BY FXbiker/Affexx
https://github.com/FXbiker/BenBenLaw-s-Mods-Upgrade-Calc
Apache Licence 2.0
''' 

ticks = int(input('ticks: '))
slots = int(input('slots: '))

def fixed(ticks, value):
    return ticks + value

def percentage(ticks, value):
    return ticks * (1-value)

upgrades = {
    'types' : {
        'fixed': {
            'func': fixed,
            'method' : 'compound',
            'upgrades': {
                'fixed_speed_1': -200,
                'fixed_speed_2': -400,
                'fixed_speed_3': -600
            }
        },
        'percentage': {
            'func': percentage,
            'method' : 'additive',
            'upgrades': {
                'percentage_speed_1': 0.2,
                'percentage_speed_2': 0.4,
                'percentage_speed_3': 0.6
            }
        }
    },
    'priority' : ['percentage', 'fixed']
}

def sort_combos(combo):
    combo = [x for x in combo]
    sort_func = lambda y: upgrades['priority'].index(y.split('.')[0])
    combo = sorted(combo, key=sort_func)
    return combo

def combos(d, l, c = []):
  yield tuple(c)
  if len(c) < l:
     yield from [i for b in d for i in combos(d, l, c+[b])]

def perform_calc(combo, debug=False):
    final_tick_value = int(ticks)
    additive_func = None
    prev_additive = False
    additive_value = 0
    for upgrade in combo:
        u_type = upgrade.split('.')
        if upgrades['types'][u_type[0]]['method'] == 'additive':
            additive_value += upgrades['types'][u_type[0]]['upgrades'][u_type[1]]
            prev_additive = True
            additive_func = upgrades['types'][u_type[0]]['func']

        elif upgrades['types'][u_type[0]]['method'] == 'compound':
            if prev_additive:
                final_tick_value = additive_func(final_tick_value, additive_value)
                prev_additive = False
                additive_value = 0
                final_tick_value = upgrades['types'][u_type[0]]['func'](final_tick_value,upgrades['types'][u_type[0]]['upgrades'][u_type[1]])
    if prev_additive:
        final_tick_value = additive_func(final_tick_value, additive_value)
        prev_additive = False
        additive_value = 0

    return final_tick_value

def filter_data(data):
    new = []
    for x in data:
        if not x['ticks'] <= 0:
            new.append(x)
    return new

def sort_data(data):
    sort_function = lambda item : item['ticks']
    new = sorted(data, key=sort_function)
    return new

def separate_data(data):
    sep_data = {x+1 : [] for x in range(slots)}
    for x in data:
        if len(x['combo']) > 0:
            sep_data[len(x['combo'])].append(x)
    return sep_data

def remove_duplicates(data):
    b = []
    for d in data:
        if d not in b:
            b.append(d)
    return b

data = []
index_all = []

for x in upgrades['types']:
    for i in upgrades['types'][x]['upgrades']:
        index_all.append(f'{x}.{i}')

all_possible=combos(index_all, slots)
all_fit = []
all_dup_check = []
for x in all_possible:
    if not len(x) > slots:
        sort = sort_combos(x)
        if not sorted(sort) in all_dup_check:
            all_fit.append(sort)
            all_dup_check.append(sorted(sort))

all_fit = remove_duplicates(all_fit)

for n, combo in enumerate(all_fit):
    data.append({
        'combo' : combo,
        'ticks' : round(perform_calc(combo))
    })

data=filter_data(data)
data=sort_data(data)

print(F'Found {len(data)} valid combinations')

sep_data = separate_data(data)
for x in sep_data:
    print(f'\nTop 3, {x} slot combos:')
    for pos in range(3):
        print(sep_data[x][pos])
