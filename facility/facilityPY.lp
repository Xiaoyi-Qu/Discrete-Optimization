\ Model facility
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  12000 open[0] + 15000 open[1] + 17000 open[2] + 13000 open[3]
   + 16000 open[4] + 4000 trans[0,0] + 2000 trans[0,1] + 3000 trans[0,2]
   + 2500 trans[0,3] + 4500 trans[0,4] + 2500 trans[1,0] + 2600 trans[1,1]
   + 3400 trans[1,2] + 3000 trans[1,3] + 4000 trans[1,4] + 1200 trans[2,0]
   + 1800 trans[2,1] + 2600 trans[2,2] + 4100 trans[2,3] + 3000 trans[2,4]
   + 2200 trans[3,0] + 2600 trans[3,1] + 3100 trans[3,2] + 3700 trans[3,3]
   + 3200 trans[3,4]
Subject To
 Capacity[0]: - 20 open[0] + trans[0,0] + trans[1,0] + trans[2,0]
   + trans[3,0] <= 0
 Capacity[1]: - 22 open[1] + trans[0,1] + trans[1,1] + trans[2,1]
   + trans[3,1] <= 0
 Capacity[2]: - 17 open[2] + trans[0,2] + trans[1,2] + trans[2,2]
   + trans[3,2] <= 0
 Capacity[3]: - 19 open[3] + trans[0,3] + trans[1,3] + trans[2,3]
   + trans[3,3] <= 0
 Capacity[4]: - 18 open[4] + trans[0,4] + trans[1,4] + trans[2,4]
   + trans[3,4] <= 0
 Demand[0]: trans[0,0] + trans[0,1] + trans[0,2] + trans[0,3] + trans[0,4]
   = 15
 Demand[1]: trans[1,0] + trans[1,1] + trans[1,2] + trans[1,3] + trans[1,4]
   = 18
 Demand[2]: trans[2,0] + trans[2,1] + trans[2,2] + trans[2,3] + trans[2,4]
   = 14
 Demand[3]: trans[3,0] + trans[3,1] + trans[3,2] + trans[3,3] + trans[3,4]
   = 20
Bounds
Binaries
 open[0] open[1] open[2] open[3] open[4]
End
