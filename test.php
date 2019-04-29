<?php
$myPDO = new PDO('pgsql:host=ec2-54-225-242-183.compute-1.amazonaws.com;dbname=d3c2hbdtu8ra5c', 'ekirkjbjamwpuk', 'ac7ebcbf546993450ac6081d88b0c3d92cb2d856b4d99d2cd74c0b379cbc8c09');
$sql = "SELECT * FROM transfer";
$result = $myPDO->prepare($sql);
$result ->execute();
$transfer = $result->fetch(PDO::FETCH_NUM);
$id = $transfer[0];
$problem = $transfer[1];

 ?>
<!DOCTYPE HTML>
<html>
<head>
<link rel="stylesheet" type="text/css" href="style-test.css">

</head>
<body>
</body>

<div id="fullcontain">
<table>
  <tr style="height:210px">
    <td>
      <div id="pointhold">
      <img width=200px height = 200px src="Images/slo.png">
    </div>
    </td>
    <td>
      <div id="pointhold">
      <img width=200px height = 200px src="Images/gro.png">
    </div>
    </td>
  </tr>
<tr>
<td>
<div>
  <p id="thequestion">
  Algorithmetic is a machine learning based math practice website for students and teachers. Algorithmetic uses specialized algorithms to generate new and unique math problems that are tailored for each student based off of their weaknesses. Algorithmetic also gives advanced student performance statistics to teachers so they can improve their in class teaching experience.
</p>
</div>

</td>
<td>
  <?php
    if(isset($_POST['Submit']))
{
$x=$_POST['fnum'];
$myPDO = new PDO('pgsql:host=ec2-54-225-242-183.compute-1.amazonaws.com;dbname=d3c2hbdtu8ra5c', 'ekirkjbjamwpuk', 'ac7ebcbf546993450ac6081d88b0c3d92cb2d856b4d99d2cd74c0b379cbc8c09');
$sql = "INSERT INTO answers (aid, answer) VALUES (?,?)";
$stmt = $myPDO->prepare($sql);
$stmt->execute([$id,$x]);




$qs="false";
$as="true";
$id=1;
$h='hello';
$sql = "UPDATE updates SET as1=?, qs1=? WHERE id=?";
$stmt= $myPDO->prepare($sql);
$stmt->execute([$as, $qs, $id]);




}


?>
<script>

</script>
  <form method="post">
<input height=400px id="theanswer" type="text" name="fnum" value="1"/>
<input id="submitbutton" type="submit"  name="Submit" value="submit"/>
</form>


</td>
</tr>
</table>


</html>
