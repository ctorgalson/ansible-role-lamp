<html>
  <body>
    <h1>PHP <?php echo phpversion(); ?></h1>
    <div>
    <?php
      $h = 'localhost';
      $d = 'lamp_db';
      $u = 'lamp_user';
      $p = 'lamp_user_password';

      try {
        $connection = new PDO("mysql:host=$h;dbname=$d", $u, $p);
        $connection->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
      }
      catch (PDOException $e) {
        echo 'ERROR: ' . $e->getMessage();
      }

      $dbs = $connection->query('SHOW DATABASES');

      while (($db = $dbs->fetchColumn(0)) !== FALSE) {
        echo $db . '<br>';
      }
    ?>
    </div>
  </body>
</html>
