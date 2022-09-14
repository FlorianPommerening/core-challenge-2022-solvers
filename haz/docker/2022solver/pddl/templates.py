
DOMAIN = """
(define (domain isr)

    (:requirements
        :negative-preconditions
        :typing
    )

    (:types
        loc
    )

    (:constants
        [LOCATIONS] - loc
    )

    (:predicates

        ; Standard move stuff
        (edge ?l1 ?l2 - loc)

        ; Free used to check independence
        (free ?l - loc)

        ; Tokened used as a (not (free ?l)) for goal specification
        (tokened ?l - loc)

        [PHASE-PRED]

    )

    [ACTIONS]

)
"""

PROBLEM = """
(define (problem isr-prob)
   (:domain isr)

   (:init

        [EDGES]

        [FREE_LOCATIONS]

        [TOKENED]

        [PHASE]

   )

   (:goal
        (and

            [GOAL]

        )
   )
)
"""

SINGLE_ACTION = """
(:action move-[LOC1]-[LOC2]
    :precondition (and
        (free [LOC2])
        (tokened [LOC1])
        [IS-COND])
    :effect (and
        (not (tokened [LOC1]))
        (free [LOC1])
        (not (free [LOC2]))
        (tokened [LOC2]))
)
"""

DUAL_ACTION_PICK = """
(:action pick-[LOC]
    :precondition (and
        (tokened [LOC])
        (handfree))
    :effect (and
        (not (tokened [LOC]))
        (free [LOC])
        (not (handfree))
        (holding))
)
"""

DUAL_ACTION_PLACE = """
(:action place-[LOC]
    :precondition (and
        (holding)
        (free [LOC])
        [IS-COND])
    :effect (and
        (not (holding))
        (tokened [LOC])
        (handfree)
        (not (free [LOC])))
)
"""


LIFTED_DOMAIN = """
(define (domain isr)

    (:requirements
        :negative-preconditions
        :adl
        :typing
    )

    (:types
        loc
    )

    (:predicates

        ; Standard move stuff
        (edge ?l1 ?l2 - loc)

        ; Free used to check independence
        (free ?l - loc)

        ; Tokened used as a (not (free ?l)) for goal specification
        (tokened ?l - loc)

    )

        (:action move

        :parameters (?l1 ?l2 - loc)

        :precondition (and

            ; standard move-from
            (free ?l2)
            (tokened ?l1)

            ; maintain independence
            (forall (?l3 - loc)
                (imply
                    (and (not (= ?l1 ?l3)) (edge ?l2 ?l3))
                    (free ?l3)
                )
            )

        )

        :effect (and

            ; standard move update
            (free ?l1)
            (tokened ?l2)

            (not (free ?l2))
            (not (tokened ?l1))

        )
    )

)
"""

LIFTED_PROBLEM = """
(define (problem isr-prob)
   (:domain isr)

   (:objects
        [LOCATIONS] - loc)

   (:init

        [EDGES]

        [FREE_LOCATIONS]

        [TOKENED]

   )

   (:goal
        (and

            [GOAL]

        )
   )
)
"""

