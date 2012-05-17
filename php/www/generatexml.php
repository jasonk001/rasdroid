<html>
<head>
<title>Add To PlayList</title>
</head>
<body>
<?php

passthru('/usr/bin/python /var/www/droidplayerxmlgen.py 1 2>&1',$retval);

echo $retval

?>

</body>
</html>
