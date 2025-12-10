<?php 
@unlink("exploit.phar");
@unlink("exploit.phar.gz");
$phar = new Phar('exploit.phar'); 
$phar->startBuffering(); 
$code1 = <<<'EOD'
<?php 
    echo "Phar stub executed\n";
    __HALT_COMPILER(); 
?> 
EOD; 

$code2 = <<<'EOD'
<?php 
    echo "Phar index.php executed\n";
?> 
EOD; 

$phar->setStub($code1); 
$phar->addFromString('index.php', $code2); 

$phar->compress(Phar::GZ);

$phar->stopBuffering();

?>