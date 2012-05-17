
<?php
$myFile = "/var/www/dataFile.txt";
$fh = fopen($myFile,'r') or die("can't open file");
$stringPlayList = fread($fh,filesize($myFile));
fclose($fh);

$order = array("/musicdrive/WMA/");
$stringPlayList = str_replace($order,"",$stringPlayList);

$order = array("/");
$stringPlayList = str_replace($order," ",$stringPlayList);

$order = array("\r\n", "\n", "\r");
$replace = "</trackdescription></track><track><trackdescription>";
$stringPlayList = str_replace($order,$replace,$stringPlayList);

$order = array(".mp3", ".wma");
$replace = "";
$stringPlayList = str_replace($order,$replace,$stringPlayList);


$stringPlayList = "<tracks><track><trackdescription>".$stringPlayList."</tracks>";

$order = array("<track><trackdescription></tracks>");
$replace = "</tracks>";
$stringPlayList = str_replace($order,$replace,$stringPlayList);

echo $stringPlayList;

?>

