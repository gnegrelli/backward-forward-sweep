
import numpy as np

Sb = 1000  # Base Power in kVA
Vb = 12.66  # Base Voltage in kV

Zb = ((Vb*1000)**2)/(Sb*1000)  # Base impedance in ohms

tolerance = 0.00001

# Bus states
bus = {}

bus['2'] = {'P': 1000/Sb, 'Q': 600/Sb, 'V': 1, 'theta': 0, 'I': 0}
bus['3'] = {'P': 900/Sb, 'Q': 400/Sb, 'V': 1, 'theta': 0, 'I': 0}
bus['4'] = {'P': 1200/Sb, 'Q': 800/Sb, 'V': 1, 'theta': 0, 'I': 0}
bus['5'] = {'P': 800/Sb, 'Q': 600/Sb, 'V': 1, 'theta': 0, 'I': 0}

# Line impedances
line = {}

line['1-2'] = {'R': 0.3220/Zb, 'X': 0.2700/Zb}
line['2-3'] = {'R': 0.4930/Zb, 'X': 0.2511/Zb}
line['3-4'] = {'R': 0.3660/Zb, 'X': 0.1864/Zb}
line['4-5'] = {'R': 0.3811/Zb, 'X': 0.1941/Zb}

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

