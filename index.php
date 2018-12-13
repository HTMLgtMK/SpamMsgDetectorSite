<!DOCTYPE html>
<html>
<?php
/**
 * index  page for spam msg
 * 2018/12/11
 * author: GT
 */
?>
<head>
	<title>Spam Msg Detect</title>
	<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
	<style type="text/css">
		body { background: #eee; margin: 0; padding: 0; height: 100%; }
		#title{ font-size: 20px; color: #fff; background: #33A2FF; padding: 20px; }
		/* left panel */
		.container{ text-align: center; width: 50%; margin: 0 auto; background: #fff; font-size: 20px; padding: 20px 0; }
		.container-title { margin-top: 20px; }
		#left-container{ float: left; }
		#msg{ width: 80%; height: 200px; }
		#classifier{ width: 80%; max-height: 50px; }
		#classifier-label {margin-left: 10%; margin-top: 20px; text-align: left; font-size: 20px;}
		button{ background: #3361FF; border-radius: 5px; color: #fff; padding: 10px; }
		#submit{ margin-top: 20px; width: 60%; }
		#description{ margin-top: 20px; margin-left: 10%; text-align: left; font-size: 20px; }
		/* right panel */
		#right-container{ float: right; }
		#result-msg { margin: 0 auto; text-align: center; font-size: 20px; width: 80%; height: 80%; border: 1px solid #c0c2c4;}

		.clearfix{ display: block; content: ""; clear: both; }
		footer{text-align: center; background: #ccccff; padding: 10px; margin-bottom: 0px; width: 100%;}
	</style>
	<script type="text/javascript" src="./resource/js/jquery-3.3.1.min.js"></script>
</head>
<?php $classifier_name = [ "all", "transformer, attention", "LR", "DT", "SVM", "GBDT"]; ?>
<body>
	<div id="title">Spam Message Detect</div>
	<div id="left-container" class="container">
		<div class="container-title">&nbsp;</div> <!-- just for align right panel top -->
		<div id="main">
			<form>
				<textarea id="msg" name="msg" autocomplete="off" placeholder="please put your message here"></textarea>
				<br/>
				<div id="classifier-label">classifier</div>
				<select id="classifier" name="classifier" multiple>
					<?php 
						foreach ($classifier_name as $k => $v) {
							echo "<option value=\"$k\">$v</option>";
						}
					?>
				</select>
				<br/>
				<button type="button" id="submit">Check</button>
			</form>
		</div>
		<div id="description">
			help:<br/>
			&nbsp; &nbsp; We have implement five different classifers: transformer attention, Logistic regression, Decission tree, SVM, GBDT.
			<br/>
			&nbsp; &nbsp; You can choose some of the classifier in the multiple selctor.
		</div>
	</div><!-- end of left panel -->
	<dir id="right-container" class="container">
		<div id="result-title" class="container-title">Results</div>
		<div id="result-msg">&nbsp;</div>
	</dir>
	<div class="clearfix"></div>
	<footer>Powered by Apache2. PHP7. Author: GT</footer>
<script type="text/javascript">
$(document).ready(function(){
	$("#submit").click(submit);
	$("#right-container").height( $("#left-container").height());
});
var classifier_name = ["all", "transformer, attention", "LR", "DT", "KNN", "GBDT"];
function submit(){
	var msg = $("#msg").val();
	var classifers = $("#classifier").val();
	for(var i=0; i<classifers.length; ++i) classifers[i]=parseInt(classifers[i]);
	$("#result-msg").html("");
	var real ;
	if($.inArray(0, classifers) != -1){ real = new Array(1,2,3,4,5); }
	else{ real=classifers; } 
	console.log(real);
	for (var i = 0; i < real.length; ++i) {
		var classifier = real[i];
		$.ajax({
			url: "./run.php",
			async: true,
			method: "POST",
			data: {
				"msg": msg,
				"classifier": classifier
			},
			dataType: "text", /* json */
			error: function(jqXHR, textStatus, errorThrown){
				console.log("error: "+textStatus);
				var div_info = $("<div>").html(textStatus);
				$("#result-msg").append(div_info);
			},
			success: function( data, textStatus, jqXHR ){
				console.log("success:" + textStatus + " "+ data);
				data = JSON.parse(data);
				console.log(data);
				var info = "";
				if(data.status == 0){
					info = "No Message!<br/>";
				}else if(data.status == 1){
					var obj = data.prediction;
					info = info + obj['classifier'] + "&nbsp;&nbsp;------ &nbsp;&nbsp; prediction: ";
					if(obj['prediction'] == 0){ info = info + " 0 (Not Spam) <br/>" ; }
					else{ info = info + " 1 (Spam Message) <br/>" ; }
				}
				var div_info = $("<div>").html(info);
				$("#result-msg").append(div_info);
			}
		});
	}
	return false;
}
</script>
</body>
</html>