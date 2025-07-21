<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST["email"];
    $password = $_POST["password"];
    
    $directory = "user_data";
    $filename = $directory . "/" . $email . ".txt";
    
    if (file_exists($filename)) {
        $file_content = file_get_contents($filename);
        preg_match('/Password: (.*)/', $file_content, $matches);
        
        if (!empty($matches) && $matches[1] === $password) {
            echo "<script> window.location.href = 'upload.html';</script>";
        } else {
            echo "<script>alert('Incorrect password!'); window.history.back();</script>";
        }
    } else {
        echo "<script>alert('Email not found! Please register first.'); window.history.back();</script>";
    }
}
?>
