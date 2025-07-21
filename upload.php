<?php

$targetDir = "C:/Users/Kenz/PycharmProjects/PythonProject/Resumestr/";


if (!is_dir($targetDir)) {
    mkdir($targetDir, 0777, true);
}


if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_FILES["file"])) {
    $fileName = basename($_FILES["file"]["name"]);
    $targetFilePath = $targetDir . $fileName;
    $fileType = pathinfo($targetFilePath, PATHINFO_EXTENSION);


    $allowedTypes = [ "pdf"];
    if (in_array(strtolower($fileType), $allowedTypes)) {
        if ($_FILES["file"]["error"] === UPLOAD_ERR_OK) {
            if (move_uploaded_file($_FILES["file"]["tmp_name"], $targetFilePath)) {
                echo "<script>
                        alert('Your file is uploaded. Have a nice day!');
                        window.location.href = 'login.html';
                      </script>";
                exit(); 
            } else {
                echo "<script>
                        alert('Sorry, uploaded file have some error please try again!');
                        window.location.href = 'upload.html';
                        </script>";
            }
        } else {
            echo "Error: " . $_FILES["file"]["error"];
        }
    } else {
        echo "<script>
                        alert('Sorry, only PDF files are allowed please check your file!');
                        window.location.href = 'upload.html';
                        </script>";
    }
} else {
    echo "No file was uploaded.";
}
?>
