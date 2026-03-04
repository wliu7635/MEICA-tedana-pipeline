 import os
 import nibabel as nib
 from nilearn.masking import compute_epi_mask  # see official API  
 
 # ① set your Echo‑1 NIfTI path
 epi_path = r"D:\MEICA\raw\sub-01\sub-01_task-rest_echo-1_bold.nii.gz"
 
 # ② set your desired output path for the mask (directories will be created)
 out_path = r"D:\MEICA\MEICA-derivatives\masks\sub-01\sub-01_task-rest_mask.nii.gz"
 
 os.makedirs(os.path.dirname(out_path), exist_ok=True)
 img = nib.load(epi_path)
 mask_img = compute_epi_mask(img)
 mask_img.to_filename(out_path)
 print("Saved mask:", out_path)
