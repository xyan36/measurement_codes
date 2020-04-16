%%3w power dependence
fname1 = '200309\200309_glass_R56_3w_measurement_1.txt';
fname2 = '200406\200406_glass_R65_3w_measurement_2.txt';
data1 = readtable(fname1);
data2 = readtable(fname2);
data1.X3_pure = data1.X3 - mean(data1.X3_ref);
data2.X3_pure = data2.X3 - mean(data2.X3_ref);
Rname = 'R56';

Re0 = 40.20; %3w_1 old value
L = 2.15e-3; %---- estimated --- #length between V1w contacts
alpha = (0.002015 + 0.002005 + 0.001989 + 0.001988) / 4;
X1_1 = 69.21e-3;
X1_2 = 0.136682;
I1w_1 = X1_1 / Re0;
I1w_2 = X1_2 / Re0;
P_1 = X1_1^2 / (Re0 * L); %power / unit length
P_2 = X1_2^2 / (Re0 * L);
data1.T_avg = data1.X3_pure / (-1/2 * alpha * X1_1 * P_1);
data2.T_avg = data2.X3_pure / (-1/2 * alpha * X1_2 * P_2);
%f = 10,108.5Hz
X3_1 = [data1.X3_pure(data1.Lockin1f == 10), ...
    data1.X3_pure(data1.Lockin1f == 37.6), data1.X3_pure(data1.Lockin1f == 108.5)];
X3_2 = [data2.X3_pure(data2.Lockin1f == 10), ...
    data2.X3_pure(data1.Lockin1f == 37.6), data2.X3_pure(data2.Lockin1f == 108.5)];

I1w3 = [I1w_1^3; I1w_2^3];
X3 = [X3_1;X3_2];

p1 = polyfit(I1w3,X3(:,1),1);
p2 = polyfit(I1w3,X3(:,2),1);
p3 = polyfit(I1w3,X3(:,3),1);
f1 = figure;
h = zeros(1,6);
h(1)= plot(I1w3,X3(:,1),'b.','DisplayName', 'data');
hold on
h(2)= plot(I1w3,X3(:,2),'b.','DisplayName', 'data');
h(3)= plot(I1w3,X3(:,3),'b.','DisplayName', 'data');
x = [0;I1w3];
h(4)= plot(x, p1(1) * x + p1(2),'b', 'DisplayName', 'f1 = 10Hz');
h(5)= plot(x, p2(1) * x + p2(2),'r', 'DisplayName', 'f2 = 37.6Hz');
h(6)= plot(x, p3(1) * x + p3(2),'g', 'DisplayName', 'f3 = 108.5Hz');
hold off
legend(h(4:6))
xlim([0,5e-8])
str = sprintf(' X3_1 = (%0.3e) * I1w^3 + (%0.3e)', p1(:));
text(1.5e-8, -4e-5, str)
str = sprintf(' X3_2 = (%0.3e) * I1w^3 + (%0.3e)', p2(:));
text(1.5e-8, -3e-5, str)
str = sprintf(' X3_3 = (%0.3e) * I1w^3 + (%0.3e)', p3(:));
text(1.5e-8, -2.5e-5, str)
xlabel('I1w^3(A^3)')
ylabel('X3(V)')
saveas(f1,['200406\', Rname,'_3w_power_dep_in_a_shell.jpg'])