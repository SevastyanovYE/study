import numpy as np
import matplotlib.pyplot as plt
import math

N=50; M=50                  #разбиение сетки
x0=0; L=1; h=(L-x0)/N       #шаги сетки
t0=0; T=1; tau=(T-t0)/M
eps=0.00001                 #точность вычисления

u = np.zeros((N+1, M+1))            #массив сеточных значений
for n in range(0, N+1):             #заполнение ГУ
    u[n, 0] = 1+n*h*n*h
for m in range(0, M+1):             #заполнение НУ
    u[0, m] = math.exp(-m*tau)

for m in range(0, M):               #заполнение массива u через метод Ньютона
    for n in range(0, N):
        x_initial = u[n, m]
        x_instant = 1
        x_final = 0
        while abs(x_final - x_instant) > eps:
            x_instant = x_initial
            x_final = x_initial-(x_instant-(tau/h)*(-math.atan(1+x_instant*x_instant))-u[n+1, m]+(tau/h)*(-math.atan(1+u[n,m+1]*u[n,m+1])))/(1-(tau/h)*(-2*x_instant/(1+(1+x_instant*x_instant)*(1+x_instant*x_instant))))
            x_initial = x_final
        u[n+1, m+1] = x_final

u_graph = np.zeros((N+1, M+1))       #инвертирование массива u по переменной x для корректного вывода графика
for m in range(0, M+1):
    for n in range(0, N+1):
        u_graph[n, m] = u[N-n, m]


#сгущение сетки

# N=10 M=20
N1=10; M1=20
x0=0; L=1; h=(L-x0)/N1
t0=0; T=1; tau=(T-t0)/M1
eps=0.00001

u1 = np.zeros((N1+1, M1+1))
for n in range(0, N1+1):
    u1[n, 0] = 1+n*h*n*h
for m in range(0, M1+1):
    u1[0, m] = math.exp(-m*tau)

for m in range(0, M1):
    for n in range(0, N1):
        x_initial = u1[n, m]
        x_instant = 1
        x_final = 0
        while abs(x_final - x_instant) > eps:
            x_instant = x_initial
            x_final = x_initial-(x_instant-(tau/h)*(-math.atan(1+x_instant*x_instant))-u1[n+1, m]+(tau/h)*(-math.atan(1+u1[n,m+1]*u1[n,m+1])))/(1-(tau/h)*(-2*x_instant/(1+(1+x_instant*x_instant)*(1+x_instant*x_instant))))
            x_initial = x_final
        u1[n+1, m+1] = x_final

u1_graph = np.zeros((N1+1, M1+1))
for m in range(0, M1+1):
    for n in range(0, N1+1):
        u1_graph[n, m] = u1[N1-n, m]

u1x = np.zeros(N1+1)
for n in range(0, N1+1):
    u1x[n] = u1_graph[n, 10]

# N=20 M=40
N2=20; M2=40
x0=0; L=1; h=(L-x0)/N2
t0=0; T=1; tau=(T-t0)/M2
eps=0.00001

u2 = np.zeros((N2+1, M2+1))
for n in range(0, N2+1):
    u2[n, 0] = 1+n*h*n*h
for m in range(0, M2+1):
    u2[0, m] = math.exp(-m*tau)

for m in range(0, M2):
    for n in range(0, N2):
        x_initial = u2[n, m]
        x_instant = 1
        x_final = 0
        while abs(x_final - x_instant) > eps:
            x_instant = x_initial
            x_final = x_initial-(x_instant-(tau/h)*(-math.atan(1+x_instant*x_instant))-u2[n+1, m]+(tau/h)*(-math.atan(1+u2[n,m+1]*u2[n,m+1])))/(1-(tau/h)*(-2*x_instant/(1+(1+x_instant*x_instant)*(1+x_instant*x_instant))))
            x_initial = x_final
        u2[n+1, m+1] = x_final

u2_graph = np.zeros((N2+1, M2+1))
for m in range(0, M2+1):
    for n in range(0, N2+1):
        u2_graph[n, m] = u2[N2-n, m]

