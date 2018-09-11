
patterncond ntshape {$l3>=3 && $l4>=2}


south is T9753 QJ Q86 A73




stringbox okbox 14 70
okbox write 4 15 "West"
okbox write 4 50 "East"
okbox write 0 30 "North"
okbox write 10 30 "South"
okbox subbox okbox.north 0 36 4 15
okbox subbox okbox.south 10 36 4 15
okbox subbox okbox.east 5 50 4 15
okbox subbox okbox.west 5 15 4 15
proc write_deal {} {
#  foreach hand {west south north east} {
#    okputhand $hand
#  }
#
#  puts "[okbox]"

#    puts [deal::tricks north notrumps]
#  puts "                       -----------------------------"
}


proc okputhand {hand} {

  okbox.$hand clear

  set rowhand 0
  foreach char {S H D C} suit {spades hearts diamonds clubs} {
    okbox.$hand write $rowhand 0 "$char [$hand -void --- $suit]"
    incr rowhand
  }
}

set countwins [dict create 3 0 4 0 5 0 6 0 7 0 8 0 9 0 10 0 11 0 12 0 13 0]
set countgames [dict create "win" 0 "lose" 0]
set count 0
set nthcp 15


proc testsyntax {} {
    puts "teststring"
}

main {
    reject unless  {[hcp north]==$nthcp && [ntshape north] && [spades north]==2}
    set tricks [deal::tricks north notrumps]
    dict incr countwins $tricks
    incr count
    #dict incr countwins 6
    if {$tricks >= 9} {dict incr countgames "win"} else {dict incr countgames "lose"}
    accept
    }

deal_finished {
    puts "deals $count, NT HCP: $nthcp"
    puts " [south]"
    foreach id [dict keys $countgames] {
	puts "$id [dict get $countgames $id]"
    }
    puts "--"

}
