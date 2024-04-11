# Dumps information

Dumps were taken within ACR122 + nfc-ltocm tool, and proxmark3.
They're differs in size, at least. (I not checked the content yet).

Dumps are structured according cartridge manufacturers, branded at cartridge case. (Real manufacturer, however, can be another. Like Dell-branded tapes are actually manufactured by Fujifilm.

Brand-new tape's dumps placed into "brand-new" subfolder of each brand.

Proxmark dumps have it's own default names, like _"hf-lto-9BC2991ADA-dump.bin"_ and placed in the same folder with ACR's dumps.

I give more detailed filenames to the ACR's dumps:

	L<n>-<serial>[-<barcode>].bin
    
where:  
	**n** is LTO generation,  
	**serial** is NFC serial number,
    **barcode** is case-label, if exist
    
Also some cartridges has hand-written **cross** on it's case (i think it indicates some sort of fault). These dumps have **-x** suffix in name.

Since nfc-tool unable to dump LTO-6 tapes, they're placed into "fixme_L6" folder for future processing.