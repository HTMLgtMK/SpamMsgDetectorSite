<?php
/**
 * Run.php is a interface to python API
 * author: GT
 * time: 2018/12/11 21:22
 */
if(empty($_POST)){
	echo "{'status':0}";
	return;
}
$data = $_POST;
$msg = $data['msg'];
$classifier = $data['classifier'];

$classifier_name = [ "all", "transformer, attention", "LR", "DT", "SVM", "GBDT"];
$result = []; // results of all the prediction
$result['status'] = 1;

$name = $classifier_name[$classifier];
if($classifier == 1){
	$cmd_str = "cd ./Model/Transformer-Spam-message-classification;python2 runAPI.py --msg=\"$msg\"";
}else{
	$cmd_str = "cd ./Model/spam_detect; python2 runAPI.py --classifier=$name --msg=\"$msg\"";
}
exec($cmd_str, $ret);
$ret = $ret[count($ret)-1];

$obj = array( 'classifier' => $name, 'prediction' => intval($ret));
$result['prediction'] = $obj;
echo json_encode($result);
?>