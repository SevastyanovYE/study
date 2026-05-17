import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

#аналитическое решение
def analytic_solution(x, y, t):
    return np.sin(2*np.pi*x)*np.sin(np.pi*y/4)*np.exp(-65*np.pi*np.pi*t/16)

#начальное условие
def initial_condition(x, y):
    return np.sin(2*np.pi*x)*np.sin(np.pi*y/4)

#инициализация сетки и массива решения, задание ГУ и НУ
#узлы сетки
N, M, J = 20, 20, 20
#границы отрезков по х, у, t
X1, X2 = 0, 1
Y1, Y2 = 0, 2
T1, T2 = 0, 0.02
#сетка
x = np.linspace(X1, X2, N)
y = np.linspace(Y1, Y2, M)
t = np.linspace(T1, T2, J)
#шаги
h_x = (X2-X1)/N
h_y = (Y2-Y1)/M
tau = (T2-T1)/J
#вспомогательные выражения
gamma_x = tau/(h_x*h_x)
gamma_y = tau/(h_y*h_y)
#массив с решением (обратите внимание на размер по t - это для полуслоев j+1/2)
# +задание НУ
u = np.zeros((N, M, 2*J+1))
for n in range(0,N):
    for m in range(0,M):
        u[n,m,0] = initial_condition(x[n], y[m])

#реализация метода переменных направлений
def F1(n, m, j):    #неоднородность в правой части для перехода j->j+1/2
    return 0.5*gamma_y*(u[n, m-1, j-1]+u[n, m+1, j-1])+(1-gamma_y)*u[n, m, j-1]

def solve_x(m, j):      #метод прогонки по x
    alpha = np.zeros(N)
    alpha[1] = 0        #значение вписывается из ГУ по х
    beta = np.zeros(N)
    A = B = 1/2*gamma_x
    C = 1 + gamma_x
    for n in range(1, N-1):     #прямой ход прогонки
        F_instant = -F1(n, m, j)
        alpha[n+1] = B/(C - A*alpha[n])
        beta[n+1] = (F_instant - A*beta[n])/(A*alpha[n]-C)
    u[N-1, m, j] = 0        #значение вписывается из ГУ по х
    for n in range(N-1, 0, -1):     #обратный ход прогонки
        u[n-1, m, j] = alpha[n]*u[n, m, j] + beta[n]

def F2(n, m, j):        #неоднородность в правой части для перехода j+1/2->j+1
    return 0.5*gamma_x*(u[n-1, m, j-1]+u[n+1, m, j-1])+(1-gamma_x)*u[n, m, j-1]

def solve_y(n, j):      #метод прогонки по y
    alpha = np.zeros(M)
    alpha[1] = 0        #значение вписывается из ГУ по у
    beta = np.zeros(M)
    A = B = 1/2*gamma_y
    C = 1 + gamma_y
    for m in range(1, M-1):     #прямой ход прогонки
        F_instant = -F2(n, m, j)
        alpha[m+1] = B/(C - A*alpha[m])
        beta[m+1] = (F_instant - A*beta[m])/(A*alpha[m]-C)
    u[n, M-1, j] = beta[M-1]/(1-alpha[M-1])     #значение вписывается из ГУ по у
    for m in range(M-1, 0, -1):     #обратный ход прогонки
        u[n, m-1, j] = alpha[m]*u[n, m, j]+beta[m]

#собственно метод переменных направлений, заполнение массива решения
for j in range(1, 2*J, 2):
    for m in range(1, M-1):
        solve_x(m, j)
    #граничные условия по х
    u[0,:,:]=u[N-1,:,:]=0
    #граничные условия по y
    u[:,0,:]=0
    u[:,M-1,:]=u[:,M-2,:]
    for n in range(1, N-1):
        solve_y(n, j+1)

#заполнение массива решения для корректного вывода графиков (инвертируем координатные индексы)
u_graph = np.zeros((M, N, 2*J+1))
for n in range(0,N):
    for m in range(0,M):
        u_graph[m,n,:]=u[n,m,:]

