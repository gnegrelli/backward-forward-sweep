
import numpy as np

Sb = 1000  # Base Power in kVA
Vb = 12.66  # Base Voltage in kV

Zb = ((Vb*1000)**2)/(Sb*1000)  # Base impedance in ohms

# Bus states
bus = {}

bus['1'] = {'P': 0/Sb, 'Q': 0/Sb, 'V': 1 + 1j*0, 'I': 0}
bus['2'] = {'P': 1000/Sb, 'Q': 600/Sb, 'V': 1 + 1j*0, 'I': 0}
bus['3'] = {'P': 900/Sb, 'Q': 400/Sb, 'V': 1 + 1j*0, 'I': 0}
bus['4'] = {'P': 1200/Sb, 'Q': 800/Sb, 'V': 1 + 1j*0, 'I': 0}
bus['5'] = {'P': 800/Sb, 'Q': 600/Sb, 'V': 1 + 1j*0, 'I': 0}

# Line impedances
line = {}

line['1-2'] = {'R': 0.3220/Zb, 'X': 0.2700/Zb, 'I': 0}
line['2-3'] = {'R': 0.4930/Zb, 'X': 0.2511/Zb, 'I': 0}
line['3-4'] = {'R': 0.3660/Zb, 'X': 0.1864/Zb, 'I': 0}
line['4-5'] = {'R': 0.3811/Zb, 'X': 0.1941/Zb, 'I': 0}

# Line admittances
Y = {}
Y['1-2'] = 1/(line['1-2']['R'] + 1j*line['1-2']['X'])
Y['2-3'] = 1/(line['2-3']['R'] + 1j*line['2-3']['X'])
Y['3-4'] = 1/(line['3-4']['R'] + 1j*line['3-4']['X'])
Y['4-5'] = 1/(line['4-5']['R'] + 1j*line['4-5']['X'])

# Nodal Admittance Matrix
Ybus = np.array([[Y['1-2'], -Y['1-2'], 0, 0, 0],
                 [-Y['1-2'], Y['1-2'] + Y['2-3'], -Y['2-3'], 0, 0],
                 [0, -Y['2-3'], Y['2-3'] + Y['3-4'], -Y['3-4'], 0],
                 [0, 0, -Y['3-4'], Y['3-4'] + Y['4-5'], -Y['4-5']],
                 [0, 0, 0, -Y['4-5'], Y['4-5']]])

# Log of voltages
Vlog = [np.array([bus['1']['V'], bus['2']['V'], bus['3']['V'], bus['4']['V'], bus['5']['V']])]

# Initializes global variables
tolerance = 0.00001
error = 1
counter = 0

# Create file
f = open("results.txt", "w+")

while error > tolerance:

    # Backward
    for key in sorted(line.keys(), reverse=True):

        # Calculate current of each bus
        bus[key[-1]]['I'] = np.conjugate(bus[key[-1]]['P'] + 1j*bus[key[-1]]['Q'])/np.conjugate(bus[key[-1]]['V'])

        # Calculate current on each line
        try:
            line[key]['I'] = bus[key[-1]]['I'] + line[key[-1] + '-' + str(int(key[-1]) + 1)]['I']
        except KeyError:
            line[key]['I'] = bus[key[-1]]['I']

    # Forward
    for key in sorted(line.keys()):
        bus[key[-1]]['V'] = bus[key[0]]['V'] - line[key]['I']/Y[key]

    # Save voltages obtained on each iteration on log
    Vlog.append(np.array([bus['1']['V'], bus['2']['V'], bus['3']['V'], bus['4']['V'], bus['5']['V']]))

    # Calculate error for this iteration and add counter
    error = (max(np.absolute(Vlog[-2]) - np.absolute(Vlog[-1])))
    counter += 1

    # Print data for this iteration
    print("Iteração #%d" % counter)
    print("Erro: %6f" % error)
    for key in bus.keys():
        print("Barra #%d: V = %f < %f° pu" % (int(key), np.absolute(bus[key]['V']), np.angle(bus[key]['V'], deg=True)))
    print(20*"-" + "\n")

    # Write in results file
    f.write("\nIteração #%d" % counter)
    f.write("\nErro: %6f" % error)
    for key in bus.keys():
        f.write("\nBarra #%d: V = %f < %f° pu" % (int(key), np.absolute(bus[key]['V']), np.angle(bus[key]['V'], deg=True)))
    f.write("\n" + 20*"-" + "\n")
