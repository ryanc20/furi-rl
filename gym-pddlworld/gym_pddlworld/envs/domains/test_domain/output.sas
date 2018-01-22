begin_version
3
end_version
begin_metric
0
end_metric
4
begin_variable
var0
-1
2
Atom switch3_on()
NegatedAtom switch3_on()
end_variable
begin_variable
var1
-1
2
Atom switch2_on()
NegatedAtom switch2_on()
end_variable
begin_variable
var2
-1
2
Atom switch1_on()
NegatedAtom switch1_on()
end_variable
begin_variable
var3
-1
2
Atom light_bulb_on()
NegatedAtom light_bulb_on()
end_variable
0
begin_state
1
1
0
1
end_state
begin_goal
1
3 0
end_goal
7
begin_operator
switchoff_switch1 
0
1
0 2 0 1
1
end_operator
begin_operator
switchoff_switch2 
0
1
0 1 0 1
1
end_operator
begin_operator
switchoff_switch3 
0
1
0 0 0 1
1
end_operator
begin_operator
switchon_bulb 
3
2 0
1 1
0 0
1
0 3 -1 0
1
end_operator
begin_operator
switchon_switch1 
0
1
0 2 1 0
1
end_operator
begin_operator
switchon_switch2 
0
1
0 1 1 0
1
end_operator
begin_operator
switchon_switch3 
0
1
0 0 1 0
1
end_operator
0
