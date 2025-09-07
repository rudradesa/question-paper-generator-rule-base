 <?php
session_start();
require('conn.php');
require 'vendor/autoload.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

if (!isset($_SESSION['register_pending'])) {
    echo "❌ Session expired. Please register again.";
    exit;
}

$user = $_SESSION['register_pending'];
$email = $user['email'];
$code = $user['code'];

$mail = new PHPMailer(true);

try {
    $mail->isSMTP();
    $mail->Host = 'smtp.gmail.com';
    $mail->SMTPAuth = true;
    $mail->Username = '';
    $mail->Password = '';//email vari sys 
    $mail->SMTPSecure = 'tls';
    $mail->Port = 587;

    $mail->setFrom('webwizard1124@gmail.com', 'questly');
    $mail->addAddress($email);
    $mail->isHTML(true);
    $mail->Subject = 'Email Verification Code';
    $mail->Body = "Your verification code is: <b>$code</b>";

    $mail->send();
    header("Location: verify.php");
    exit;
} catch (Exception $e) {
    echo "❌ Mail error: " . $mail->ErrorInfo;
}
?>
