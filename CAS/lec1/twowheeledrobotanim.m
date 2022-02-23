function [sys,x0]=twowheeledrobotanim(t,x,u,flag);

%   Jerome Jouffroy, September 2021

global TwoWheeledAnim
 
% body
    Ybody = [ -0.2 ; -0.2 ; 0.2 ; 0.2 ];
    Xbody = [ -0.15 ; 0.15 ; 0.15 ; -0.15 ]; 

% front
    Yfront = [ -0.2 ; -0.1 ; 0.1 ; 0.2 ];
    Xfront = [ 0.15 ; 0.2 ; 0.2 ; 0.15 ];
    
% wheel model
    Yw = [ -0.02 ; -0.02 ; 0.02 ; 0.02 ];
    Xw = [ -0.13 ; 0.13 ; 0.13 ; -0.13 ];
    
% left wheel
    Ywl = Yw + 0.21;
    Xwl = Xw;
    
% right wheel    
    Ywr = Yw - 0.21;
    Xwr = Xw;
    

if flag==2,
    
    %display all hidden hand objects
    shh = get(0,'ShowHiddenHandles');
    set(0,'ShowHiddenHandles','on');
    
    
  if any(get(0,'Children')==TwoWheeledAnim),
    if strcmp(get(TwoWheeledAnim,'Name'),'Two-wheeled robot'),
      set(0,'currentfigure',TwoWheeledAnim);
      hndlList=get(gca,'UserData');
      % draw robot body
      [PosXbody,PosYbody] = rot(Xbody,Ybody,u(3));
      PosXbody = PosXbody + u(1);
      PosYbody = PosYbody + u(2);
      [PosXwl,PosYwl] = rot(Xwl,Ywl,u(3));
      PosXwl = PosXwl + u(1);
      PosYwl = PosYwl + u(2);
      [PosXwr,PosYwr] = rot(Xwr,Ywr,u(3));
      PosXwr = PosXwr + u(1);
      PosYwr = PosYwr + u(2);
      [PosXfront,PosYfront] = rot(Xfront,Yfront,u(3));
      PosXfront = PosXfront + u(1);
      PosYfront = PosYfront + u(2);
      set(hndlList(1),'XData',PosXbody,'YData',PosYbody);
      set(hndlList(2),'XData',PosXwl,'YData',PosYwl);
      set(hndlList(3),'XData',PosXwr,'YData',PosYwr);
      set(hndlList(4),'XData',PosXfront,'YData',PosYfront);
      drawnow;     
    end
  end
  sys=[];
  set(0,'ShowHiddenHandles',shh);    %restore the hidden property
elseif flag==0,
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Initialization (flag==0) %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  % Initialize the figure for use with this simulation
   [TwoWheeledAnim, Axes] = animinit('Two-wheeled robot'); % ANIMINIT Initializes a figure for Simulink animations.

 
   %  This function is OBSOLETE and may be removed in future versions.
    shh = get(0,'ShowHiddenHandles');
  set(0,'ShowHiddenHandles','on');
   figure(TwoWheeledAnim);
  
  axis(Axes,[-1 6 -1 6], 'on');
  grid on
	% AXIS([XMIN XMAX YMIN YMAX]) sets scaling for the x- and y-axes
   %     on the current plot.

  hold(Axes,'on');
	% HOLD ON holds the current plot and all axis properties so that
   %  subsequent graphing commands add to the existing graph.
   
  
  hndlList(1)= fill(Xbody,Ybody,'r');
  hndlList(2)= fill(Xwl,Ywl,'b');
  hndlList(3)= fill(Xwr,Ywr,'b');
  hndlList(4)= fill(Xfront,Yfront,'g');
  set(gca,'DataAspectRatio',[ 1  1  1 ]);
  set(gca,'UserData',hndlList);

  sys = [ 0  0  0  3  0  0 ];
  x0 = [];
  
 set(0,'ShowHiddenHandles',shh);  %restore the hidden property
end
% End of function

% function "rot" that rotates a graphical object
function [PosX,PosY] = rot(X,Y,angle)

dim = size(X,1);

Mrot = [ cos(angle) -sin(angle)  ;
         sin(angle)  cos(angle) ]; 

for i=1:dim
    Pos_i = Mrot * [ X(i,1) ; Y(i,1) ];
    PosX(i,1) = Pos_i(1,1);
    PosY(i,1) = Pos_i(2,1);
end
