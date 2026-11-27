"""
Práctica 4: Sistema endócrino

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Gustavo Ortega Odabachea
Número de control: 23212223
Correo institucional: L23212223@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
t0, tend, dt, w, h = 0, 10, 1E-3, 7, 3.5
N = round(tend / dt) + 1
t = np.linspace(t0, tend, N)

# Señal de entrada: Escalón unitario en t = 1 s
u = np.zeros(N)
u[round(1 / dt):] = 1

# Función de transferencia: Control (Sano)
num_ctrl = [0.01, 100.1, 1000]
den_ctrl = [0.02, 300.1, 2000]
sys_control = ctrl.tf(num_ctrl, den_ctrl)
print(f"Función de transferencia Control:\n{sys_control}\n")

L_ctrl = np.roots(den_ctrl)
print(f"Polos Control: L1 = {L_ctrl[0]:.3e}, L2 = {L_ctrl[1]:.3e}\n")

# Función de transferencia: Caso (Enfermo)
num_caso = [0.5, 10000.5, 10000]
den_caso = [0.55, 12000.5, 11000]
sys_caso = ctrl.tf(num_caso, den_caso)
print(f"Función de transferencia Caso:\n{sys_caso}\n")

L_caso = np.roots(den_caso)
print(f"Polos Caso: L1 = {L_caso[0]:.3e}, L2 = {L_caso[1]:.3e}\n")

# Componentes del controlador Integral (P = 0, I = 466.9116, D = 0)
kI = 466.9116
Cr = 1E-6
Re = 1 / (Cr * kI)
numPID = [1]
denPID = [Re * Cr, 0]  # Integrador puro: 1 / (Re * Cr * s) = kI / s
PID = ctrl.tf(numPID, denPID)
print(f"El valor de la capacitancia Cr es de {Cr} Faradios.")
print(f"El valor de la resistencia Re es de {Re:.4f} Ohms.\n")
print(f"Función de transferencia del controlador:\n{PID}\n")

# Sistema de control en lazo cerrado (Tratamiento sobre la planta Caso)
x = ctrl.series(PID, sys_caso)
sysPID = ctrl.feedback(x, 1, sign=-1)
print(f"Función de transferencia en lazo cerrado:\n{sysPID}\n")

# Paleta de colores (idéntica al cuaderno de MATLAB)
clr1 = np.array([9, 21, 64]) / 255      # Ve(t) - Entrada
clr2 = np.array([27, 94, 32]) / 255     # Vs(t): Control
clr3 = np.array([246, 36, 64]) / 255    # Vs(t): Caso
clr4 = np.array([245, 153, 198]) / 255  # PID(t): Tratamiento

# Funciones de respuesta en lazo abierto y lazo cerrado
def openloop(t, sys, u):
    _, Vsu = ctrl.forced_response(sys, t, u)
    return Vsu

def closedloop(t, sysPID, ref):
    _, PIDu = ctrl.forced_response(sysPID, t, ref)
    return PIDu

# Respuesta al escalón: Simulación numérica
Control_u = openloop(t, sys_control, u)
Caso_u = openloop(t, sys_caso, u)
PID_u = closedloop(t, sysPID, Control_u)  # La referencia del PID es [Control]

fg = plt.figure(1)
fg.set_size_inches(w, h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']

plt.plot(t, u, '--', linewidth=1.5, color=clr1, label='$V_e(t)$')
plt.plot(t, Control_u, ':', linewidth=1.5, color=clr2, label='$V_s(t)$: Control')
plt.plot(t, Caso_u, '-', linewidth=1.5, color=clr3, label='$V_s(t)$: Caso')
plt.plot(t, PID_u, '-.', linewidth=1.5, color=clr4, label='$PID(t)$: Tratamiento')

plt.xlim(0, 10)
plt.xticks(np.arange(0, 11, 1))
plt.ylim(-0.1, 1.2)
plt.yticks(np.arange(-0.1, 1.3, 0.1))
plt.xlabel('$t$ [s]')
plt.ylabel('$V_s(t)$ [V]')
plt.legend(bbox_to_anchor=(0.5, 1.12), loc='center', ncol=4, frameon=False)
plt.show()
fg.savefig('step_python.pdf', bbox_inches='tight')