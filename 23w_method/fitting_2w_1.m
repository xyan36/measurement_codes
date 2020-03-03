%define surface direction as y, perpendicular direction as x, follow
    %[2015] axes notation
%define k matrix and other parameters
data = readtable('200303_glass_R43_R2019_2w_modified.csv');
Lh =  
alpha = 
Rh =
Rt =
V1w =


global kxx kxy kyy cv
%str = 'Ramu2012';
str = 'glass';
switch str
    case 'glass'
        kxx = 1; %W/mK
        kxy = 0;
        kyy = 1;
        cv = 2.108e6; %J/m^3K
    case 'Ga2O3'
        kxx = 25; %W/mK
        kxy = 0;
        kyy = 10;
        cv = 6.35e5; %J/m^3K
    case 'Ramu2012'
        kxx = 5.2; %W/mK
        kxy = 0;
        kyy = 9;
        cv = 2.902e6; %J/m^3K
    otherwise
        disp('invalid case');
end

k0 = [kxx,kxy;kxy,kyy];
angle = -75;
kr = rotation(k0,angle);
kxx = kr(1,1);
kxy = kr(1,2);
kyy = kr(2,2);

%%design parameters of the heater & thermometer lines
D = 50 * 1e-6; %m
wt = 20* 1e-6; %m
wh = 20 * 1e-6; %m

%%findout T2w for a frequency range f
f = 20:5:2000;
T = zeros(1, length(f));
for i = 1:1:length(f)
    T(1, i) = calcTempAni2w(f(i), D(1), wt(1), wh(1));
end
%%plot T2w vs. f
f1 = figure;
semilogx(f, real(T(1,:)), 'lineWidth', 2)
xlabel('f(Hz)')
ylabel('TO in phase with applied power(K)')
%title('kxx = 4, kxy = sqrt(5), kyy = 2')
% legend([str, ' D=', num2str(D(1)*1e6), 'um', ', wt=', num2str(wt(1)*1e6), 'um', ', wh=', num2str(wh(1)*1e6), 'um'],...
%     [str, ' D=', num2str(D(2)*1e6), 'um', ', wt=', num2str(wt(2)*1e6), 'um', ', wh=', num2str(wh(2)*1e6), 'um'], ...
%     [str, ' D=', num2str(D(3)*1e6), 'um', ', wt=', num2str(wt(3)*1e6), 'um', ', wh=', num2str(wh(3)*1e6), 'um'], ...
%     [str, ' D=', num2str(D(4)*1e6), 'um', ', wt=', num2str(wt(4)*1e6), 'um', ', wh=', num2str(wh(4)*1e6), 'um'])
%saveas(f1,'glass_D50_w5-30.jpg')

%%function to calculate T2w for a given frequency and given metal line designs
function Ttmp = calcTempAni2w(f, D, wt, wh)
    %define surface direction as y, perpendicular direction as x, follow
    %[2015] axes notation
    P = 1e2; %W/m
    L = 1; %m
    global kxx kxy kyy cv
    detk = sqrt(kxx*kyy - kxy^2);
    qxx = @(omega) sqrt(1j*2*omega*cv/kxx); 
    int_wt_wh = integral2(@(t,y) besselk(0, qxx(2.*pi.*f) .* kxx * abs(D + t - y) / detk), -wt / 2, wt / 2, -wh / 2, wh / 2);
    Ttmp = P / (pi .* L .* detk .* wt .* wh) .* int_wt_wh;
end

function kr = rotation(k0,angle)
    ar = angle/180*pi;
    R = [cos(ar), -sin(ar);sin(ar), cos(ar)];
    kr = inv(R) * k0 * R;
end