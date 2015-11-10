<?php
/* General purpose correction form for Sanskrit-Lexicon.
    Mar 17, 2014
   Accepts some url parameters:
    dict  A dictionary identifier
*/
 $dict = $_GET['dict'];
 if (!$dict) {$dict = '?';}

?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>

<meta http-equiv="Content-type" content="text/html; charset=utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=10; chrome=1;">
<meta name="fragment" content="!">
<base target="_blank">
<title>Sanskrit-Lexicon Correction Form </title>

<!--
<link href='https://docs.google.com/static/forms/client/css/656316836-formview_ltr.css' type='text/css' rel='stylesheet'>
-->
<link href='correction_form.css' type='text/css' rel='stylesheet'>

<style type="text/css">

</style>

<meta name="viewport" content="width=device-width">
<!--
<link href='/static/forms/client/css/1393690164-mobile_formview_ltr.css' type='text/css' rel='stylesheet' media='screen and (max-device-width: 721px)'>
-->

</head>
<!--
<p style="color:red; text-align:center">
The correction form is broken.  
<br/>Please save your correction and resubmit
in a day or two.
</br> We apologize for the inconvenience.  (Nov 5, 2015)
</p>
<hr/>
-->
<body dir="ltr" class="ss-base-body">
<div itemscope itemtype="http://schema.org/CreativeWork/FormObject">
<!--
<meta itemprop="name" content="Sanskrit-Lexicon Correction Form ">
<meta itemprop="description" content="Instructions:  http://www.sanskrit-lexicon.uni-koeln.de/doc/corrections/help.html">

<meta itemprop="url" content="https://docs.google.com/forms/d/1InNaDMuakzrKpkSXlzVn0ocnD3My2uBMWypUEebrO4c/viewform">
<meta itemprop="embedUrl" content="https://docs.google.com/forms/d/1InNaDMuakzrKpkSXlzVn0ocnD3My2uBMWypUEebrO4c/viewform?embedded=true">
<meta itemprop="faviconUrl" content="https://ssl.gstatic.com/docs/spreadsheets/forms/favicon_jfk2.png">
<a class="ss-edit-link" href="https://docs.google.com/forms/d/1InNaDMuakzrKpkSXlzVn0ocnD3My2uBMWypUEebrO4c/edit">Edit this form</a>

-->

<div class="ss-form-container"><div class="ss-top-of-page">


<div class="ss-form-heading">

<h1 class="ss-form-title" dir="ltr">Sanskrit-Lexicon Correction Form </h1>
<h3>For typographical errors</h3>
<div class="ss-form-desc ss-no-ignore-whitespace"> 
<a href="http://www.sanskrit-lexicon.uni-koeln.de/doc/corrections/help.html"
 target="CorrectionHelp">Instructions</a>. (Also help via tooltips).
</div>

<hr class="ss-email-break" style="display:none;">
<div class="ss-required-asterisk" style="display:none">* Required</div></div></div>

<div class="ss-form">
<script type="text/javascript">var submitted=false;</script>
    <iframe name="hidden_iframe" id="hidden_iframe" style="display:none;"     
onload="if(submitted) {window.location='correction_form_thankyou.php';submitted=false;}">
    </iframe>
<form action="correction_form_response.php"
<?php
 //$action = '"https://docs.google.com/forms/d/1InNaDMuakzrKpkSXlzVn0ocnD3My2uBMWypUEebrO4c/formResponse"';
 //echo $action;
?>
 method="post" target="hidden_iframe" 
onsubmit="submitted=true;">
<div class="ss-form-question errorbox-good">
<div dir="ltr" class="ss-item ss-item-required ss-text"><div class="ss-form-entry"><label aria-hidden="true" class="ss-q-item-label" for="entry_dict"><div class="ss-q-title" title="Prefilled. Do not change">Which Dictionary?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" title="Required">*</span>
&nbsp;&nbsp;
<?php
/* Use 'id' field of <input> to match with names in correction_form_response.php
   Leave 'name' field unchanged from the one originally used by Google
*/
 //$val = "<input type=\"text\" name=\"entry.1072768805\" value=\"$dict\" class=\"ss-q-short\" id=\"entry_1072768805\" dir=\"auto\" aria-label=\"Which Dictionary?  \" aria-required=\"true\" required=\"\" style=\"width:80px;position:relative;left:50px;\"  ></input>";
 $val = "<input type=\"text\" name=\"entry_dict\" value=\"$dict\" class=\"ss-q-short\" id=\"entry_dict\" dir=\"auto\" aria-label=\"Which Dictionary?  \" aria-required=\"true\" required=\"\" style=\"width:80px;position:relative;left:50px;\"  ></input>";
 echo $val;
?>
<div class="error-message"></div>
</div>

</div></div></div> 

<div class="ss-form-question errorbox-good">
<div dir="ltr" class="ss-item ss-item-required ss-text">
<div class="ss-form-entry">
 <label aria-hidden="true" class="ss-q-item-label" for="entry_L">
  <div class="ss-q-title" title="Record # where typo noticed. See Help.">Which L code?
  <label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
  <span class="ss-required-asterisk" title="Required">*</span>
  <div class="ss-q-help ss-secondary-text" dir="ltr" style="display:none;">This is number appears on the display as L=1234.</div>
 </label>
