<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST["email"];
    $password = $_POST["password"];
    $confirm_password = $_POST["confirm-password"];

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo "<script>alert('Invalid email format!'); window.history.back();</script>";
        exit();
    }

    if ($password !== $confirm_password) {
        echo "<script>alert('Passwords do not match!'); window.history.back();</script>";
        exit();
    }



    $directory = "user_data";
    if (!is_dir($directory)) {
        mkdir($directory, 0777, true);
    }


    $filename = $directory . "/" . $email . ".txt";
    $user_data = "Email: " . $email . "\nPassword: " . $password . "\n";

    if (file_put_contents($filename, $user_data) !== false) {
        echo "<script>alert('Registration successful! Redirecting to login page...'); window.location.href = 'login.html';</script>";
    } else {
        echo "<script>alert('Error saving user data! Please try again.'); window.history.back();</script>";
    }
}
?>
