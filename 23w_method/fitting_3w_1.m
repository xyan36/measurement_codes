%define surface direction as y, perpendicular direction as x, follow
    %[2015] axes notation
%define k matrix and other parameters
%fname = '200408\200408_glass_R1516_3w_measurement_2.txt';
%fname = '200309\200309_glass_R56_3w_measurement_1.txt';
%fname = '200406\200406_glass_R65_3w_measurement_2.txt';
%fname = '200407\200407_glass_R43_3w_measurement_2.txt';
fname = '200416\200416_glass_R65_3w_V1p0.txt';
data = readtable(fname);
switch fname
    case '200408\200408_glass_R1516_3w_measurement_2.txt'
        Re0 = 39.92;%39.75;
        V1w = 0.135148;%67.95e-3;
        Rname = 'R78';
    case '200406\200406_glass_R65_3w_measurement_2.txt'
        Re0 = 40.20; %3w_1 old value
        V1w = 0.136682;%69.21e-3;
        Rname = 'R56';
    case '200407\200407_glass_R43_3w_measurement_2.txt'
        Re0 = 38.86;%3w_1 old value
        V1w = 0.132249;%66.86e-3;
        Rname = 'R43';
    case '200309\200309_glass_R56_3w_measurement_1.txt'
        Re0 = 40.20; %3w_1 old value
        V1w = 69.21e-3;
        Rname = 'R56_1';
    case '200416\200416_glass_R65_3w_V1p0.txt'
        Re0 = 40.20; %3w_1 old value
        V1w = mean([0.0858006,0.0858769,0.08581590, 0.0857778]);
        Rname = 'R56_2';
    otherwise
        disp('invalid case');
end
I1w = V1w / Re0;
alpha = (0.002015 + 0.002005 + 0.001989 + 0.001988) / 4;
data.f = data.Lockin1f;
X3_offset = 1.2724e-6;%-1.7497e-05; %intercept from power dependence 3w analysis)
data.X3_off = data.X3 - X3_offset; %expected offset = 2.58e-5V
%data.Y3_pure = data.Y3 - X3_offset;
L = 1.83e-3;%2.15e-3; %---- estimated --- #length between V1w contacts
P = V1w^2 / (Re0 * L); %power / unit length
data.T_avg = data.X3_off / (-1/2 * alpha * V1w * P);
%data.T_avg_img = data.Y3_pure / (-1/2 * alpha * V1w * P);
C = 2.11e6;
b = 10e-6; %half heater line width
r = 0.5772;

% fo = fitoptions('Method','NonlinearLeastSquares',...
%                'Lower',[0,0,0],...
%                'Upper',[10,10,10],...
%                'StartPoint',[1,1,1]);

%p = polyfit(log(data.Lockin1f),data.T_avg,1);
% plot(log(data.Lockin1f),data.T_avg,'b.')
% hold on
% plot(log(data.Lockin1f),polyval(p,log(data.Lockin1f)))
% hold off
%detk = (1 / (pi * -2 * p(1)))^2;

%ft = fittype( 'anisotropicT3w(x,detk,p0)', 'problem','detk');
ft = fittype('anisotropicT3w(x,detk,p0)');
%f = fit( data.Lockin1f, data.T_avg, ft, 'problem', detk, 'StartPoint', [1]);
f = fit( data.Lockin1f, data.T_avg, ft, 'StartPoint', [1,1]);
p0 = f.p0;
detk = f.detk;
confintf = confint(f);
% f1 = figure;
% plot(f, data.Lockin1f, data.T_avg)
% ax = gca;
% ax.XScale = 'log';
% ax.XLabel.String = 'f(Hz)';
% ax.YLabel.String = 'T3w(K)';
fparam = [f.detk,f.p0];
result = [fparam; confintf];
% str = sprintf('Coefficients (with 95%% confidence bounds):\np0 = %0.3f, (%0.3f, %0.3f)', result(:));
% text(100, -0.05, str)

%size = 1.0e+03 * [0.0010, 0.0010, 1.2800, 0.6473];
%f2 = figure('Position', size);
f2 = figure;
plot(log(data.Lockin1f), data.T_avg, 'b.', 'DisplayName', 'data')
hold on
%plot(log(data.Lockin1f), polyval(p,log(data.Lockin1f)),'color','cyan', 'LineWidth', 0.5)
plot(log(data.Lockin1f), anisotropicT3w(data.Lockin1f, detk, f.p0), 'r', 'lineWidth', 1, ...
    'DisplayName', 'magnitude best fit')
plot(log(data.Lockin1f), anisotropicT3w(data.Lockin1f, detk, 1/sqrt(detk)),'g', 'LineWidth', 1, ...
    'DisplayName', 'expected with kxx=kyy=sqrt(detk)')
hold off
str = sprintf('kxx / detk = %0.3f, (%0.3f, %0.3f)', result(:,2));
text(2, 0.5, str)
str = sprintf('detk = %0.3f, (%0.3f, %0.3f)', result(:,1));
text(2, 0.55, str)
legend('show')
xlabel('ln(f)')
ylabel('T(K)')
title([Rname, ' 3w slope and magnitude analysis'])
saveas(f2,[fname(1:end-4),'_T3w_slope_real_corrected.jpg'])
