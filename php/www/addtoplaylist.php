<html>
<head>
<title>Add To PlayList</title>
</head>
<body>
<?php

$myFile = "/var/www/dataFile.txt";
$fh = fopen($myFile,'a') or die("can't open file");
$stringData = $_GET['song'];
fwrite($fh,$stringData);
fwrite($fh,"\n");
fclose($fh);

$fh = fopen($myFile,'r') or die("can't open file");
$stringPlayList = fread($fh,filesize($myFile));
fclose($fh);
echo '<p>Playlist updated</p>';
$order = array("\r\n", "\n", "\r");
$replace = "<br />";

$stringPlayList = str_replace($order,$replace,$stringPlayList);
echo $stringPlayList;

?>

</body>
</html>
