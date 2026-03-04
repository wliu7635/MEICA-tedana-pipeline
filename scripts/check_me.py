 import nibabel as nib

 paths = [
     r"D:\MEICA\raw\sub-01\sub-01_task-rest_echo-1_bold.nii.gz",  # ③ your echo‑1
     r"D:\MEICA\raw\sub-01\sub-01_task-rest_echo-2_bold.nii.gz",  # ③ your echo‑2
     r"D:\MEICA\raw\sub-01\sub-01_task-rest_echo-3_bold.nii.gz",  # ③ your echo‑3
 ]
 imgs   = [nib.load(p) for p in paths]
 shapes = [img.shape for img in imgs]
 print("Shapes:", shapes)
 assert len({s[:3] for s in shapes}) == 1 and len({s[3] for s in shapes}) == 1, "Mismatch in size or nTR"
 print("Looks aligned & same length.")
