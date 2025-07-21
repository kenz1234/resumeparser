<!DOCTYPE html>
<html>
<head>
    <title>Aptitude Test</title>
</head>
<body>
    <?php
    session_start();

    $questions = [
        "What does HTML stand for?" => ["Hyper Text Markup Language", "High Tech Modern Language", "Hyperlink and Text Management Language", "Home Tool Markup Language"],
        "Which language is used for web development?" => ["Java", "C++", "JavaScript", "Python"],
        "What is PHP mainly used for?" => ["Frontend scripting", "Server-side scripting", "Database management", "Game development"],
        "Which is not a programming language?" => ["Python", "Java", "C++", "HTTP"],
        "What is the primary language for Android development?" => ["Swift", "Kotlin", "Java", "C#"],
        "Which database is commonly used with PHP?" => ["MongoDB", "MySQL", "Oracle", "PostgreSQL"],
        "Which of the following is a version control system?" => ["Git", "Linux", "Apache", "Docker"],
        "What does CSS stand for?" => ["Computer Style Sheets", "Cascading Style Sheets", "Creative Style Syntax", "Code Styling System"],
        "Which language is best for data science?" => ["Ruby", "Perl", "Python", "Go"],
        "What does API stand for?" => ["Application Programming Interface", "Advanced Processing Input", "Automated Program Interaction", "Applied Protocol Integration"]
    ];

    $correct_answers = [
        "What does HTML stand for?" => "Hyper Text Markup Language",
        "Which language is used for web development?" => "JavaScript",
        "What is PHP mainly used for?" => "Server-side scripting",
        "Which is not a programming language?" => "HTTP",
        "What is the primary language for Android development?" => "Java",
        "Which database is commonly used with PHP?" => "MySQL",
        "Which of the following is a version control system?" => "Git",
        "What does CSS stand for?" => "Cascading Style Sheets",
        "Which language is best for data science?" => "Python",
        "What does API stand for?" => "Application Programming Interface"
    ];


    $keys = array_keys($questions);
    shuffle($keys);
    $random_questions = array_slice($keys, 0, 10);


    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $score = 0;
        foreach ($random_questions as $question) {
            if (isset($_POST[md5($question)]) && $_POST[md5($question)] === $correct_answers[$question]) {
                $score++;
            }
        }
        $_SESSION['score'] = $score;
        if ($score == 10) {
            echo "<p>Congratulations! You scored 10/10. <a href='upload.html'>Proceed to Next Page</a></p>";
        } else {
            echo "<p>Your score: $score/10. You have failed the test. Session terminated.</p>";
            session_destroy();
        }
        exit();
    }
    ?>

    <h2>Aptitude Test</h2>
    <form method="POST">
        <?php
        foreach ($random_questions as $question) {
            echo "<p>$question</p>";
            foreach ($questions[$question] as $option) {
                echo "<input type='radio' name='" . md5($question) . "' value='$option' required> $option<br>";
            }
            echo "<br>";
        }
        ?>
        <input type="submit" value="Submit">
    </form>
</body>
</html>