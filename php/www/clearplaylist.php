<html>
<head>
<title>Clear PlayList</title>
</head>
<body>
<?php

$myFile = "/var/www/dataFile.txt";
$fh = fopen($myFile,'w') or die("can't open file");
$stringData ="";
fwrite($fh,$stringData);
fclose($fh);
echo '<p>Playlist cleared</p>';
?>
</body>
</html>
