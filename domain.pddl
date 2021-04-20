(define (domain remote-inspection)
(:requirements :typing)
(:types robot cell tank - object)

(:predicates 	
	(robot-at ?r - robot ?x - cell)
	(tank-at ?t - tank ?x - cell)
	(up ?x - cell ?y - cell)
	(down ?x - cell ?y - cell)
	(right ?x - cell ?y - cell)
	(left ?x - cell ?y - cell)
	(empty ?x - cell)
	(inspected ?t - tank)
	(radiation ?x - cell)
)

; Robot movements
(:action up 
  :parameters (?r - robot ?x - cell ?y - cell)
  :precondition (and (robot-at ?r ?x) (up ?x ?y) (empty ?y) (not (radiation ?y)))
  :effect (and (robot-at ?r ?y) (not (robot-at ?r ?x))
               (empty ?x) (not (empty ?y))
            )
)

(:action down 
  :parameters (?r - robot ?x - cell ?y - cell)
  :precondition (and (robot-at ?r ?x) (down ?x ?y) (empty ?y) (not (radiation ?y)))
  :effect (and (robot-at ?r ?y) (not (robot-at ?r ?x))
               (empty ?x) (not (empty ?y))
            )
)

(:action right 
  :parameters (?r - robot ?x - cell ?y - cell)
  :precondition (and (robot-at ?r ?x) (right ?x ?y) (empty ?y) (not (radiation ?y)))
  :effect (and (robot-at ?r ?y) (not (robot-at ?r ?x))
               (empty ?x) (not (empty ?y))
	     )
)

(:action left 
  :parameters (?r - robot ?x - cell ?y - cell)
  :precondition (and (robot-at ?r ?x) (left ?x ?y) (empty ?y) (not (radiation ?y)))
  :effect (and (robot-at ?r ?y) (not (robot-at ?r ?x))
               (empty ?x) (not (empty ?y))
            )
)

(:action inspect-up
  :parameters (?r - robot ?x - cell ?y - cell ?t - tank)
  :precondition (and (robot-at ?r ?x) (tank-at ?t ?y) (up ?x ?y) (not (inspected ?t)))
  :effect (and (inspected ?t)
            )
)

(:action inspect-down
  :parameters (?r - robot ?x - cell ?y - cell ?t - tank)
  :precondition (and (robot-at ?r ?x) (tank-at ?t ?y) (down ?x ?y) (not (inspected ?t)))
  :effect (and (inspected ?t)
            )
)

(:action inspect-right
  :parameters (?r - robot ?x - cell ?y - cell ?t - tank)
  :precondition (and (robot-at ?r ?x) (tank-at ?t ?y) (right ?x ?y) (not (inspected ?t)))
  :effect (and (inspected ?t)
            )
)

(:action inspect-left
  :parameters (?r - robot ?x - cell ?y - cell ?t - tank)
  :precondition (and (robot-at ?r ?x) (tank-at ?t ?y) (left ?x ?y) (not (inspected ?t)))
  :effect (and (inspected ?t)
            )
)

)

