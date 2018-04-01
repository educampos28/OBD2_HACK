clear all;
fid =fopen('Output2.txt');
A = fscanf(fid,'%c');
B  = strsplit(A,'\r\n');
L=[];
X1=[];
X2=[];
X3=[];

%Pacote 420
%A[1]-40 -> Temperatura do motor

%Pacote 430
%( A[1]*256 + A[2] ) / 65536  -> Nivel do tanque
%A[7] == 20 -> Freio Puxado

%Pacote 201
%( A[1]*256 + A[2] ) / 4 -> RPM 
%( A[6]*256 + A[7] ) -> ??? 

pos=1;
for loop=B 
  C{pos}=strsplit(loop{1});
  if (strcmp(C{pos}{1},"430") && length(C{pos})>=10)
    L(end+1)=(hex2dec(C{pos}{2})*256 + hex2dec(C{pos}{3}))/65536;
  endif
   if (strcmp(C{pos}{1},"201") && length(C{pos})>=10)
    X1(end+1)=(hex2dec(C{pos}{7})*256 + hex2dec(C{pos}{8}));
    X2(end+1)=(hex2dec(C{pos}{7}));
    X3(end+1)=(hex2dec(C{pos}{8}));
  endif
  pos=pos+1;
endfor
figure
plot(X1,"linewidth", 2)
figure
plot(X2,"linewidth", 2)
figure
plot(X3,"linewidth", 2)