#заполнение массива аналитического решения
xx, yy = np.meshgrid(x, y)
u_analytical = np.zeros((N, M, 2*J+1))
for n in range(0, N):
    for m in range(0, M):
        for j in range(0, 2*J, 2):
            u_analytical[n,m,j] = analytic_solution(x[n], y[m], t[j // 2])

#заполнение массива аналитического решения для корректного вывода графиков
u_analytical_graph = np.zeros((M, N, 2*J+1))
for n in range(0, N):
    for m in range(0, M):
        u_analytical_graph[m,n,:] = u_analytical[n,m,:]

#заполнение массива аналитического решения для момента времени t=0.01-tau/2
u_an = np.zeros((N,M))
for n in range(0, N):
    for m in range(0, M):
        u_an[n, m] = analytic_solution(x[n], y[m], 0.01-tau/2)

#массив ошибки, то есть модуля разности между численным и аналитическим решением на слое j+1/2
error = np.zeros((M, N))
for n in range(0, N):
    for m in range(0, M):
        error[m,n] = np.abs(u[n, m, J-1]-u_an[n, m])

#эта часть кода выводит величину h_x^2+h_y+tau^2 и максимум модуля ошибки для
#заданного в начале программы количества узлов сетки N, M, J
max_error = np.max(error)
accuracy = h_x**2+h_y+tau**2
print(accuracy)
print(max_error)

#построение графиков
#график численного решения

fig = plt.figure(figsize=(10,10))
plt.suptitle(r'Размер сетки: $N='+str(N)+',~ M='+str(M)+',~J='+str(J)+'$')
ax = fig.add_subplot(1,3,1, projection='3d')
ax.plot_surface(xx, yy, u_graph[:,:,J], rstride=1, cstride=1, cmap='inferno')
ax.set_title('График численного решения' + "\n" + '$u(x, y, t = 0.01)$')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('u')
ax.set_xlim(X1, X2)
ax.set_ylim(Y1, Y2)

#график аналитического решения
ax = fig.add_subplot(1,3,2, projection='3d')
ax.plot_surface(xx, yy, u_analytical_graph[:,:,J], rstride=1, cstride=1, cmap='inferno')
ax.set_title('График аналитического решения'+"\n"+ '$u(x, y, t = 0.01)$')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('u')
ax.set_xlim(X1, X2)
ax.set_ylim(Y1, Y2)

#график ошибки, то есть модуля разности двух решений
ax = fig.add_subplot(1,3,3, projection='3d')
ax.plot_surface(xx, yy, error, rstride=1, cstride=1, cmap='inferno')
ax.set_title('График модуля разности двух решений' + "\n" + '$ERR(x, y, t = 0.01)$')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_xlim(X1, X2)
ax.set_ylim(Y1, Y2)
plt.show()

#проверка НУ

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,3,1, projection='3d')
ax.plot_surface(xx, yy, u_graph[:,:,0], rstride=1, cstride=1, cmap='inferno')
ax.set_title('График численного решения при t=0')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('u')
ax.set_xlim(X1, X2)
ax.set_ylim(Y1, Y2)

ax = fig.add_subplot(1,3,3, projection='3d')
ax.plot_surface(xx, yy, u_analytical_graph[:,:,0], rstride=1, cstride=1, cmap='inferno')
ax.set_title('График аналитического решения при t=0')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('u')
ax.set_xlim(X1, X2)
ax.set_ylim(Y1, Y2)
plt.show()


#проверка ГУ
#x=0

yy, tt = np.meshgrid(y, t)
u_temp_num = np.zeros((J,M,N))
for j in range(0, 2*J, 2):
    for m in range(0,M):
        for n in range(0,N):
            u_temp_num[j // 2,m,n] = u[n,m,j]
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,3,1, projection='3d')
ax.plot_surface(yy, tt, u_temp_num[:,:,0], rstride=1, cstride=1, cmap='inferno')
ax.set_title('График численного решения при x=0')
ax.set_xlabel('y')
ax.set_ylabel('t')
ax.set_zlabel('u')
ax.set_xlim(Y1, Y2)
ax.set_ylim(T1, T2)

u_temp_an = np.zeros((J,M,N))
for j in range(0, 2*J, 2):
    for m in range(0,M):
        for n in range(0,N):
            u_temp_an[j // 2,m,n] = u_analytical[n,m,j]
ax = fig.add_subplot(1,3,3, projection='3d')
ax.plot_surface(yy, tt, u_temp_an[:,:,0], rstride=1, cstride=1, cmap='inferno')
ax.set_title('График аналитического решения при x=0')
ax.set_xlabel('y')
ax.set_ylabel('t')
ax.set_zlabel('u')
ax.set_xlim(Y1, Y2)
ax.set_ylim(T1, T2)
plt.show()


#x=1

yy, tt = np.meshgrid(y, t)
u_temp_num = np.zeros((J,M,N))
for j in range(0, 2*J, 2):
    for m in range(0,M):
        for n in range(0,N):
            u_temp_num[j // 2,m,n] = u[n,m,j]
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,3,1, projection='3d')
ax.plot_surface(yy, tt, u_temp_num[:,:,N-1], rstride=1, cstride=1, cmap='inferno')
ax.set_title('График численного решения при x=1')
ax.set_xlabel('y')
ax.set_ylabel('t')
ax.set_zlabel('u')
ax.set_xlim(Y1, Y2)
ax.set_ylim(T1, T2)

u_temp_an = np.zeros((J,M,N))
for j in range(0, 2*J, 2):
    for m in range(0,M):
        for n in range(0,N):
            u_temp_an[j // 2,m,n] = round(u_analytical[n,m,j],10)
ax = fig.add_subplot(1,3,3, projection='3d')
ax.plot_surface(yy, tt, u_temp_an[:,:,N-1], rstride=1, cstride=1, cmap='inferno')
ax.set_title('График аналитического решения при x=1')
ax.set_xlabel('y')
ax.set_ylabel('t')
ax.set_zlabel('u')
ax.set_xlim(Y1, Y2)
ax.set_ylim(T1, T2)
plt.show()


#y=0

xx, tt = np.meshgrid(x, t)
u_temp_num = np.zeros((J,N,M))
for j in range(0, 2*J, 2):
    for m in range(0,M):
        for n in range(0,N):
            u_temp_num[j // 2,n,m] = u[n,m,j]
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,3,1, projection='3d')
ax.plot_surface(xx, tt, u_temp_num[:,:,0], rstride=1, cstride=1, cmap='inferno')
ax.set_title('График численного решения при y=0')
ax.set_xlabel('x')
ax.set_ylabel('t')
ax.set_zlabel('u')
ax.set_xlim(X1, X2)
ax.set_ylim(T1, T2)

u_temp_an = np.zeros((J,N,M))
for j in range(0, 2*J, 2):
    for m in range(0,M):
        for n in range(0,N):
            u_temp_an[j // 2,n,m] = u[n,m,j]
ax = fig.add_subplot(1,3,3, projection='3d')
ax.plot_surface(xx, tt, u_temp_an[:,:,0], rstride=1, cstride=1, cmap='inferno')
ax.set_title('График аналитического решения при y=0')
ax.set_xlabel('x')
ax.set_ylabel('t')
ax.set_zlabel('u')
ax.set_xlim(X1, X2)
ax.set_ylim(T1, T2)
plt.show()


#y=2

xx, tt = np.meshgrid(x, t)
u_temp_num = np.zeros((J,N,M))
for j in range(0, 2*J, 2):
    for m in range(0,M):
        for n in range(0,N):
            u_temp_num[j // 2,n,m] = u[n,m,j]
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,3,1, projection='3d')
ax.plot_surface(xx, tt, u_temp_num[:,:,M-1], rstride=1, cstride=1, cmap='inferno')
ax.set_title('График численного решения при y=2')
ax.set_xlabel('x')
ax.set_ylabel('t')
ax.set_zlabel('u')
ax.set_xlim(X1, X2)
ax.set_ylim(T1, T2)

u_temp_an = np.zeros((J,N,M))
for j in range(0, 2*J, 2):
    for m in range(0,M):
        for n in range(0,N):
            u_temp_an[j // 2,n,m] = u[n,m,j]
ax = fig.add_subplot(1,3,3, projection='3d')
ax.plot_surface(xx, tt, u_temp_an[:,:,M-1], rstride=1, cstride=1, cmap='inferno')
ax.set_title('График аналитического решения при y=2')
ax.set_xlabel('x')
ax.set_ylabel('t')
ax.set_zlabel('u')
ax.set_xlim(X1, X2)
ax.set_ylim(T1, T2)
plt.show()