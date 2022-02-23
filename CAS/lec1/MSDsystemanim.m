function [sys,x0]=MSDsystemanim(t,x,u,flag);

% Jerome Jouffroy, September 2008
% modified by Qiuyang zhou, July 2013
% modified by Jerome Jouffroy, September 2014

global MSDsystemAnim

% the mass
    Xmass = [ 5 ; 5 ; -5 ; -5 ; 5 ];
    Ymass = [ -5 ; 5 ; 5 ; -5 ; -5]; 

% the spring
    %Xspring = [ -29 ; -25 ; -23 ; -19 ; -15 ; -11 ; -9 ; -5 ];
    Xspring = [ 0 ; 4 ; 6 ; 10 ; 14 ; 18 ; 20 ; 24 ];
    Yspring = [ 0 ; 0 ; 3 ; -3 ; 3 ; -3 ; 0 ; 0 ];

  
if flag ==2,
    
    %display all hidden hand objects
    shh = get(0,'ShowHiddenHandles');
    set(0,'ShowHiddenHandles','on');
    
    if any(get(0,'Children')==MSDsystemAnim),
     if strcmp(get(MSDsystemAnim,'Name'),'Mass-Spring-Damper'),
      set(0,'currentfigure',MSDsystemAnim);
      hndlList=get(gca,'UserData');
      PosXmass = Xmass +  u(1);
      PosYmass = Ymass;
      PosXspring = Xspring/24*(u(1)+24) - 29;
      PosYspring = Yspring;
      set(hndlList(1),'XData',PosXmass,'YData',PosYmass);
      set(hndlList(2),'XData',PosXspring,'YData',PosYspring);
      drawnow;
    end
    end
  
  set(0,'ShowHiddenHandles',shh);    %restore the hidden property
  sys=[];

elseif flag==0,
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Initialization (flag==0) %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  % animinit Initialize the figure for use with this simulation
  [MSDsystemAnim, MSDAxes] = animinit('Mass-Spring-Damper'); 
    
  %display all hiden figure objects
  shh = get(0,'ShowHiddenHandles');
  set(0,'ShowHiddenHandles','on');
 
  figure(MSDsystemAnim);
  
  
  
  axis(MSDAxes, [-40 40 -10 10],'on'); 
  % AXIS([XMIN XMAX YMIN YMAX]) sets scaling for the x- and y-axes
  % on the current plot. and also turn on the axis (show the axis on the graph)
  grid on

  set(MSDAxes, 'XTick', [-40 -30 -20 -10 0 10 20 30 40],'YTick', [-10 0 10]);
  % set the tick on x and y axis
  hold(MSDAxes,'on');
  % HOLD ON holds the current plot and all axis properties so that
  %  subsequent graphing commands add to the existing graph.
 
  hndlList(1)= fill(Xmass,Ymass,'r');  
  % draw the red square represent the mass
  %hndlList(1)= plot(MSDAxes, Xmass,Ymass,'r','Linewidth', 1);  
 
  
  hndlList(2)= plot(MSDAxes,Xspring -29,Yspring,'b','Linewidth',3); 
  % draw the line represent the spring
  
   
  plot(MSDAxes,[-29 -29],[-10 10],'k','Linewidth',3); %draw a thick line on the left
  plot(MSDAxes,[0 0],[-10 -7],'k','Linewidth',2);  %draw a thin line at position x = 0
 
  set(MSDAxes,'DataAspectRatio',[ 1  1  1 ]);
  set(MSDAxes,'UserData',hndlList);
  box(MSDAxes, 'on');
  sys = [ 0  0  0  1  0  0 ];
  x0 = [];
  
 set(0,'ShowHiddenHandles',shh);  %restore the hidden property

end
% End of function MSDsystemanim
