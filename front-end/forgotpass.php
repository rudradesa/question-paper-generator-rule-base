 <?php
      session_start();

?><!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Questly - Reset Password</title>
  <link rel="icon" href="ES.png" type="image/png">
  <style>
    *{
            font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;

    }
    :root {
       --primary: #ff6b00;
            --primary-dark: #e06106ff;
            --secondary: #10b981;
            
      --dark: #1e293b;
      --light: #f8fafc;
      --gray: #64748b;
    }

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    body {
      background-color: var(--light);
      color: var(--dark);
      line-height: 1.6;
      display: flex;
      flex-direction: column;
      min-height: 100vh;
    }

    header {
      background-color: white;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      padding: 1rem 2rem;
      position: fixed;
      width: 100%;
      z-index: 100;
    }

    nav {
      display: flex;
      justify-content: space-between;
      align-items: center;
      max-width: 1200px;
      margin: 0 auto;
      flex-wrap: wrap;
    }

    .logo {
      display: flex;
      align-items: center;
      font-size: 1.8rem;
      font-weight: 700;
      color: var(--primary);
    }

    .logo span {
      color: var(--secondary);
    }

    .nav-links, .auth-buttons {
      display: flex;
      gap: 2rem;
    }

    .nav-links a,
    .auth-buttons a {
      text-decoration: none;
      color: var(--dark);
      font-weight: 500;
      transition: color 0.3s;
    }

    .nav-links a:hover {
      color: var(--primary);
    }

    .hamburger {
      display: none;
      font-size: 2rem;
      cursor: pointer;
      color: var(--primary);
    }

    .form-container {
      max-width: 500px;
      width: 90%;
      margin: 120px auto 40px;
      background-color: white;
      border-radius: 10px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      padding: 2.5rem;
    }

    .form-title {
      text-align: center;
      margin-bottom: 2rem;
      color: var(--dark);
      font-size: 1.8rem;
    }

    .form-subtitle {
      text-align: center;
      margin-bottom: 2rem;
      color: var(--gray);
      font-size: 1rem;
    }

    .reset-form {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .form-group label {
      font-weight: 500;
      color: var(--dark);
    }

    .form-group input {
      padding: 0.8rem 1rem;
      border: 1px solid #e2e8f0;
      border-radius: 5px;
      font-size: 1rem;
      transition: border-color 0.3s;
    }

    .form-group input:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }

    .form-group input::placeholder {
      color: #94a3b8;
    }

    .btn {
      padding: 0.8rem 1.5rem;
      border-radius: 5px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.3s;
      text-decoration: none;
      display: inline-block;
      text-align: center;
      font-size: 1rem;
    }

    .btn-primary {
      background-color: var(--primary);
      color: white;
      border: none;
    }

    .btn-primary:hover {
      background-color: var(--primary-dark);
    }

    .back-link {
      text-align: center;
      margin-top: 1.5rem;
    }

    .back-link a {
      color: var(--primary);
      text-decoration: none;
      font-weight: 500;
      transition: color 0.3s;
    }

    .back-link a:hover {
      color: var(--primary-dark);
      text-decoration: underline;
    }

    .status-message {
      padding: 0.8rem;
      border-radius: 5px;
      margin-bottom: 1.5rem;
      text-align: center;
    }

    .success-message {
      background-color: rgba(16, 185, 129, 0.1);
      color: #065f46;
      border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .error-message {
      background-color: rgba(239, 68, 68, 0.1);
      color: #b91c1c;
      border: 1px solid rgba(239, 68, 68, 0.2);
    }

    footer {
      background-color: var(--dark);
      color: white;
      padding: 3rem 2rem;
      margin-top: auto;
    }

    .footer-content {
      max-width: 1200px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 2rem;
    }

    .footer-logo {
      font-size: 1.5rem;
      font-weight: 700;
      margin-bottom: 1rem;
      color: white;
    }

    .footer-logo span {
      color: var(--secondary);
    }

    .copyright {
      max-width: 1200px;
      margin: 2rem auto 0;
      padding-top: 2rem;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      text-align: center;
      color: rgba(255, 255, 255, 0.6);
    }

    @media (max-width: 768px) {
      .hamburger {
        display: block;
      }

      .nav-links,
      .auth-buttons {
        display: none;
        flex-direction: column;
        width: 100%;
        text-align: center;
        margin-top: 1rem;
      }

      .nav-links.active,
      .auth-buttons.active {
        display: flex;
      }

      .form-container {
        padding: 1.5rem;
        margin-top: 100px;
      }
    }
  </style>
</head>
<body>
  

  <main>
    <div class="form-container">
      <h2 class="form-title">Reset Password</h2>
      <p class="form-subtitle">Enter your email to receive a password reset link</p>
      
      <?php
      require('conn.php');
      require 'vendor/autoload.php';
      use PHPMailer\PHPMailer\SMTP;
      use PHPMailer\PHPMailer\PHPMailer;
      use PHPMailer\PHPMailer\Exception;
      
      function sendMail($email, $reset_token) {
          try {
              $mail = new PHPMailer(true);
              $mail->isSMTP();
              $mail->Host = 'smtp.gmail.com';
              $mail->SMTPAuth = true;
              $mail->Username = '';
              $mail->Password = ''; // Gmail App Password
              $mail->SMTPSecure = 'tls';
              $mail->Port = 587;
              $mail->setFrom('eduspace29@gmail.com', 'Questly');
              $mail->addAddress($email);
              $mail->isHTML(true);
              $mail->Subject = "Password Reset Link from Questly";
              $mail->Body = "Your Reset link is <a href='http://localhost/qp-genrator/reset-password.php?email=$email&reset_token=$reset_token'>here</a>.";
              $mail->send();
              echo "<div class='status-message success-message'>✅ Reset link sent to $email</div>";
              return true;
          } catch (Exception $e) {
              echo "<div class='status-message error-message'>Mailer Error: {$mail->ErrorInfo}</div>";
              return false;
          }
      }
      
      if (isset($_POST['send-reset-link'])) {
          $email = $_POST['email'];
          $query = "SELECT * FROM register_user WHERE email = '$email'";
          $result = mysqli_query($conn, $query);
          if ($result && mysqli_num_rows($result) == 1) {
              $reset_token = bin2hex(random_bytes(16));
              date_default_timezone_set('Asia/Kolkata');
              $data = date("Y-m-d");
              $query = "UPDATE register_user SET resettoken='$reset_token', resettokenexp='$data' WHERE email='$email'";
              if (mysqli_query($conn, $query) && sendMail($email, $reset_token)) {
                      }
              else {
                  echo "<div class='status-message error-message'>❌ Failed to send reset email.</div>";
              }
          } else {
              echo "<div class='status-message error-message'>❌ Email not found.</div>";
          }
      }
      ?>
      
      <form action="forgotpass.php" method="post" class="reset-form">
        <div class="form-group">
          <label for="email">Email Address</label>
          <input type="email" id="email" name="email" placeholder="Enter your email" required>
        </div>
        <button type="submit" class="btn btn-primary" name="send-reset-link">Send Reset Link</button>
        <div class="back-link">
          <a href="login.php">Back to Login</a>
        </div>
      </form>
    </div>
  </main>



  <script>
    function toggleMenu() {
      document.getElementById("navLinks").classList.toggle("active");
      document.getElementById("authButtons").classList.toggle("active");
    }
  </script>
</body>
</html