u2x = np.zeros(N2+1)
for n in range(0, N2+1):
    u2x[n] = u2_graph[n, 20]

# N=40 M=80
N3=40; M3=80
x0=0; L=1; h=(L-x0)/N3
t0=0; T=1; tau=(T-t0)/M3
eps=0.00001

u3 = np.zeros((N3+1, M3+1))
for n in range(0, N3+1):
    u3[n, 0] = 1+n*h*n*h
for m in range(0, M3+1):
    u3[0, m] = math.exp(-m*tau)

for m in range(0, M3):
    for n in range(0, N3):
        x_initial = u3[n, m]
        x_instant = 1
        x_final = 0
        while abs(x_final - x_instant) > eps:
            x_instant = x_initial
            x_final = x_initial-(x_instant-(tau/h)*(-math.atan(1+x_instant*x_instant))-u3[n+1, m]+(tau/h)*(-math.atan(1+u3[n,m+1]*u3[n,m+1])))/(1-(tau/h)*(-2*x_instant/(1+(1+x_instant*x_instant)*(1+x_instant*x_instant))))
            x_initial = x_final
        u3[n+1, m+1] = x_final

u3_graph = np.zeros((N3+1, M3+1))
for m in range(0, M3+1):
    for n in range(0, N3+1):
        u3_graph[n, m] = u3[N3-n, m]

u3x = np.zeros(N3+1)
for n in range(0, N3+1):
    u3x[n] = u3_graph[n, 40]

# N=80 M=160
N4=80; M4=160
x0=0; L=1; h=(L-x0)/N4
t0=0; T=1; tau=(T-t0)/M4
eps=0.00001

u4 = np.zeros((N4+1, M4+1))
for n in range(0, N4+1):
    u4[n, 0] = 1+n*h*n*h
for m in range(0, M4+1):
    u4[0, m] = math.exp(-m*tau)

for m in range(0, M4):
    for n in range(0, N4):
        x_initial = u4[n, m]
        x_instant = 1
        x_final = 0
        while abs(x_final - x_instant) > eps:
            x_instant = x_initial
            x_final = x_initial-(x_instant-(tau/h)*(-math.atan(1+x_instant*x_instant))-u4[n+1, m]+(tau/h)*(-math.atan(1+u4[n,m+1]*u4[n,m+1])))/(1-(tau/h)*(-2*x_instant/(1+(1+x_instant*x_instant)*(1+x_instant*x_instant))))
            x_initial = x_final
        u4[n+1, m+1] = x_final

u4_graph = np.zeros((N4+1, M4+1))
for m in range(0, M4+1):
    for n in range(0, N4+1):
        u4_graph[n, m] = u4[N4-n, m]

u4x = np.zeros(N4+1)
for n in range(0, N4+1):
    u4x[n] = u4_graph[n, 80]

#отрисовка профилей решения u(x) при t=0.5 для разных N и M

x1 = np.arange(-1.0, 0.1, 0.1)
x2 = np.arange(-1.0, 0.05, 0.05)
x3 = np.arange(-1.0, 0.025, 0.025)
x4 = np.arange(-1.0, 0.0125, 0.0125)
plt.plot(x1, u1x, color='r')
plt.plot(x2, u2x, color='g')
plt.plot(x3, u3x, color='b')
plt.plot(x4, u4x, color='m')
plt.xlabel('x')
plt.ylabel('u')
plt.show()

#отрисовка 3D-графика численного решения

xn = np.linspace(-L, 0, num=N+1)
tm = np.linspace(0, T, num=M+1)
grid_x, grid_t = np.meshgrid(tm, xn)
fig = plt.figure()
plot1 = fig.add_subplot(111, projection='3d')
graph = plot1.plot_surface(grid_x, grid_t, u_graph, cmap='inferno')
plot1.set_xlabel('t', rotation=0, fontsize=20, labelpad=10)
plot1.set_zlabel('u', rotation=0, fontsize=20, labelpad=10)
plot1.set_ylabel('x', rotation=0, fontsize=20, labelpad=10)
plt.show()
