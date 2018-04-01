pos=1;
RPM=[];
for loop=B 
  C{pos}=strsplit(loop{1});
  if (strcmp(C{pos}{1},"201") && length(C{pos})>=10)
    RPM(end+1)=(hex2dec(C{pos}{2})*256 + hex2dec(C{pos}{3}))/4;
  endif
  pos=pos+1;
endfor
figure
plot(RPM,"linewidth", 2)

indices = cellfun(@(x) strcmp(x{1},"4FF"), C);
D=C(indices)
indices = cellfun(@(x) strcmp(x{2},"11"), D);
D10=D(indices)


P3=[]
P4=[]
P5=[]
P6=[]
P7=[]
P8=[]
for loop=D10
    P3(end+1)=hex2dec(loop{1}{3});
    P4(end+1)=hex2dec(loop{1}{4});
    P5(end+1)=hex2dec(loop{1}{5});
    P6(end+1)=hex2dec(loop{1}{6});
    P7(end+1)=hex2dec(loop{1}{7});
    P8(end+1)=hex2dec(loop{1}{8});
endfor

% pacote 4FF 10
%A[8] -> ? Close loop

figure
plot(P3)
figure
plot(P4)
figure
plot(P5)
figure
plot(P6)
figure
plot(P7)
figure
plot(P8)

