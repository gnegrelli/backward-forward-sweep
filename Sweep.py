
import numpy as np

Sb = 1000  # Base Power in kVA
Vb = 12.66  # Base Voltage in kV

Zb = ((Vb*1000)**2)/(Sb*1000)  # Base impedance in ohms

bus = {}

bus['2'] = {'P': 1000/Sb, 'Q': 600/Sb, 'V': 1, 'theta': 0, 'I': 0}
bus['3'] = {'P': 900/Sb, 'Q': 400/Sb, 'V': 1, 'theta': 0, 'I': 0}
bus['4'] = {'P': 1200/Sb, 'Q': 800/Sb, 'V': 1, 'theta': 0, 'I': 0}
bus['5'] = {'P': 800/Sb, 'Q': 600/Sb, 'V': 1, 'theta': 0, 'I': 0}

