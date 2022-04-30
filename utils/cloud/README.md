# util/cloud : Miscellaneous tools for cloud operation

* update-sg.sh
    * A tiny script to update AWS Security Group Rule.
	* Useful for SG rule catching up with your home IP change.
	* Install awscli, curl, jq and configure at lesat the following environment variables:
	    * PROFILE, REGION, SG_ID, SGR_ID
        * RANGE is up to you. In case of me, I'm using 32 (unicast).
