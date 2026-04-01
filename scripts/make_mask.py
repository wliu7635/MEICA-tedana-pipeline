REM ==========================================
REM Step 1: fMRIPrep (Docker) - multi-echo run
REM ==========================================

REM Replace ①–④ with your own paths:
REM ① BIDS root (input):        D:/MEICA/bids
REM ② Derivatives (output):     D:/MEICA/derivatives
REM ③ Work directory (temp):    D:/MEICA/work
REM ④ FreeSurfer license dir:   D:/MEICA/freesurfer   (contains license.txt)

docker run --rm -it ^
  -v "D:/MEICA/bids:/data:ro" ^                  rem ① input BIDS dataset (read-only)
  -v "D:/MEICA/derivatives:/out" ^               rem ② output derivatives directory
  -v "D:/MEICA/work:/work" ^                     rem ③ working directory
  -v "D:/MEICA/freesurfer:/opt/freesurfer" ^     rem ④ FreeSurfer license folder
  nipreps/fmriprep:latest ^
  /data /out participant ^
  --participant-label 01 ^                       rem ⑤ subject label (e.g., 01)
  --fs-license-file /opt/freesurfer/license.txt ^ rem ⑥ FreeSurfer license
  --work-dir /work ^                             rem ⑦ work dir inside container
  --output-spaces T1w MNI152NLin2009cAsym ^       rem ⑧ typical output spaces
  --me-output-echos ^                            rem ⑨ write echo-wise minimally processed series
  --nprocs 8 --omp-nthreads 8 --mem 16000        rem ⑩ tune for your machine
