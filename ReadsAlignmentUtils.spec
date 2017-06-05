
/**
    A KBase module: ReadsAlignmentUtils

    This module is intended for use by Aligners and Assemblers to upload and download alignment files.
    The alignment may be uploaded as .sam or .bam files. Once uploaded, the alignment can be
    downloaded in .sam, sorted .bam or .bai file formats. This utility also generates stats from
    the stored alignment.
**/


module ReadsAlignmentUtils {

   /* A boolean - 0 for false, 1 for true.
       @range (0, 1)
   */
   typedef int boolean;
   typedef string ws_bowtieIndex_id;
   typedef string ws_Sampleset_id;

   /** Input parameters for validating a reads alignment **/

   typedef structure {
       string file_path;    /* path to sam or bam file generated by
                               the alignment program */
       list<string> ignore; /* Optional. List of validation errors to ignore.
                               Default: ['MATE_NOT_FOUND','MISSING_READ_GROUP',
                                         'INVALID_MAPPING_QUALITY']
                               See http://broadinstitute.github.io/picard/command-line-overview.html#ValidateSamFile */
   }  ValidateAlignmentParams;


   /** Results from validate alignment **/

   typedef structure {
       boolean validated;
   } ValidateAlignmentOutput;


   funcdef  validate_alignment(ValidateAlignmentParams params)
            returns (ValidateAlignmentOutput)
            authentication required;

   /**

      Required input parameters for uploading a reads alignment

      string destination_ref -  object reference of alignment destination. The
                                object ref is 'ws_name_or_id/obj_name_or_id'
                                where ws_name_or_id is the workspace name or id
                                and obj_name_or_id is the object name or id

	  file_path      -  Source: file with the path of the sam or bam file to be uploaded

	  library_type   - ‘single_end’ or ‘paired_end’
	  condition      - experimental condition (test, control etc.)
	  genome_id      -  workspace id of genome annotation that was
                            used to build the alignment
      read_sample_id    -  workspace id of read sample used to make
                            the alignment file

    **/

   typedef structure {

       string destination_ref;
       string file_path;

	   string library_type;
	   string condition;
       string genome_id;
	   string read_sample_id;

       string aligned_using;             /* Optional ‘hisat2’, ‘tophat2’, ‘bowtie2’ or some other aligner name */
       string aligner_version;           /* Optional */
       mapping<string opt_name, string opt_value> aligner_opts;  /* Optional */

       string replicate_id;              /* Optional. Id of biological replicate for a given condition */
       string platform;                  /* Optional */
       ws_bowtieIndex_id bowtie2_index;  /* Optional */

       ws_Sampleset_id sampleset_id;     /* Optional. workspace id of sample_set to which
                                            the read_sample_id may belong  **/

       mapping<string condition,mapping<string sample_id , string replicate_id>> mapped_sample_id; /* Optional */

       boolean validate; /* Optional. Set to True if input needs to be validated. Default: False */

       list<string> ignore; /* Optional. List of validation errors to ignore.
                               Default: ['MATE_NOT_FOUND','MISSING_READ_GROUP',
                                        'INVALID_MAPPING_QUALITY']
                               See http://broadinstitute.github.io/picard/command-line-overview.html#ValidateSamFile */

   }  UploadAlignmentParams;


   /**  Output from uploading a reads alignment  **/

    typedef structure {
        string obj_ref;
    } UploadAlignmentOutput;


   /**  Validates and uploads the reads alignment  **/

     funcdef upload_alignment(UploadAlignmentParams params)
                     returns (UploadAlignmentOutput)
                     authentication required;

    /**

      Required input parameters for downloading a reads alignment

      string source_ref -  object reference of alignment source. The
                           object ref is 'ws_name_or_id/obj_name_or_id'
                           where ws_name_or_id is the workspace name or id
                           and obj_name_or_id is the object name or id
    **/

     typedef structure {

        string ws_id_or_name;
        string obj_id_or_name;
        boolean downloadBAM;    /*  Optional - default is True */
        boolean downloadSAM;    /*  Optional - default is False */
        boolean downloadBAI;    /*  Optional - default is False */
        boolean validate; /* Optional. Set to true if input needs to be validated. Default: False */
        list<string> ignore; /* Optional. List of validation errors to ignore.
                              Default: ['MATE_NOT_FOUND','MISSING_READ_GROUP',
                                        'INVALID_MAPPING_QUALITY']
                              See http://broadinstitute.github.io/picard/command-line-overview.html#ValidateSamFile */

     } DownloadAlignmentParams;


    /** @optional singletons multiple_alignments, properly_paired,
                  alignment_rate, unmapped_reads, mapped_sections total_reads,
                  mapped_reads
    **/

     typedef structure {
         int    properly_paired;
         int    multiple_alignments;
         int    singletons;
         float  alignment_rate;
         int    unmapped_reads;
         int    mapped_reads;
         int    total_reads;
     } AlignmentStats;


    /**  The output of the download method.  **/

     typedef structure {
         string ws_id;     /* source */
         string bam_file;  /* file name along with path  */
         string sam_file;  /* file name along with path  */
         string bai_file;  /* file name along with path  */
         AlignmentStats stats;
     } DownloadAlignmentOutput;


     /** Downloads alignment files in .bam, .sam and .bai formats. Also downloads alignment stats **/

      funcdef download_alignment(DownloadAlignmentParams params)
                         returns (DownloadAlignmentOutput)
                         authentication required;

    /**

      Required input parameters for exporting a reads alignment

      string source_ref -  object reference of alignment source. The
                           object ref is 'ws_name_or_id/obj_name_or_id'
                           where ws_name_or_id is the workspace name or id
                           and obj_name_or_id is the object name or id
    **/

     typedef structure {
         string source_ref;   /* workspace object reference */
     } ExportParams;

     typedef structure {
         string shock_id;    /* shock id of file to export */
     } ExportOutput;


    /** Wrapper function for use by in-narrative downloaders to download alignments from shock **/

     funcdef export_alignment(ExportParams params)
                     returns (ExportOutput output)
                     authentication required;
};
