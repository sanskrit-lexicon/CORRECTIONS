<?php
 $outar=array();
 // date-time stamp: 3/18/2014 14:48:54
 $outar[]=date("m/d/Y H:i:s");
 $columns=array("entry_dict","entry_L","entry_hw","entry_old",
  "entry_new","entry_comment","entry_email");
 foreach($columns as $postkey) {
  if (isset($_POST[$postkey])) {
   $val = $_POST[$postkey];
   // Alter newline and tab
   $val = preg_replace("|[\n\r]+|"," LB ",$val);
   $val = preg_replace("|[\t]|","  ",$val);  
  }else {
   $val = "";
  }
  #$outar[]="$postkey=$val";
  $outar[]=$val;
 }
/*
 foreach($_POST as $key=>$val) {
  $outar[]="$key->$val";
 }
*/
 $out = join("\t",$outar);
 // Append 'out' to two files
 // (a) correction_response/cfr-yyyymmdd.tsv
 $filedate = date("Ymd");
 $fileout = "correction_response/cfr-$filedate.tsv";
 $fp = fopen($fileout,"a");
 fwrite($fp,"$out\n");
 fclose($fp);
 // (b) correction_response/cfr.tsv
 $fileout = "correction_response/cfr.tsv";
 $fp = fopen($fileout,"a");
 fwrite($fp,"$out\n");
 fclose($fp);

?>
