<?php
$myPDO = new PDO('pgsql:host=ec2-54-225-242-183.compute-1.amazonaws.com;dbname=d3c2hbdtu8ra5c', 'ekirkjbjamwpuk', 'ac7ebcbf546993450ac6081d88b0c3d92cb2d856b4d99d2cd74c0b379cbc8c09');
$sql = "INSERT INTO answers (aid, answer) VALUES (?,?)";
$stmt = $myPDO->prepare($sql);
$stmt->execute([$id,$x]);




?>
