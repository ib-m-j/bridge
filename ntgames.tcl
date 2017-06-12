source format/none

patterncond ntshape {$l3>=3 && $l4>=2}
patterncond onesuiter {$l1>=6 && $l2<=3}	
patterncond twosuiter {$l1>=5 && $l2>=5}

shapefunc longsuit {
		if {$s>=6} {return spades}
		if {$h>=6} {return hearts}
		if {$d>=6} {return diamonds}
		if {$c>=6} {return clubs}
}

patternfunc longsize {
		return $l1
}

set dealdata [open "~/GitHub/bridge/results/gamedeals.csv" "w"]
puts $dealdata "GameNo;SouthHcp;SouthControls;NorthHcp;NorthControls;HandType;NTTricks;SuitTricks;SumControls;SumHcp;NTMaxLength"

sdev onesuiters
sdev twosuiters
sdev balanced
sdev others

set count 0
set counthcp [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]
set counthcpone [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]
set counthcptwo [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]
set counthcpbalanced [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]
set counthcpother [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]
set gamehcp [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]
set gamehcpone [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]
set gamehcptwo [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]
set gamehcpbalanced [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]
set gamehcpother [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]

main { 
		reject unless {[hcp north]>=15 && [hcp north]<=17 && [ntshape north] && [hcp south] >= 7 && [hcp south] <= 11} 

		set tricks [deal::tricks south notrumps]
		set suittricks -1
		set hcpssouth  [hcp south]
		dict incr counthcp $hcpssouth
		if {[onesuiter south]} {
				set suittricks [deal::tricks south [longsuit south]]
				onesuiters add 1
				if {$suittricks >= 10} {
						dict incr gamehcpone $hcpssouth
				}
				dict incr counthcpone $hcpssouth
				set type "onesuit"
		}	elseif {[twosuiter south]} {
				twosuiters add 1
				if {$tricks >= 9} {
						dict incr gamehcptwo $hcpssouth
				}
				dict incr counthcptwo $hcpssouth
				set type "twosuit"
		}	elseif {[ntshape south]} {
				balanced add 1
				if {$tricks >= 9} {
						dict incr gamehcpbalanced $hcpssouth
				}
				dict incr counthcpbalanced $hcpssouth
				set type "ntshape"
		}	else {
				others add 1
				if {$tricks >= 9} {
						dict incr gamehcpother $hcpssouth
				}
				dict incr counthcpother $hcpssouth
				set type "other"
		}

		if {$tricks >= 9} {
				dict incr gamehcp $hcpssouth
		}

		#set controlssouth  [controls south]
		#dict incr countcontrol $controlssouth
		set controls [expr [controls north] + [controls south]]
		#set controls  [controls north]

		incr count
		# "GameNo;SouthHcp;SouthControls;NorthHcp;NorthControls;HandType;NTTricks;SuitTricks;SumControls;SumHcp;NTMaxLength"
		puts $dealdata "$count;[hcp south];[controls south];[hcp north];[controls north];$type;$tricks;$suittricks;[expr [controls south] + [controls north]];[expr [hcp south] + [hcp north]];[longsize north]"
		accept
}