&nbsp;&nbsp;
<input type="text" name="entry_L" 
 value="
<?php
 if ($dict == 'APES'){
  echo "0(NA)";
 }else {
  echo "";
 }
?>
 " 
 class="ss-q-short" id="entry_L" dir="auto" aria-label="Which L code?  " aria-required="true" required="" title="" style="width:80px;position:relative;left:70px;">
<div class="error-message"></div>
<div class="required-message" style="display:none;">This is a required question</div>
</div></div></div> 

<div class="ss-form-question errorbox-good">
<div dir="ltr" class="ss-item ss-item-required ss-text">
<div class="ss-form-entry">
 <label aria-hidden="true" class="ss-q-item-label" for="entry_hw">
  <div class="ss-q-title" title="The headword where typo noticed">Which Headword?
  <label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
  <span class="ss-required-asterisk" title="Required">*</span>
  <div class="ss-q-help ss-secondary-text" dir="ltr" style="display:none;">The headword under which you are submitting a correction</div>
 </label>
&nbsp;&nbsp;
<input type="text" name="entry_hw" value="" class="ss-q-short" id="entry_hw" dir="auto" aria-label="Headword The headword under which you are submitting a correction " aria-required="true" required="" title="" style="width:80px;position:relative;left:48px;">
<div class="error-message"></div>
<div class="required-message" style="display:none;">This is a required question</div>
</div>
</div></div></div> 

<div class="ss-form-question errorbox-good">
<div dir="ltr" class="ss-item  ss-paragraph-text">
<div class="ss-form-entry">
 <label aria-hidden="true" class="ss-q-item-label" for="entry_old">
  <div class="ss-q-title" title="The text that is wrong">What is the typo?
  <div class="ss-q-help ss-secondary-text" dir="ltr" style="display:none;">The text that is wrong</div>

 </label>
 </div>
<textarea name="entry_old" rows="2" cols="30" class="ss-q-long" id="entry_old" dir="auto" aria-label="Old  The text that is wrong "></textarea>

<div class="error-message"></div>
<div class="required-message" style="display:none;">This is a required question</div>

</div></div></div> 

<div class="ss-form-question errorbox-good">
<div dir="ltr" class="ss-item  ss-paragraph-text"><div class="ss-form-entry"><label aria-hidden="true" class="ss-q-item-label" for="entry_new">
<div class="ss-q-title" title="The corrected text">What is the correction?
</div>
<div class="ss-q-help ss-secondary-text" dir="ltr" style="display:none";>The text that is correct</div></label>
<textarea name="entry_new" rows="2" cols="40" class="ss-q-long" id="entry_new" dir="auto" aria-label="New The text that is correct "></textarea>
<div class="error-message"></div>
<div class="required-message" style="display:none;">This is a required question</div>

</div></div></div> <div class="ss-form-question errorbox-good">
<div dir="ltr" class="ss-item  ss-paragraph-text"><div class="ss-form-entry"><label aria-hidden="true" class="ss-q-item-label" for="entry_comment"><div class="ss-q-title" title="Typo, scan, other">What kind of error?
</div>
<div class="ss-q-help ss-secondary-text" dir="ltr" style="display:none;">Any additional explanation of the error </div></label>
<textarea name="entry_comment" rows="2" cols="40" class="ss-q-long" id="entry_comment" dir="auto" aria-label="Comment Any additional explanation of the error  ">Typo</textarea>
<div class="error-message"></div>
<div class="required-message" style="display:none;">This is a required question</div>

</div></div></div> <div class="ss-form-question errorbox-good">
<div dir="ltr" class="ss-item  ss-paragraph-text"><div class="ss-form-entry"><label aria-hidden="true" class="ss-q-item-label" for="entry_email"><div class="ss-q-title" title="Your Email Address or Name; Optional"
>Your Name or e-mail ID?
</div>
<div class="ss-q-help ss-secondary-text" dir="ltr" style="display:none;">Optional, if you with to be notified when the correction is made</div></label>
<textarea name="entry_email" rows="1" cols="40" class="ss-q-long" id="entry_email" dir="auto" aria-label="Your Email Address Optional, if you with to be notified when the correction is made "></textarea>
<div class="error-message"></div>
<div class="required-message" style="display:none;">This is a required question</div>

</div></div></div>
<!--
<input type="hidden" name="draftResponse" value="[,,&quot;-720978696993452283&quot;]">
<input type="hidden" name="pageHistory" value="0">
<input type="hidden" name="fbzx" value="-720978696993452283">
-->
<div class="ss-item ss-navigate"><table id="navigation-table"><tbody><tr><td class="ss-form-entry goog-inline-block" id="navigation-buttons" dir="ltr">
<input type="submit" name="submit" value="Submit" id="ss-submit">
<div class="ss-secondary-text" style="display:none;">Never submit passwords through Google Forms.</div></td>
</tr></tbody></table></div></ol></form></div>


<div id="docs-aria-speakable" class="docs-a11y-ariascreenreader-speakable docs-offscreen" aria-live="assertive" role="region" aria-atomic></div></div>

<script type='text/javascript' src='/static/forms/client/js/2161195797-formviewer_prd.js'></script>
<script type="text/javascript">H5F.setup(document.getElementById('ss-form'));_initFormViewer(
          "[100,\x22#ccc\x22,[]\n]\n");
      </script></div>
</body>
</html>
