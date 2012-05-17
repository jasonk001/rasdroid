<?php
// The file
$filePath = "/var/www/dataFile.txt";

// Grab file into an array, by lines
$fileArr = file( $filePath );
$index = $_GET['index'];
// Remove desired line
unset( $fileArr[$index] ); // $fileArr[3] == line #4

$success = FALSE;
if ( file_put_contents( $filePath, implode( '', $fileArr ), LOCK_EX ) )
{
    $success = TRUE;
}
echo $success
?>
