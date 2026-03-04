# MEICA-tedana-pipeline
Multi-echo fMRI ME-ICA workflow using tedana, including preprocessing, T2*, optimal combination, ICA classification, and surface mapping.

This repository implements a complete ME‑ICA workflow with tedana: voxelwise T2*/S0 fitting → optimal combination (OC) → ICA‑based component classification → denoised reconstruction. It then computes tSNR for TE2, OC, and ME‑ICA‑denoised data and compares them in volume space (no surface mapping).
All references to tool behavior and parameters point to the official documentation: tedana usage/outputs, nilearn.compute_epi_mask, AFNI’s definition of tSNR, and Workbench palette names/options (including videen_style)


0. Environment & Setup (Windows CMD workflow, no conda)
Run Python and tedana directly from Windows CMD. Simply install dependencies via pip (run CMD as Administrator if needed):

      :: (Optional) check Python version (3.10+ recommended)
   
       python --version
      
      :: Install dependencies (no conda required)
   
       pip install tedana nibabel nilearn numpy scipy matplotlib

tedana: ME‑ICA workflow tool; CLI options, workflow stages, and BIDS‑derivative outputs are described in the official docs. https://tedana.readthedocs.io/en/24.0.0/generated/tedana.workflows.tedana_workflow.html

nilearn: compute_epi_mask is used for EPI masking; if you do not pass --mask, tedana derives a mask from the first echo internally. 

(All subsequent sections—masking, echo sanity check, running tedana, tSNR, volume comparison, optional surfaces—remain unchanged.)


1. (Optional) Explicit EPI mask
If --mask is not provided, tedana derives a mask from the first echo using Nilearn’s compute_epi_mask. Provide an explicit mask for reproducibility if you prefer.

        scripts\make_mask.py
   Replace: ① ②

        import os
        import nibabel as nib
        from nilearn.masking import compute_epi_mask  # see official API  [3](https://blog.csdn.net/weixin_45090728/article/details/114285892)
        
        # ① set your Echo‑1 NIfTI path
        epi_path = r"D:\MEICA\raw\sub-01\sub-01_task-rest_echo-1_bold.nii.gz"
        
        # ② set your desired output path for the mask (directories will be created)
        out_path = r"D:\MEICA\MEICA-derivatives\masks\sub-01\sub-01_task-rest_mask.nii.gz"
        
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        img = nib.load(epi_path)
        mask_img = compute_epi_mask(img)
        mask_img.to_filename(out_path)
        print("Saved mask:", out_path)


2. Sanity check: dimensions & length across echoes
   
        scripts\check_me.py
    Replace: ③

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


3. Run the full ME‑ICA workflow with tedana (T2/S0, OC, ICA, classification, denoising)
   
   Command‑line options (from the official docs & API)
   
    -d: Provide echo‑wise 4D NIfTI files in ascending TE order
   
    -e: Echo times (BIDS recommends seconds; milliseconds are still accepted but deprecated).
Example: 15.2 ms / 34.23 ms / 53.26 ms → 0.0152 0.03423 0.05326.

    --out-dir: Output directory (created if missing).

   --prefix: Common filename prefix for all outputs.

   --convention bids: Use BIDS Derivatives naming (e.g., desc-optcom_bold.nii.gz, desc-denoised_bold.nii.gz).

   --fittype: T2* fitting — loglin (default) or curvefit.

   --mask: Optional explicit mask (see Section 1). If omitted, tedana internally calls compute_epi_mask to derive an adaptive mask.

   --n-threads: Number of threads. [tedana.rea...thedocs.io]

   Internals: PCA→ICA decomposition; TE‑dependence metrics (Kappa/Rho) + decision tree for BOLD vs. non‑BOLD classification; non‑BOLD time series are regressed out from OC to yield the denoised output.

    Replace ④–⑧
    
       tedana ^
          -d ^
          "D:\MEICA\raw\sub-01\sub-01_task-rest_echo-1_bold.nii.gz" ^  rem ④ your echo‑1
          "D:\MEICA\raw\sub-01\sub-01_task-rest_echo-2_bold.nii.gz" ^  rem ⑤ your echo‑2
          "D:\MEICA\raw\sub-01\sub-01_task-rest_echo-3_bold.nii.gz" ^  rem ⑥ your echo‑3
          -e 0.0152 0.03423 0.05326 ^                                  rem ⑦ your TEs (seconds; BIDS‑recommended)  [1](https://tedana.readthedocs.io/en/24.0.0/generated/tedana.workflows.tedana_workflow.html)
          --out-dir "D:\MEICA\MEICA-derivatives\tedana\sub-01_task-rest" ^  rem ⑧ your output dir
          --prefix sub-01_rest_ ^
          --convention bids ^
          --fittype curvefit ^
          --n-threads 8
          rem (optional) --mask "D:\MEICA\MEICA-derivatives\masks\sub-01\sub-01_task-rest_mask.nii.gz"
   Core outputs from this single command (BIDS derivatives):
   
    (Path: D:\MEICA\MEICA-derivatives\tedana\sub-01_task-rest\)

   * sub-01_rest_desc-optcom_bold.nii.gz — Optimally combined (OC) 4D time series.

   * sub-01_rest_desc-denoised_bold.nii.gz — ME‑ICA denoised 4D time series (non‑BOLD ICs regressed out of OC); recommended for downstream analysis. 
   
   * sub-01_rest_T2starmap.nii.gz, sub-01_rest_S0map.nii.gz — T2*/S0 maps.

   * sub-01_rest_desc-adaptiveGoodSignal_mask.nii.gz — Adaptive mask used internally.

   * sub-01_rest_desc-ICA_components.nii.gz, sub-01_rest_desc-ICA_mixing.tsv — ICA spatial maps and mixing matrix. 

   * sub-01_rest_desc-accepted_components.txt, ...rejected_components.txt — component classification lists; plus tedana_report.html (interactive report).

   The key→filename mapping for these BIDS outputs is tabulated in the “Outputs of tedana” documentation, which also explains classification products and the report structure

4. Compute tSNR for TE2, OC, and ME‑ICA
   
    Definition: mean/std per voxel over time; AFNI’s 3dTstat -tsnr computes |mean|/stdev (no detrend), equivalent for comparison purposes.

        scripts\make_tsnr.py
    
    Replace: ⑨–⑫

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

   
5.  Main path: Volume‑space comparison only (no surfaces) with fixed range ([-100, 100])
   
    Load the three volume tSNR maps side‑by‑side or overlaid

        tsnr_TE2_raw.nii.gz
        tsnr_OC.nii.gz
        tsnr_MEICA_denoised.nii.gz

    Open them in Workbench to compare TE2 vs OC vs ME‑ICA; no surface mapping is required. in Workbench palette options，choose videen_style and use fix range [-100, 100].


6. Key tedana stages & outputs (Sources)

    T2*/S0 fitting: monoexponential S(TE)=S0e−TE/T2\*S(TE)=S_0 e^{-TE/T2^\*}S(TE)=S0​e−TE/T2\*, --fittype loglin/curvefit.
   
    Optimal Combination (OC): voxelwise T2*‑weighted combination across echoes → desc-optcom_bold.nii.gz.
   
    ICA & classification: TE‑dependence metrics (Kappa/Rho) + decision tree → accepted/rejected component lists and tedana_report.html.
   
    BIDS derivatives: --convention bids provides standardized names and a registry mapping keys to files.
   
    Masking: if --mask is omitted, Nilearn’s compute_epi_mask is used internally on Echo‑1. 















