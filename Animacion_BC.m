%%%%%%%%%%%%%%%% LECTURA DE TABLA %%%%%%%%%%%%%%%%%%%%%%%%%%%
dataraw = load('dump_vis.txt');
data=sortrows(dataraw,[6,1]);
%#n seria las personas, m la cantidad de timesteps
n=max(data(:,1));  m=length(data(:,1))/n;
types=(data(1:n,2));  NTypes=max(types);

xraw=data(:,3);
yraw=data(:,4);
c1raw=data(:,5);

x=zeros(n,m); y=x; c1=x; t=zeros(1,m);%inicializo las matrices. 
%x(i,j) es el x de la persona i en el timestep j
for i=1:m
x(:,i)=xraw(n*(i-1)+1 : n*i);
y(:,i)=yraw(n*(i-1)+1 : n*i);
c1(:,i)=c1raw(n*(i-1)+1 : n*i);
t(i)=data(i*n,6);
end
c1=c1>0;
type_colors=rand(1,NTypes); colors=0*types;
for i=1:n
colors(i)=type_colors(types(i));
end
%%%%%%%%%%%%%% CANTIDAD DE GENTE EN CLUSTERS EN FUNCION DEL TIEMPO %%%%%%%%%%
sizebc=t*0;
for j=1:m
sizebc(j)=sum(c1(:,j));
end
plot(t,sizebc) 
xlabel ("Tiempo",'fontsize',18);
ylabel ("Cantidad de personas en BC",'fontsize',18);
title ("Cantidad de personas en BC    (0=no hay BC)",'fontsize',18);

%%%%%%%%%%%%%% DURACION CLUSTERS EN FUNCION DEL TIEMPO %%%%%%%%%%%%%
list=[];
listas=cell(1,m); #Lista negra de gente que bloquea para cada t
for j=1:m
    for id=1:n
          if c1(id,j)==1
          list=[list,id];
          end
    end
    listas{j}=list;
    list=[];
end

duracion=0; duratemp=0;
for j=2:m
  if length(listas{j})==0
  duracion=[duracion,0];
  else
     if length(listas{j})==length(listas{j-1})   
        if listas{j}==listas{j-1}
        duratemp+=1;
        else
        duracion(j-duratemp:j)=duratemp;
        duratemp=0;
        end
     else
        duracion(j-duratemp:j)=duratemp;
        duratemp=0;
     end
  end
end  
duracion(length(duracion):m)=0;
plot(t,duracion*0.05)
xlabel ("Tiempo",'fontsize',18);
ylabel ("Duracion",'fontsize',18);
title ("Duracion de BC    (0=no hay BC)",'fontsize',18);

hist(duracion*0.05,15,'g');


%%%%%%%%%%%%%%%% GENERACION DE LA ANIMACION %%%%%%%%%%%%%%%%%%%

lin=4;
for j=1:1:m
 clf,hold on
 box off
axis([12 21 3 17])
plot([0,0],[0,20],'k','linewidth',lin)
plot([20,20],[0,10-0.46],'k','linewidth',lin)
plot([20,20],[10+0.46,20],'k','linewidth',lin)
plot([0,20],[0,0],'k','linewidth',lin)
plot([0,20],[20,20],'k','linewidth',lin)
scatter(x(:,j),y(:,j),c1(:,j)*17,'k','filled')
scatter(x(:,j),y(:,j),12,colors,'filled')
title(sprintf(['t=',num2str(t(j))]),'fontsize',18)
%pause(0.05), drawnow
    filename=sprintf('output/%05d.png',j);     print(filename);
end




