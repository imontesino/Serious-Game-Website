
<html>
  <head>
   <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
    <!--[if IE]>
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <![endif]-->
    <title>Affectation d'une tache</title>
 
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
    
    <link href="static/assets/css/bootstrap.css" rel="stylesheet" />
    
    <link href="static/assets/css/font-awesome.min.css" rel="stylesheet" />
    
    <link href="static/assets/css/style.css" rel="stylesheet" />
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
  </head>
  <body>
  <div class="row main-top-margin text-center">
<div class="col-md-8 col-md-offset-2 col-sm-10 col-sm-offset-1" data-scrollreveal="enter top and move 100px, wait 0.5s">
<h1>Formulaire d'affectation d'une tache</h1>
<h4>
Veuillez renseigner les informations ci-dessous pour programmer une tache
 </h4>
</div>
</div>

<?php
$bdd = new PDO("mysql:host=127.0.0.1;dbname=atelier_fabrication;charset=utf8","root","");
$requete = $bdd->prepare("insert into tache(code_tache,code_resp,code_tec,type_tache,date_debut,date_fin) values(?,?,?,?,?,?)");
$requete->execute(array($_POST['code_tache'],$_POST['code_resp'],$_POST['code_tec'],$_POST['type_tache'],$_POST['date_debut'],$_POST['date_fin']));
?>

 <br><br><br><br><a href="ajout_tache.html"> Retour a la page precedante<a> <br><br><br><br>
  </body>
  <div class="navbar navbar-inverse navbar-fixed-top">
        <div class="container">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="#">Atelier de fabrication KMNO</a>
            </div>
</html>
