    import os, nibabel as nib, numpy as np
 
 def tsnr_4d(path_4d, out_path):
     img  = nib.load(path_4d)
     dat  = img.get_fdata()
     tsnr = dat.mean(3) / dat.std(3, ddof=1)
     os.makedirs(os.path.dirname(out_path), exist_ok=True)
     nib.Nifti1Image(tsnr, img.affine, img.header).to_filename(out_path)
     print("Saved:", out_path)
 
 # ⑨ raw dir
 raw_dir = r"D:\MEICA\raw\sub-01"
 
 # ⑩ tedana output dir (Section 3 --out-dir)
 td_dir  = r"D:\MEICA\MEICA-derivatives\tedana\sub-01_task-rest"
 
 # ⑪ tSNR output dir
 qc_dir  = r"D:\MEICA\MEICA-derivatives\qc\sub-01_tSNR_TE2_OC_MEICA"
 os.makedirs(qc_dir, exist_ok=True)
 
 # ⑫ if you compare echo‑2, keep this; otherwise change to echo‑1/3 name
 tsnr_4d(os.path.join(raw_dir, "sub-01_task-rest_echo-2_bold.nii.gz"),
         os.path.join(qc_dir,  "tsnr_TE2_raw.nii.gz"))
 
 tsnr_4d(os.path.join(td_dir,  "sub-01_rest_desc-optcom_bold.nii.gz"),
         os.path.join(qc_dir,  "tsnr_OC.nii.gz"))
 
 tsnr_4d(os.path.join(td_dir,  "sub-01_rest_desc-denoised_bold.nii.gz"),
         os.path.join(qc_dir,  "tsnr_MEICA_denoised.nii.gz"))
