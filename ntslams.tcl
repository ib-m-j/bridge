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
set slamhcp [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]
set slamhcpone [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]
set slamhcptwo [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]
set slamhcpbalanced [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]
set slamhcpother [dict create 11 0 12 0 13 0 14 0 15 0 16 0 17 0]

deal_finished {
		puts "Onesuiters = [onesuiters count]"
		puts "Twosuiters = [twosuiters count]"
		puts "Balanced = [balanced count]"
		puts "Others = [others count]"

		puts "counts deals\talld\toned\ttwod\tbald\tothd"
		foreach hcp [dict keys $counthcp]  {
				set count [dict get $counthcp $hcp]
				set countone [dict get $counthcpone $hcp]
				set counttwo [dict get $counthcptwo $hcp]
				set countbalanced [dict get $counthcpbalanced $hcp]
				set countother [dict get $counthcpother $hcp]
				puts "Hcp: $hcp  \t$count\t$countone\t$counttwo\t$countbalanced\t$countother "
		}

		puts "counts slams\talls\tones\ttwos\tbals\toths"
		foreach hcp [dict keys $counthcp]  {
				set slams [dict get  $slamhcp $hcp]
				set slamsone [dict get  $slamhcpone $hcp]
				set slamstwo [dict get  $slamhcptwo $hcp]
				set slamsbalanced [dict get $slamhcpbalanced $hcp]
				set slamsother [dict get $slamhcpother $hcp]
				puts "Hcp: $hcp  \t$slams\t$slamsone\t$slamstwo\t$slamsbalanced\t$slamsother "
		}

		puts "% slams\talls\tones\ttwos\tbals\toths"
		foreach hcp [dict keys $counthcp]  {
				set count [dict get $counthcp $hcp]
				set countone [dict get $counthcpone $hcp]
				set counttwo [dict get $counthcptwo $hcp]
				set countbalanced [dict get $counthcpbalanced $hcp]
				set countother [dict get $counthcpother $hcp]
				set slams [dict get  $slamhcp $hcp]
				set slamsone [dict get  $slamhcpone $hcp]
				set slamstwo [dict get  $slamhcptwo $hcp]
				set slamsbalanced [dict get $slamhcpbalanced $hcp]
				set slamsother [dict get $slamhcpother $hcp]

				if {$count > 0} {
						set percentage [expr 100 * $slams / $count]
				}	else {
						set percentage 0
				}
				if {$countone > 0} {
						set percentageone [expr 100 * $slamsone / $countone]
				}	else {
						set percentageone 0
				}
				if {$counttwo > 0} {
						set percentagetwo [expr 100 * $slamstwo / $counttwo]
				}	else {
						set percentagetwo 0
				}
				if {$countbalanced > 0} {
						set percentagebalanced [expr 100 * $slamsbalanced / $countbalanced]
				}	else {
						set percentagebalanced 0
				}
				if {$countother > 0} {
						set percentageother [expr 100 * $slamsother / $countother]
				}	else {
						set percentageother 0
				}
		
				puts "Hcp: $hcp  \t$percentage\t$percentageone\t$percentagetwo\t$percentagebalanced\t$percentageother "
		}

}

main { 
		reject unless {[hcp north]>=15 && [hcp north]<=17 && [ntshape north] && [hcp south] >= 11 && [hcp south] <= 17} 

		set tricks [deal::tricks south notrumps]
		set hcpssouth  [hcp south]
		dict incr counthcp $hcpssouth
		set type 0
		if {[onesuiter south]} {
				set tricks [deal::tricks south [longsuit south]]
				onesuiters add 1
				if {$tricks >= 12} {
						dict incr slamhcpone $hcpssouth
				}
				dict incr counthcpone $hcpssouth
				set type 1
		}	elseif {[twosuiter south]} {
				twosuiters add 1
				if {$tricks >= 12} {
						dict incr slamhcptwo $hcpssouth
				}
				dict incr counthcptwo $hcpssouth
				set type 2
		}	elseif {[ntshape south]} {
				balanced add 1
				if {$tricks >= 12} {
						dict incr slamhcpbalanced $hcpssouth
				}
				dict incr counthcpbalanced $hcpssouth
				set type 3
		}	else {
				others add 1
				if {$tricks >= 12} {
						dict incr slamhcpother $hcpssouth
				}
				dict incr counthcpother $hcpssouth
				set type 4
		}

		if {$tricks >= 12} {
				dict incr slamhcp $hcpssouth
		}

		#set controlssouth  [controls south]
		#dict incr countcontrol $controlssouth
		set controls [expr [controls north] + [controls south]]
		#set controls  [controls north]
		puts "Type: $type; [longsuit south]; [controls south]; [hcp south]; $tricks"
		accept
}
