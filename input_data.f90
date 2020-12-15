!
! input_data.f90
! Copyright (C) 2020 dlilien <dlilien@hozideh>
!
! Distributed under terms of the MIT license.
!

        FUNCTION Beta( Model, nodenumber, dumy) RESULT(betav)
            USE DefUtils
            USE types

            IMPLICIT NONE
            TYPE(Model_t) :: Model
            REAL(kind=dp) :: dumy,betav
            INTEGER :: nodenumber, nentries, i, ind
            REAL(kind=dp) :: x, dx
            REAL(kind=dp) :: n
            REAL(kind=dp), DIMENSION(:), ALLOCATABLE :: dist, betaarr
            LOGICAL :: gotit, FIRSTTIME=.TRUE.
            CHARACTER(len=MAX_NAME_LEN) :: beta_fn
            CHARACTER(len=1) :: header

            REAL(kind=dp) :: A, rho, g, H, alpha, yis

            SAVE dx, dist, nentries, betaarr, FIRSTTIME

            IF (FIRSTTIME) THEN
                FIRSTTIME = .FALSE.


                WRITE(beta_fn,"(A,I1 A)") 'true_beta.txt'

                OPEN(10, file=beta_fn)
                READ(10, *) header, nentries

                ALLOCATE(dist(nentries), betaarr(nentries))

                DO i=1,nentries
                    READ(10, *) dist(i), betaarr(i)
                END DO
                CLOSE(10)

                dx = (dist(nentries) - dist(1)) / (nentries - 1) 
            END IF

            x=Model % Nodes % x (nodenumber)
            ind = floor((x-dist(1)) / dx) + 1
            ind = max(ind, 1)
            ind = min(ind, nentries - 1)
            betav = betaarr(ind) + (x - dist(ind)) * &
                (betaarr(ind+1) - betaarr(ind)) / (dist(ind+1) - dist(ind))

            RETURN 
        END

        FUNCTION VX( Model, nodenumber, dumy) RESULT(betav)
            USE DefUtils
            USE types

            IMPLICIT NONE
            TYPE(Model_t) :: Model
            REAL(kind=dp) :: dumy,betav
            INTEGER :: nodenumber, nentries, i, ind
            REAL(kind=dp) :: x, dx
            REAL(kind=dp) :: n
            REAL(kind=dp), DIMENSION(:), ALLOCATABLE :: dist, betaarr
            LOGICAL :: gotit, FIRSTTIME=.TRUE.
            CHARACTER(len=MAX_NAME_LEN) :: beta_fn
            CHARACTER(len=1) :: header

            REAL(kind=dp) :: A, rho, g, H, alpha, yis

            SAVE dx, dist, nentries, betaarr, FIRSTTIME

            IF (FIRSTTIME) THEN
                FIRSTTIME = .FALSE.
                WRITE(beta_fn,"(A,I1 A)") 'vx.txt'

                OPEN(10, file=beta_fn)
                READ(10, *) header, nentries

                ALLOCATE(dist(nentries), betaarr(nentries))

                DO i=1,nentries
                    READ(10, *) dist(i), betaarr(i)
                END DO
                CLOSE(10)

                dx = (dist(nentries) - dist(1)) / (nentries - 1) 
            END IF

            x=Model % Nodes % x (nodenumber)
            ind = floor((x-dist(1)) / dx) + 1
            ind = max(ind, 1)
            ind = min(ind, nentries - 1)
            betav = betaarr(ind) + (x - dist(ind)) * &
                (betaarr(ind+1) - betaarr(ind)) / (dist(ind+1) - dist(ind))

            RETURN 
        END
