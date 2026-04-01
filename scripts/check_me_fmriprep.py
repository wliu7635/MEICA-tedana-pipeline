import nibabel as nib

paths = [
    r"D:\MEICA\derivatives\fmriprep\sub-01\func\sub-01_task-rest_echo-1_desc-preproc_bold.nii.gz",  # ③ echo-1 preproc
    r"D:\MEICA\derivatives\fmriprep\sub-01\func\sub-01_task-rest_echo-2_desc-preproc_bold.nii.gz",  # ③ echo-2 preproc
    r"D:\MEICA\derivatives\fmriprep\sub-01\func\sub-01_task-rest_echo-3_desc-preproc_bold.nii.gz",  # ③ echo-3 preproc
]

imgs   = [nib.load(p) for p in paths]
shapes = [img.shape for img in imgs]

print("Shapes:", shapes)

# Ensure spatial dims match and number of timepoints (nTR) match
assert len({s[:3] for s in shapes}) == 1 and len({s[3] for s in shapes}) == 1, \
    "Mismatch in spatial size or nTR across echoes"

print("Echo-wise preprocessed series are spatially aligned and have identical length.")
